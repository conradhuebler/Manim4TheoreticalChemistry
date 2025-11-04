#!/usr/bin/env python3
"""
Non-bonded Interactions Visualization
Visualisierung nichtbindender Wechselwirkungen

Shows van der Waals (Lennard-Jones) and electrostatic interactions:
- Left: Two non-bonded atoms approaching each other
- Right Top: Lennard-Jones potential V = 4ε[(σ/r)¹² - (σ/r)⁶]
- Right Bottom: Coulomb potential V = kq₁q₂/r

Animation demonstrates attractive and repulsive regions,
equilibrium distance, and the famous "12-6" potential.
"""

from manimlib import *
import numpy as np

# Language setting
LANGUAGE = "EN"  # Set to "EN" for English

STRINGS = {
    "DE": {
        "title": "Nichtbindende Wechselwirkungen",
        "molecule_view": "Atom-Atom Abstand",
        "lj_potential": "Lennard-Jones Potential",
        "coulomb_potential": "Coulomb Potential",
        "distance": "Abstand r (Å)",
        "energy": "Energie (kcal/mol)",
        "attractive": "Attraktiv (van der Waals)",
        "repulsive": "Repulsiv (Pauli)",
        "equilibrium": "Gleichgewicht (r_min)",
        "vdw_radius": "van der Waals Radius",
        "far_apart": "Weit entfernt",
        "close_contact": "Naher Kontakt",
        "optimal_distance": "Optimaler Abstand",
        "too_close": "Zu nah - Abstoßung!",
        "lj_formula": r"V_{LJ} = 4\varepsilon[(\sigma/r)^{12}-(\sigma/r)^6]",
        "coulomb_formula": r"V_C = kq_1q_2/r",
        "total_formula": r"V_{tot} = V_{LJ} + V_C",
        "phase1_title": "Phase 1: Neutrale Atome",
        "phase2_title": "Phase 2: Entgegengesetzte Ladungen (+/-)",
        "phase3_title": "Phase 3: Gleichnamige Ladungen (+/+)",
        "coulomb_attractive": "Coulomb-Anziehung",
        "coulomb_repulsive": "Coulomb-Abstoßung",
        "charged_attraction": "Ladungsanziehung dominiert!",
        "charged_repulsion": "Ladungsabstoßung!",
    },
    "EN": {
        "title": "Non-bonded Interactions",
        "molecule_view": "Atom-Atom Distance",
        "lj_potential": "Lennard-Jones Potential",
        "coulomb_potential": "Coulomb Potential",
        "distance": "Distance r (Å)",
        "energy": "Energy (kcal/mol)",
        "attractive": "Attractive (van der Waals)",
        "repulsive": "Repulsive (Pauli)",
        "equilibrium": "Equilibrium (r_min)",
        "vdw_radius": "van der Waals Radius",
        "far_apart": "Far Apart",
        "close_contact": "Close Contact",
        "optimal_distance": "Optimal Distance",
        "too_close": "Too Close - Repulsion!",
        "lj_formula": r"V_{LJ} = 4\varepsilon[(\sigma/r)^{12}-(\sigma/r)^6]",
        "coulomb_formula": r"V_C = kq_1q_2/r",
        "total_formula": r"V_{tot} = V_{LJ} + V_C",
        "phase1_title": "Phase 1: Neutral Atoms",
        "phase2_title": "Phase 2: Opposite Charges (+/-)",
        "phase3_title": "Phase 3: Like Charges (+/+)",
        "coulomb_attractive": "Coulomb Attraction",
        "coulomb_repulsive": "Coulomb Repulsion",
        "charged_attraction": "Charge attraction dominates!",
        "charged_repulsion": "Charge repulsion!",
    }
}

def get_string(key):
    return STRINGS[LANGUAGE].get(key, key)


