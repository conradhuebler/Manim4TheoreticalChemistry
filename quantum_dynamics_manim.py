#!/usr/bin/env python3
"""
Quantum Dynamics: Wavepacket Propagation in Double-Well Potential
Quantendynamik: Wellenpaket-Propagation im Doppeltopf-Potential

Visualizes the time evolution of a quantum wavepacket using the split-step
Fourier method. Shows the probability density |ψ(x,t)|² propagating in a
double-well potential.

Educational goals:
- Understanding quantum wavepacket dynamics
- Visualization of tunneling through potential barriers
- Split-step Fourier method for solving Schrödinger equation
"""

from manimlib import *
import numpy as np

# Language setting
LANGUAGE = "EN"  # Set to "EN" for English, "DE" for German

STRINGS = {
    "DE": {
        "title": "Quantendynamik: Wellenpaket im Doppeltopf-Potential",
        "probability": "Aufenthaltswahrscheinlichkeit",
        "potential": "Potential-Energie",
        "position": "Position x (Bohr)",
        "probability_density": "|ψ(x,t)|²",
        "energy": "Energie (a.u.)",
        "time": "Zeit",
        "barrier": "Barriere",
        "width": "Breite",
        "initial_pos": "Startposition",
    },
    "EN": {
        "title": "Quantum Dynamics: Wavepacket in Double-Well Potential",
        "probability": "Probability Density",
        "potential": "Potential Energy",
        "position": "Position x (Bohr)",
        "probability_density": "|ψ(x,t)|²",
        "energy": "Energy (a.u.)",
        "time": "Time",
        "barrier": "Barrier",
        "width": "Width",
        "initial_pos": "Initial Position",
    }
}

def get_string(key):
    return STRINGS[LANGUAGE].get(key, key)


# =============================================================================
# PREDEFINED SCENARIOS - Select one to visualize different physics
# =============================================================================

SCENARIOS = {
    "TUNNELING": {
        "description": "Quantum Tunneling - wavepacket tunnels through barrier",
        "barrier": 100.0,         # kcal/mol - low barrier
        "alpha": 5,           # broad wavepacket
        "x0": -1.5,            # start at left minimum
        "duration": 15.0,
        "pot_scale": 1.0,
    },

    "CLASSICAL_TRAPPED": {
        "description": "Classical Trapping - particle confined to one well",
        "barrier": 100.0,       # kcal/mol - very high barrier
        "alpha": 10.0,          # narrow (classical-like)
        "x0": -1.5,
        "duration": 12.0,
        "pot_scale": 1.0,       # no scaling (barrier too high)
    },

    "HIGH_ENERGY": {
        "description": "Over-Barrier Motion - particle has enough energy",
        "barrier": 3.0,         # kcal/mol - low barrier
        "alpha": 3.0,           # quite narrow
        "x0": -2.0,            # start further left (more energy)
        "duration": 10.0,
        "pot_scale": 40.0,
    },

    "DISPERSION": {
        "description": "Strong Dispersion - wavepacket spreads significantly",
        "barrier": 10.0,        # kcal/mol
        "alpha": 0.2,           # very broad → high momentum uncertainty
        "x0": -1.5,
        "duration": 15.0,
        "pot_scale": 30.0,
    },

    "COHERENT": {
        "barrier": 8.0,         # kcal/mol
        "alpha": 1.0,           # medium width
        "x0": -1.5,
        "duration": 15.0,
        "pot_scale": 35.0,
    },
}

# SELECT SCENARIO HERE:
SCENARIO = "TUNNELING"  # Change to: CLASSICAL_TRAPPED, HIGH_ENERGY, DISPERSION, COHERENT


