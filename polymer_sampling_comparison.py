#!/usr/bin/env python3
"""
Polymer Sampling & Optimization Comparison
Vergleich von vier Methoden zur Polymer-Konfigurationsoptimierung

Methoden:
1. MC (Metropolis Monte Carlo) - Stochastisches Sampling mit Boltzmann-Gewichtung
2. NAIVE (Naive Sampling + Optimization) - Random Config → Gradient Descent
3. MD (Molecular Dynamics + Berendsen) - Velocity Verlet Integration
4. OPT (Pure Optimization) - Direkter Gradient Descent ohne Sampling

Alle Methoden:
- Nutzen die gleichen physikalischen Parameter
- Zeigen verschiedene Konvergenz-Strategien
- Vergleichbar durch einheitliche Initial Configuration
- Adaptierte Visualisierung pro Methode
"""

from manimlib import *
import numpy as np

# ============================================================================
# KONFIGURATION - Alles hier ändern!
# ============================================================================

SAMPLING_METHOD = "MC"  # Wähle: "MC", "NAIVE", "MD", "OPT"
INITIAL_CONFIG = "LINEAR"  # "LINEAR" oder "RANDOM"
N_STEPS = 40000

# ============================================================================
# PHYSIKALISCHE PARAMETER (einheitlich für alle Methoden)
# ============================================================================

COMMON_PARAMS = {
    # Polymer-Struktur (FESTE TOPOLOGIE)
    "n_beads": 20,

    # Geometrie
    "box_size": 35.0,
    "initial_spacing": 1.7,  # Für LINEAR init

    # Bindungs-Potential
    "r0_bond": 1.5,  # Å - Gleichgewicht
    "k_bond": 0.0,  # kcal/(mol·Å²) 30 default

    # Lennard-Jones
    "epsilon_lj": 0.0,  # kcal/mol
    "sigma_lj": 2.5,  # Å
    "cutoff_lj": 100.0,  # Å - kein Cutoff

    # Sonstiges
    "mass": 12.0,  # amu (Carbon)
    "k_B": 0.001987,  # kcal/(mol·K) - Boltzmann constant (für MC und MD)
}

# ============================================================================
# METHODEN-SPEZIFISCHE PARAMETER
# ============================================================================

METHOD_PARAMS = {
    "MC": {
        "temperature": 300.0,  # K
        "max_displacement": 0.2,  # Å
        "steps_per_frame": 1,
    },
    "NAIVE": {
        "perturbation_strength": 0.3,  # Å
        "opt_max_steps": 50,
        "opt_tolerance": 1e-3,
        "steps_per_frame": 1,
    },
    "MD": {
        "dt": 0.0001,  # ps - Integration step
        "temperature": 300.0,  # K
        "berendsen_tau": 0.1,  # ps - Thermostat coupling
        "steps_per_frame": 1  # MD steps pro Frame
    },
    "OPT": {
        "temperature": 300.0,  # K (nicht aktiv genutzt, aber für beta nötig)
        "opt_max_steps": 500,
        "opt_tolerance": 1e-4,
        "alpha_init": 0.05,  # Initiale Schrittweite
        "steps_per_frame": 1,
    }
}

# ============================================================================
# SPRACHE
# ============================================================================

LANGUAGE = "EN"

STRINGS = {
    "DE": {
        "title": "Polymer Sampling & Optimization Vergleich",
        "simulation": "Simulationsbox",
        "energy_plot": "Energieverlauf",
        "statistics": "Statistik",
        "rg_plot": "Gyrationsradius",
        "mc_steps": "Schritte",
        "energy": "Energie (kcal/mol)",
        "rg_label": "R_g (Å)",
        "method_mc": "Monte Carlo",
        "method_naive": "Naive + Opt",
        "method_md": "MD Simulation",
        "method_opt": "Pure Optimization",
    },
    "EN": {
        "title": "Polymer Sampling & Optimization Comparison",
        "simulation": "Simulation Box",
        "energy_plot": "Energy Evolution",
        "statistics": "Statistics",
        "rg_plot": "Radius of Gyration",
        "mc_steps": "Steps",
        "energy": "Energy (kcal/mol)",
        "rg_label": "R_g (Å)",
        "method_mc": "Monte Carlo",
        "method_naive": "Naive + Opt",
        "method_md": "MD Simulation",
        "method_opt": "Pure Optimization",
    },
}

def get_string(key):
    return STRINGS[LANGUAGE].get(key, key)