class NonbondedInteractions(Scene):
    def construct(self):
        # Lennard-Jones parameters (typical C-C interaction)
        self.epsilon = 0.086  # kcal/mol - well depth
        self.sigma = 3.40     # Å - zero-crossing distance
        self.r_min = self.sigma * (2 ** (1/6))  # Minimum energy distance

        # Coulomb parameters
        self.k_coulomb = 332.1  # kcal·Å/(mol·e²)

        # Animation parameters
        self.r_start = 6.0  # Å
        self.r_end = 2.5    # Å

        # Setup layout
        self.setup_layout()

        # Phase 1: Neutral atoms
        self.run_phase(
            phase_title=get_string("phase1_title"),
            q1=0.0, q2=0.0,
            atom1_label="Ar₁", atom2_label="Ar₂",
            atom1_color=BLUE_D, atom2_color=BLUE_D
        )

        self.wait(2)
        self.clear_phase()

        # Phase 2: Opposite charges (+/-)
        self.run_phase(
            phase_title=get_string("phase2_title"),
            q1=1.0, q2=-1.0,
            atom1_label="Na⁺", atom2_label="Cl⁻",
            atom1_color=RED_D, atom2_color=BLUE_D
        )

        self.wait(2)
        self.clear_phase()

        # Phase 3: Like charges (+/+)
        self.run_phase(
            phase_title=get_string("phase3_title"),
            q1=1.0, q2=1.0,
            atom1_label="Na⁺", atom2_label="Na⁺",
            atom1_color=RED_D, atom2_color=RED_D
        )

        self.wait(2)

    def setup_layout(self):
        """Create layout with molecule on left, two plots on right"""
        # Title
        self.main_title = Text(get_string("title"), color=YELLOW).scale(0.7)
        self.main_title.to_edge(UP, buff=0.3)

        # Dividing line
        self.divider = Line(UP * 3.5 + LEFT * 0.1, DOWN * 3.5 + LEFT * 0.1,
                      stroke_width=2, color=WHITE)

        # Panel labels
        self.mol_label = Text(get_string("molecule_view"), color=BLUE_C).scale(0.5)
        self.mol_label.move_to(LEFT * 3.5 + UP * 3.2)

        self.lj_label = Text(get_string("lj_potential"), color=GREEN_C).scale(0.5)
        self.lj_label.move_to(RIGHT * 3.5 + UP * 3.2)

        # Don't add them yet - they will be added in first phase

    def run_phase(self, phase_title, q1, q2, atom1_label, atom2_label, atom1_color, atom2_color):
        """Run one phase of the animation with specific parameters"""
        # Set charges
        self.q1 = q1
        self.q2 = q2

        # On first phase, show layout elements
        if not hasattr(self, '_layout_shown'):
            self.add(self.main_title, self.divider, self.mol_label, self.lj_label)
            self._layout_shown = True
            self.wait(0.5)

        # Add phase title (positioned at bottom of left panel)
        self.phase_label = Text(phase_title, color=ORANGE).scale(0.45)
        self.phase_label.move_to(LEFT * 3.5 + DOWN * 3.2)
        self.add(self.phase_label)
        self.wait(0.3)

        # Create atoms with charges
        self.create_atoms_charged(atom1_label, atom2_label, atom1_color, atom2_color, q1, q2)

        # Create potential curves
        self.create_potential_plot()

        # Run animation
        self.animate_approach()

    def clear_phase(self):
        """Clear all objects from current phase"""
        # Preserve layout elements
        preserve = []
        if hasattr(self, 'main_title'):
            preserve.append(self.main_title)
        if hasattr(self, 'divider'):
            preserve.append(self.divider)
        if hasattr(self, 'mol_label'):
            preserve.append(self.mol_label)
        if hasattr(self, 'lj_label'):
            preserve.append(self.lj_label)

        # Clear everything else
        all_mobs = self.mobjects.copy()
        for mob in all_mobs:
            if mob not in preserve:
                self.remove(mob)

        # Explicitly clear references
        attrs_to_clear = ['atom_group', 'atom1', 'atom2', 'distance_label', 'distance_line',
                         'vdw_circle1', 'vdw_circle2', 'state_label', 'axes', 'potential_graph',
                         'current_dot', 'phase_label']
        for attr in attrs_to_clear:
            if hasattr(self, attr):
                delattr(self, attr)

    def create_atoms_charged(self, label1, label2, color1, color2, q1, q2):
        """Create two atoms with specified labels, colors, and charges"""
        self.mol_center = LEFT * 3.5 + DOWN * 0.5

        # Create two atoms with charges
        self.atom1 = self.create_atom(label1, color1, radius=0.4, charge=q1)
        self.atom2 = self.create_atom(label2, color2, radius=0.4, charge=q2)

        # Distance label
        self.distance_label = DecimalNumber(
            self.r_start, num_decimal_places=2, color=YELLOW
        ).scale(0.6)

        # Distance line
        self.distance_line = Line(LEFT, RIGHT, stroke_width=2, color=YELLOW)

        # Add interaction regions indicator (must be created before update_atom_positions)
        self.create_interaction_regions()

        # Position atoms at starting distance
        self.update_atom_positions(self.r_start)

        # Add to scene
        self.atom_group = VGroup(self.atom1, self.atom2, self.distance_line)
        self.add(self.atom_group, self.distance_label)
        self.wait(0.3)

    def create_atom(self, label_text, color, radius=0.3, charge=0):
        """Create an atom with label and optional charge symbol"""
        circle = Circle(radius=radius, fill_color=color, fill_opacity=0.8,
                       stroke_color=WHITE, stroke_width=2)
        label = Text(label_text, color=WHITE).scale(0.35)

        # Add charge symbol if charged
        if charge != 0:
            charge_symbol = Text("+" if charge > 0 else "−", color=YELLOW).scale(0.5)
            charge_symbol.move_to(circle.get_corner(UR) + LEFT * 0.15 + DOWN * 0.15)
            atom = VGroup(circle, label, charge_symbol)
        else:
            atom = VGroup(circle, label)

        return atom

    def create_interaction_regions(self):
        """Create visual indicators for interaction regions"""
        # van der Waals radius circles (faint)
        self.vdw_circle1 = Circle(
            radius=self.sigma * 0.35,  # Scaled for visualization
            stroke_color=GREEN, stroke_width=1, stroke_opacity=0.3,
            fill_opacity=0.0
        )
        self.vdw_circle2 = Circle(
            radius=self.sigma * 0.35,
            stroke_color=GREEN, stroke_width=1, stroke_opacity=0.3,
            fill_opacity=0.0
        )

    def update_atom_positions(self, r_distance):
        """Update atom positions based on separation distance"""
        # Scale distance for visualization (make smaller for screen)
        r_visual = r_distance * 0.6

        # Position atoms symmetrically
        pos1 = self.mol_center + LEFT * r_visual / 2
        pos2 = self.mol_center + RIGHT * r_visual / 2

        self.atom1.move_to(pos1)
        self.atom2.move_to(pos2)

        # Update distance line
        self.distance_line.put_start_and_end_on(pos1, pos2)

        # Update distance label
        self.distance_label.set_value(r_distance)
        self.distance_label.move_to(self.mol_center + UP * 1.5)

        # Update vdW circles
        self.vdw_circle1.move_to(pos1)
        self.vdw_circle2.move_to(pos2)

        # Show/hide vdW circles based on distance
        # Show when atoms are close enough (independent of charge)
        distance_threshold = 5.0  # Å - show vdW spheres when atoms are closer than this
        if r_distance < distance_threshold:
            if self.vdw_circle1 not in self.mobjects:
                self.add(self.vdw_circle1, self.vdw_circle2)
        else:
            if self.vdw_circle1 in self.mobjects:
                self.remove(self.vdw_circle1, self.vdw_circle2)

    def create_potential_plot(self):
        """Create potential curve (LJ or LJ+Coulomb depending on charges)"""
        # Determine if we need to show Coulomb contribution
        has_charge = (self.q1 != 0 or self.q2 != 0)

        # Adjust y-range for charged systems
        if has_charge:
            # Wider range for charged systems
            if self.q1 * self.q2 < 0:  # Opposite charges (attractive)
                y_range = [-1.0, 0.6, 0.2]
            else:  # Like charges (repulsive)
                y_range = [-0.2, 2.0, 0.4]
        else:
            y_range = [-0.2, 0.6, 0.2]

        # Create axes
        self.axes = Axes(
            x_range=[0, 7.0, 1.0],   # Distance in Å
            y_range=y_range,  # Energy in kcal/mol
            width=6,
            height=5,
            axis_config={"include_tip": True, "include_numbers": True},
        )
        self.axes.move_to(RIGHT * 3.5 + DOWN * 0.3)

        # Axis labels
        self.x_label = Text(get_string("distance"), color=WHITE).scale(0.35)
        self.x_label.next_to(self.axes.get_x_axis(), DOWN, buff=0.3)

        self.y_label = Text(get_string("energy"), color=WHITE).scale(0.35)
        self.y_label.next_to(self.axes.get_y_axis(), LEFT, buff=0.3)
        self.y_label.rotate(90 * DEGREES)

        # Show axes first
        self.add(self.axes, self.x_label, self.y_label)
        self.wait(0.3)

        # Choose which potential to plot
        if has_charge:
            # Plot only Coulomb potential (isolated interaction)
            potential_func = self.coulomb_potential
            graph_color = PURPLE
        else:
            # Plot only LJ potential (isolated interaction)
            potential_func = self.lennard_jones
            graph_color = BLUE

        # Plot potential
        self.potential_graph = self.axes.get_graph(
            potential_func,
            x_range=[1.0, 7.0],
            color=graph_color,
            stroke_width=3
        )
        self.add(self.potential_graph)
        self.wait(0.5)

        # Mark minimum - only for neutral systems (LJ has a clear minimum)
        # For Coulomb: no minimum marker (attractive goes to -∞, repulsive has no minimum)
        if not has_charge:
            r_min_actual = self.r_min
            energy_min = self.lennard_jones(self.r_min)

            point_min = self.axes.coords_to_point(r_min_actual, energy_min)
            dot_min = Dot(point_min, color=GREEN, radius=0.08)

            # Vertical line at r_min
            r_min_line = DashedLine(
                self.axes.coords_to_point(r_min_actual, self.axes.y_range[0]),
                self.axes.coords_to_point(r_min_actual, self.axes.y_range[1]),
                stroke_width=2, color=GREEN, dash_length=0.1
            )

            # Mark sigma (zero crossing)
            point_sigma = self.axes.coords_to_point(self.sigma, 0)
            dot_sigma = Dot(point_sigma, color=YELLOW, radius=0.06)

            # Show all markers
            markers = [dot_min, r_min_line, dot_sigma]
            for m in markers:
                self.add(m)

        # Region labels (adjust based on charge)
        if not has_charge:
            attractive_label = Text(get_string("attractive"), color=GREEN).scale(0.3)
            attractive_label.move_to(self.axes.coords_to_point(5.0, -0.15))

            repulsive_label = Text(get_string("repulsive"), color=RED).scale(0.3)
            repulsive_label.move_to(self.axes.coords_to_point(2.8, 0.4))

            self.add(attractive_label, repulsive_label)

        # Create moving dot
        self.current_dot = Dot(
            self.axes.coords_to_point(self.r_start, potential_func(self.r_start)),
            color=RED, radius=0.1
        )
        self.add(self.current_dot)

        # Add formula (depends on charge)
        if has_charge:
            formula = Tex(get_string("coulomb_formula"), color=YELLOW).scale(0.4)
            formula.move_to(self.axes.get_top() + UP * 0.4)
        else:
            formula = Tex(get_string("lj_formula"), color=YELLOW).scale(0.4)
            formula.move_to(self.axes.get_top() + UP * 0.4)

        # Add parameter info (compact)
        if has_charge:
            # For Coulomb: show only Coulomb-relevant parameters
            params = VGroup(
                Tex(f"k = {self.k_coulomb:.1f}~\\text{{kcal}}\\cdot\\text{{Å}}/\\text{{mol}}", color=WHITE).scale(0.3),
                Tex(f"q_1 = {self.q1:+.1f}e", color=YELLOW).scale(0.3),
                Tex(f"q_2 = {self.q2:+.1f}e", color=YELLOW).scale(0.3),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        else:
            # For LJ: show LJ parameters
            params = VGroup(
                Tex(f"\\epsilon = {self.epsilon:.3f}~\\text{{kcal/mol}}", color=WHITE).scale(0.3),
                Tex(f"\\sigma = {self.sigma:.2f}~\\text{{Å}}", color=WHITE).scale(0.3),
                Tex(f"r_{{min}} = {self.r_min:.2f}~\\text{{Å}}", color=WHITE).scale(0.3),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        params.move_to(self.axes.get_corner(UR) + LEFT * 1.0 + DOWN * 0.4)

        # Show formula and parameters
        self.add(formula, params)
        self.wait(0.3)

        # Add attractive/repulsive term decomposition (only for neutral)
        if not has_charge:
            self.create_term_decomposition()

    def create_term_decomposition(self):
        """Show r⁻¹² (repulsive) and r⁻⁶ (attractive) terms"""
        # Plot r⁻¹² term (repulsive)
        repulsive_term = self.axes.get_graph(
            lambda r: 4 * self.epsilon * (self.sigma / r) ** 12,
            x_range=[1.0, 7.0],
            color=RED, stroke_width=2, stroke_opacity=0.5
        )

        # Plot -r⁻⁶ term (attractive)
        attractive_term = self.axes.get_graph(
            lambda r: -4 * self.epsilon * (self.sigma / r) ** 6,
            x_range=[1.0, 7.0],
            color=GREEN, stroke_width=2, stroke_opacity=0.5
        )

        # Labels
        rep_label = Tex("r^{-12}", color=RED).scale(0.4)
        rep_label.move_to(self.axes.coords_to_point(2.7, 0.5))

        attr_label = Tex("-r^{-6}", color=GREEN).scale(0.4)
        attr_label.move_to(self.axes.coords_to_point(6.5, -0.1))

        # Show decomposition terms
        self.add(repulsive_term, attractive_term, rep_label, attr_label)
        self.wait(0.3)

    def lennard_jones(self, r):
        """Calculate Lennard-Jones potential"""
        # V = 4ε[(σ/r)¹² - (σ/r)⁶]
        # Avoid division by zero
        if r < 0.1:
            return 10.0
        sigma_over_r = self.sigma / r
        return 4 * self.epsilon * (sigma_over_r**12 - sigma_over_r**6)

    def coulomb_potential(self, r):
        """Calculate Coulomb potential"""
        # V = k*q1*q2/r
        # Avoid division by zero
        if r < 0.1:
            return 10.0 if self.q1 * self.q2 > 0 else -10.0
        return self.k_coulomb * self.q1 * self.q2 / r

    def total_potential(self, r):
        """Calculate total potential (LJ + Coulomb)"""
        return self.lennard_jones(r) + self.coulomb_potential(r)

    def animate_approach(self):
        """Animate atoms approaching from far to close contact"""
        duration = 10.0  # seconds
        fps = 30
        frames = int(duration * fps)

        # Determine which potential function to use
        has_charge = (self.q1 != 0 or self.q2 != 0)
        if has_charge:
            potential_func = self.coulomb_potential
        else:
            potential_func = self.lennard_jones

        # Animation path depends on system type
        if has_charge:
            # For Coulomb: simple linear approach from r_start to r_end
            # No minimum to target
            for frame in range(frames):
                progress = frame / frames
                r_current = self.r_start - progress * (self.r_start - self.r_end)

                # Update atoms
                self.update_atom_positions(r_current)

                # Update distance label
                self.remove(self.distance_label)
                self.distance_label = DecimalNumber(
                    r_current, num_decimal_places=2, color=YELLOW
                ).scale(0.6)
                self.distance_label.move_to(self.mol_center + UP * 1.5)
                self.add(self.distance_label)

                # Update dot on potential curve
                energy = potential_func(r_current)
                point = self.axes.coords_to_point(r_current, energy)
                self.current_dot.move_to(point)

                self.update_charged_state_label(r_current, has_charge, frame)
                self.wait(1/fps)
        else:
            # For LJ: two-phase animation (approach minimum, then push closer)
            r_min_actual = self.r_min

            # First phase: approach from r_start to r_min (attractive)
            phase1_frames = int(frames * 0.4)
            # Second phase: continue to r_end (repulsive)
            phase2_frames = frames - phase1_frames

            for frame in range(frames):
                t = frame / fps

                if frame < phase1_frames:
                    # Phase 1: approach to minimum
                    progress = frame / phase1_frames
                    r_current = self.r_start - progress * (self.r_start - r_min_actual)
                else:
                    # Phase 2: push closer (into repulsive region)
                    progress = (frame - phase1_frames) / phase2_frames
                    r_current = r_min_actual - progress * (r_min_actual - self.r_end)

                # Update atoms
                self.update_atom_positions(r_current)

                # Update distance label
                self.remove(self.distance_label)
                self.distance_label = DecimalNumber(
                    r_current, num_decimal_places=2, color=YELLOW
                ).scale(0.6)
                self.distance_label.move_to(self.mol_center + UP * 1.5)
                self.add(self.distance_label)

                # Update dot on potential curve
                energy = potential_func(r_current)
                point = self.axes.coords_to_point(r_current, energy)
                self.current_dot.move_to(point)

                # Update state label
                if frame % 20 == 0:  # Update frequently
                    if hasattr(self, 'state_label'):
                        self.remove(self.state_label)

                    # For LJ: use r_min as reference
                    if r_current > r_min_actual * 1.2:
                        state = get_string("far_apart")
                        color = BLUE
                    elif r_current > r_min_actual * 0.95 and r_current < r_min_actual * 1.05:
                        state = get_string("optimal_distance")  # Neutral LJ
                        color = GREEN
                    elif r_current > r_min_actual * 0.85:
                        state = get_string("close_contact")
                        color = ORANGE
                    else:
                        state = get_string("too_close")  # Generic repulsion
                        color = RED

                    self.state_label = Text(state, color=color).scale(0.5)
                    self.state_label.move_to(self.mol_center + DOWN * 2.5)
                    self.add(self.state_label)

                self.wait(1/fps)

    def update_charged_state_label(self, r_current, has_charge, frame):
        """Update state label for charged systems"""
        if frame % 20 == 0:  # Update frequently
            if hasattr(self, 'state_label'):
                self.remove(self.state_label)

            # For Coulomb: different labels based on charge type
            if r_current > 5.0:
                state = get_string("far_apart")
                color = BLUE
            elif r_current > 3.5:
                if self.q1 * self.q2 < 0:
                    state = get_string("charged_attraction")  # Opposite charges
                else:
                    state = get_string("close_contact")  # Like charges approaching
                color = ORANGE
            else:
                if self.q1 * self.q2 > 0:
                    state = get_string("charged_repulsion")  # Like charges too close
                else:
                    state = get_string("charged_attraction")  # Opposite charges close
                color = RED if self.q1 * self.q2 > 0 else GREEN

            self.state_label = Text(state, color=color).scale(0.5)
            self.state_label.move_to(self.mol_center + DOWN * 2.5)
            self.add(self.state_label)


if __name__ == "__main__":
    # Run with: manimgl nonbonded_interactions.py NonbondedInteractions
    pass
