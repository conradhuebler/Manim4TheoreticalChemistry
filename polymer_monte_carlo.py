#!/usr/bin/env python3
"""
Polymer Coarse-Graining Monte Carlo Simulation
Polymer Coarse-Graining Monte Carlo Simulation

Demonstrates Monte Carlo simulation of a coarse-grained polymer:
- Left: Simulation box with 20 polymer segments (beads)
- Right Top: Energy evolution with accept/reject markers
- Right Bottom: Statistics (acceptance rate, energy components)

Physics model:
- Harmonic bonds between adjacent beads
- Lennard-Jones interactions between all bead pairs
- Metropolis Monte Carlo at T = 300 K

Animation shows polymer collapsing from stretched to coiled state.
"""

from manimlib import *
import numpy as np

# Language setting
LANGUAGE = "EN"  # Set to "EN" for English

STRINGS = {
    "DE": {
        "title": "Monte Carlo: Polymer Coarse-Graining",
        "simulation": "Simulationsbox",
        "energy_plot": "Energieverlauf",
        "statistics": "Statistik",
        "mc_steps": "MC Steps",
        "energy": "Energie (kcal/mol)",
        "total_energy": "Gesamtenergie",
        "bond_energy": "Bindungsenergie",
        "lj_energy": "LJ-Energie",
        "temperature": "Temperatur",
        "acceptance_rate": "Akzeptanzrate",
        "accepted": "Akzeptiert",
        "rejected": "Abgelehnt",
        "current_move": "Aktueller Move",
        "step": "Schritt",
        "metropolis_title": "Metropolis-Kriterium",
        "delta_e": "ΔE",
        "random_r": "Zufallszahl r",
        "prob_accept": "P(accept)",
        "decision": "Entscheidung",
        "accept_label": "✓ AKZEPTIERT",
        "reject_label": "✗ ABGELEHNT",
    },
    "EN": {
        "title": "Monte Carlo: Polymer Coarse-Graining",
        "simulation": "Simulation Box",
        "energy_plot": "Energy Evolution",
        "statistics": "Statistics",
        "mc_steps": "MC Steps",
        "energy": "Energy (kcal/mol)",
        "total_energy": "Total Energy",
        "bond_energy": "Bond Energy",
        "lj_energy": "LJ Energy",
        "temperature": "Temperature",
        "acceptance_rate": "Acceptance Rate",
        "accepted": "Accepted",
        "rejected": "Rejected",
        "current_move": "Current Move",
        "step": "Step",
        "metropolis_title": "Metropolis Criterion",
        "delta_e": "ΔE",
        "random_r": "Random r",
        "prob_accept": "P(accept)",
        "decision": "Decision",
        "accept_label": "✓ ACCEPTED",
        "reject_label": "✗ REJECTED",
    }
}

def get_string(key):
    return STRINGS[LANGUAGE].get(key, key)


# ============================================================================
# PARAMETER PRESETS - Verschiedene vordefinierte Konfigurationen
# ============================================================================
# Wähle eins der Presets unten aus und ändere ACTIVE_PRESET entsprechend:
# "REALISTIC", "DEMO", "SLOW", oder "EDUCATIONAL"

