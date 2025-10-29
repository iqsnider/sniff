from sniff.graph_theory import Graph
from sniff.simulation import Simulate
from sniff.statistics import Plot

import typer
import numpy as np

app = typer.Typer()


@app.command()
def protocol_1D(
    n: int = 5,
    link: float = 1.0,
    time: float = 10.0,
    time_step: float = 0.01,
    noise_strength: float = 0.1,
    noise_model: str = 'piecewise',
    noise_update_rate: float = 0.1,
    save: str = None
):
    graph = Graph(n)
    A = graph.erdos_renyi_adj(link)

    x0 = np.random.random(n)
    simulation = Simulate(A, time, time_step, x0,
                          noise_model, noise_update_rate)
    logs = simulation.solve_consensus_dynamics_w_GOE_noise(noise_strength)

    plotter = Plot(logs)
    plotter.plot_1D_convergence(save)


@app.command()
def protocol_2D(
    n: int = 5,
    link: float = 1.0,
    time: float = 10.0,
    time_step: float = 0.01,
    alpha: float = 1.0,
    beta: float = 1.0,
    noise_strength: float = 0.1,
    noise_model: str = 'piecewise',
    noise_update_rate: float = 0.1,
    p_track: tuple[float, float] = (0.0, 0.0),
    save: str = None
):
    graph = Graph(n)
    A = graph.erdos_renyi_adj(link)

    x0 = np.random.random((n, 2))
    p0 = x0.flatten()
    simulation = Simulate(A, time, time_step, p0,
                          noise_model, noise_update_rate)
    logs = simulation.solve_consensus_setpoint_tracking_w_GOE_noise(
        alpha=alpha, beta=beta, p_track=p_track, noise_strength=noise_strength
    )

    plotter = Plot(logs)
    plotter.plot_2D_paths(p0, save)


@app.command()
def formation(
    n: int = 5,
    link: float = 1.0,
    time: float = 10.0,
    time_step: float = 0.01,
    alpha: float = 1.0,
    beta: float = 1.0,
    noise_strength: float = 0.1,
    noise_model: str = 'piecewise',
    noise_update_rate: float = 0.1,
    spacing: float = 0.05,
    p_track: tuple[float, float] = (0.0, 0.0),
    save: str = None
):
    graph = Graph(n)
    A = graph.erdos_renyi_adj(link)

    x0 = np.random.random((n, 2))
    p0 = x0.flatten()

    simulation = Simulate(A, time, time_step, p0,
                          noise_model, noise_update_rate)
    logs = simulation.solve_consensus_formation_setpoint_tracking_w_GOE_noise(
        alpha=alpha, beta=beta, p_track=p_track, noise_strength=noise_strength, spacing=spacing)

    plotter = Plot(logs)
    plotter.plot_2D_paths(p0, save)


@app.command()
def circle(
    n: int = 5,
    link: float = 1.0,
    time: float = 10.0,
    time_step: float = 0.01,
    alpha: float = 1.0,
    beta: float = 1.0,
    noise_strength: float = 0.1,
    noise_model: str = 'piecewise',
    noise_update_rate: float = 0.1,
    spacing: float = 0.05,
    center: tuple[float, float] = (0.0, 0.0),
    radius: float = 0.5,
    ang_vel: float = 1.0,
    save: str = None
):
    graph = Graph(n)
    A = graph.erdos_renyi_adj(link)

    x0 = np.random.random((n, 2))
    p0 = x0.flatten()

    simulation = Simulate(A, time, time_step, p0,
                          noise_model, noise_update_rate)
    logs = simulation.solve_consensus_formation_circle_tracking_w_GOE_noise(
        alpha=alpha, beta=beta, center=center, radius=radius, ang_vel=ang_vel, noise_strength=noise_strength, spacing=spacing)

    plotter = Plot(logs)
    plotter.plot_2D_paths(p0, save)


if __name__ == "__main__":
    app()
