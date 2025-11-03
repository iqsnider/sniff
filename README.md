# sniff
[![Build](https://github.com/iqsnider/sniff/actions/workflows/pytest.yml/badge.svg)](https://github.com/iqsnider/sniff/actions/workflows/pytest.yml)
[![codecov](https://codecov.io/gh/iqsnider/sniff/graph/badge.svg?token=0UFPF4SNKI)](https://codecov.io/gh/iqsnider/sniff)

Consensus protocol for a random graph of agents perturbed with Gaussian Orthogonal Ensemble (GOE) noise.

---

## Overview
An Erdos–Renyi graph is used to make random undirected connections between network nodes.  
A connection is formed between nodes only if the probability threshold is satisfied.  
The basic graph is defined as follows:

$$
U = (U_{ij})_{i,j=1}^n, \quad \text{where } U_{ij} \stackrel{\text{i.i.d.}}{\sim} \text{Unif}[0, 1)
$$

A Bernoulli random matrix is then formed by selecting a matrix of ones conditional upon a connection probability $p$:

$$
B = \mathbf{1}[U < p] \in \{0,1\}^{n \times n}, \quad 
\text{with } 
B_{ij} =
\begin{cases}
1, & U_{ij} < p \\
0, & U_{ij} \ge p
\end{cases}
$$

To ensure that the matrix is undirected, we first keep only the strict upper-triangular section of $B$ by forming a matrix $C$ such that:

$$
C_{ij} =
\begin{cases}
B_{ij}, & i < j \\
0, & i \ge j
\end{cases}
$$

Then, the final undirected (and symmetric) adjacency matrix $A$ is formed by summing $C$ and its transpose:

$$
A = C + C^\mathsf{T}
$$

## Installation (with uv)

`sniff` uses [uv](https://github.com/astral-sh/uv), a fast Python package manager and environment builder.  
You **don’t** need to manually activate virtual environments.

### 1. Clone the repository
```bash
git clone git@github.com:iqsnider/sniff.git
cd sniff
````

### 2. Install dependencies and sync environment

```bash
uv sync
```

---

## Usage

Run simulations directly with `uv run`. All CLI commands have default values.

### Basic example

```bash
uv run sniff protocol-1d
```
<p align="center">
  <img src="docs/assets/figures/protocol-1d.png" width="500"/>
  <br>
  <em>Figure 1: Consensus Protocol for noisy 1D agents.</em>
</p>

### Running simple 2D setpoint tracking
```bash
uv run sniff protocol-2d --n 20 --p-track 0.0 0.0
```

<p align="center">
  <img src="docs/assets/figures/protocol-2d.png" width="400"/>
  <br>
  <em>Figure 2: Consensus Protocol for noisy 2D agents tracking a setpoint.</em>
</p>

### Running grid formation consensus
```bash
uv run sniff formation --n 20 --p-track 0.0 0.0
```

<p align="center">
  <img src="docs/assets/figures/formation.png" width="400"/>
  <br>
  <em>Figure 3: Consensus Protocol for noisy 2D agents forming a grid.</em>
</p>

### Running dynamic circle consensus
```bash
uv run sniff circle --n 30
```

<p align="center">
  <img src="circle.png" width="400"/>
  <br>
  <em>Figure 4: Consensus Protocol for noisy 2D agents tracking a circle.</em>
</p>