PARAMETER_PRESETS = {
    "REALISTIC": {
        "description": "Physikalisch realistische Parameter für echte Polymersimulationen",
        "polymer_geometry": {
            "n_beads": 20,
            "initial_spacing": 1.6,  # Å - Kette: 19 × 1.6 / √2 = 21.4 Å diagonal
            "box_size": 35.0,        # Å - Puffer: 13.6 Å für Bewegungen
            "r0_bond": 1.5,          # Å - Gleichgewichts-Bindungslänge
        },
        "physical_forces": {
            "k_bond": 300.0,         # kcal/(mol·Å²) - typisch für C-C Bindungen
            "epsilon_lj": 1.5,       # kcal/mol - Van-der-Waals Anziehung
            "sigma_lj": 1.2,         # Å - kleinere Beads, spacing/sigma ≈ 1.33
            "cutoff_lj": 100.0,      # Å - Kein Cutoff, alle LJ-Paare berechnet
        },
        "mc_simulation": {
            "temperature": 300.0,     # K - Zimmertemperatur
            "k_B": 0.001987,          # kcal/(mol·K) - Boltzmann-Konstante
            "max_displacement": 0.15, # Å - optimiert für ~30-40% Akzeptanzrate
        },
        "visualization": {
            "visual_scale": 0.20,     # Skalierung für 35 Å Box
        },
    },

    "DEMO": {
        "description": "Optimiert für schnelle visuelle Demonstration mit gutem Kollaps",
        "polymer_geometry": {
            "n_beads": 20,
            "initial_spacing": 1.7,   # Å - Kette: 19 × 1.7 / √2 = 22.8 Å diagonal
            "box_size": 35.0,         # Å - Puffer: 12.2 Å für Bewegungen
            "r0_bond": 1.5,
        },
        "physical_forces": {
            "k_bond": 25.0,          # kcal/(mol·Å²) - etwas weicher
            "epsilon_lj": 30.0,        # kcal/mol - stärkere Anziehung → schnellerer Kollaps
            "sigma_lj": 2.2,          # Å - kleine Beads
            "cutoff_lj": 100.0,       # Å - Kein Cutoff, alle LJ-Paare berechnet
        },
        "mc_simulation": {
            "temperature": 600.0,
            "k_B": 0.001987,
            "max_displacement": 0.5,  # Å - größere Schritte → schneller
        },
        "visualization": {
            "visual_scale": 0.20,     # Skalierung für 35 Å Box
        },
    },

    "SLOW": {
        "description": "Langsame Relaxation - schwächere Kräfte für graduelle Animation",
        "polymer_geometry": {
            "n_beads": 20,
            "initial_spacing": 1.65,  # Å - Kette: 19 × 1.65 / √2 = 22.1 Å diagonal
            "box_size": 35.0,         # Å - Puffer: 12.9 Å für Bewegungen
            "r0_bond": 1.5,
        },
        "physical_forces": {
            "k_bond": 150.0,          # kcal/(mol·Å²) - weiche Bindungen
            "epsilon_lj": 0.5,        # kcal/mol - schwache Anziehung
            "sigma_lj": 1.2,          # Å - kleine Beads
            "cutoff_lj": 100.0,       # Å - Kein Cutoff, alle LJ-Paare berechnet
        },
        "mc_simulation": {
            "temperature": 350.0,     # K - höhere Temperatur → mehr Bewegung
            "k_B": 0.001987,
            "max_displacement": 0.1,  # Å - kleinere Schritte → glattere Animation
        },
        "visualization": {
            "visual_scale": 0.20,     # Skalierung für 35 Å Box
        },
    },

    "EDUCATIONAL": {
        "description": "Mit ausführlichen Erklärungen - wie REALISTIC aber für Lehre",
        "polymer_geometry": {
            "n_beads": 20,
            # Initiale Abstände bestimmen die Anfangskonfiguration
            # Zu große Werte → LJ-Wechselwirkungen außerhalb Cutoff, keine Anziehung
            # Optimal: initial_spacing ~ 1.3 × sigma (spacing/sigma > 1 verhindert Überlappung)
            "initial_spacing": 1.6,
            # Box-Größe muss genug Platz für diagonal gestreckte Kette haben
            # Diagonal: 19 Bindungen × 1.6 Å / √2 = 21.4 Å
            # Box: 35 Å gibt Puffer von 13.6 Å für Bewegungen
            "box_size": 35.0,
            # Gleichgewichts-Bindungslänge (wird durch Harmon. Potential optimiert)
            "r0_bond": 1.5,
        },
        "physical_forces": {
            # Bindungsfederkonstante
            # Höher = stärkere Rückstellkraft = stärkere Bindung
            # Typisch für C-C: 200-400 kcal/(mol·Å²)
            "k_bond": 300.0,
            # Lennard-Jones: tiefe der Potentialwanne
            # Höher = stärkere Van-der-Waals Anziehung
            "epsilon_lj": 1.5,
            # Lennard-Jones: charakteristische Länge
            # σ ≈ Größe der Beads im coarse-graining (1.2 Å)
            "sigma_lj": 1.2,
            # Cutoff-Distanz: Nur Wechselwirkungen bis hier berechnen
            # Kein Cutoff: alle LJ-Paare berechnet
            "cutoff_lj": 100.0,
        },
        "mc_simulation": {
            # Temperatur: steuert thermale Fluktuationen
            # 300 K = Zimmertemperatur
            "temperature": 300.0,
            # Boltzmann-Konstante in korrekten Einheiten
            # = 0.001987 kcal/(mol·K)
            "k_B": 0.001987,
            # Max. Verschiebung pro MC-Schritt
            # Zu groß → niedrige Akzeptanzrate, ineffizient
            # Zu klein → viele Schritte nötig
            # Optimal: 20-40% Akzeptanz → hier: 0.15 Å
            "max_displacement": 0.15,
        },
        "visualization": {
            # Skalierungsfaktor zur Anpassung an Bildschirm
            # Für 35 Å Box
            "visual_scale": 0.20,
        },
    },

    # ======================================================================
    # POTENZIAL-VERGLEICH SZENARIEN - Didaktische Varianten
    # ======================================================================

    "NO_LJ": {
        "description": "Nur harmonische Bindungen - zeigt Equilibrium ohne LJ Kollaps",
        "polymer_geometry": {
            "n_beads": 20,
            "initial_spacing": 1.7,
            "box_size": 35.0,
            "r0_bond": 1.5,
        },
        "physical_forces": {
            "k_bond": 300.0,         # Bindungen aktiv
            "epsilon_lj": 0.0,       # KEINE Lennard-Jones
            "sigma_lj": 1.2,
            "cutoff_lj": 100.0,
        },
        "mc_simulation": {
            "temperature": 300.0,
            "k_B": 0.001987,
            "max_displacement": 0.2,
        },
        "visualization": {
            "visual_scale": 0.20,
        },
    },

    "NO_BONDS": {
        "description": "Nur Lennard-Jones - zeigt LJ-Cluster ohne Ketten-Topologie",
        "polymer_geometry": {
            "n_beads": 20,
            "initial_spacing": 1.3,  # Kleiner für LJ Zusammenhalt
            "box_size": 35.0,
            "r0_bond": 1.5,
        },
        "physical_forces": {
            "k_bond": 0.0,           # KEINE Bindungen
            "epsilon_lj": 2.0,       # LJ aktiv (stark)
            "sigma_lj": 1.2,
            "cutoff_lj": 100.0,
        },
        "mc_simulation": {
            "temperature": 300.0,
            "k_B": 0.001987,
            "max_displacement": 0.2,
        },
        "visualization": {
            "visual_scale": 0.20,
        },
    },

    "BOTH": {
        "description": "Beide Potentiale aktiv - realistisches Polymer-Verhalten",
        "polymer_geometry": {
            "n_beads": 20,
            "initial_spacing": 1.7,
            "box_size": 35.0,
            "r0_bond": 1.5,
        },
        "physical_forces": {
            "k_bond": 300.0,         # Bindungen aktiv
            "epsilon_lj": 5000.0,       # LJ aktiv
            "sigma_lj": 2.4,
            "cutoff_lj": 100.0,      # Kein Cutoff
        },
        "mc_simulation": {
            "temperature": 300.0,
            "k_B": 0.001987,
            "max_displacement": 0.1,
        },
        "visualization": {
            "visual_scale": 0.20,
        },
    },

    "NONE": {
        "description": "Keine Potentiale - reine Brownian Diffusion",
        "polymer_geometry": {
            "n_beads": 20,
            "initial_spacing": 1.7,
            "box_size": 35.0,
            "r0_bond": 1.5,
        },
        "physical_forces": {
            "k_bond": 0.0,           # KEINE Bindungen
            "epsilon_lj": 0.0,       # KEINE LJ
            "sigma_lj": 1.2,
            "cutoff_lj": 100.0,
        },
        "mc_simulation": {
            "temperature": 300.0,
            "k_B": 0.001987,
            "max_displacement": 0.3,  # Größer da keine Kräfte widersprechen
        },
        "visualization": {
            "visual_scale": 0.20,
        },
    },
}

