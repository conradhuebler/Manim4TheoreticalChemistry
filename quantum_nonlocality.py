#!/usr/bin/env python3
"""
Quantum Non-Locality Visualization
Nicht-Lokalität in der Quantenmechanik

Educational animation showing the transition from classical to quantum two-particle systems
in a box (particle-in-a-box):
1. Classical: Two point particles in 1D boxes → 2D configuration space
2. Hybrid: One classical point + one quantum wavefunction (particle-in-box)
3. Full QM: Both particles as wavefunctions (particle-in-box solutions)

Lehranimation zeigt Übergang von klassisch zu quantenmechanisch:
Beide Teilchen im Kasten (Teilchen im Kasten):
1. Klassisch: Zwei Punktteilchen in 1D-Kästen → 2D Konfigurationsraum
2. Hybrid: Ein klassischer Punkt + eine QM-Wellenfunktion (Teilchen im Kasten)
3. Voll-QM: Beide Teilchen als Wellenfunktionen (Teilchen-im-Kasten-Lösungen)
"""

from manimlib import *
import numpy as np
import os

# Ensure directories exist
os.makedirs("./videos", exist_ok=True)
os.makedirs("./images", exist_ok=True)

# Language setting
LANGUAGE = "EN"  # Set to "EN" for English

# Bilingual strings / Zweisprachige Texte
STRINGS = {
    "DE": {
        "title": "Nicht-Lokalität in der Quantenmechanik",
        "scene1_title": "Szene 1: Klassisches 2-Teilchen-System im Kasten",
        "scene2_title": "Szene 2: Hybrid-System (1 klassisch, 1 QM)",
        "scene3_title": "Szene 3: Beide Teilchen quantenmechanisch",
        "scene3a_title": "Intuition: Zwei-Münzen-Analogie",
        "scene3b_title": "Korrelation vs. Unkorreliert (2D Beispiel)",
        "scene4_title": "Szene 4: Verschränkung - Nicht-separabel",
        "particle1": "Teilchen 1",
        "particle2": "Teilchen 2",
        "particle1_box": "Teilchen 1 (x-Richtung, 0→L)",
        "particle2_box": "Teilchen 2\n (y-Richtung, 0→L)",
        "distance": "Abstand",
        "one_line": "Eine Linie verbindet beide Teilchen",
        "many_lines": "Viele Linien zu allen möglichen Positionen",
        "network": "Netzwerk: Jede Position interagiert mit jeder",
        "classical_eq": "Klassisch: V = k·q₁·q₂/r",
        "hybrid_eq": "Hybrid: V = ∫ k·q₁·q₂/|x-y| |ψ₂(y)| dy",
        "fullqm_eq": "Voll-QM: V = ∫∫ k·q₁·q₂/|x-y| |ψ₁(x)||ψ₂(y)| dx dy",
        "wavefunction": "Wellenfunktion",
        "box_wf": "ψ(x) = √(2/L)·sin(πx/L)",
        "dimensionality_1": "Klassisch: 2 Punktkoordinaten (x, y)",
        "dimensionality_2": "Hybrid: 1 Punkt + 1D-Wellenfunktion ψ(x)",
        "dimensionality_3": "Voll-QM: 2D-Wellenfunktion ψ(x,y)",
        "product_wf": "Produkt-Wellenfunktion",
        "separable": "ψ(x,y) = ψ₁(x) · ψ₂(y) - separabel",
        "not_separable": "ψ(x,y) ≠ ψ₁(x) · ψ₂(y) - verschränkt",
        "heatmap_label": "Wahrscheinlichkeit |ψ(x,y)|²",
        "independent": "Teilchen unabhängig",
        "entangled_info": "Korrelation: Teilchen nicht unabhängig!",
        "transition": "Jetzt: Mit Korrelation...",
        "uncorrelated": "Unkorreliert: y = const (unabhängig von x)",
        "correlated": "Korreliert: y ≈ x (y hängt von x ab)",
        "marginals": "Randverteilungen",
        "marginal_px": "P(x)",
        "marginal_py": "P(y)",
        "rank1": "Separabel: Heatmap = P(x) × P(y) (Rang 1)",
        "rank_high": "Verschränkt: Gleiche Ränder, andere Heatmap! (Rang > 1)",
        "coin1": "Münze 1",
        "coin2": "Münze 2",
        "heads": "Kopf",
        "tails": "Zahl",
        "coin_uncorr": "Unkorreliert: Alle 4 Kombinationen gleich (25%)",
        "coin_corr": "Korreliert: Nur (K,K) und (Z,Z) möglich (50%)",
        "coin_marginals": "Randverteilungen: Beide 50% Kopf, 50% Zahl",
        "coin_insight": "GLEICHE Ränder → VERSCHIEDENE 2D-Verteilungen!",
        "coin_to_quantum": "Gleiches Prinzip bei Quantenverschränkung →",
    },
    "EN": {
        "title": "Non-Locality in Quantum Mechanics",
        "scene1_title": "Scene 1: Classical 2-Particle System in Box",
        "scene2_title": "Scene 2: Hybrid System (1 classical, 1 QM)",
        "scene3_title": "Scene 3: Both Particles Quantum Mechanical",
        "scene3a_title": "Intuition: Two-Coin Analogy",
        "scene3b_title": "Correlation vs. Uncorrelated (2D Example)",
        "scene4_title": "Scene 4: Entanglement - Non-separable",
        "particle1": "Particle 1",
        "particle2": "Particle 2",
        "particle1_box": "Particle 1 (x-direction, 0→L)",
        "particle2_box": "Particle 2\n(y-direction, 0→L)",
        "distance": "Distance",
        "one_line": "One line connects both particles",
        "many_lines": "Many lines to all possible positions",
        "network": "Network: Every position interacts with every other",
        "classical_eq": "Classical: V = k·q₁·q₂/r",
        "hybrid_eq": "Hybrid: V = ∫ k·q₁·q₂/|x-y| |ψ₂(y)| dy",
        "fullqm_eq": "Full QM: V = ∫∫ k·q₁·q₂/|x-y| |ψ₁(x)||ψ₂(y)| dx dy",
        "wavefunction": "Wavefunction",
        "box_wf": "ψ(x) = √(2/L)·sin(πx/L)",
        "dimensionality_1": "Classical: 2 point coordinates (x, y)",
        "dimensionality_2": "Hybrid: 1 point + 1D wavefunction ψ(x)",
        "dimensionality_3": "Full QM: 2D wavefunction ψ(x,y)",
        "product_wf": "Product wavefunction",
        "separable": "ψ(x,y) = ψ₁(x) · ψ₂(y) - separable",
        "not_separable": "ψ(x,y) ≠ ψ₁(x) · ψ₂(y) - entangled",
        "heatmap_label": "Probability |ψ(x,y)|²",
        "independent": "Particles independent",
        "entangled_info": "Correlation: Particles are NOT\n moving independently!",
        "transition": "Now: With correlation...",
        "uncorrelated": "Uncorrelated: y = const (independent of x)",
        "correlated": "Correlated: y ≈ x (y depends on x)",
        "marginals": "Marginal distributions",
        "marginal_px": "P(x)",
        "marginal_py": "P(y)",
        "rank1": "Separable: Heatmap = P(x) × P(y) (Rank 1)",
        "rank_high": "Entangled: Same margins, different heatmap! (Rank > 1)",
        "coin1": "Coin 1",
        "coin2": "Coin 2",
        "heads": "Heads",
        "tails": "Tails",
        "coin_uncorr": "Uncorrelated: All 4 combinations equal (25%)",
        "coin_corr": "Correlated: Only (H,H) and (T,T) possible (50%)",
        "coin_marginals": "Marginals: Both 50% Heads, 50% Tails",
        "coin_insight": "SAME margins → DIFFERENT 2D distributions!",
        "coin_to_quantum": "Same principle in quantum entanglement →",
    }
}