class QuantumDynamics(Scene):
    def construct(self):
        # Setup and animation
        self.setup_parameters()
        self.setup_layout()
        self.initialize_wavefunction()
        self.compute_operators()
        self.create_visualization()
        self.animate_propagation()
        self.wait(2)

    def setup_parameters(self):
        """Define physical constants and simulation parameters"""
        # Load selected scenario
        if SCENARIO not in SCENARIOS:
            raise ValueError(f"Unknown scenario: {SCENARIO}. Available: {list(SCENARIOS.keys())}")

        scenario = SCENARIOS[SCENARIO]
        print(f"🎬 Loading scenario: {SCENARIO}")
        print(f"   Description: {scenario['description']}")

        # Physical constants (atomic units)
        self.LENGTH = 5.12              # Box length (Bohr)
        self.MASS = 50         # Proton mass (a.u.)
        self.PI = np.pi

        # Potential parameters (from scenario)
        self.BARRIER = scenario["barrier"] / 627.509    # Convert kcal/mol → a.u.
        self.WIDTH = 3.0                                # Double-well width (Bohr)

        # Wavepacket parameters (from scenario)
        self.X0 = scenario["x0"]        # Initial position (Bohr)
        self.ALPHA = scenario["alpha"]  # Gaussian width parameter

        # Simulation parameters
        self.NPOINTS = 8192             # Number of grid points (high resolution!)
        self.DT = 0.01 * 41.341         # Time step (a.u.)
        self.SNAPSHOT_FREQ = 10         # Frames between updates

        # Animation parameters (from scenario)
        self.duration = scenario["duration"]
        self.fps = 30

        # Visualization parameters (from scenario)
        self.POTENTIAL_SCALE = scenario["pot_scale"]
        self.X_PLOT_RANGE = 4.0         # Only plot |x| <= this value
        self.VIS_DOWNSAMPLE = 8         # Show every Nth point for visualization

        # Grid setup (CORRECTED to match original!)
        self.dx = self.LENGTH / self.NPOINTS
        self.x = np.linspace(-self.LENGTH/2, self.LENGTH/2, self.NPOINTS)

    def setup_layout(self):
        """Create single-panel layout with title"""
        # Title with scenario name
        main_title = Text(get_string("title"), color=YELLOW).scale(0.6)
        scenario_label = Text(f"[{SCENARIO}]", color=GREEN).scale(0.45)

        title_group = VGroup(main_title, scenario_label).arrange(DOWN, buff=0.15)
        title_group.to_edge(UP, buff=0.3)
        self.add(title_group)

    def initialize_wavefunction(self):
        """Create initial Gaussian wavepacket"""
        # Gaussian wavepacket
        psi0 = np.exp(-self.ALPHA * (self.x - self.X0)**2)
        psi0 = psi0.astype(np.complex128)

        # Normalize
        norm = np.sqrt(np.sum(np.abs(psi0)**2) * self.dx)
        self.psi = psi0 / norm

    def compute_operators(self):
        """Prepare split-step Fourier operators"""
        # Momentum grid
        p = np.fft.fftfreq(self.NPOINTS, self.dx) * 2 * self.PI

        # Potential operator exp(-i V dt)
        V = self.double_well_potential(self.x)
        self.exp_pot = np.exp(-1j * self.DT * V)

        # Kinetic operator exp(-i T dt)
        T = 0.5 * p**2 / self.MASS
        self.exp_kin = np.exp(-1j * self.DT * T)

    def double_well_potential(self, x):
        """Calculate double-well potential"""
        a = self.WIDTH
        return self.BARRIER * (16 * (x/a)**4 - 8 * (x/a)**2 + 1)

    def create_visualization(self):
        """Set up combined axes, graphs, and labels"""
        # Single combined plot for both probability and potential
        self.axes = Axes(
            x_range=[-self.X_PLOT_RANGE, self.X_PLOT_RANGE, 1],
            y_range=[0, 1.5, 0.3],
            width=12,
            height=5.5,
            axis_config={"include_tip": True},
        )
        self.axes.move_to(DOWN * 0.4)
        self.add(self.axes)

        # Add axis labels
        x_label = Text(get_string("position"), color=WHITE).scale(0.4)
        x_label.next_to(self.axes.get_x_axis(), DOWN, buff=0.3)

        y_label = Text(get_string("probability_density") + " / " + get_string("potential"),
                      color=WHITE).scale(0.4)
        y_label.next_to(self.axes.get_y_axis(), LEFT, buff=0.3)
        y_label.rotate(90 * DEGREES)

        self.add(x_label, y_label)

        # Plot double-well potential (scaled for visibility)
        V = self.double_well_potential(self.x)

        # Filter for visible range only
        mask = np.abs(self.x) <= self.X_PLOT_RANGE
        x_plot = self.x[mask]
        V_plot = V[mask] * self.POTENTIAL_SCALE

        # Create potential curve points
        pot_points = [self.axes.coords_to_point(x_plot[i], V_plot[i])
                     for i in range(len(x_plot))]
        self.potential_curve = VMobject(color=BLUE, stroke_width=2)
        self.potential_curve.set_points_as_corners(pot_points)
        self.add(self.potential_curve)

        # Mark equilibrium positions (minima of double well)
        for eq_x in [-self.WIDTH, self.WIDTH]:
            if np.abs(eq_x) <= self.X_PLOT_RANGE:
                eq_point = self.axes.coords_to_point(eq_x, 0)
                eq_dot = Dot(eq_point, color=GREEN, radius=0.06)
                eq_line = DashedLine(
                    eq_point,
                    self.axes.coords_to_point(eq_x, 0.15),
                    stroke_width=1.5,
                    color=GREEN,
                    dash_length=0.05
                )
                self.add(eq_line, eq_dot)

        # Create initial probability density curve
        psi_squared = np.abs(self.psi)**2

        # Apply mask and downsample for visualization
        mask = np.abs(self.x) <= self.X_PLOT_RANGE
        x_masked = self.x[mask]
        psi_masked = psi_squared[mask]

        # Downsample for smooth visualization
        x_vis = x_masked[::self.VIS_DOWNSAMPLE]
        psi_vis = psi_masked[::self.VIS_DOWNSAMPLE]

        prob_points = [self.axes.coords_to_point(x_vis[i], psi_vis[i])
                      for i in range(len(x_vis))]
        self.prob_curve = VMobject(color=RED, stroke_width=3)
        self.prob_curve.set_points_as_corners(prob_points)
        self.add(self.prob_curve)

        # Add legend with parameters underneath
        legend_scale = 0.4
        param_scale = 0.35

        # Legend entries
        legend_entries = VGroup(
            VGroup(Line(LEFT * 0.3, RIGHT * 0.3, color=RED, stroke_width=3),
                   Text(get_string("probability_density"), color=WHITE).scale(legend_scale)).arrange(RIGHT, buff=0.2),
            VGroup(Line(LEFT * 0.3, RIGHT * 0.3, color=BLUE, stroke_width=2),
                   Text(get_string("potential") + " (×" + f"{self.POTENTIAL_SCALE:.0f}" + ")",
                        color=WHITE).scale(legend_scale)).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)

        # Separator line
        separator = Line(LEFT * 2, RIGHT * 2, stroke_width=1, color=GREY).scale(0.5)

        # Parameter info
        params = VGroup(
            Text(f"Scenario: {SCENARIO}", color=GREEN).scale(param_scale),
            Text(f"{get_string('barrier')}: {self.BARRIER * 627.509:.1f} kcal/mol",
                 color=WHITE).scale(param_scale),
            Text(f"α: {self.ALPHA:.2f}",
                 color=WHITE).scale(param_scale),
            Text(f"x₀: {self.X0:.2f} Bohr",
                 color=WHITE).scale(param_scale)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)

        # Combine legend and parameters
        legend_box = VGroup(legend_entries, separator, params).arrange(DOWN, buff=0.2)
        legend_box.to_corner(UR, buff=0.6)
        self.add(legend_box)

        # Time display (bottom left)
        self.time_label = DecimalNumber(
            0, num_decimal_places=1, color=YELLOW
        ).scale(0.6)
        time_text = Text(get_string("time") + ": ", color=WHITE).scale(0.5)
        time_text.next_to(self.time_label, LEFT)
        time_group = VGroup(time_text, self.time_label)
        time_group.to_edge(DOWN, buff=0.5).to_edge(LEFT, buff=1.0)
        self.add(time_group)

    def split_step_propagation(self):
        """Perform one step of split-step Fourier propagation"""
        # 1. Multiply by exp(-i V dt) in position space
        self.psi *= self.exp_pot

        # 2. FFT to momentum space
        self.psi = np.fft.fft(self.psi)

        # 3. Multiply by exp(-i T dt) in momentum space
        self.psi *= self.exp_kin

        # 4. IFFT back to position space
        self.psi = np.fft.ifft(self.psi)

    def animate_propagation(self):
        """Main animation loop with wavepacket propagation"""
        frames = int(self.duration * self.fps)

        for frame in range(frames):
            t = frame / self.fps

            # Propagate wavefunction for several steps per frame
            for _ in range(self.SNAPSHOT_FREQ):
                self.split_step_propagation()

            # Update probability density curve
            psi_squared = np.abs(self.psi)**2

            # Filter to visible range
            mask = np.abs(self.x) <= self.X_PLOT_RANGE
            x_masked = self.x[mask]
            psi_masked = psi_squared[mask]

            # Downsample for visualization (reduces rendering artifacts)
            x_vis = x_masked[::self.VIS_DOWNSAMPLE]
            psi_vis = psi_masked[::self.VIS_DOWNSAMPLE]

            # Create points for curve
            prob_points = [self.axes.coords_to_point(x_vis[i], psi_vis[i])
                          for i in range(len(x_vis))]

            # Update curve efficiently
            self.remove(self.prob_curve)
            self.prob_curve = VMobject(color=RED, stroke_width=3)
            self.prob_curve.set_points_as_corners(prob_points)
            self.add(self.prob_curve)

            # Update time display
            time_au = frame * self.SNAPSHOT_FREQ * self.DT
            time_fs = time_au / 41.341  # Convert to fs
            self.time_label.set_value(time_fs)

            # Wait for next frame
            self.wait(1/self.fps)


