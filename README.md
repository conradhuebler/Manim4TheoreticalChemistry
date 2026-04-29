# Manim4TheoreticalChemistry

Educational Manim animations for theoretical chemistry and molecular modeling.

## Overview

This repository contains a collection of ManimGL animations designed for teaching theoretical chemistry, molecular dynamics, quantum mechanics, and statistical mechanics. Each animation is self-contained and includes bilingual support (English/German).

All animations are developed for university lectures and focus on visualizing abstract concepts in computational chemistry.

## Requirements

- Python 3.13
- ManimGL
- NumPy, SciPy (for select animations)

## Animation Files

### Molecular Dynamics & Quantum Mechanics

| File | Description |
|------|-------------|
| `h2_md_full_refactored.py` | H₂ molecule formation: from free atoms to Born-Oppenheimer approximation. 5-phase animation with MD simulation, Morse potential, and adaptive time axes. |
| `quantum_dynamics_manim.py` | Wavepacket propagation in a double-well potential using the split-step Fourier method. |
| `quantum_nonlocality.py` | Visualization of quantum nonlocality and entanglement. |
| `nh3_inversion.py` | Ammonia inversion barrier and umbrella motion. |
| `h3_reaction_pathway.py` | Reaction pathway visualization for the H₃ system. |

### Force Field & Interactions

| File | Description |
|------|-------------|
| `bond_stretching.py` | Harmonic bond potential: real-time energy tracking during stretching and compression. |
| `angle_bending.py` | Harmonic angle bending potential. |
| `torsion_angle_optimized.py` | Torsional potential and dihedral angle rotations. |
| `nonbonded_interactions.py` | Lennard-Jones and electrostatic interactions. |
| `polarization_forcefield.py` | Polarizable force field concepts. |
| `particle_interactions_combinatorics.py` | Combinatorics of particle interactions in force fields. |

### Statistical Mechanics & Sampling

| File | Description |
|------|-------------|
| `metropolis_animation.py` | Metropolis algorithm: acceptance probability and step dynamics at different temperatures. |
| `monte_carlo_pi.py` | Monte Carlo estimation of π via random point sampling. |
| `polymer_monte_carlo.py` | Monte Carlo simulation of polymer chains. |
| `polymer_sampling_comparison.py` | Comparison of different polymer sampling methods. |
| `metadynamics_visualization.py` | Metadynamics and free energy surface exploration. |
| `pca_molecular_dynamics.py` | Principal component analysis of molecular dynamics trajectories. |

### Optimization & Mathematical Methods

| File | Description |
|------|-------------|
| `geometry_optimization.py` | Newton method with modifications for finding energy minima on potential surfaces. |
| `variational_method.py` | Variational method applied to the harmonic oscillator. |

## Technical Details

- **Language:** Set `LANGUAGE = "EN"` or `LANGUAGE = "DE"` at the top of each file.
- **Numerical Stability:** Small timesteps (0.05–0.1 fs), clamping, and overflow protection for MD simulations.
- **Output:** Videos saved to `./videos/`, frames to `./images/`.

## Funding

The development of Manim4TheoreticalChemistry is funded by:

- TUBAFdigital
- European Union (Erasmus+ National Agency for Higher Education)

C. H. gratefully acknowledges TUBAFdigital for funding.

Funded by the European Union. Views and opinions expressed are however those of the author(s) only and do not necessarily reflect those of the European Union or Erasmus+ National Agency for Higher Education (German Academic Exchange Service). Neither the European Union nor the granting authority can be held responsible for them.

![Co-funded by the European Union](https://github.com/conradhuebler/Manim4TheoreticalChemistry/raw/master/EN%20Co-funded%20by%20the%20EU_POS.jpg)