# ============================================================================
# WÄHLE HIER DAS AKTIVE PRESET (kann jederzeit geändert werden)
# ============================================================================
# Existierende: "REALISTIC", "DEMO", "SLOW", "EDUCATIONAL"
# Neue Varianten: "NO_LJ", "NO_BONDS", "BOTH", "NONE"
ACTIVE_PRESET = "DEMO"  # Test mit beiden Potentialen + aktiviertem LJ


class PolymerMonteCarlo(Scene):
    def construct(self):
        # Setup
        self.setup_parameters()
        self.setup_layout()
        self.create_polymer()
        self.create_energy_plot()
        self.create_statistics()
        self.create_metropolis_box()

        self.wait(0.5)

        # Run simulation
        self.run_simulation()

        self.wait(3)

    def setup_parameters(self):
        """Initialize all simulation parameters from active preset"""
        # Load active preset
        if ACTIVE_PRESET not in PARAMETER_PRESETS:
            raise ValueError(f"Unknown preset: {ACTIVE_PRESET}. Choose from: {list(PARAMETER_PRESETS.keys())}")

        preset = PARAMETER_PRESETS[ACTIVE_PRESET]
        print(f"\n{'='*70}")
        print(f"Loading preset: {ACTIVE_PRESET.upper()}")
        print(f"Description: {preset['description']}")
        print(f"{'='*70}\n")

        self.steps = 10000
        # ====== POLYMER GEOMETRY ======
        geometry = preset["polymer_geometry"]
        self.n_beads = geometry["n_beads"]
        self.initial_spacing = geometry["initial_spacing"]
        self.box_size = geometry["box_size"]
        self.r0_bond = geometry["r0_bond"]

        # ====== PHYSICAL FORCES ======
        forces = preset["physical_forces"]
        self.k_bond = forces["k_bond"]
        self.epsilon_lj = forces["epsilon_lj"]
        self.sigma_lj = forces["sigma_lj"]
        self.cutoff_lj = forces["cutoff_lj"]

        # ====== MC SIMULATION ======
        mc = preset["mc_simulation"]
        self.temperature = mc["temperature"]
        self.k_B = mc["k_B"]
        self.beta = 1.0 / (self.k_B * self.temperature)
        self.max_displacement = mc["max_displacement"]

        # ====== VISUALIZATION ======
        vis = preset["visualization"]
        self.visual_scale = vis["visual_scale"]

        # Bead radius based on Lennard-Jones σ parameter (physical interpretation)
        # σ represents the bead "diameter" in coarse-graining
        self.bead_radius = 0.5 * self.sigma_lj * self.visual_scale

        # Initialize polymer positions (stretched diagonal chain)
        # Diagonal initialization: from bottom-left to top-right
        # Provides more space than horizontal, especially important for larger chains
        self.bead_positions = np.zeros((self.n_beads, 2))
        chain_length = (self.n_beads - 1) * self.initial_spacing

        # Direction: diagonal (normalized to 45°)
        direction = np.array([1.0, 1.0]) / np.sqrt(2.0)

        # Starting position: center the chain within the box
        start_pos = -0.5 * chain_length * direction

        for i in range(self.n_beads):
            self.bead_positions[i] = start_pos + i * self.initial_spacing * direction

        # Simulation state
        self.mc_step = 0
        self.n_accepted = 0
        self.n_rejected = 0
        self.current_energy = self.calculate_total_energy()

        # Tracking data
        self.energy_history = [self.current_energy]
        self.bond_energy_history = [self.calculate_bond_energy()]
        self.lj_energy_history = [self.calculate_lj_energy()]
        self.step_history = [0]
        self.accepted_steps = []
        self.rejected_steps = []

        # Calculate appropriate energy range for plotting
        initial_bond = self.calculate_bond_energy()
        initial_lj = self.calculate_lj_energy()
        print(f"Initial energies - Bond: {initial_bond:.1f}, LJ: {initial_lj:.1f}, Total: {self.current_energy:.1f}")

        # Set y_range based on initial energy
        # Expect energy to decrease, so set range accordingly
        self.energy_y_min = min(-100, self.current_energy - 200)
        self.energy_y_max = max(400, self.current_energy + 100)
        print(f"Energy plot range: [{self.energy_y_min}, {self.energy_y_max}]")

    def setup_layout(self):
        """Create layout: simulation box left, plots right"""
        # Title
        title = Text(get_string("title"), color=YELLOW).scale(0.7)
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

        # Simulation label
        sim_label = Text(get_string("simulation"), color=BLUE).scale(0.5)
        sim_label.next_to(self.sim_box, UP, buff=0.2)
        self.add(sim_label)

        # Energy plot region (right top)
        self.energy_plot_center = RIGHT * 3.5 + UP * 1.5
        energy_plot_box = Rectangle(
            width=6, height=3,
            stroke_color=GREEN, stroke_width=1
        ).move_to(self.energy_plot_center)
        self.add(energy_plot_box)

        energy_label = Text(get_string("energy_plot"), color=GREEN).scale(0.4)
        energy_label.next_to(energy_plot_box, UP, buff=0.1)
        self.add(energy_label)

        # Statistics region (right bottom)
        self.stats_center = RIGHT * 3.5 + DOWN * 1.8
        stats_box = Rectangle(
            width=6, height=2.5,
            stroke_color=ORANGE, stroke_width=1
        ).move_to(self.stats_center)
        self.add(stats_box)

        stats_label = Text(get_string("statistics"), color=ORANGE).scale(0.4)
        stats_label.next_to(stats_box, UP, buff=0.1)
        self.add(stats_label)

    def create_polymer(self):
        """Create visual representation of polymer"""
        self.bead_dots = []
        self.bond_lines = []

        # Create beads
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

        # Create bonds
        for i in range(self.n_beads - 1):
            line = Line(
                self.bead_dots[i].get_center(),
                self.bead_dots[i+1].get_center(),
                stroke_width=2,
                color=WHITE
            )
            self.bond_lines.append(line)
            self.add(line)

    def create_energy_plot(self):
        """Create energy evolution plot"""
        # Axes (use dynamic range based on initial energy)
        # Fewer ticks for faster rendering
        x_step = 100  # Ticks every 100 steps instead of 50
        y_step = 1000000  # Larger energy steps

        self.energy_axes = Axes(
            x_range=[0, self.steps, self.steps/10],
            y_range=[self.energy_y_min, 100, y_step],
            width=5.5,
            height=2.5,
            axis_config={"include_tip": True}
        ).move_to(self.energy_plot_center)

        # Axis labels
        x_label = Text(get_string("mc_steps"), color=WHITE).scale(0.3)
        x_label.next_to(self.energy_axes.get_x_axis(), DOWN, buff=0.2)

        y_label = Text(get_string("energy"), color=WHITE).scale(0.3)
        y_label.next_to(self.energy_axes.get_y_axis(), LEFT, buff=0.3)
        y_label.rotate(90 * DEGREES)

        self.add(self.energy_axes, x_label, y_label)

        # Energy curve
        self.energy_curve = VMobject()
        self.add(self.energy_curve)

        # Accepted/Rejected markers storage
        self.accept_markers = []
        self.reject_markers = []

    def create_statistics(self):
        """Create statistics display"""
        stats_pos = self.stats_center + DOWN * 0.3

        # Use DecimalNumber for efficient updates
        # All consistent: scale=0.35, buff=0.08
        self.step_display = VGroup(
            Text(get_string("step") + ": ", color=WHITE).scale(0.35),
            Integer(0, color=WHITE).scale(0.35)
        ).arrange(RIGHT, buff=0.08)

        self.acceptance_display = VGroup(
            Text(get_string("acceptance_rate") + ": ", color=GREEN).scale(0.35),
            DecimalNumber(0, num_decimal_places=1, color=GREEN).scale(0.35),
            Text("%", color=GREEN).scale(0.35)
        ).arrange(RIGHT, buff=0.08)

        self.accepted_display = VGroup(
            Text(get_string("accepted") + ": ", color=GREEN).scale(0.35),
            Integer(0, color=GREEN).scale(0.35)
        ).arrange(RIGHT, buff=0.08)

        self.rejected_display = VGroup(
            Text(get_string("rejected") + ": ", color=RED).scale(0.35),
            Integer(0, color=RED).scale(0.35)
        ).arrange(RIGHT, buff=0.08)

        self.energy_display = VGroup(
            Text(get_string("total_energy") + ": ", color=YELLOW).scale(0.35),
            DecimalNumber(self.current_energy, num_decimal_places=1, color=YELLOW).scale(0.35)
        ).arrange(RIGHT, buff=0.08)

        self.bond_energy_display = VGroup(
            Text(get_string("bond_energy") + ": ", color=BLUE).scale(0.35),
            DecimalNumber(0, num_decimal_places=1, color=BLUE).scale(0.35)
        ).arrange(RIGHT, buff=0.08)

        self.lj_energy_display = VGroup(
            Text(get_string("lj_energy") + ": ", color=RED).scale(0.35),
            DecimalNumber(0, num_decimal_places=1, color=RED).scale(0.35)
        ).arrange(RIGHT, buff=0.08)

        self.temp_display = VGroup(
            Text(get_string("temperature") + ": ", color=ORANGE).scale(0.35),
            Text(f"{self.temperature:.0f} K", color=ORANGE).scale(0.35)
        ).arrange(RIGHT, buff=0.08)

        # Arrange in two columns: Simulation progress (left) and Energetics (right)
        left_column = VGroup(
            self.step_display,
            self.acceptance_display,
            self.accepted_display,
            self.rejected_display
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)

        right_column = VGroup(
            self.energy_display,
            self.bond_energy_display,
            self.lj_energy_display,
            self.temp_display
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)

        stats_group = VGroup(left_column, right_column).arrange(RIGHT, buff=0.4)
        stats_group.move_to(stats_pos)

        self.add(stats_group)

    def create_metropolis_box(self):
        """Create Metropolis algorithm visualization box"""
        # Position in the lower part of the stats area
        metro_pos = self.stats_center + UP * 0.8

        # Title
        metro_title = Text(get_string("metropolis_title"), color=YELLOW).scale(0.45)
        metro_title.move_to(metro_pos + UP * 0.5)
        #self.add(metro_title)

        # Create displays for Metropolis data with consistent formatting
        # All use scale 0.35 for text/numbers, buff=0.08 for spacing
        self.metro_delta_e_display = VGroup(
            Text(get_string("delta_e") + ": ", color=WHITE).scale(0.35),
            DecimalNumber(0, num_decimal_places=1, color=YELLOW).scale(0.35),
            Text(" kcal/mol", color=WHITE).scale(0.3)
        ).arrange(RIGHT, buff=0.08)

        self.metro_random_display = VGroup(
            Text(get_string("random_r") + ": ", color=WHITE).scale(0.35),
            DecimalNumber(0, num_decimal_places=3, color=BLUE).scale(0.35)
        ).arrange(RIGHT, buff=0.08)

        self.metro_prob_display = VGroup(
            Text(get_string("prob_accept") + ": ", color=WHITE).scale(0.35),
            DecimalNumber(0, num_decimal_places=3, color=GREEN).scale(0.35)
        ).arrange(RIGHT, buff=0.08)

        # Decision display (will be updated with color)
        self.metro_decision_text = Text(get_string("decision") + ": ", color=WHITE).scale(0.35)
        self.metro_decision_label = Text("---", color=WHITE).scale(0.35)
        self.metro_decision_display = VGroup(
            self.metro_decision_text,
            self.metro_decision_label
        ).arrange(RIGHT, buff=0.08)

        # Arrange in two columns for compact layout
        left_column = VGroup(
            self.metro_delta_e_display,
            self.metro_prob_display
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)

        right_column = VGroup(
            self.metro_random_display,
            self.metro_decision_display
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)

        metro_group = VGroup(left_column, right_column).arrange(RIGHT, buff=0.4)
        metro_group.move_to(metro_pos + DOWN * 0.15)

        self.metropolis_group = metro_group
        self.add(metro_group)

    def update_metropolis_display(self, metropolis_data):
        """Update Metropolis visualization with current move data"""
        delta_e = metropolis_data['delta_e']
        random_r = metropolis_data['random_r']
        prob_accept = metropolis_data['prob_accept']
        accepted = metropolis_data['accepted']

        # Update values
        self.metro_delta_e_display[1].set_value(delta_e)
        self.metro_random_display[1].set_value(random_r)
        self.metro_prob_display[1].set_value(prob_accept)

        # Update decision with color
        self.remove(self.metro_decision_label)
        if accepted:
            self.metro_decision_label = Text(get_string("accept_label"), color=GREEN).scale(0.35)
        else:
            self.metro_decision_label = Text(get_string("reject_label"), color=RED).scale(0.35)

        # Reposition
        self.metro_decision_label.next_to(self.metro_decision_text, RIGHT, buff=0.08)
        self.add(self.metro_decision_label)

        # Color delta_e based on sign
        if delta_e < 0:
            self.metro_delta_e_display[1].set_color(GREEN)
        else:
            self.metro_delta_e_display[1].set_color(RED)

    def calculate_bond_energy(self):
        """Calculate harmonic bond energy"""
        energy = 0.0
        for i in range(self.n_beads - 1):
            r = np.linalg.norm(self.bead_positions[i+1] - self.bead_positions[i])
            energy += 0.5 * self.k_bond * (r - self.r0_bond)**2
        return energy

    def calculate_lj_energy(self):
        """Calculate Lennard-Jones energy with cutoff"""
        energy = 0.0
        for i in range(self.n_beads):
            # Skip i+1 (bonded pair) and i+2 (nearest LJ neighbor, to prevent zigzag)
            # This prevents alternating bond compression from LJ attractions
            for j in range(i + 2, self.n_beads):
                r = np.linalg.norm(self.bead_positions[j] - self.bead_positions[i])
                print(f"Calculating LJ between beads {i} and {j} with distance {r:.3f} Å")

                if r < self.cutoff_lj and r > 0.1:  # Apply cutoff and avoid division by zero
                    sigma_over_r = self.sigma_lj / r
                    energy += 4 * self.epsilon_lj * (sigma_over_r**12 - sigma_over_r**6)
                    print(f"  LJ contribution: {4 * self.epsilon_lj * (sigma_over_r**12 - sigma_over_r**6):.3f} kcal/mol")
        return energy

    def calculate_total_energy(self):
        """Calculate total energy"""
        return self.calculate_bond_energy() + self.calculate_lj_energy()

    def debug_bond_lengths(self):
        """Debug function: Print bond lengths to detect zigzag patterns"""
        bond_lengths = []
        for i in range(self.n_beads - 1):
            r = np.linalg.norm(self.bead_positions[i+1] - self.bead_positions[i])
            bond_lengths.append(r)

        # Calculate statistics
        bonds_array = np.array(bond_lengths)
        mean_length = np.mean(bonds_array)
        std_length = np.std(bonds_array)

        # Check for alternating pattern: compare odd vs even bonds
        odd_bonds = bonds_array[::2]  # indices 0, 2, 4, ...
        even_bonds = bonds_array[1::2]  # indices 1, 3, 5, ...

        print(f"Step {self.mc_step}: Bond lengths - Mean: {mean_length:.4f}, Std: {std_length:.4f}")
        if len(odd_bonds) > 0:
            print(f"  Even-indexed bonds: mean={np.mean(odd_bonds):.4f}, std={np.std(odd_bonds):.4f}")
        if len(even_bonds) > 0:
            print(f"  Odd-indexed bonds:  mean={np.mean(even_bonds):.4f}, std={np.std(even_bonds):.4f}")
        print(f"  First 5 bonds: {[f'{x:.3f}' for x in bond_lengths[:5]]}")

    def monte_carlo_move(self):
        """Perform one Monte Carlo move and return Metropolis data"""
        # Select random bead (avoid endpoints for stability)
        bead_index = np.random.randint(1, self.n_beads - 1)

        # Store old position
        old_position = self.bead_positions[bead_index].copy()
        old_energy = self.current_energy

        # Propose new position
        displacement = np.random.uniform(-self.max_displacement, self.max_displacement, size=2)
        self.bead_positions[bead_index] += displacement

        # Calculate new energy
        new_energy = self.calculate_total_energy()
        delta_energy = new_energy - old_energy

        # Metropolis acceptance criterion
        accept = False
        random_number = np.random.random()
        acceptance_prob = 1.0  # Default for delta_energy < 0

        if delta_energy < 0:
            # Always accept if energy decreases
            accept = True
            acceptance_prob = 1.0
        else:
            # Accept with probability exp(-ΔE/kT)
            acceptance_prob = np.exp(-self.beta * delta_energy)
            if random_number < acceptance_prob:
                accept = True

        if accept:
            # Accept move
            self.current_energy = new_energy
            self.n_accepted += 1
        else:
            # Reject move - restore old position
            self.bead_positions[bead_index] = old_position
            self.n_rejected += 1

        # Return all Metropolis data for visualization
        metropolis_data = {
            'bead_index': bead_index,
            'accepted': accept,
            'delta_e': delta_energy,
            'random_r': random_number,
            'prob_accept': acceptance_prob
        }

        return metropolis_data

    def update_polymer_visual(self, highlight_bead=None, accepted=None):
        """Update polymer visualization"""
        # Update bead positions
        for i in range(self.n_beads):
            pos = self.bead_positions[i]
            screen_pos = self.sim_box_center + np.array([
                pos[0] * self.visual_scale,
                pos[1] * self.visual_scale,
                0
            ])
            self.bead_dots[i].move_to(screen_pos)

            # Highlight current bead
            if i == highlight_bead:
                if accepted is None:
                    self.bead_dots[i].set_color(YELLOW)
                elif accepted:
                    self.bead_dots[i].set_color(GREEN)
                else:
                    self.bead_dots[i].set_color(RED)
            else:
                self.bead_dots[i].set_color(BLUE)

        # Update bonds
        for i in range(self.n_beads - 1):
            self.bond_lines[i].put_start_and_end_on(
                self.bead_dots[i].get_center(),
                self.bead_dots[i+1].get_center()
            )

    def update_energy_plot(self, accepted):
        """Update energy plot"""
        # Add current step to history
        self.step_history.append(self.mc_step)
        self.energy_history.append(self.current_energy)
        self.bond_energy_history.append(self.calculate_bond_energy())
        self.lj_energy_history.append(self.calculate_lj_energy())

        if accepted:
            self.accepted_steps.append((self.mc_step, self.current_energy))
        else:
            self.rejected_steps.append((self.mc_step, self.current_energy))

        # Update energy curve
        if len(self.step_history) > 1:
            self.remove(self.energy_curve)

            # Adjust x_range dynamically if needed
            max_step = max(self.step_history)
            if max_step > self.energy_axes.x_range[1] - 50:
                new_max = max_step + 50
                # Don't rebuild axes, just update range reference
                self.energy_axes.x_range[1] = new_max

            # Create curve
            points = []
            for step, energy in zip(self.step_history, self.energy_history):
                if self.energy_axes.x_range[0] <= step <= self.energy_axes.x_range[1]:
                    points.append(self.energy_axes.coords_to_point(step, energy))

            if len(points) > 1:
                self.energy_curve = VMobject()
                self.energy_curve.set_points_as_corners(points)
                self.energy_curve.set_stroke(YELLOW, width=2)
                self.add(self.energy_curve)

        # Add marker for current step (but limit total markers for performance)
        if accepted:
            marker = Dot(
                self.energy_axes.coords_to_point(self.mc_step, self.current_energy),
                radius=0.05,
                color=GREEN,
                fill_opacity=0.9
            )
            self.accept_markers.append(marker)
            self.add(marker)

            # Remove old markers if too many
            if len(self.accept_markers) > 150:
                old_marker = self.accept_markers.pop(0)
                self.remove(old_marker)
        else:
            marker = Dot(
                self.energy_axes.coords_to_point(self.mc_step, self.current_energy),
                radius=0.04,
                color=RED,
                fill_opacity=0.8,
                stroke_width=1,
                stroke_color=RED
            )
            self.reject_markers.append(marker)
            self.add(marker)

            # Remove old markers if too many
            if len(self.reject_markers) > 150:
                old_marker = self.reject_markers.pop(0)
                self.remove(old_marker)

    def update_statistics(self):
        """Update statistics display"""
        # Calculate acceptance rate
        total_moves = self.n_accepted + self.n_rejected
        acceptance_rate = 100.0 * self.n_accepted / total_moves if total_moves > 0 else 0.0

        # Update displays
        self.step_display[1].set_value(self.mc_step)
        self.energy_display[1].set_value(self.current_energy)
        self.bond_energy_display[1].set_value(self.calculate_bond_energy())
        self.lj_energy_display[1].set_value(self.calculate_lj_energy())
        self.acceptance_display[1].set_value(acceptance_rate)
        self.accepted_display[1].set_value(self.n_accepted)
        self.rejected_display[1].set_value(self.n_rejected)

    def run_simulation(self):
        """Run Monte Carlo simulation"""
        # Phase 1: Slow demonstration with Metropolis visualization (20 steps)
        for i in range(10):
            self.mc_step += 1

            # Perform Monte Carlo move
            metro_data = self.monte_carlo_move()

            # Update Metropolis display
            self.update_metropolis_display(metro_data)

            # Highlight bead being moved
            self.update_polymer_visual(highlight_bead=metro_data['bead_index'])
            self.wait(3.5)

            # Show result
            self.update_polymer_visual(
                highlight_bead=metro_data['bead_index'],
                accepted=metro_data['accepted']
            )
            self.update_energy_plot(metro_data['accepted'])
            self.update_statistics()

            self.wait(3.5)

            # Reset bead color
            self.update_polymer_visual()

        # Debug after Phase 1
        print("\n=== DEBUG: After Phase 1 (20 steps) ===")
        self.debug_bond_lengths()
        print()

        # Phase 2: Medium speed (80 steps) - still show Metropolis
        for step_count in range(80):
            self.mc_step += 1
            metro_data = self.monte_carlo_move()

            self.update_metropolis_display(metro_data)
            self.update_polymer_visual()
            self.update_energy_plot(metro_data['accepted'])
            self.update_statistics()

            self.wait(0.02)

        # Debug after Phase 2
        print("\n=== DEBUG: After Phase 2 (100 steps total) ===")
        self.debug_bond_lengths()
        print()

        # Phase 3: Fast thermalization (400 steps) - hide Metropolis box
        self.remove(self.metropolis_group)
        self.remove(self.metro_decision_label)
        init_steps = self.mc_step
        for _ in range(self.steps - init_steps):
            self.mc_step += 1
            metro_data = self.monte_carlo_move()

            self.update_polymer_visual()
            self.update_energy_plot(metro_data['accepted'])
            self.update_statistics()

            self.wait(0.0001)

        # Debug after Phase 3
        print("\n=== DEBUG: After Phase 3 (1100 steps total) ===")
        self.debug_bond_lengths()
        print()


if __name__ == "__main__":
    # Run with: manimgl polymer_monte_carlo.py PolymerMonteCarlo
    pass