if __name__ == "__main__":
    """
    Run with: manimgl quantum_dynamics_manim.py QuantumDynamics

    SCENARIOS GUIDE:
    ================

    1. TUNNELING (Default)
       - Shows quantum tunneling through a barrier
       - Low barrier (5 kcal/mol) + broad wavepacket (α=0.5)
       - Wavepacket oscillates between wells
       - Duration: 15s

    2. CLASSICAL_TRAPPED
       - Particle confined to single well (classical behavior)
       - Very high barrier (100 kcal/mol) + narrow packet (α=10)
       - No tunneling - particle stays in left well
       - Duration: 12s

    3. HIGH_ENERGY
       - Particle has enough energy to cross barrier classically
       - Low barrier (3 kcal/mol) + narrow packet (α=3)
       - Rapid oscillation between wells
       - Duration: 10s

    4. DISPERSION
       - Demonstrates strong wavepacket spreading
       - Very broad initial packet (α=0.2) → high momentum uncertainty
       - Delocalization increases over time
       - Duration: 15s

    5. COHERENT
       - Balanced demonstration of tunneling + minimal dispersion
       - Medium barrier (8 kcal/mol) + medium width (α=1)
       - Clean periodic oscillation
       - Duration: 15s

    To change scenario: Edit SCENARIO variable at line ~105
    """
    pass
