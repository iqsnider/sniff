from sniff.noise import RMT
from sniff.graph_theory import Graph

import numpy as np
from scipy.integrate import solve_ivp


class Simulate:
    def __init__(self, A, time, time_step, x0,
                 noise_model='piecewise', noise_update_rate=0.1,
                 seed=None):
        """
        The noise model options:
        'static' :  single GOE sample for fixed uncertain channels
        'piecewise' : update GOE sample at noise_update_rate intervals
        'white' : update GOE sample at every time step
        """
        self.T = time
        self.dT = time_step
        self.x0 = x0
        self.noise_model = noise_model
        self.noise_update_rate = noise_update_rate
        self.current_L_noisy = None
        self.last_noise_update = -np.inf

        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.rmo = RMT(A, seed=seed)

    def _get_noisy_laplacian(self, t, noise_strength):
        """
        Returns the proper noisy laplacian based on the simulation
        specifications
        """
        if self.noise_model == 'white':
            return self.rmo.noise_GOE(noise_strength)

        elif self.noise_model == 'static':
            if self.current_L_noisy is None:
                self.current_L_noisy = self.rmo.noise_GOE(noise_strength)
            return self.current_L_noisy

        elif self.noise_model == 'piecewise':
            if self.current_L_noisy is None:
                self.current_L_noisy = self.rmo.noise_GOE(noise_strength)
                self.last_noise_update = t
            elif t - self.last_noise_update >= self.noise_update_rate:
                self.current_L_noisy = self.rmo.noise_GOE(noise_strength)
                self.last_noise_update = t
            return self.current_L_noisy

        else:
            raise ValueError(f"Unknown noise_model: {self.noise_model}")

    def solve_consensus_dynamics_w_GOE_noise(self, noise_strength=0.1):
        """
        Solves the consensus dynamics
        """
        self.current_L_noisy = None
        self.last_noise_update = -np.inf

        t_span = (0, self.T)
        t_eval = np.linspace(*t_span, int(self.T/self.dT))

        solution = solve_ivp(self._consensus_dynamics_w_GOE_noise,
                             t_span, self.x0, t_eval=t_eval,
                             method='RK45', args=(noise_strength,))

        return solution

    def _consensus_dynamics_w_GOE_noise(self, t, x, noise_strength):
        """
        Consensus dynamics state-space model
        """
        L_noisy = self._get_noisy_laplacian(t, noise_strength)
        return -L_noisy @ x

    def solve_consensus_setpoint_tracking_w_GOE_noise(self, alpha=1, beta=1, p_track=[0, 0], noise_strength=0.1):
        """
        Solves the consensus dynamics for converging to a 2D
        setpoint
        """
        self.current_L_noisy = None
        self.last_noise_update = -np.inf

        t_span = (0, self.T)
        t_eval = np.linspace(*t_span, int(self.T/self.dT))

        solution = solve_ivp(self._consensus_2D_setpoint_w_GOE_noise,
                             t_span,
                             self.x0,
                             t_eval=t_eval,
                             args=(alpha, beta, p_track, noise_strength),
                             method='RK45')

        return solution

    def _consensus_2D_setpoint_w_GOE_noise(self, t, x, alpha, beta, p_track, noise_strength):
        L_noisy = self._get_noisy_laplacian(t, noise_strength)
        B, c = Graph.make_setpoint_transform_2D(
            L_noisy, alpha=alpha, beta=beta, p_track=p_track)
        return B @ x + c

    def solve_consensus_formation_setpoint_tracking_w_GOE_noise(self, alpha=1, beta=1, p_track=[0, 0], noise_strength=0.1, spacing=0.05):
        """
        Solves the consensus dynamics for converging to a 2D
        setpoint and arranges agents into a formation
        """
        self.current_L_noisy = None
        self.last_noise_update = -np.inf

        t_span = (0, self.T)
        t_eval = np.linspace(*t_span, int(self.T/self.dT))

        solution = solve_ivp(self._consensus_formation_2D_setpoint_w_GOE_noise,
                             t_span,
                             self.x0,
                             t_eval=t_eval,
                             method='RK45',
                             args=(alpha, beta, p_track, noise_strength, spacing))

        return solution

    def _consensus_formation_2D_setpoint_w_GOE_noise(self, t, x, alpha, beta, p_track, noise_strength, spacing):
        L_noisy = self._get_noisy_laplacian(t, noise_strength)
        formation = Simulate.generate_formation(L_noisy.shape[0], spacing)
        B, c = Graph.make_setpoint_formation_transform_2D(
            L_noisy, alpha=alpha, beta=beta, p_track=p_track, formation_offsets=formation)
        return B @ x + c

    @staticmethod
    def generate_formation(n, spacing) -> np.ndarray:
        """
        Generates a deterministic square grid formation
        with consistent ordering and spacing.
        """
        side = int(np.ceil(np.sqrt(n)))
        coords = np.array(
            [[i*spacing, j*spacing] for i in range(side) for j in range(side)])
        return coords[:n]

    def solve_consensus_formation_circle_tracking_w_GOE_noise(self, alpha=1, beta=1, center=(0.5, 0.5), radius=0.25, ang_vel=1.0, noise_strength=0.1, spacing=0.05):
        """
        Solves the consensus dynamics for converging to a 2D
        setpoint and arranges agents into a formation
        """
        self.current_L_noisy = None
        self.last_noise_update = -np.inf

        n_agents = len(self.x0)//2
        phase_offsets = np.linspace(0, 2*np.pi, n_agents, endpoint=False)

        def circle(t):
            p_targets = np.zeros((n_agents, 2))
            for i in range(n_agents):
                theta = ang_vel * t + phase_offsets[i]
                p_targets[i, 0] = center[0] + radius * np.cos(theta)
                p_targets[i, 1] = center[1] + radius * np.sin(theta)
            return p_targets.flatten()

        t_span = (0, self.T)
        t_eval = np.linspace(*t_span, int(self.T/self.dT))

        solution = solve_ivp(self._consensus_formation_2D_circle_w_GOE_noise,
                             t_span,
                             self.x0,
                             t_eval=t_eval,
                             method='RK45',
                             args=(alpha, beta, circle, radius, noise_strength, spacing))

        return solution

    def _consensus_formation_2D_circle_w_GOE_noise(self, t, x, alpha, beta, circle, radius, noise_strength, spacing):
        p_target = circle(t)
        L_noisy = self._get_noisy_laplacian(t, noise_strength)
        formation = radius * \
            Simulate.generate_formation(L_noisy.shape[0], spacing)
        B, c = Graph.make_circle_formation_transform_2D(
            L_noisy, alpha=alpha, beta=beta, p_track=p_target, formation_offsets=formation)
        return B @ x + c