def get_string(key):
    """Get string in current language"""
    return STRINGS[LANGUAGE].get(key, key)


# Color scheme
PARTICLE1_COLOR = BLUE
PARTICLE2_COLOR = RED
LINE_COLOR = YELLOW
QM_COLOR = "#00D9FF"  # Cyan for quantum
ENTANGLED_COLOR = PURPLE


class QuantumNonLocality(Scene):
    """Main scene showing quantum non-locality with particle-in-a-box.

    GUI-compatible PARAMETERS structure for quantum non-locality animation.
    """

    # ✅ Central parameter dictionary for GUI tool compatibility
    PARAMETERS = {
        # ========================================================================
        # PHYSICAL PARAMETERS
        # ========================================================================
        "box_length": {
            "value": np.pi,
            "type": float,
            "unit": "-",
            "description": "Box length L for particle-in-a-box (0 to L)",
            "min": 1.0,
            "max": 10.0
        }
    }

    def construct(self):
        # Extract parameters
        self.L = self.PARAMETERS["box_length"]["value"]

        # Main title
        self.show_title()

        # Scene 1: Classical two-particle system
        self.scene1_classical()

        # Scene 2: Hybrid system (1 classical, 1 QM)
        self.scene2_hybrid()

        # Scene 3: Full quantum (both wavefunctions)
        self.scene3_full_quantum()

        # Scene 3a: Coin analogy for intuition
      #  self.scene3a_coin_analogy()

        # Scene 3b: Simple 2D correlation example
        self.scene3b_correlation_intro()

        # Scene 4: 2D wavefunction as heatmap
        self.scene4_2d_wavefunction()

        self.wait(2)

    def show_title(self):
        """Show main title"""
        title = Text(get_string("title"), color=YELLOW).scale(0.9)
        title.to_edge(UP, buff=0.3)
        self.add(title)
        self.wait(1)
        self.main_title = title

    def scene1_classical(self):
        """Scene 1: Classical two-particle system in boxes (0 to L)"""

        # Update title
        scene_title = Text(get_string("scene1_title"), color=BLUE_C).scale(0.65)
        scene_title.to_edge(UP, buff=0.3)
        self.play(Transform(self.main_title, scene_title))

        # Create coordinate system: 0 to L on both axes
        axes = Axes(
            x_range=[0, self.L, self.L/4],
            y_range=[0, self.L, self.L/4],
            width=6,
            height=6,
            axis_config={"include_tip": True, "color": WHITE}
        ).shift(LEFT * 1.5 + DOWN * 0.5)

        # Axis labels
        x_label = Text("x", color=WHITE).scale(0.5).next_to(axes.get_x_axis(), RIGHT)
        y_label = Text("y", color=WHITE).scale(0.5).next_to(axes.get_y_axis(), UP)

        # Box boundaries
        L_label_x = Text("L", color=WHITE).scale(0.4).next_to(axes.coords_to_point(self.L, 0), DOWN)
        L_label_y = Text("L", color=WHITE).scale(0.4).next_to(axes.coords_to_point(0, self.L), LEFT)

        self.play(ShowCreation(axes), FadeIn(x_label), FadeIn(y_label), FadeIn(L_label_x), FadeIn(L_label_y))

        # Create two classical particles in boxes
        # Particle 1 on x-axis (oscillates in box 0 to L)
        particle1_start = axes.coords_to_point(self.L * 0.6, 0)
        particle1 = Dot(particle1_start, color=PARTICLE1_COLOR, radius=0.15)
        label1 = Text(get_string("particle1_box"), color=PARTICLE1_COLOR).scale(0.35)
        label1.next_to(particle1, DOWN, buff=0.25)

        # Particle 2 on y-axis (oscillates in box 0 to L)
        particle2_start = axes.coords_to_point(0, self.L * 0.7)
        particle2 = Dot(particle2_start, color=PARTICLE2_COLOR, radius=0.15)
        label2 = Text(get_string("particle2_box"), color=PARTICLE2_COLOR).scale(0.35)
        label2.next_to(particle2, LEFT, buff=0.25)

        self.play(
            FadeIn(particle1), FadeIn(label1),
            FadeIn(particle2), FadeIn(label2)
        )

        # Connection line showing distance
        connection_line = Line(particle1.get_center(), particle2.get_center(), color=LINE_COLOR, stroke_width=3)
        self.play(ShowCreation(connection_line))

        # Distance label
        distance_text = Text(get_string("distance") + " r", color=LINE_COLOR).scale(0.4)
        distance_text.move_to(connection_line.get_center() + UP * 0.3 + RIGHT * 0.3)
        self.add(distance_text)

        # Equation - moved to top right
        equation = Tex(r"V = \frac{k \cdot q_1 \cdot q_2}{r}", color=YELLOW).scale(0.7)
        equation.move_to(RIGHT * 3.5 + UP * 2.5)
        self.play(FadeIn(equation))

        # Description
        description = Text(get_string("one_line"), color=WHITE).scale(0.45)
        description.move_to(RIGHT * 3.5 + UP * 1.8)
        self.play(FadeIn(description))

        # Show dimensionality
        dim_text = Text(get_string("dimensionality_1"), color=YELLOW).scale(0.45)
        dim_text.move_to(RIGHT * 3.5 + UP * 1.2)
        self.play(FadeIn(dim_text))

        # Animate oscillation in boxes
        def update_positions(mob, alpha):
            # Particle 1 oscillates on x-axis within box [0, L]
            # Use 0.5*(1 + 0.6*sin) to keep in range [0.2L, 0.8L]
            x1 = self.L * 0.5 * (1 + 0.6 * np.sin(2 * PI * alpha))
            p1_pos = axes.coords_to_point(x1, 0)
            particle1.move_to(p1_pos)
            label1.next_to(particle1, DOWN, buff=0.25)

            # Particle 2 oscillates on y-axis within box [0, L]
            y2 = self.L * 0.5 * (1 + 0.6 * np.sin(2 * PI * alpha + PI/3))
            p2_pos = axes.coords_to_point(0, y2)
            particle2.move_to(p2_pos)
            label2.next_to(particle2, LEFT, buff=0.25)

            # Update connection line
            connection_line.put_start_and_end_on(p1_pos, p2_pos)
            distance_text.move_to(connection_line.get_center() + UP * 0.3 + RIGHT * 0.3)

        # Run oscillation animation
        self.play(
            UpdateFromAlphaFunc(VGroup(), update_positions),
            run_time=4,
            rate_func=linear
        )

        self.wait(2)

        # Store for next scene
        self.axes = axes
        self.x_label = x_label
        self.y_label = y_label
        self.L_label_x = L_label_x
        self.L_label_y = L_label_y
        self.particle1 = particle1
        self.particle2 = particle2
        self.label1 = label1
        self.label2 = label2
        self.connection_line = connection_line
        self.distance_text = distance_text
        self.equation = equation
        self.description = description
        self.dim_text = dim_text

    def scene2_hybrid(self):
        """Scene 2: Hybrid system - particle 1 (x-axis) becomes QM, particle 2 (y-axis) stays classical"""

        # Update title
        scene_title = Text(get_string("scene2_title"), color=GREEN_C).scale(0.65)
        scene_title.to_edge(UP, buff=0.3)
        self.play(Transform(self.main_title, scene_title))

        # Remove old description, equation, and dim_text
        self.play(FadeOut(self.description), FadeOut(self.equation), FadeOut(self.dim_text))

        # Particle 2 stays classical on y-axis, move to fixed position in box
        particle2_pos = self.axes.coords_to_point(0, self.L * 0.6)
        self.play(
            self.particle2.animate.move_to(particle2_pos),
            self.label2.animate.next_to(self.particle2, LEFT, buff=0.25)
        )

        # Transform particle 1 into particle-in-box wavefunction on x-axis
        # ψ(x) = √(2/L) * sin(πx/L) for ground state (n=1)
        wavefunction_dots = VGroup()
        wavefunction_lines = VGroup()

        # Sample points along x-axis in box [0, L]
        x_samples = np.linspace(0.1, self.L - 0.1, 20)

        for x in x_samples:
            # Particle-in-box probability: |ψ(x)|² = (2/L) * sin²(πx/L)
            prob = (2 / self.L) * (np.sin(np.pi * x / self.L)) ** 2

            if prob > 0.05:  # Only show significant probabilities
                pos = self.axes.coords_to_point(x, 0)

                # Create dot with size proportional to probability
                dot = Dot(pos, color=QM_COLOR, radius=0.04 + 0.12 * prob)
                dot.set_opacity(0.3 + 0.7 * prob)
                wavefunction_dots.add(dot)

                # Create line from this wavefunction position to particle 2
                line = Line(
                    pos,
                    self.particle2.get_center(),
                    color=LINE_COLOR,
                    stroke_width=0.5 + 3 * prob
                )
                line.set_opacity(0.15 + 0.65 * prob)
                wavefunction_lines.add(line)

        # Create continuous line for |ψ(x)|² probability distribution
        # Scale it visually above x-axis
        def prob_density(x):
            return (2 / self.L) * (np.sin(np.pi * x / self.L)) ** 2

        # Create points for continuous curve
        wf_curve_points = []
        x_continuous = np.linspace(0, self.L, 100)
        scale_factor = 0.5  # Scale to make visible above x-axis

        for x in x_continuous:
            prob = prob_density(x)
            y_offset = prob * scale_factor
            point = self.axes.coords_to_point(x, y_offset)
            wf_curve_points.append(point)

        wavefunction_curve = VMobject()
        wavefunction_curve.set_points_as_corners(wf_curve_points)
        wavefunction_curve.set_stroke(color=QM_COLOR, width=3)

        # Animate transformation: particle 1 becomes wavefunction
        self.play(
            FadeOut(self.particle1),
            FadeOut(self.connection_line),
            FadeOut(self.distance_text),
            FadeIn(wavefunction_dots),
            ShowCreation(wavefunction_curve),
            run_time=2
        )

        # Update label with wavefunction
        wf_label = Tex(r"|\psi_1(x)|^2", color=QM_COLOR).scale(0.5)
        wf_label.next_to(self.axes.coords_to_point(self.L * 0.5, 0.3), UP, buff=0.1)
        self.play(FadeIn(wf_label))

        # Store curve
        self.wavefunction_curve = wavefunction_curve

        # Show many lines connecting wavefunction to classical particle
        self.play(ShowCreation(wavefunction_lines), run_time=2)

        # New equation with integral
        equation = Tex(
            r"V = \int_0^L \frac{k \cdot q_1 \cdot q_2}{|x - y|} |\psi_1(x)|^2 \, dx",
            color=YELLOW
        ).scale(0.55)
        equation.move_to(RIGHT * 3.5 + UP * 2.5)
        self.play(FadeIn(equation))

        # Description
        description = Text(get_string("many_lines"), color=WHITE).scale(0.45)
        description.move_to(RIGHT * 3.5 + UP * 1.8)
        self.play(FadeIn(description))

        # Dimensionality info
        dim_text = Text(get_string("dimensionality_2"), color=YELLOW).scale(0.45)
        dim_text.move_to(RIGHT * 3.5 + UP * 1.2)
        self.play(FadeIn(dim_text))

        self.wait(3)

        # Animate: move particle 2 to show all lines change
        new_pos = self.axes.coords_to_point(0, self.L * 0.3)

        def update_lines(mob):
            for i, line in enumerate(wavefunction_lines):
                line.put_start_and_end_on(
                    line.get_start(),
                    self.particle2.get_center()
                )

        wavefunction_lines.add_updater(update_lines)
        self.label2.add_updater(lambda m: m.next_to(self.particle2, LEFT, buff=0.25))

        self.play(
            self.particle2.animate.move_to(new_pos),
            run_time=3
        )

        wavefunction_lines.clear_updaters()
        self.label2.clear_updaters()

        self.wait(2)

        # Store for next scene
        self.wavefunction_dots = wavefunction_dots
        self.wavefunction_lines = wavefunction_lines
        self.wavefunction_curve = wavefunction_curve
        self.wf_label = wf_label
        self.equation = equation
        self.description = description
        self.dim_text = dim_text

    def scene3_full_quantum(self):
        """Scene 3: Both particles as quantum wavefunctions (particle-in-box)"""

        # Update title
        scene_title = Text(get_string("scene3_title"), color=ORANGE).scale(0.65)
        scene_title.to_edge(UP, buff=0.3)
        self.play(Transform(self.main_title, scene_title))

        # Remove old description, equation, and dim_text
        self.play(FadeOut(self.description), FadeOut(self.equation), FadeOut(self.dim_text))

        # Transform particle 2 into particle-in-box wavefunction on y-axis
        # ψ(y) = √(2/L) * sin(πy/L) for ground state (n=1)
        wavefunction2_dots = VGroup()
        y_samples = np.linspace(0.1, self.L - 0.1, 20)

        for y in y_samples:
            # Particle-in-box probability: |ψ(y)|² = (2/L) * sin²(πy/L)
            prob = (2 / self.L) * (np.sin(np.pi * y / self.L)) ** 2

            if prob > 0.05:
                pos = self.axes.coords_to_point(0, y)
                dot = Dot(pos, color=PARTICLE2_COLOR, radius=0.04 + 0.12 * prob)
                dot.set_opacity(0.3 + 0.7 * prob)
                wavefunction2_dots.add(dot)

        # Create continuous line for |ψ(y)|² on y-axis
        def prob_density_y(y):
            return (2 / self.L) * (np.sin(np.pi * y / self.L)) ** 2

        wf_curve2_points = []
        y_continuous = np.linspace(0, self.L, 100)
        scale_factor = 0.5

        for y in y_continuous:
            prob = prob_density_y(y)
            x_offset = prob * scale_factor
            point = self.axes.coords_to_point(x_offset, y)
            wf_curve2_points.append(point)

        wavefunction_curve2 = VMobject()
        wavefunction_curve2.set_points_as_corners(wf_curve2_points)
        wavefunction_curve2.set_stroke(color=PARTICLE2_COLOR, width=3)

        # Animate transformation: particle 2 becomes wavefunction
        self.play(
            FadeOut(self.particle2),
            FadeOut(self.wavefunction_lines),
            FadeIn(wavefunction2_dots),
            ShowCreation(wavefunction_curve2),
            run_time=2
        )

        # Update label for particle 2
        wf_label2 = Tex(r"|\psi_2(y)|^2", color=PARTICLE2_COLOR).scale(0.5)
        wf_label2.next_to(self.axes.coords_to_point(0.3, self.L * 0.5), RIGHT, buff=0.1)
        self.play(Transform(self.label2, wf_label2))

        # Create network of lines: many-to-many connections
        # For visualization, sample representative connections from both wavefunctions
        network_lines = VGroup()

        # Sample fewer points for better visibility
        y_samples_network = np.linspace(0.2, self.L - 0.2, 10)
        x_samples_network = np.linspace(0.2, self.L - 0.2, 10)

        for x in x_samples_network:
            prob1 = (2 / self.L) * (np.sin(np.pi * x / self.L)) ** 2

            if prob1 > 0.1:
                for y in y_samples_network:
                    prob2 = (2 / self.L) * (np.sin(np.pi * y / self.L)) ** 2

                    if prob2 > 0.1:
                        prob_product = prob1 * prob2

                        if prob_product > 0.05:
                            pos1 = self.axes.coords_to_point(x, 0)
                            pos2 = self.axes.coords_to_point(0, y)

                            line = Line(
                                pos1, pos2,
                                color=LINE_COLOR,
                                stroke_width=0.3 + 2.5 * prob_product
                            )
                            line.set_opacity(0.08 + 0.5 * prob_product)
                            network_lines.add(line)

        # Show network
        self.play(ShowCreation(network_lines), run_time=3)

        # New equation with double integral - moved to top right
        equation = Tex(
            r"V = \int_0^L \int_0^L \frac{k \cdot q_1 \cdot q_2}{|x - y|} |\psi_1(x)|^2 |\psi_2(y)|^2 \, dx \, dy",
            color=YELLOW
        ).scale(0.45)
        equation.move_to(RIGHT * 3.5 + UP * 2.5)
        self.play(FadeIn(equation))

        # Description
        description = Text(get_string("network"), color=WHITE).scale(0.45)
        description.move_to(RIGHT * 3.5 + UP * 1.8)
        self.play(FadeIn(description))

        # Show dimensionality info
        dim_info = Text(get_string("dimensionality_3"), color=YELLOW).scale(0.45)
        dim_info.move_to(RIGHT * 3.5 + UP * 1.2)
        self.play(FadeIn(dim_info))

        self.wait(5)

        # Store for cleanup (though scene 4 is disabled)
        self.wavefunction2_dots = wavefunction2_dots
        self.wavefunction_curve2 = wavefunction_curve2
        self.network_lines = network_lines
        self.equation = equation
        self.description = description
        self.dim_info = dim_info

    def scene3a_coin_analogy(self):
        """Scene 3a: Two-coin analogy to illustrate marginals vs joint distribution"""

        # Update title
        scene_title = Text(get_string("scene3a_title"), color=GOLD).scale(0.65)
        scene_title.to_edge(UP, buff=0.3)
        self.play(Transform(self.main_title, scene_title))

        # Fade out previous elements
        self.play(
            FadeOut(self.wavefunction_dots),
            FadeOut(self.wavefunction_curve),
            FadeOut(self.wf_label),
            FadeOut(self.wavefunction2_dots),
            FadeOut(self.wavefunction_curve2),
            FadeOut(self.label1),
            FadeOut(self.label2),
            FadeOut(self.network_lines),
            FadeOut(self.description),
            FadeOut(self.equation),
            FadeOut(self.dim_info)
        )

        # Fade out axes too - we'll use a simpler visualization
        self.play(
            FadeOut(self.axes),
            FadeOut(self.x_label),
            FadeOut(self.y_label),
            FadeOut(self.L_label_x),
            FadeOut(self.L_label_y)
        )

        self.wait(1)

        # ===== Create 2x2 grid for coin outcomes =====
        # Grid represents: (Coin1, Coin2)
        # Layout:
        #   (T,H) | (H,H)
        #   ------|------
        #   (T,T) | (H,T)

        square_size = 1.5
        grid_center = LEFT * 2.5 + DOWN * 0.5

        # Create 4 squares
        squares = VGroup()
        labels = VGroup()

        # Define positions and labels
        positions = [
            (0, 1, "T,K"),  # Top-left: (Tails, Heads)
            (1, 1, "K,K"),  # Top-right: (Heads, Heads)
            (0, 0, "Z,Z"),  # Bottom-left: (Tails, Tails)
            (1, 0, "K,Z"),  # Bottom-right: (Heads, Tails)
        ]

        for i, j, label_text in positions:
            sq = Square(side_length=square_size, color=WHITE, stroke_width=2)
            sq.move_to(grid_center + RIGHT * i * square_size + UP * j * square_size)
            squares.add(sq)

            lbl = Text(label_text, color=WHITE).scale(0.5)
            lbl.move_to(sq.get_center())
            labels.add(lbl)

        self.play(ShowCreation(squares), FadeIn(labels))

        # Axis labels
        coin1_label = Text(get_string("coin1") + " →", color=YELLOW).scale(0.5)
        coin1_label.next_to(squares, DOWN, buff=0.3)

        coin2_label = Text(get_string("coin2") + " ↑", color=YELLOW).scale(0.5)
        coin2_label.next_to(squares, LEFT, buff=0.3)

        self.play(FadeIn(coin1_label), FadeIn(coin2_label))

        self.wait(2)

        # ===== Phase 1: Uncorrelated (all 4 equal) =====
        uncorr_fills = VGroup()
        for sq in squares:
            fill = sq.copy()
            fill.set_fill(BLUE, opacity=0.5)
            fill.set_stroke(width=0)
            uncorr_fills.add(fill)

        description_uncorr = Text(get_string("coin_uncorr"), color=WHITE).scale(0.45)
        description_uncorr.move_to(RIGHT * 3.5 + UP * 2)

        self.play(
            FadeIn(uncorr_fills),
            FadeIn(description_uncorr)
        )

        self.wait(2)

        # Show marginals for uncorrelated
        marginal_text = Text(get_string("coin_marginals"), color=YELLOW).scale(0.4)
        marginal_text.move_to(RIGHT * 3.5 + UP * 1.2)
        self.play(FadeIn(marginal_text))

        # Marginal bars
        # Coin 1: 50% H, 50% T (bottom: sum of bottom row)
        bar1_H = Rectangle(width=0.5, height=0.3, fill_color=YELLOW, fill_opacity=0.7, stroke_width=1)
        bar1_H.next_to(squares[1], DOWN, buff=0.7).shift(LEFT * 0.3)
        bar1_T = Rectangle(width=0.5, height=0.3, fill_color=YELLOW, fill_opacity=0.7, stroke_width=1)
        bar1_T.next_to(squares[0], DOWN, buff=0.7).shift(LEFT * 0.3)

        # Coin 2: 50% H, 50% T (left: sum of left column)
        bar2_H = Rectangle(width=0.3, height=0.5, fill_color=YELLOW, fill_opacity=0.7, stroke_width=1)
        bar2_H.next_to(squares[0], LEFT, buff=0.7).shift(DOWN * 0.3)
        bar2_T = Rectangle(width=0.3, height=0.5, fill_color=YELLOW, fill_opacity=0.7, stroke_width=1)
        bar2_T.next_to(squares[2], LEFT, buff=0.7).shift(DOWN * 0.3)

        marginal_bars_uncorr = VGroup(bar1_H, bar1_T, bar2_H, bar2_T)

        self.play(FadeIn(marginal_bars_uncorr))
        self.wait(3)

        # ===== Phase 2: Correlated (only diagonal) =====
        # Create new fills - only diagonal bright
        corr_fills = VGroup()
        for i, sq in enumerate(squares):
            fill = sq.copy()
            # Only (H,H) and (T,T) are bright (indices 1 and 2)
            if i == 1 or i == 2:  # (K,K) or (Z,Z)
                fill.set_fill(RED, opacity=0.8)
            else:
                fill.set_fill(BLUE, opacity=0.1)
            fill.set_stroke(width=0)
            corr_fills.add(fill)

        description_corr = Text(get_string("coin_corr"), color=WHITE).scale(0.45)
        description_corr.move_to(RIGHT * 3.5 + UP * 2)

        # Marginals are THE SAME!
        marginal_bars_corr = marginal_bars_uncorr.copy()

        self.play(
            Transform(uncorr_fills, corr_fills),
            Transform(description_uncorr, description_corr),
            run_time=3,
            rate_func=smooth
        )

        self.wait(2)

        # THE KEY INSIGHT
        insight_text = Text(get_string("coin_insight"), color=GOLD).scale(0.5)
        insight_text.move_to(RIGHT * 3.5 + DOWN * 0.5)
        self.play(FadeIn(insight_text))

        self.wait(4)

        # Transition to quantum
        quantum_text = Text(get_string("coin_to_quantum"), color=GREEN).scale(0.5)
        quantum_text.move_to(RIGHT * 3.5 + DOWN * 1.5)
        self.play(FadeIn(quantum_text))

        self.wait(3)

        # Clean up
        self.play(
            FadeOut(squares),
            FadeOut(labels),
            FadeOut(uncorr_fills),
            FadeOut(description_uncorr),
            FadeOut(marginal_text),
            FadeOut(marginal_bars_uncorr),
            FadeOut(coin1_label),
            FadeOut(coin2_label),
            FadeOut(insight_text),
            FadeOut(quantum_text)
        )

        # Restore axes for next scene
        self.play(
            FadeIn(self.axes),
            FadeIn(self.x_label),
            FadeIn(self.y_label),
            FadeIn(self.L_label_x),
            FadeIn(self.L_label_y)
        )

    def scene3b_correlation_intro(self):
        """Scene 3b: Simple 2D example showing uncorrelated vs correlated"""

        # Clean up
        self.play(
            FadeOut(self.wavefunction_dots),
            FadeOut(self.wavefunction_curve),
            FadeOut(self.wf_label),
            FadeOut(self.wavefunction2_dots),
            FadeOut(self.wavefunction_curve2),
            FadeOut(self.label1),
            FadeOut(self.label2),
            FadeOut(self.network_lines),
            FadeOut(self.description),
            FadeOut(self.equation),
            FadeOut(self.dim_info)
        )

        # Restore axes for next scene
        self.play(
            FadeIn(self.axes),
            FadeIn(self.x_label),
            FadeIn(self.y_label),
            FadeIn(self.L_label_x),
            FadeIn(self.L_label_y)
        )

        # Update title
        scene_title = Text(get_string("scene3b_title"), color=TEAL).scale(0.65)
        scene_title.to_edge(UP, buff=0.3)
        self.play(Transform(self.main_title, scene_title))

        # No need to fade out - elements were already removed in scene3a
        # Axes are already restored
        self.wait(1)

        # ===== Show uncorrelated points =====
        # y = const for all x values
        n_points = 15
        y_const = self.L * 0.5
        uncorrelated_points = VGroup()

        for i in range(n_points):
            x = self.L * (0.1 + 0.8 * i / (n_points - 1))
            # Add small random variation for visual effect
            y = y_const + self.L * 0.05 * np.random.randn()
            pos = self.axes.coords_to_point(x, y)
            point = Dot(pos, color=BLUE, radius=0.08)
            uncorrelated_points.add(point)

        # Label for uncorrelated
        uncorr_label = Text(get_string("uncorrelated"), color=BLUE).scale(0.5)
        uncorr_label.move_to(RIGHT * 3.5 + UP * 2.2)

        # Show uncorrelated points
        self.play(
            FadeIn(uncorrelated_points, lag_ratio=0.05),
            FadeIn(uncorr_label),
            run_time=2
        )

        self.wait(2)

        # ===== Show conditional probability: fix x, see y distribution =====
        # Choose a fixed x value
        x_fixed = self.L * 0.6

        # Vertical line at fixed x
        #vertical_line = Line(
        #    self.axes.coords_to_point(x_fixed, 0),
        #    self.axes.coords_to_point(x_fixed, self.L),
        #    color=YELLOW,
        #    stroke_width=3
        #)

        # For uncorrelated: multiple y values at this x
        uncorr_vertical_points = VGroup()
        for j in range(8):
            y_val = self.L * (0.15 + 0.7 * j / 7)
            pos = self.axes.coords_to_point(x_fixed, y_val)
            point = Dot(pos, color=YELLOW, radius=0.1)
            uncorr_vertical_points.add(point)

        #self.play(
        #    ShowCreation(vertical_line),
        #    FadeIn(uncorr_vertical_points, lag_ratio=0.1),
        #    run_time=2
        #)
        #self.wait(2)

        # Fade out vertical visualization
        #self.play(
        #    FadeOut(vertical_line),
        #    FadeOut(uncorr_vertical_points)
        #)

        # ===== Transition to correlated points =====
        # Create correlated points along y ≈ x
        correlated_points = VGroup()

        for i in range(n_points):
            x = self.L * (0.1 + 0.8 * i / (n_points - 1))
            # y follows x with small noise
            y = x + self.L * 0.08 * np.random.randn()
            pos = self.axes.coords_to_point(x, y)
            point = Dot(pos, color=RED, radius=0.08)
            correlated_points.add(point)

        
        # Label for correlated
        corr_label = Text(get_string("correlated"), color=RED).scale(0.5)
        corr_label.move_to(RIGHT * 3.5 + UP * 2.2)

        # Animate transition
        self.play(
            Transform(uncorrelated_points, correlated_points),
            Transform(uncorr_label, corr_label),
            run_time=3,
            rate_func=smooth
        )

        self.wait(2)

        # ===== Show conditional probability for correlated: fix x, see narrow y =====
        # Vertical line at fixed x
        #vertical_line2 = Line(
        #    self.axes.coords_to_point(x_fixed, 0),
        #    self.axes.coords_to_point(x_fixed, self.L),
        #    color=YELLOW,
        #    stroke_width=3
        #)

        # For correlated: only one point near y ≈ x
        corr_vertical_points = VGroup()
        y_val = x_fixed  # y = x for perfect correlation
        pos = self.axes.coords_to_point(x_fixed, y_val)
        point = Dot(pos, color=YELLOW, radius=0.12)
        corr_vertical_points.add(point)

        self.play(
        #    ShowCreation(vertical_line2),
            FadeIn(corr_vertical_points),
            run_time=2
        )
        self.wait(3)

        # Clean up for next scene
        self.play(
            FadeOut(uncorrelated_points),
            FadeOut(uncorr_label),
        #    FadeOut(vertical_line2),
            FadeOut(corr_vertical_points)
        )

    def scene4_2d_wavefunction(self):
        """Scene 4: Morphing transition from separable to entangled wavefunction"""

        # Update title
        scene_title = Text(get_string("scene4_title"), color=PURPLE).scale(0.65)
        scene_title.to_edge(UP, buff=0.3)
        self.play(Transform(self.main_title, scene_title))

        # No need to fade out - already done in scene3b
        self.wait(0.5)

        # ===== Create heatmap with morphing capability =====

        # Higher resolution for better contrast
        resolution = 60
        x_range_grid = np.linspace(0, self.L, resolution)
        y_range_grid = np.linspace(0, self.L, resolution)

        # Stronger correlation for ellipse shape
        correlation_strength = 10.0

        # Calculate square size directly from axes dimensions
        # This ensures perfectly square heatmap cells
        square_width = self.axes.get_width() / resolution
        square_height = self.axes.get_height() / resolution

        # Store probability data and create squares
        heatmap_squares = []

        for i, x in enumerate(x_range_grid[:-1]):
            for j, y in enumerate(y_range_grid[:-1]):
                # Separable probability
                prob_x = (2 / self.L) * (np.sin(np.pi * x / self.L)) ** 2
                prob_y = (2 / self.L) * (np.sin(np.pi * y / self.L)) ** 2
                prob_sep = prob_x * prob_y

                # Entangled probability (with correlation)
                envelope_x = np.sin(np.pi * x / self.L) ** 2
                envelope_y = np.sin(np.pi * y / self.L) ** 2
                envelope = envelope_x * envelope_y
                correlation = np.exp(-correlation_strength * ((x - y) / self.L) ** 2)
                prob_ent = envelope * correlation / 0.15  # Normalize

                # Only create square if either probability is significant
                if prob_sep > 0.005 or prob_ent > 0.01:
                    dx = x_range_grid[1] - x_range_grid[0]
                    dy = y_range_grid[1] - y_range_grid[0]

                    square = Rectangle(
                        width=square_width,
                        height=square_height,
                        fill_color=BLUE,
                        fill_opacity=0.2 + 0.8 * prob_sep / 0.4,
                        stroke_width=0
                    )
                    square.move_to(self.axes.coords_to_point(x + dx/2, y + dy/2))

                    # Store probabilities for morphing
                    square.prob_sep = prob_sep
                    square.prob_ent = prob_ent

                    heatmap_squares.append(square)

        heatmap = VGroup(*heatmap_squares)

        # Show initial separable heatmap
        self.play(FadeIn(heatmap), run_time=2)

        # Labels for separable
        equation_sep = Tex(
            r"\psi(x, y) = \psi_1(x) \cdot \psi_2(y)",
            color=BLUE
        ).scale(0.6)
        equation_sep.move_to(RIGHT * 3.5 + UP * 2.5)
        self.play(FadeIn(equation_sep))

        description_sep = Text(get_string("separable"), color=WHITE).scale(0.45)
        description_sep.move_to(RIGHT * 3.5 + UP * 1.8)
        self.play(FadeIn(description_sep))

        info_sep = Text(get_string("independent"), color=BLUE).scale(0.45)
        info_sep.move_to(RIGHT * 3.5 + UP * 1.2)
        self.play(FadeIn(info_sep))

        self.wait(2)

        # ===== Show conditional probability for separable: fix x, y is uniform =====
        x_fixed = self.L * 0.6
        vertical_line_sep = Line(
            self.axes.coords_to_point(x_fixed, 0),
            self.axes.coords_to_point(x_fixed, self.L),
            color=WHITE,
            stroke_width=4
        )
        self.play(ShowCreation(vertical_line_sep))
        self.wait(2)
        self.play(FadeOut(vertical_line_sep))

        self.wait(1)

        # ===== Show marginal distributions for separable =====
        # For separable: P(x) = |ψ₁(x)|², P(y) = |ψ₂(y)|²
        # These are different! P(x) = sin²(πx/L), P(y) = sin²(πy/L)

        n_bars = 30
        marginal_x_bars = VGroup()
        marginal_y_bars = VGroup()

        # P(x) - shown above the heatmap
        bar_width_x = self.axes.get_width() / n_bars
        for i in range(n_bars):
            x_center = self.L * (i + 0.5) / n_bars
            prob_x = (2 / self.L) * (np.sin(np.pi * x_center / self.L)) ** 2

            # Scale for visibility
            bar_height = prob_x * 0.8

            bar = Rectangle(
                width=bar_width_x * 0.9,
                height=bar_height,
                fill_color=BLUE,
                fill_opacity=0.7,
                stroke_width=0.5,
                stroke_color=WHITE
            )
            bar_pos = self.axes.coords_to_point(x_center, 0)
            bar.next_to(bar_pos, UP, buff=0)
            bar.shift(UP * 0.3)  # Move above axes
            marginal_x_bars.add(bar)

        # P(y) - shown to the right of the heatmap
        bar_width_y = self.axes.get_height() / n_bars
        for i in range(n_bars):
            y_center = self.L * (i + 0.5) / n_bars
            prob_y = (2 / self.L) * (np.sin(np.pi * y_center / self.L)) ** 2

            # Scale for visibility
            bar_length = prob_y * 0.8

            bar = Rectangle(
                width=bar_length,
                height=bar_width_y * 0.9,
                fill_color=BLUE,
                fill_opacity=0.7,
                stroke_width=0.5,
                stroke_color=WHITE
            )
            bar_pos = self.axes.coords_to_point(0, y_center)
            bar.next_to(bar_pos, RIGHT, buff=0)
            bar.shift(RIGHT * 0.3)  # Move right of axes
            marginal_y_bars.add(bar)

        # Labels
        px_label = Tex(get_string("marginal_px"), color=BLUE).scale(0.5)
        px_label.next_to(marginal_x_bars, UP, buff=0.1)

        py_label = Tex(get_string("marginal_py"), color=BLUE).scale(0.5)
        py_label.next_to(marginal_y_bars, RIGHT, buff=0.1)

        # Show marginals
        self.play(
            FadeIn(marginal_x_bars, lag_ratio=0.02),
            FadeIn(marginal_y_bars, lag_ratio=0.02),
            FadeIn(px_label),
            FadeIn(py_label),
            run_time=2
        )

        # Explanation
        rank1_text = Text(get_string("rank1"), color=YELLOW).scale(0.4)
        rank1_text.move_to(RIGHT * 3.5 + DOWN * 0.5)
        self.play(FadeIn(rank1_text))

        self.wait(3)

        # Fade out marginals before morphing
        self.play(
            FadeOut(marginal_x_bars),
            FadeOut(marginal_y_bars),
            FadeOut(px_label),
            FadeOut(py_label),
            FadeOut(rank1_text)
        )

        # ===== Morphing transition =====

        # Show transition text
        transition_text = Text(get_string("transition"), color=YELLOW).scale(0.6)
        transition_text.move_to(ORIGIN)
        self.play(FadeIn(transition_text), run_time=0.5)
        self.wait(0.8)
        self.play(FadeOut(transition_text), run_time=0.5)

        # Prepare new labels (will fade in during morph)
        equation_ent = Tex(
            r"\psi(x, y) \neq \psi_1(x) \cdot \psi_2(y)",
            color=RED
        ).scale(0.6)
        equation_ent.move_to(RIGHT * 3.5 + UP * 2.5)

        description_ent = Text(get_string("not_separable"), color=WHITE).scale(0.45)
        description_ent.move_to(RIGHT * 3.5 + UP * 1.8)

        info_ent = Text(get_string("entangled_info"), color=RED).scale(0.45)
        info_ent.move_to(RIGHT * 3.5 + UP * 1.2)

        # Morphing function: interpolate probabilities and colors
        def morph_heatmap(mob, alpha):
            for square in heatmap_squares:
                # Interpolate probability
                prob = (1 - alpha) * square.prob_sep + alpha * square.prob_ent

                # Interpolate color: BLUE → PURPLE
                from manimlib.utils.color import interpolate_color
                color = interpolate_color(BLUE, PURPLE, alpha)

                # Update square
                opacity = 0.2 + 0.8 * min(prob / 0.4, 1.0)
                square.set_fill(color, opacity=opacity)

        # Animate morphing with label transitions
        self.play(
            UpdateFromAlphaFunc(heatmap, morph_heatmap),
            Transform(equation_sep, equation_ent),
            Transform(description_sep, description_ent),
            Transform(info_sep, info_ent),
            run_time=4,
            rate_func=smooth
        )

        self.wait(2)

        # ===== Show conditional probability for entangled: fix x, y is narrow =====
        vertical_line_ent = Line(
            self.axes.coords_to_point(x_fixed, 0),
            self.axes.coords_to_point(x_fixed, self.L),
            color=WHITE,
            stroke_width=4
        )
        #self.play(ShowCreation(vertical_line_ent))
        #self.wait(3)
        #self.play(FadeOut(vertical_line_ent))

        self.wait(1)

        # ===== Show marginal distributions for entangled =====
        # CRUCIAL: For entangled, both marginals are IDENTICAL sin²!
        # P(x) = ∫ |ψ(x,y)|² dy = sin²(πx/L) (after integration)
        # P(y) = ∫ |ψ(x,y)|² dx = sin²(πy/L) (after integration)
        # But the heatmap is DIFFERENT from separable!

        marginal_x_bars_ent = VGroup()
        marginal_y_bars_ent = VGroup()

        # P(x) - shown above the heatmap (same as before!)
        for i in range(n_bars):
            x_center = self.L * (i + 0.5) / n_bars
            prob_x = (2 / self.L) * (np.sin(np.pi * x_center / self.L)) ** 2

            bar_height = prob_x * 0.8

            bar = Rectangle(
                width=bar_width_x * 0.9,
                height=bar_height,
                fill_color=PURPLE,
                fill_opacity=0.7,
                stroke_width=0.5,
                stroke_color=WHITE
            )
            bar_pos = self.axes.coords_to_point(x_center, 0)
            bar.next_to(bar_pos, UP, buff=0)
            bar.shift(UP * 0.3)
            marginal_x_bars_ent.add(bar)

        # P(y) - shown to the right of the heatmap (same as before!)
        for i in range(n_bars):
            y_center = self.L * (i + 0.5) / n_bars
            prob_y = (2 / self.L) * (np.sin(np.pi * y_center / self.L)) ** 2

            bar_length = prob_y * 0.8

            bar = Rectangle(
                width=bar_length,
                height=bar_width_y * 0.9,
                fill_color=PURPLE,
                fill_opacity=0.7,
                stroke_width=0.5,
                stroke_color=WHITE
            )
            bar_pos = self.axes.coords_to_point(0, y_center)
            bar.next_to(bar_pos, RIGHT, buff=0)
            bar.shift(RIGHT * 0.3)
            marginal_y_bars_ent.add(bar)

        # Labels
        px_label_ent = Tex(get_string("marginal_px"), color=PURPLE).scale(0.5)
        px_label_ent.next_to(marginal_x_bars_ent, UP, buff=0.1)

        py_label_ent = Tex(get_string("marginal_py"), color=PURPLE).scale(0.5)
        py_label_ent.next_to(marginal_y_bars_ent, RIGHT, buff=0.1)

        # Show marginals
        self.play(
            FadeIn(marginal_x_bars_ent, lag_ratio=0.02),
            FadeIn(marginal_y_bars_ent, lag_ratio=0.02),
            FadeIn(px_label_ent),
            FadeIn(py_label_ent),
            run_time=2
        )

        # THE KEY INSIGHT!
        rank_high_text = Text(get_string("rank_high"), color=YELLOW).scale(0.4)
        rank_high_text.move_to(RIGHT * 3.5 + DOWN * 0.5)
        self.play(FadeIn(rank_high_text))

        self.wait(4)

        # Clean up
        self.play(
            FadeOut(marginal_x_bars_ent),
            FadeOut(marginal_y_bars_ent),
            FadeOut(px_label_ent),
            FadeOut(py_label_ent),
            FadeOut(rank_high_text)
        )

        self.wait(2)


if __name__ == "__main__":
    # Run with: manimgl quantum_nonlocality.py QuantumNonLocality
    # or: python -m manimlib quantum_nonlocality.py QuantumNonLocality
    import subprocess
    import sys
    subprocess.run([
        sys.executable, "-m", "manimlib",
        __file__, "QuantumNonLocality"
    ])