class PolymerSamplingComparison(Scene):
    """Polymer sampling comparison: 4 methods (MC, NAIVE, MD, OPT) with unified physics.

    GUI-compatible PARAMETERS structure with method-specific parameters.
    """

    # ✅ Central parameter dictionary for GUI tool compatibility
    PARAMETERS = {
        # ========================================================================
        # GENERAL CONFIGURATION
        # ========================================================================
        "sampling_method": {
            "value": SAMPLING_METHOD,
            "type": str,
            "unit": "-",
            "description": "Sampling method: MC (Monte Carlo), NAIVE (Random+Opt), MD (Molecular Dynamics), OPT (Pure Optimization)",
            "min": None,
            "max": None
        },
        "initial_config": {
            "value": INITIAL_CONFIG,
            "type": str,
            "unit": "-",
            "description": "Initial configuration: LINEAR (chain along diagonal) or RANDOM (uniform in box)",
            "min": None,
            "max": None
        },
        "n_steps": {
            "value": N_STEPS,
            "type": int,
            "unit": "steps",
            "description": "Total number of simulation steps",
            "min": 100,
            "max": 100000
        },

        # ========================================================================
        # COMMON PHYSICS PARAMETERS (all methods)
        # ========================================================================
        "n_beads": {
            "value": 20,
            "type": int,
            "unit": "-",
            "description": "Number of beads in polymer chain (fixed topology)",
            "min": 3,
            "max": 100
        },
        "box_size": {
            "value": 35.0,
            "type": float,
            "unit": "Å",
            "description": "Simulation box size (square)",
            "min": 10.0,
            "max": 100.0
        },
        "initial_spacing": {
            "value": 1.7,
            "type": float,
            "unit": "Å",
            "description": "Initial spacing between beads (LINEAR config only)",
            "min": 0.5,
            "max": 5.0
        },
        "r0_bond": {
            "value": 1.5,
            "type": float,
            "unit": "Å",
            "description": "Equilibrium bond length",
            "min": 0.5,
            "max": 3.0
        },
        "k_bond": {
            "value": 0.0,
            "type": float,
            "unit": "kcal/(mol·Å²)",
            "description": "Harmonic bond force constant (0 = no bonds, 30 = typical)",
            "min": 0.0,
            "max": 100.0
        },
        "epsilon_lj": {
            "value": 0.0,
            "type": float,
            "unit": "kcal/mol",
            "description": "Lennard-Jones well depth (0 = no LJ)",
            "min": 0.0,
            "max": 10.0
        },
        "sigma_lj": {
            "value": 2.5,
            "type": float,
            "unit": "Å",
            "description": "Lennard-Jones size parameter",
            "min": 0.5,
            "max": 5.0
        },
        "cutoff_lj": {
            "value": 100.0,
            "type": float,
            "unit": "Å",
            "description": "Lennard-Jones cutoff distance (100 = no cutoff)",
            "min": 3.0,
            "max": 200.0
        },
        "mass": {
            "value": 12.0,
            "type": float,
            "unit": "amu",
            "description": "Bead mass (12 = Carbon)",
            "min": 1.0,
            "max": 100.0
        },
        "k_B": {
            "value": 0.001987,
            "type": float,
            "unit": "kcal/(mol·K)",
            "description": "Boltzmann constant (physical constant)",
            "min": 0.001,
            "max": 0.01
        },

        # ========================================================================
        # MC METHOD PARAMETERS
        # ========================================================================
        "mc_temperature": {
            "value": 300.0,
            "type": float,
            "unit": "K",
            "description": "[MC] Simulation temperature for Metropolis criterion",
            "min": 1.0,
            "max": 1000.0
        },
        "mc_max_displacement": {
            "value": 0.2,
            "type": float,
            "unit": "Å",
            "description": "[MC] Maximum random displacement per MC move",
            "min": 0.01,
            "max": 5.0
        },
        "mc_steps_per_frame": {
            "value": 1,
            "type": int,
            "unit": "steps/frame",
            "description": "[MC] MC steps per visualization frame",
            "min": 1,
            "max": 100
        },

        # ========================================================================
        # NAIVE METHOD PARAMETERS
        # ========================================================================
        "naive_perturbation_strength": {
            "value": 0.3,
            "type": float,
            "unit": "Å",
            "description": "[NAIVE] Random perturbation amplitude before optimization",
            "min": 0.01,
            "max": 2.0
        },
        "naive_opt_max_steps": {
            "value": 50,
            "type": int,
            "unit": "steps",
            "description": "[NAIVE] Max gradient descent steps per perturbation",
            "min": 1,
            "max": 500
        },
        "naive_opt_tolerance": {
            "value": 1e-3,
            "type": float,
            "unit": "kcal/(mol·Å)",
            "description": "[NAIVE] Convergence tolerance (force norm)",
            "min": 1e-6,
            "max": 1.0
        },
        "naive_steps_per_frame": {
            "value": 1,
            "type": int,
            "unit": "steps/frame",
            "description": "[NAIVE] Sampling cycles per visualization frame",
            "min": 1,
            "max": 100
        },

        # ========================================================================
        # MD METHOD PARAMETERS
        # ========================================================================
        "md_dt": {
            "value": 0.0001,
            "type": float,
            "unit": "ps",
            "description": "[MD] Integration timestep for Velocity Verlet",
            "min": 1e-6,
            "max": 0.01
        },
        "md_temperature": {
            "value": 300.0,
            "type": float,
            "unit": "K",
            "description": "[MD] Target temperature for Berendsen thermostat",
            "min": 1.0,
            "max": 1000.0
        },
        "md_berendsen_tau": {
            "value": 0.1,
            "type": float,
            "unit": "ps",
            "description": "[MD] Berendsen thermostat coupling time constant",
            "min": 0.001,
            "max": 10.0
        },
        "md_steps_per_frame": {
            "value": 1,
            "type": int,
            "unit": "steps/frame",
            "description": "[MD] MD steps per visualization frame",
            "min": 1,
            "max": 100
        },

        # ========================================================================
        # OPT METHOD PARAMETERS
        # ========================================================================
        "opt_temperature": {
            "value": 300.0,
            "type": float,
            "unit": "K",
            "description": "[OPT] Temperature (for beta calculation, not actively used)",
            "min": 1.0,
            "max": 1000.0
        },
        "opt_max_steps": {
            "value": 500,
            "type": int,
            "unit": "steps",
            "description": "[OPT] Maximum optimization steps",
            "min": 10,
            "max": 10000
        },
        "opt_tolerance": {
            "value": 1e-4,
            "type": float,
            "unit": "kcal/(mol·Å)",
            "description": "[OPT] Convergence tolerance (force norm)",
            "min": 1e-8,
            "max": 1.0
        },
        "opt_alpha_init": {
            "value": 0.05,
            "type": float,
            "unit": "Å",
            "description": "[OPT] Initial step size for gradient descent",
            "min": 0.001,
            "max": 1.0
        },
        "opt_steps_per_frame": {
            "value": 1,
            "type": int,
            "unit": "steps/frame",
            "description": "[OPT] Optimization steps per visualization frame",
            "min": 1,
            "max": 100
        }
    }

    def construct(self):
        self.setup_parameters()
        self.setup_layout()
        self.create_polymer()
        self.initialize_configuration()  # Muss VOR create_energy_plot() sein!
        self.create_energy_plot()  # Nutzt initial_energy
        self.create_rg_plot()  # Nutzt initial R_g

        self.wait(0.5)
        self.run_simulation()
        self.wait(3)

    # ========================================================================
    # SETUP & INITIALIZATION
    # ========================================================================

    def setup_parameters(self):
        """Extract parameters from central PARAMETERS dictionary"""
        # General configuration
        self.sampling_method = self.PARAMETERS["sampling_method"]["value"]
        self.initial_config = self.PARAMETERS["initial_config"]["value"]
        self.n_steps = self.PARAMETERS["n_steps"]["value"]

        # Common physics parameters
        self.n_beads = self.PARAMETERS["n_beads"]["value"]
        self.box_size = self.PARAMETERS["box_size"]["value"]
        self.initial_spacing = self.PARAMETERS["initial_spacing"]["value"]
        self.r0_bond = self.PARAMETERS["r0_bond"]["value"]
        self.k_bond = self.PARAMETERS["k_bond"]["value"]
        self.epsilon_lj = self.PARAMETERS["epsilon_lj"]["value"]
        self.sigma_lj = self.PARAMETERS["sigma_lj"]["value"]
        self.cutoff_lj = self.PARAMETERS["cutoff_lj"]["value"]
        self.mass = self.PARAMETERS["mass"]["value"]
        self.k_B = self.PARAMETERS["k_B"]["value"]

        # Method-specific parameters (extract based on selected method)
        if self.sampling_method == "MC":
            self.temperature = self.PARAMETERS["mc_temperature"]["value"]
            self.max_displacement = self.PARAMETERS["mc_max_displacement"]["value"]
            self.steps_per_frame = self.PARAMETERS["mc_steps_per_frame"]["value"]
        elif self.sampling_method == "NAIVE":
            self.perturbation_strength = self.PARAMETERS["naive_perturbation_strength"]["value"]
            self.opt_max_steps = self.PARAMETERS["naive_opt_max_steps"]["value"]
            self.opt_tolerance = self.PARAMETERS["naive_opt_tolerance"]["value"]
            self.steps_per_frame = self.PARAMETERS["naive_steps_per_frame"]["value"]
        elif self.sampling_method == "MD":
            self.dt = self.PARAMETERS["md_dt"]["value"]
            self.temperature = self.PARAMETERS["md_temperature"]["value"]
            self.berendsen_tau = self.PARAMETERS["md_berendsen_tau"]["value"]
            self.steps_per_frame = self.PARAMETERS["md_steps_per_frame"]["value"]
        elif self.sampling_method == "OPT":
            self.temperature = self.PARAMETERS["opt_temperature"]["value"]
            self.opt_max_steps = self.PARAMETERS["opt_max_steps"]["value"]
            self.opt_tolerance = self.PARAMETERS["opt_tolerance"]["value"]
            self.alpha_init = self.PARAMETERS["opt_alpha_init"]["value"]
            self.steps_per_frame = self.PARAMETERS["opt_steps_per_frame"]["value"]

        # Boltzmann constant for MC and MD
        self.beta = 1.0 / (self.k_B * self.temperature)

        # Konvertierung: kcal/mol → kcal/(mol·ps²)·Å² für MD
        # F = m·a; E_unit_conversion
        self.kcal_to_internal = 418.4  # Konversionsfaktor

        # Simulation state
        self.step = 0
        self.current_energy = 0

        # Tracking
        self.step_history = [0]
        self.energy_history = []
        self.energy_before_history = []
        self.energy_after_history = []
        self.ke_history = []
        self.pe_history = []
        self.temp_history = []
        self.rg_history = []
        self.current_rg = 0

        # Visualisierungs-Throttle (je mehr Schritte, desto seltener updaten)
        # Ziel: ~200 Visualisierungen pro Lauf
        self.vis_freq = max(1, self.n_steps // 2000)

        # Visual scaling
        self.visual_scale = 0.20

        # Bond topology (FEST!)
        self.bond_list = [(i, i+1) for i in range(self.n_beads - 1)]

        # Set für schnelle Überprüfung ob Paar gebunden ist
        self.bonded_pairs = set()
        for i, j in self.bond_list:
            self.bonded_pairs.add((i, j))
            self.bonded_pairs.add((j, i))  # Beide Richtungen

        print(f"\n{'='*70}")
        print(f"Method: {self.sampling_method.upper()}")
        print(f"Initial Config: {self.initial_config}")
        print(f"Parameters loaded successfully")
        print(f"{'='*70}\n")

    def setup_layout(self):
        """Erstelle Layout: Simulation links, Plots rechts"""
        # Title
        title = Text(get_string("title"), color=YELLOW).scale(0.6)
        title.to_edge(UP, buff=0.3)
        self.add(title)

        # Divider
        divider = Line(UP * 3.5, DOWN * 3.5, stroke_width=2, color=WHITE)
        self.add(divider)

        # Simulation box (left)
        self.sim_box_center = LEFT * 3.5
        self.sim_box = Rectangle(
            width=6, height=6,
            stroke_color=WHITE, stroke_width=2
        ).move_to(self.sim_box_center)
        self.add(self.sim_box)

        sim_label = Text(get_string("simulation"), color=BLUE).scale(0.5)
        sim_label.next_to(self.sim_box, UP, buff=0.2)
        self.add(sim_label)

        # Energy plot (right top)
        self.energy_plot_center = RIGHT * 3.5 + UP * 1.5
        energy_plot_box = Rectangle(
            width=6, height=3,
            stroke_color=GREEN, stroke_width=1
        ).move_to(self.energy_plot_center)
        self.add(energy_plot_box)

        energy_label = Text(get_string("energy_plot"), color=GREEN).scale(0.4)
        energy_label.next_to(energy_plot_box, UP, buff=0.1)
        self.add(energy_label)

        # Radius of Gyration Plot (right bottom)
        self.rg_plot_center = RIGHT * 3.5 + DOWN * 1.8
        rg_box = Rectangle(
            width=6, height=2.5,
            stroke_color=ORANGE, stroke_width=1
        ).move_to(self.rg_plot_center)
        self.add(rg_box)

        rg_label = Text(get_string("rg_plot"), color=ORANGE).scale(0.4)
        rg_label.next_to(rg_box, UP, buff=0.1)
        self.add(rg_label)

        # Bead and bond lists
        self.bead_dots = []
        self.bond_lines = []

    def create_polymer(self):
        """Erstelle Polymer-Visualisierung"""
        # Platzhalter - wird in initialize_configuration gefüllt
        pass

    def create_energy_plot(self):
        """Erstelle Energy Evolution Plot (mit y-range basierend auf initial energy)"""
        # Berechne y-range aus initialer Energie mit 1.1x Puffer in beide Richtungen
        E_init = self.initial_energy
        y_min = -100 #E_init * -1.1  # 10% unter initial
        y_max = 30 #E_init * 1.1  # 10% über initial
        y_step = max(10, (y_max - y_min) / 5)  # ~5 Ticks auf der y-Achse

        self.energy_axes = Axes(
            x_range=[0, self.n_steps, max(1, self.n_steps // 10)],
            y_range=[y_min, y_max, y_step],
            width=5.5,
            height=2.5,
            axis_config={"include_tip": True}
        ).move_to(self.energy_plot_center)

        # Speichere für Energy-Plot Updates
        self.energy_y_min = y_min
        self.energy_y_max = y_max

        x_label = Text(get_string("mc_steps"), color=WHITE).scale(0.3)
        x_label.next_to(self.energy_axes.get_x_axis(), DOWN, buff=0.2)

        y_label = Text(get_string("energy"), color=WHITE).scale(0.3)
        y_label.next_to(self.energy_axes.get_y_axis(), LEFT)
        y_label.rotate(90 * DEGREES)

        self.add(self.energy_axes, x_label, y_label)
        self.energy_curve = VMobject()
        self.add(self.energy_curve)

    def create_rg_plot(self):
        """Erstelle Radius of Gyration Plot"""
        # Schätze sinnvolle y-range basierend auf initial R_g
        # Für LINEAR config ist R_g typisch ~3-6 Å
        # Für RANDOM config kann R_g größer sein
        rg_init = self.initial_rg
        y_min = 0  # R_g ist immer positiv
        y_max = max(15.0, rg_init * 2.0)  # Mindestens 15 Å oder 2x initial
        y_step = max(1.0, y_max / 5)  # ~5 Ticks

        self.rg_axes = Axes(
            x_range=[0, self.n_steps, max(1, self.n_steps // 10)],
            y_range=[y_min, y_max, y_step],
            width=5.5,
            height=2.0,
            axis_config={"include_tip": True}
        ).move_to(self.rg_plot_center)

        # Speichere für R_g-Plot Updates
        self.rg_y_min = y_min
        self.rg_y_max = y_max

        x_label = Text(get_string("mc_steps"), color=WHITE).scale(0.3)
        x_label.next_to(self.rg_axes.get_x_axis(), DOWN, buff=0.2)

        y_label = Text(get_string("rg_label"), color=WHITE).scale(0.3)
        y_label.next_to(self.rg_axes.get_y_axis(), LEFT)
        y_label.rotate(90 * DEGREES)

        self.add(self.rg_axes, x_label, y_label)
        self.rg_curve = VMobject()
        self.add(self.rg_curve)

    def initialize_configuration(self):
        """Initialisiere Polymer-Konfiguration mit FESTER Topologie"""
        if self.initial_config == "LINEAR":
            self.bead_positions = np.zeros((self.n_beads, 2))
            direction = np.array([1.0, 1.0]) / np.sqrt(2.0)
            chain_length = (self.n_beads - 1) * self.initial_spacing
            start_pos = -0.5 * chain_length * direction

            for i in range(self.n_beads):
                self.bead_positions[i] = start_pos + i * self.initial_spacing * direction

        elif self.initial_config == "RANDOM":
            # Zufällige Positionen (uniform in Box)
            self.bead_positions = np.random.uniform(
                -self.box_size / 2, self.box_size / 2,
                size=(self.n_beads, 2)
            )
            # TOPOLOGIE bleibt (0-1), (1-2), ... (18-19)
            # auch wenn Abstände groß sind!

            # Verifiziere dass alle Beads IN der Box sind
            box_half = self.box_size / 2
            for i in range(self.n_beads):
                assert np.all(np.abs(self.bead_positions[i]) <= box_half), \
                    f"Bead {i} is outside box!"
            print(f"✓ All {self.n_beads} beads initialized within box [-{box_half}, {box_half}]")

        # Setze Boundary Wall bei 1.1 * box_size
        self.wall_distance = 1.1 * self.box_size / 2  # Harmonische Wand bei 1.1*box_size
        self.k_wall = 100.0  # kcal/(mol·Å²) - Federkonstante der Wand

        # Für MD: Initialgeschwindigkeiten (Maxwell-Boltzmann)
        if self.sampling_method == "MD":
            sigma_v = np.sqrt(self.k_B * self.temperature / self.mass)  # Å/ps
            self.velocities = np.random.normal(0, sigma_v, size=(self.n_beads, 2))
        else:
            self.velocities = np.zeros((self.n_beads, 2))

        # Erstelle Visualisierung
        self._create_polymer_visual()

        # Initial energy
        self.initial_energy = self.calculate_total_energy()
        self.current_energy = self.initial_energy
        self.energy_history.append(self.current_energy)

        # Initial radius of gyration
        self.initial_rg, _ = self.calculate_radius_of_gyration()
        self.current_rg = self.initial_rg
        self.rg_history.append(self.current_rg)

    def _create_polymer_visual(self):
        """Erstelle Bead und Bond Visualisierung"""
        # Clear old
        for dot in self.bead_dots:
            self.remove(dot)
        for line in self.bond_lines:
            self.remove(line)

        self.bead_dots = []
        self.bond_lines = []

        # Create beads
        self.bead_radius = 0.5 * self.r0_bond * self.visual_scale

        for i in range(self.n_beads):
            pos = self.bead_positions[i]
            screen_pos = self.sim_box_center + np.array([
                pos[0] * self.visual_scale,
                pos[1] * self.visual_scale,
                0
            ])

            bead = Dot(
                point=screen_pos,
                radius=self.bead_radius,
                color=BLUE,
                fill_opacity=0.8
            )
            self.bead_dots.append(bead)
            self.add(bead)

        # Create bonds (entlang self.bond_list)
        for i, j in self.bond_list:
            line = Line(
                self.bead_dots[i].get_center(),
                self.bead_dots[j].get_center(),
                stroke_width=2,
                color=WHITE
            )
            self.bond_lines.append(line)
            self.add(line)

        # Create Radius of Gyration visualization (transparent circle + COM dot)
        rg, com = self.calculate_radius_of_gyration()

        # Schwerpunkt (Center of Mass)
        com_screen = self.sim_box_center + np.array([
            com[0] * self.visual_scale,
            com[1] * self.visual_scale,
            0
        ])
        self.com_dot = Dot(
            point=com_screen,
            radius=0.08,
            color=RED,
            fill_opacity=0.6
        )

        # R_g Kreis (transparent)
        rg_screen_radius = rg * self.visual_scale
        self.rg_circle = Circle(
            radius=rg_screen_radius,
            stroke_color=ORANGE,
            stroke_width=1.5,
            fill_opacity=0.1,
            fill_color=ORANGE
        ).move_to(com_screen)

        self.add(self.rg_circle)
        self.add(self.com_dot)

    # ========================================================================
    # ENERGY CALCULATIONS
    # ========================================================================

    def calculate_bond_energy(self):
        """Berechne Bindungsenergie über FESTE TOPOLOGIE"""
        energy = 0.0
        for i, j in self.bond_list:
            r_vec = self.bead_positions[j] - self.bead_positions[i]
            r = np.linalg.norm(r_vec)
            if r > 0.01:
                energy += 0.5 * self.k_bond * (r - self.r0_bond) ** 2
        return energy

    def calculate_lj_energy(self):
        """Berechne Lennard-Jones Energie (nur direkt gebundene Paare werden übersprungen)"""
        energy = 0.0
        for i in range(self.n_beads):
            for j in range(i + 1, self.n_beads):
                # Überspringe direkt gebundene Paare
                if (i, j) in self.bonded_pairs:
                    continue

                r_vec = self.bead_positions[j] - self.bead_positions[i]
                r = np.linalg.norm(r_vec)

                if r < self.cutoff_lj and r > 0.1:
                    sigma_over_r = self.sigma_lj / r
                    energy += 4 * self.epsilon_lj * (sigma_over_r**12 - sigma_over_r**6)

        return energy

    def calculate_wall_energy(self):
        """Berechne harmonische Wand-Potential Energie"""
        energy = 0.0
        for i in range(self.n_beads):
            for dim in range(2):
                pos = self.bead_positions[i, dim]

                # Obere Wand
                if pos > self.wall_distance:
                    penetration = pos - self.wall_distance
                    energy += 0.5 * self.k_wall * penetration**2

                # Untere Wand
                elif pos < -self.wall_distance:
                    penetration = -self.wall_distance - pos
                    energy += 0.5 * self.k_wall * penetration**2

        return energy

    def calculate_total_energy(self):
        """Berechne Gesamtenergie (inkl. Wand-Potential)"""
        return self.calculate_bond_energy() + self.calculate_lj_energy() + self.calculate_wall_energy()

    def calculate_radius_of_gyration(self):
        """Berechne Gyrationsradius und Schwerpunkt

        Returns:
            rg (float): Gyrationsradius in Å
            com (np.array): Schwerpunkt (2D)
        """
        # Schwerpunkt berechnen (center of mass)
        com = np.mean(self.bead_positions, axis=0)

        # Gyrationsradius: R_g = sqrt((1/N) * sum_i |r_i - r_COM|^2)
        distances_sq = np.sum((self.bead_positions - com) ** 2, axis=1)
        rg = np.sqrt(np.mean(distances_sq))

        return rg, com

    def calculate_forces(self):
        """Berechne Kräfte F = -∇E (für OPT, NAIVE, MD)"""
        forces = np.zeros_like(self.bead_positions)

        # Bond forces
        for i, j in self.bond_list:
            r_vec = self.bead_positions[j] - self.bead_positions[i]
            r = np.linalg.norm(r_vec)
            if r > 0.01:
                direction = r_vec / r
                force_mag = self.k_bond * (r - self.r0_bond)
                forces[i] += force_mag * direction
                forces[j] -= force_mag * direction

        # LJ forces
        for i in range(self.n_beads):
            for j in range(i + 1, self.n_beads):
                # Überspringe direkt gebundene Paare
                if (i, j) in self.bonded_pairs:
                    continue

                r_vec = self.bead_positions[j] - self.bead_positions[i]
                r = np.linalg.norm(r_vec)

                if r < self.cutoff_lj and r > 0.1:
                    direction = r_vec / r
                    sigma_over_r = self.sigma_lj / r
                    lj_deriv = 24 * self.epsilon_lj / r * (2 * sigma_over_r**12 - sigma_over_r**6)
                    forces[i] += lj_deriv * direction
                    forces[j] -= lj_deriv * direction

        # Harmonische Wand-Potentialwand bei 1.1*box_size (versteckt)
        # Verhindert dass Beads die Box verlassen
        for i in range(self.n_beads):
            for dim in range(2):  # x und y Richtung
                pos = self.bead_positions[i, dim]

                # Obere Wand (positiv)
                if pos > self.wall_distance:
                    penetration = pos - self.wall_distance
                    forces[i, dim] -= self.k_wall * penetration  # Rückstellkraft

                # Untere Wand (negativ)
                elif pos < -self.wall_distance:
                    penetration = -self.wall_distance - pos
                    forces[i, dim] += self.k_wall * penetration  # Rückstellkraft

        return forces

    # ========================================================================
    # METHODEN-IMPLEMENTIERUNG (werden in den nächsten Teilen gefüllt)
    # ========================================================================

    def run_simulation(self):
        """Dispatcher zu richtigem Sampling-Ansatz"""
        print(f"Starting {self.sampling_method} sampling...")

        if self.sampling_method == "MC":
            self._run_mc()
        elif self.sampling_method == "NAIVE":
            self._run_naive()
        elif self.sampling_method == "MD":
            self._run_md()
        elif self.sampling_method == "OPT":
            self._run_optimization()

        print(f"Finished!")

    # ========================================================================
    # SAMPLING METHODEN
    # ========================================================================

    def _run_optimization(self):
        """Pure Gradient Descent Optimization mit normalisierter Schrittweite"""
        print("Starting Pure Gradient Descent Optimization...")

        for step in range(self.n_steps):
            self.step = step + 1

            # Calculate forces
            forces = self.calculate_forces()
            force_norm = np.linalg.norm(forces)

            # Normalisiere Kräfte um Explosion zu verhindern
            if force_norm > 1e-6:
                forces_normalized = forces / force_norm
            else:
                forces_normalized = forces

            # Adaptive step size (sehr konservativ bei großen Kräften)
            alpha = self.alpha_init
            old_energy = self.calculate_total_energy()
            old_positions = self.bead_positions.copy()

            # Versuche Schritt mit normalisierten Kräften
            self.bead_positions = old_positions + alpha * forces_normalized
            new_energy = self.calculate_total_energy()

            # Backtracking if energy increases
            backtrack_count = 0
            while new_energy > old_energy and backtrack_count < 10:
                alpha *= 0.5
                # Rückgängigmachen und neuer kleinerer Schritt
                self.bead_positions = old_positions + alpha * forces_normalized
                new_energy = self.calculate_total_energy()
                backtrack_count += 1

            # Wenn zu viel Backtracking nötig war, akzeptiere dennoch kleinen Schritt
            if backtrack_count >= 10:
                self.bead_positions = old_positions + 0.001 * forces_normalized
                new_energy = self.calculate_total_energy()

            self.current_energy = new_energy

            # Track (immer)
            self.step_history.append(self.step)
            self.energy_history.append(new_energy)
            self.current_rg, _ = self.calculate_radius_of_gyration()
            self.rg_history.append(self.current_rg)

            # Visualize (nur periodisch)
            if self.step % self.vis_freq == 0 or self.step <= 10:
                self.update_polymer_visual()
                self._update_energy_plot_opt(force_norm, alpha)
                self._update_rg_plot()
                self.wait(0.001)

            # Convergence check
            if force_norm < self.opt_tolerance:
                print(f"Converged at step {self.step} (F_norm={force_norm:.2e})")
                break

            if self.step % 50 == 0:
                print(f"Step {self.step}: E={new_energy:.2f}, F_norm={force_norm:.2e}, α={alpha:.4f}")

    def _run_naive(self):
        """Naive Sampling + Geometry Optimization"""
        print("Starting Naive Sampling with Gradient Descent...")

        for step in range(self.n_steps):
            self.step = step + 1

            # 1. Random perturbation (ALL beads)
            displacement = np.random.randn(self.n_beads, 2) * self.perturbation_strength
            self.bead_positions += displacement

            # 2. Energy before optimization
            energy_before = self.calculate_total_energy()

            # 3. Gradient Descent (mit adaptiver Schrittweite)
            for opt_step in range(self.opt_max_steps):
                forces = self.calculate_forces()
                force_norm = np.linalg.norm(forces)

                if force_norm < self.opt_tolerance:
                    break

                # Normalisiere Kräfte
                if force_norm > 1e-6:
                    forces_normalized = forces / force_norm
                else:
                    forces_normalized = forces

                # Adaptive Schrittweite mit Backtracking
                alpha = 0.01  # Konservativ
                old_energy = self.calculate_total_energy()
                old_pos = self.bead_positions.copy()

                # Versuche Schritt
                self.bead_positions = old_pos + alpha * forces_normalized
                new_energy = self.calculate_total_energy()

                # Backtracking
                backtrack_count = 0
                while new_energy > old_energy and backtrack_count < 5:
                    alpha *= 0.5
                    self.bead_positions = old_pos + alpha * forces_normalized
                    new_energy = self.calculate_total_energy()
                    backtrack_count += 1

            # 4. Energy after optimization
            energy_after = self.calculate_total_energy()
            energy_reduction = energy_before - energy_after

            self.current_energy = energy_after

            # Track (immer)
            self.step_history.append(self.step)
            self.energy_before_history.append(energy_before)
            self.energy_after_history.append(energy_after)
            self.energy_history.append(energy_after)
            self.current_rg, _ = self.calculate_radius_of_gyration()
            self.rg_history.append(self.current_rg)

            # Visualize (nur periodisch)
            if self.step % self.vis_freq == 0 or self.step <= 10:
                self.update_polymer_visual()
                self._update_energy_plot_naive(energy_before, energy_after)
                self._update_rg_plot()
                self.wait(0.001)

            if self.step % 50 == 0:
                print(f"Step {self.step}: E_before={energy_before:.2f}, E_after={energy_after:.2f}, ΔE={energy_reduction:.2f}")

    def clamp_velocities(self):
            """Clamp velocities to prevent unphysical motion"""
            if not self.enable_velocity_clamping:
                return
                
            clamped_count = 0
            max_vel_found = 0.0
            
            for i in range(len(self.velocities)):
                vel_magnitude = np.linalg.norm(self.velocities[i])
                max_vel_found = max(max_vel_found, vel_magnitude)
                
                if vel_magnitude > self.max_velocity:
                    # Scale velocity to maximum allowed magnitude
                    self.velocities[i] = (self.velocities[i] / vel_magnitude) * self.max_velocity
                    clamped_count += 1
                elif vel_magnitude > self.velocity_warning_threshold:
                    # Optional: Log high velocity warning
                    if self.step % 100 == 0:  # Don't spam warnings
                        print(f"Warning: High velocity {vel_magnitude:.2f} at bead {i}, step {self.step}")
            
            # Log clamping events
            if clamped_count > 0 and self.step % 50 == 0:
                print(f"Step {self.step}: Clamped {clamped_count} velocities (max found: {max_vel_found:.2f})")


    def _run_md(self):
        """Molecular Dynamics with Velocity Verlet + Berendsen"""
        print("Starting Molecular Dynamics...")

        self.max_velocity = 15.0  # Maximum allowed velocity magnitude (Å/ps)
        self.velocity_warning_threshold = 3.0  # Threshold for warnings
        self.enable_velocity_clamping = False  # Toggle for clamping

        for step in range(self.n_steps):
            # Multiple MD steps per frame
            for _ in range(self.steps_per_frame):
                self.step += 1

                # 1. Half-step velocity update
                forces = self.calculate_forces()
                self.velocities += 0.5 * self.dt * forces / self.mass
                self.clamp_velocities()
                # 2. Full-step position update
                self.bead_positions += self.dt * self.velocities

                # 3. New forces
                forces = self.calculate_forces()

                # 4. Half-step velocity update
                self.velocities += 0.5 * self.dt * forces / self.mass
                self.clamp_velocities()
                # 5. Berendsen thermostat
                temp = self._berendsen_thermostat()

                # 6. Calculate energies
                ke = 0.5 * self.mass * np.sum(self.velocities ** 2)
                pe = self.calculate_total_energy()
                total_e = ke + pe

                # Track
                self.ke_history.append(ke)
                self.pe_history.append(pe)
                self.energy_history.append(total_e)
                self.temp_history.append(temp)
                self.current_energy = total_e
                self.current_rg, _ = self.calculate_radius_of_gyration()
                self.rg_history.append(self.current_rg)

            self.step_history.append(self.step)

            # Visualize (periodically)
            if step % self.vis_freq == 0 or step <= 10:
                self.update_polymer_visual()
                self._update_energy_plot_md()
                self._update_rg_plot()
                self.wait(0.001)

            if self.step % 100 == 0:
                print(f"Step {self.step}: T={temp:.1f}K, KE={ke:.2f}, PE={pe:.2f}")

    def _run_mc(self):
        """Monte Carlo with Metropolis Algorithm"""
        print("Starting Monte Carlo sampling...")

        n_accepted = 0
        n_rejected = 0

        for step in range(self.n_steps):
            self.step = step + 1

            # Select random bead (avoid endpoints)
            bead_idx = np.random.randint(0, self.n_beads)

            # Store old state
            old_pos = self.bead_positions[bead_idx].copy()
            old_energy = self.calculate_total_energy()

            # Propose move
            displacement = np.random.uniform(-self.max_displacement, self.max_displacement, size=2)
            self.bead_positions[bead_idx] += displacement

            # New energy
            new_energy = self.calculate_total_energy()
            delta_e = new_energy - old_energy

            # Metropolis criterion
            if delta_e < 0:
                accept = True
                p_accept = 1.0
            else:
                p_accept = np.exp(-self.beta * delta_e)
                accept = np.random.random() < p_accept

            if accept:
                self.current_energy = new_energy
                n_accepted += 1
                accepted = True
            else:
                self.bead_positions[bead_idx] = old_pos
                n_rejected += 1
                accepted = False

            # Track (immer)
            self.step_history.append(self.step)
            self.energy_history.append(self.current_energy)
            self.current_rg, _ = self.calculate_radius_of_gyration()
            self.rg_history.append(self.current_rg)

            # Visualize (nur periodisch)
            if self.step % self.vis_freq == 0 or self.step <= 10:
                self.update_polymer_visual()
                self._update_energy_plot_mc(accepted)
                self._update_rg_plot()
                self.wait(0.001)

            if self.step % 100 == 0:
                accept_rate = 100 * n_accepted / (n_accepted + n_rejected) if (n_accepted + n_rejected) > 0 else 0
                print(f"Step {self.step}: E={self.current_energy:.2f}, Accept={accept_rate:.1f}%")

    # ========================================================================
    # HILFSMETHODEN
    # ========================================================================

    def _berendsen_thermostat(self):
        """Berendsen velocity rescaling thermostat"""
        # Calculate kinetic energy and current temperature
        ke = 0.5 * self.mass * np.sum(self.velocities ** 2)
        # In 2D: T = 2*KE / (N * k_B)
        T_current = 2 * ke / (self.n_beads * self.k_B)

        # Scaling factor
        lambda_scale = np.sqrt(1 + (self.dt / self.berendsen_tau) * (self.temperature / T_current - 1))

        # Rescale velocities
        self.velocities *= lambda_scale

        return T_current

    # ========================================================================
    # VISUALISIERUNGS-UPDATE METHODEN
    # ========================================================================

    def _update_energy_plot_opt(self, force_norm, alpha):
        """Update plot für OPT"""
        if len(self.step_history) > 1:
            self.remove(self.energy_curve)

            points = []
            for step, energy in zip(self.step_history, self.energy_history):
                x = step
                y = energy
                if self.energy_y_min <= y <= self.energy_y_max:
                    points.append(self.energy_axes.coords_to_point(x, y))

            if len(points) > 1:
                self.energy_curve = VMobject()
                self.energy_curve.set_points_as_corners(points)
                self.energy_curve.set_stroke(GREEN, width=2)
                self.add(self.energy_curve)

    def _update_energy_plot_naive(self, e_before, e_after):
        """Update plot für NAIVE (zwei Kurven)"""
        if len(self.energy_before_history) > 1:
            self.remove(self.energy_curve)

            # Before curve (blue)
            points_before = []
            for step, energy in zip(self.step_history, self.energy_before_history):
                if self.energy_y_min <= energy <= self.energy_y_max:
                    points_before.append(self.energy_axes.coords_to_point(step, energy))

            if len(points_before) > 1:
                self.energy_curve = VMobject()
                self.energy_curve.set_points_as_corners(points_before)
                self.energy_curve.set_stroke(BLUE, width=2)
                self.add(self.energy_curve)

            # After curve (green)
            points_after = []
            for step, energy in zip(self.step_history, self.energy_after_history):
                if self.energy_y_min <= energy <= self.energy_y_max:
                    points_after.append(self.energy_axes.coords_to_point(step, energy))

            if len(points_after) > 1:
                curve_after = VMobject()
                curve_after.set_points_as_corners(points_after)
                curve_after.set_stroke(GREEN, width=2)
                self.add(curve_after)

    def _update_energy_plot_md(self):
        """Update plot für MD (drei Kurven: KE, PE, Total)"""
        if len(self.ke_history) > 1:
            self.remove(self.energy_curve)

            # Total energy (yellow)
            points_total = []
            for step, energy in zip(self.step_history, self.energy_history):
                if self.energy_y_min <= energy <= self.energy_y_max:
                    points_total.append(self.energy_axes.coords_to_point(step, energy))

            if len(points_total) > 1:
                self.energy_curve = VMobject()
                self.energy_curve.set_points_as_corners(points_total)
                self.energy_curve.set_stroke(YELLOW, width=2)
                self.add(self.energy_curve)

    def _update_energy_plot_mc(self, accepted):
        """Update plot für MC (eine Kurve + Dots)"""
        if len(self.step_history) > 1:
            self.remove(self.energy_curve)

            points = []
            for step, energy in zip(self.step_history, self.energy_history):
                if self.energy_y_min <= energy <= self.energy_y_max:
                    points.append(self.energy_axes.coords_to_point(step, energy))

            if len(points) > 1:
                self.energy_curve = VMobject()
                self.energy_curve.set_points_as_corners(points)
                self.energy_curve.set_stroke(YELLOW, width=2)
                self.add(self.energy_curve)

            # Add marker
            marker_color = GREEN if accepted else RED
            marker = Dot(
                self.energy_axes.coords_to_point(self.step, self.current_energy),
                radius=0.04,
                color=marker_color,
                fill_opacity=0.8
            )
            self.add(marker)

    def _update_rg_plot(self):
        """Update R_g Plot"""
        if len(self.step_history) > 1:
            self.remove(self.rg_curve)

            points = []
            for step, rg in zip(self.step_history, self.rg_history):
                if self.rg_y_min <= rg <= self.rg_y_max:
                    points.append(self.rg_axes.coords_to_point(step, rg))

            if len(points) > 1:
                self.rg_curve = VMobject()
                self.rg_curve.set_points_as_corners(points)
                self.rg_curve.set_stroke(ORANGE, width=2)
                self.add(self.rg_curve)


    def update_polymer_visual(self):
        """Update Bead Positionen, Bonds, R_g Kreis und Schwerpunkt"""
        for i in range(self.n_beads):
            pos = self.bead_positions[i]
            screen_pos = self.sim_box_center + np.array([
                pos[0] * self.visual_scale,
                pos[1] * self.visual_scale,
                0
            ])
            self.bead_dots[i].move_to(screen_pos)

        for idx, (i, j) in enumerate(self.bond_list):
            self.bond_lines[idx].put_start_and_end_on(
                self.bead_dots[i].get_center(),
                self.bead_dots[j].get_center()
            )

        # Update R_g Kreis und Schwerpunkt
        rg, com = self.calculate_radius_of_gyration()
        com_screen = self.sim_box_center + np.array([
            com[0] * self.visual_scale,
            com[1] * self.visual_scale,
            0
        ])

        # Update COM dot position
        self.com_dot.move_to(com_screen)

        # Update R_g circle (remove old, create new)
        self.remove(self.rg_circle)
        rg_screen_radius = rg * self.visual_scale
        self.rg_circle = Circle(
            radius=rg_screen_radius,
            stroke_color=ORANGE,
            stroke_width=1.5,
            fill_opacity=0.1,
            fill_color=ORANGE
        ).move_to(com_screen)
        self.add(self.rg_circle)


if __name__ == "__main__":
    # Run with: manimgl polymer_sampling_comparison.py PolymerSamplingComparison
    pass
