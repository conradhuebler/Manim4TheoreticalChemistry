#!/usr/bin/env python3
"""
Particle Interactions Combinatorics
Kombinatorik von Partikel-Wechselwirkungen

Educational animation demonstrating:
- Combinatorial growth of particle interactions: n(n-1)/2
- Naive vs. correct loop implementation
- Water molecule example with nuclei and electrons
- O(N²) scaling problem
- Optimization strategies

Lehranimation zur Demonstration:
- Kombinatorisches Wachstum von Partikel-Wechselwirkungen: n(n-1)/2
- Naive vs. korrekte Schleifen-Implementierung
- Wassermolekül-Beispiel mit Kernen und Elektronen
- O(N²) Skalierungsproblem
- Optimierungsstrategien
"""

from manimlib import *
import numpy as np

# Language setting
LANGUAGE = "EN"  # Set to "EN" for English

STRINGS = {
    "DE": {
        "title": "Kombinatorik von Partikel-Wechselwirkungen",
        "scene1_title": "Szenario 1: Wachstum der Wechselwirkungen",
        "scene2_title": "Szenario 2: Naive vs. Korrekte Schleife",
        "scene3_title": "Szenario 3: Wassermolekül (H₂O)",
        "scene4_title": "Szenario 4: Skalierungsproblem",
        "scene5_title": "Szenario 5: Optimierungsstrategien",

        # Scenario 1
        "n_particles": "Anzahl Teilchen: ",
        "n_interactions": "Wechselwirkungen: ",
        "formula": "Formel: n(n-1)/2",
        "particle": "Teilchen",
        "particles": "Teilchen",
        "interaction": "Wechselwirkung",
        "interactions": "Wechselwirkungen",
        "warning_title": "⚠ ACHTUNG: Naiver Ansatz!",
        "warning_subtitle": "Wir zeigen zuerst den FALSCHEN Weg (führt zu Doppelzählung)",
        "count_from_each": "Zähle von jedem der {n} Teilchen aus:",
        "from_particle": "Von Teilchen {i}:",
        "particle_label": "Teilchen {i}: {count} WW",
        "sum_label": "Summe: {n}×{n_minus_1} = {total} WW",
        "n_times_explanation": "{n} Teilchen × je {n_minus_1} Nachbarn",
        "all_together": "Alle zusammen: {total} WW gezählt",
        "each_twice": "Jede WW wurde 2× gezählt!",
        "remove_duplicates": "Duplikate entfernen →",
        "correct_count": "Korrekt: {n} WW",

        # Scenario 2
        "naive_loop": "Naive Schleife",
        "correct_loop": "Korrekte Schleife",
        "naive_code": "for i in range(N):\\n    for j in range(N):\\n        if i ≠ j:\\n            count += 1",
        "correct_code": "for i in range(N):\\n    for j in range(i+1, N):\\n        count += 1",
        "double_counted": "Doppelt gezählt!",
        "correctly_counted": "Korrekt gezählt",
        "naive_result": "Naive Zählung: n(n-1) = ",
        "correct_result": "Korrekte Zählung: n(n-1)/2 = ",

        # Scenario 3
        "nuclei": "Kerne",
        "electrons": "Elektronen",
        "nucleus_nucleus": "Kern-Kern WW",
        "nucleus_electron": "Kern-Elektron WW",
        "electron_electron": "Elektron-Elektron WW",
        "total_interactions": "Gesamt-WW",
        "oxygen": "Sauerstoff (O)",
        "hydrogen": "Wasserstoff (H)",
        "electron": "Elektron (e⁻)",
        "simplified": "Vereinfacht: 3 Kerne",
        "with_electrons": "Mit 10 Elektronen",
        "alternative_simple": "Einfacher: Teilchentyp ist egal!",
        "total_particles_count": "13 Teilchen gesamt",
        "same_result": "Gleiches Ergebnis!",
        "nucleus_calc_label": "Kern-Kern:",
        "electron_calc_label": "Elektron-Elektron:",
        "mixed_calc_label": "Kern-Elektron:",
        "different_types": "(unterschiedliche Typen!)",
        "summary": "Zusammenfassung:",
        "summary_nucleus_nucleus": "Kern-Kern: 3 WW",
        "summary_electron_electron": "Elektron-Elektron: 45 WW",
        "summary_nucleus_electron": "Kern-Elektron: 30 WW",

        # Scenario 4
        "number_of_particles": "Anzahl Teilchen (N)",
        "number_of_interactions": "Anzahl Wechselwirkungen",
        "scaling": r"\text{Skalierung: } O(N^2)",
        "example_10": "10 Teilchen → 45 WW",
        "example_50": "50 Teilchen → 1225 WW",
        "example_100": "100 Teilchen → 4950 WW",

        # Scenario 5
        "optimization": "Optimierung",
        "strategy_symmetry": "1. Symmetrie nutzen: i < j",
        "strategy_cutoff": "2. Cut-off Radius: r < r_cut",
        "strategy_neighborlist": "3. Nachbarlisten",
        "speedup": "Beschleunigung: ",
        "cutoff_radius": "Cut-off Radius",
        "all_interactions": "Alle WW",
        "cutoff_interactions": "WW mit Cut-off",
    },
    "EN": {
        "title": "Combinatorics of Particle Interactions",
        "scene1_title": "Scenario 1: Growth of Interactions",
        "scene2_title": "Scenario 2: Naive vs. Correct Loop",
        "scene3_title": "Scenario 3: Water Molecule (H₂O)",
        "scene4_title": "Scenario 4: Scaling Problem",
        "scene5_title": "Scenario 5: Optimization Strategies",

        # Scenario 1
        "n_particles": "Number of particles: ",
        "n_interactions": "Interactions: ",
        "formula": "Formula: n(n-1)/2",
        "particle": "particle",
        "particles": "particles",
        "interaction": "interaction",
        "interactions": "interactions",
        "warning_title": "⚠ WARNING: Naive Approach!",
        "warning_subtitle": "We first show the WRONG way (leads to double counting)",
        "count_from_each": "Count from each of the {n} particles:",
        "from_particle": "From particle {i}:",
        "particle_label": "Particle {i}: {count} int.",
        "sum_label": "Sum: {n}×{n_minus_1} = {total} int.",
        "n_times_explanation": "{n} particles × {n_minus_1} neighbors each",
        "all_together": "All together: {total} int. counted",
        "each_twice": "Each interaction counted 2× !",
        "remove_duplicates": "Remove duplicates →",
        "correct_count": "Correct: {n} int.",

        # Scenario 2
        "naive_loop": "Naive Loop",
        "correct_loop": "Correct Loop",
        "naive_code": "for i in range(N):\\n    for j in range(N):\\n        if i ≠ j:\\n            count += 1",
        "correct_code": "for i in range(N):\\n    for j in range(i+1, N):\\n        count += 1",
        "double_counted": "Double counted!",
        "correctly_counted": "Correctly counted",
        "naive_result": "Naive count: n(n-1) = ",
        "correct_result": "Correct count: n(n-1)/2 = ",

        # Scenario 3
        "nuclei": "Nuclei",
        "electrons": "Electrons",
        "nucleus_nucleus": "Nucleus-Nucleus Int.",
        "nucleus_electron": "Nucleus-Electron Int.",
        "electron_electron": "Electron-Electron Int.",
        "total_interactions": "Total Interactions",
        "oxygen": "Oxygen (O)",
        "hydrogen": "Hydrogen (H)",
        "electron": "Electron (e⁻)",
        "simplified": "Simplified: 3 Nuclei",
        "with_electrons": "With 10 Electrons",
        "alternative_simple": "Simpler: Particle type doesn't matter!",
        "total_particles_count": "13 particles total",
        "same_result": "Same result!",
        "nucleus_calc_label": "Nucleus-Nucleus:",
        "electron_calc_label": "Electron-Electron:",
        "mixed_calc_label": "Nucleus-Electron:",
        "different_types": "(different particle types!)",
        "summary": "Summary:",
        "summary_nucleus_nucleus": "Nucleus-Nucleus: 3 Int.",
        "summary_electron_electron": "Electron-Electron: 45 Int.",
        "summary_nucleus_electron": "Nucleus-Electron: 30 Int.",

        # Scenario 4
        "number_of_particles": "Number of Particles (N)",
        "number_of_interactions": "Number of Interactions",
        "scaling": r"\text{Scaling: } O(N^2)",
        "example_10": "10 particles → 45 interactions",
        "example_50": "50 particles → 1225 interactions",
        "example_100": "100 particles → 4950 interactions",

        # Scenario 5
        "optimization": "Optimization",
        "strategy_symmetry": "1. Use symmetry: i < j",
        "strategy_cutoff": "2. Cut-off radius: r < r_cut",
        "strategy_neighborlist": "3. Neighbor lists",
        "speedup": "Speedup: ",
        "cutoff_radius": "Cut-off Radius",
        "all_interactions": "All Interactions",
        "cutoff_interactions": "Interactions with Cut-off",
    }
}

def get_string(key):
    return STRINGS[LANGUAGE].get(key, key)


class ParticleInteractionsCombinatorics(Scene):
    """Main scene combining all scenarios"""

    def construct(self):
        # Title
        title = Text(get_string("title"), color=YELLOW).scale(0.8)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))
        self.wait(1)

        # Run all scenarios
        self.scenario_1_growth()
        # self.scenario_2_loops()  # Deactivated
        self.scenario_3_water()
        self.scenario_4_scaling()
        # self.scenario_5_optimization()  # Deactivated - for other lecture

        # Fade out title at the end
        self.play(FadeOut(title))
        self.wait(2)

    def scenario_1_growth(self):
        """Scenario 1: Count from each particle's perspective to show duplication"""
        # Clear scene except title
        self.clear_scene_except_title()

        # Scene title
        scene_title = Text(get_string("scene1_title"), color=BLUE_C).scale(0.6)
        scene_title.move_to(UP * 3.0)
        self.play(Write(scene_title))
        self.wait(1)

        # WARNING: Show that we're demonstrating the WRONG approach first
        warning_box = Rectangle(
            width=7,
            height=1.2,
            fill_color=RED,
            fill_opacity=0.15,
            stroke_color=RED,
            stroke_width=3
        )
        warning_box.move_to(ORIGIN + UP * 0.3)

        warning_title = Text(get_string("warning_title"), color=RED, weight=BOLD).scale(0.6)
        warning_title.move_to(ORIGIN + UP * 0.6)

        warning_subtitle = Text(
            get_string("warning_subtitle"),
            color=ORANGE
        ).scale(0.4)
        warning_subtitle.move_to(ORIGIN + UP * 0.1)

        self.play(
            ShowCreation(warning_box),
            Write(warning_title),
            Write(warning_subtitle)
        )
        self.wait(2.5)

        self.play(
            FadeOut(warning_box),
            FadeOut(warning_title),
            FadeOut(warning_subtitle)
        )
        self.wait(0.5)

        # Particle display area (center-left)
        particle_center = LEFT * 2.5 + DOWN * 0.5

        # List position (right side)
        list_pos = RIGHT * 3.5 + UP * 1.5

        # Color palette for particles
        particle_colors = [BLUE, RED, GREEN, PURPLE, ORANGE]

        # Animate for 2, 3, and 4 particles
        for n in range(2, 5):
            n_naive = n * (n - 1)  # Naive counting (with duplicates)
            n_correct = n * (n - 1) // 2  # Correct counting

            # Create colored particles
            particles = VGroup()
            if n == 1:
                particle = self.create_atom("1", particle_colors[0], radius=0.2*0.7, label_scale=0.4)
                particle.move_to(particle_center)
                particles.add(particle)
            else:
                for i in range(n):
                    angle = i * TAU / n - PI/2
                    pos = particle_center + 1.5 * 0.7 * np.array([np.cos(angle), np.sin(angle), 0])
                    particle = self.create_atom(str(i+1), particle_colors[i], radius=0.2*0.7, label_scale=0.4)
                    particle.move_to(pos)
                    particles.add(particle)

            self.play(FadeIn(particles))
            self.wait(0.5)

            # Particle count
            particle_label = Text(
                f"{get_string('n_particles')}{n}",
                color=WHITE
            ).scale(0.6)
            particle_label.move_to(list_pos + UP)
            self.play(Write(particle_label))
            self.wait(0.5)

            positions = [p.get_center() for p in particles]

            # Step 1: Count from EACH particle's perspective separately
            intro_text = Text(
                get_string("count_from_each").format(n=n),
                color=BLUE_C
            ).scale(0.45)
            intro_text.move_to(UP * 2.2)
            self.play(Write(intro_text))
            self.wait(1)

            # Create counting list
            count_list = VGroup()

            # For each particle i, show counting from its perspective
            for i in range(n):
                particle_color = particle_colors[i]

                # Highlight current particle
                highlight = Circle(
                    radius=0.35,
                    stroke_color=particle_color,
                    stroke_width=4,
                    fill_opacity=0
                ).move_to(positions[i])

                perspective_text = Text(
                    get_string("from_particle").format(i=i+1),
                    color=particle_color
                ).scale(0.45)
                perspective_text.move_to(UP * 2.2)

                self.play(
                    FadeOut(intro_text) if i == 0 else FadeOut(prev_perspective_text),
                    Write(perspective_text),
                    ShowCreation(highlight)
                )
                self.wait(0.3)

                # Create arrows from i to all others
                arrows_from_i = VGroup()
                for j in range(n):
                    if i != j:
                        arrow = Arrow(
                            positions[i],
                            positions[j],
                            buff=0.25,
                            stroke_width=3,
                            color=particle_color,
                            max_tip_length_to_length_ratio=0.2
                        )
                        arrows_from_i.add(arrow)

                # Show arrows
                self.play(ShowCreation(arrows_from_i), run_time=0.5)

                # Add to counting list
                list_entry = Text(
                    get_string("particle_label").format(i=i+1, count=n-1)
                ).scale(0.4)
                list_entry.set_color(particle_color)  # Set color after creation
                list_entry.move_to(list_pos + DOWN * (0.4 * i))
                count_list.add(list_entry)
                self.play(Write(list_entry))
                self.wait(0.6)

                # Remove highlight and arrows for next particle
                self.play(
                    FadeOut(highlight),
                    FadeOut(arrows_from_i)
                )

                prev_perspective_text = perspective_text

            # Remove last perspective text
            self.play(FadeOut(prev_perspective_text))
            self.wait(0.5)

            # Add horizontal line and sum
            sum_line = Line(
                list_pos + DOWN * (0.4 * n) + LEFT * 0.8,
                list_pos + DOWN * (0.4 * n) + RIGHT * 0.8,
                color=WHITE,
                stroke_width=2
            )
            sum_text = Text(
                get_string("sum_label").format(n=n, n_minus_1=n-1, total=n_naive),
                color=ORANGE
            ).scale(0.45)
            sum_text.move_to(list_pos + DOWN * (0.4 * n + 0.5))

            self.play(ShowCreation(sum_line))
            self.play(Write(sum_text))
            self.wait(1)

            # Explanation for n×(n-1)
            explanation = Text(
                get_string("n_times_explanation").format(n=n, n_minus_1=n-1),
                color=ORANGE
            ).scale(0.38)
            explanation.move_to(list_pos + DOWN * (0.4 * n + 1.0))
            self.play(Write(explanation))
            self.wait(1.5)

            # Step 2: Show ALL arrows together (naive count)
            naive_text = Text(
                get_string("all_together").format(total=n_naive),
                color=ORANGE
            ).scale(0.45)
            naive_text.move_to(UP * 2.2)
            self.play(Write(naive_text))
            self.wait(0.5)

            # Recreate all arrows
            all_arrows = VGroup()
            for i in range(n):
                for j in range(n):
                    if i != j:
                        arrow = Arrow(
                            positions[i],
                            positions[j],
                            buff=0.25,
                            stroke_width=2,
                            color=ORANGE,
                            max_tip_length_to_length_ratio=0.2
                        )
                        all_arrows.add(arrow)

            self.play(ShowCreation(all_arrows), run_time=1)

            naive_count_label = Text(
                f"n(n-1) = {n_naive}",
                color=ORANGE
            ).scale(0.5)
            naive_count_label.move_to(particle_center + DOWN * 2.5)
            self.play(Write(naive_count_label))
            self.wait(1.5)

            # Step 3: Mark duplicates
            duplicate_text = Text(
                get_string("each_twice"),
                color=RED
            ).scale(0.45)
            duplicate_text.move_to(UP * 2.2)
            self.play(FadeOut(naive_text))
            self.play(Write(duplicate_text))
            self.wait(0.5)

            # Separate arrows into duplicates and unique
            duplicates = VGroup()
            unique_arrows = VGroup()

            arrow_idx = 0
            for i in range(n):
                for j in range(n):
                    if i != j:
                        if j < i:  # This is the duplicate direction
                            duplicates.add(all_arrows[arrow_idx])
                        else:  # This is the unique direction (i<j)
                            unique_arrows.add(all_arrows[arrow_idx])
                        arrow_idx += 1

            # Color duplicates red
            self.play(*[arrow.animate.set_color(RED) for arrow in duplicates], run_time=1)
            self.wait(1.5)

            # Step 4: Remove duplicates
            remove_text = Text(
                get_string("remove_duplicates"),
                color=GREEN
            ).scale(0.45)
            remove_text.move_to(UP * 2.2)
            self.play(FadeOut(duplicate_text))
            self.play(Write(remove_text))
            self.wait(0.5)

            self.play(FadeOut(duplicates))
            self.wait(0.5)

            # Convert remaining arrows to undirected lines
            correct_lines = VGroup()
            for i in range(n):
                for j in range(i + 1, n):
                    line = Line(
                        positions[i],
                        positions[j],
                        stroke_width=3,
                        color=GREEN
                    )
                    correct_lines.add(line)

            self.play(
                FadeOut(unique_arrows),
                ShowCreation(correct_lines)
            )

            # Step 5: Show correct count
            correct_count_label = Text(
                get_string("correct_count").format(n=n_correct),
                color=GREEN
            ).scale(0.5)
            correct_count_label.move_to(list_pos + DOWN * (0.4 * n + 1.8))
            self.play(Write(correct_count_label))
            self.wait(0.5)

            # Show formula
            formula_calc = Tex(
                f"n(n-1)/2 = {n} \\cdot {n-1} / 2 = {n_correct}",
                color=GREEN
            ).scale(0.5)
            formula_calc.move_to(list_pos + DOWN * (0.4 * n + 2.4))
            self.play(Write(formula_calc))
            self.wait(2)

            # Clean up for next iteration (except last)
            if n < 4:
                self.play(
                    FadeOut(particles),
                    FadeOut(correct_lines),
                    FadeOut(particle_label),
                    FadeOut(remove_text),
                    FadeOut(naive_count_label),
                    FadeOut(correct_count_label),
                    FadeOut(formula_calc),
                    FadeOut(count_list),
                    FadeOut(sum_line),
                    FadeOut(sum_text),
                    FadeOut(explanation)
                )
                self.wait(0.5)

        self.wait(2)

        # Final cleanup
        self.play(*[FadeOut(mob) for mob in self.mobjects if mob != self.mobjects[0]])
        self.wait(0.5)

    def scenario_2_loops(self):
        """Scenario 2: Naive vs. correct loop implementation"""
        self.clear_scene_except_title()

        # Scene title
        scene_title = Text(get_string("scene2_title"), color=BLUE_C).scale(0.6)
        scene_title.move_to(UP * 3.0)
        self.play(Write(scene_title))
        self.wait(1)

        # Split screen: left = naive, right = correct
        divider = Line(UP * 3, DOWN * 3, stroke_width=2, color=WHITE)
        self.play(ShowCreation(divider))

        # Left side: Naive loop
        naive_title = Text(get_string("naive_loop"), color=RED).scale(0.5)
        naive_title.move_to(LEFT * 3 + UP * 2)

        naive_code = Text(
            get_string("naive_code"),
            color=WHITE
        ).scale(0.35)
        naive_code_bg = Rectangle(
            width=naive_code.get_width() + 0.3,
            height=naive_code.get_height() + 0.3,
            fill_color=BLACK,
            fill_opacity=0.7,
            stroke_color=RED,
            stroke_width=2
        )
        naive_code_group = VGroup(naive_code_bg, naive_code)
        naive_code_group.move_to(LEFT * 3 + UP * 0.5)

        # Right side: Correct loop
        correct_title = Text(get_string("correct_loop"), color=GREEN).scale(0.5)
        correct_title.move_to(RIGHT * 3 + UP * 2)

        correct_code = Text(
            get_string("correct_code"),
            color=WHITE
        ).scale(0.35)
        correct_code_bg = Rectangle(
            width=correct_code.get_width() + 0.3,
            height=correct_code.get_height() + 0.3,
            fill_color=BLACK,
            fill_opacity=0.7,
            stroke_color=GREEN,
            stroke_width=2
        )
        correct_code_group = VGroup(correct_code_bg, correct_code)
        correct_code_group.move_to(RIGHT * 3 + UP * 0.5)

        self.play(
            Write(naive_title),
            Write(correct_title)
        )
        self.play(
            FadeIn(naive_code_group),
            FadeIn(correct_code_group)
        )
        self.wait(1)

        # Visual demonstration with 4 particles
        n = 4

        # Naive loop particles (left)
        naive_particles = self.create_particle_group(n, LEFT * 3 + DOWN * 1.5, scale=0.4)
        # Correct loop particles (right)
        correct_particles = self.create_particle_group(n, RIGHT * 3 + DOWN * 1.5, scale=0.4)

        self.play(FadeIn(naive_particles), FadeIn(correct_particles))
        self.wait(1)

        # Animate naive loop (counts each pair twice)
        naive_count = 0
        naive_lines = VGroup()

        positions_naive = [p[0].get_center() for p in naive_particles]

        for i in range(n):
            for j in range(n):
                if i != j:
                    # Draw line from i to j
                    line = Arrow(
                        positions_naive[i],
                        positions_naive[j],
                        buff=0.2,
                        stroke_width=2,
                        color=RED if (j, i) in [(prev_j, prev_i) for prev_i, prev_j in [(x, y) for x in range(n) for y in range(n) if x != y and (x, y) < (i, j)]] else ORANGE,
                        max_tip_length_to_length_ratio=0.15
                    )
                    naive_lines.add(line)
                    self.play(ShowCreation(line), run_time=0.2)
                    naive_count += 1

        # Animate correct loop (counts each pair once)
        correct_count = 0
        correct_lines = VGroup()

        positions_correct = [p[0].get_center() for p in correct_particles]

        for i in range(n):
            for j in range(i + 1, n):
                # Draw undirected line from i to j
                line = Line(
                    positions_correct[i],
                    positions_correct[j],
                    stroke_width=3,
                    color=GREEN
                )
                correct_lines.add(line)
                self.play(ShowCreation(line), run_time=0.3)
                correct_count += 1

        self.wait(1)

        # Show results
        naive_result = Text(
            f"{get_string('naive_result')}{naive_count}",
            color=RED
        ).scale(0.5)
        naive_result.move_to(LEFT * 3 + DOWN * 3)

        correct_result = Text(
            f"{get_string('correct_result')}{correct_count}",
            color=GREEN
        ).scale(0.5)
        correct_result.move_to(RIGHT * 3 + DOWN * 3)

        self.play(Write(naive_result), Write(correct_result))
        self.wait(2)

        # Clean up
        self.play(
            FadeOut(scene_title),
            FadeOut(divider),
            FadeOut(naive_title),
            FadeOut(correct_title),
            FadeOut(naive_code_group),
            FadeOut(correct_code_group),
            FadeOut(naive_particles),
            FadeOut(correct_particles),
            FadeOut(naive_lines),
            FadeOut(correct_lines),
            FadeOut(naive_result),
            FadeOut(correct_result)
        )

    def scenario_3_water(self):
        """Scenario 3: Water molecule with nuclei and electrons"""
        self.clear_scene_except_title()

        # Scene title
        scene_title = Text(get_string("scene3_title"), color=BLUE_C).scale(0.6)
        scene_title.move_to(UP * 3.0)
        self.play(Write(scene_title))
        self.wait(1)

        # Phase 1: 3 nuclei only
        phase1_label = Text(get_string("simplified"), color=WHITE).scale(0.5)
        phase1_label.move_to(UP * 2.3)
        self.play(Write(phase1_label))

        # Create nuclei
        o_nucleus = self.create_atom("O", RED, radius=0.4, label_scale=0.5)
        h1_nucleus = self.create_atom("H", WHITE, radius=0.25, label_scale=0.4)
        h2_nucleus = self.create_atom("H", WHITE, radius=0.25, label_scale=0.4)

        # Position nuclei in H2O geometry
        center = LEFT * 2.5 + UP * 0.3
        o_nucleus.move_to(center)
        h1_nucleus.move_to(center + UP * 0.8 + LEFT * 0.6)
        h2_nucleus.move_to(center + UP * 0.8 + RIGHT * 0.6)

        nuclei_group = VGroup(o_nucleus, h1_nucleus, h2_nucleus)

        self.play(FadeIn(nuclei_group))
        self.wait(1.5)

        # Show nucleus-nucleus calculation
        nn_calc_text = Text(get_string("nucleus_calc_label"), color=YELLOW).scale(0.45)
        nn_calc_text.move_to(RIGHT * 3 + UP * 2.2)
        self.play(Write(nn_calc_text))

        # Show formula
        nn_formula = Tex(
            r"\frac{3 \times 2}{2} = 3~\text{WW}",
            color=YELLOW
        ).scale(0.5)
        nn_formula.move_to(RIGHT * 3 + UP * 1.6)
        self.play(Write(nn_formula))
        self.wait(1)

        # Draw the 3 lines one by one
        nn_lines = VGroup()
        nn_positions = [o_nucleus.get_center(), h1_nucleus.get_center(), h2_nucleus.get_center()]

        for i in range(3):
            for j in range(i+1, 3):
                line = Line(nn_positions[i], nn_positions[j], color=YELLOW, stroke_width=3)
                nn_lines.add(line)
                self.play(ShowCreation(line), run_time=0.5)

        self.wait(1.5)

        # Phase 2: Add 10 electrons
        phase2_label = Text(get_string("with_electrons"), color=WHITE).scale(0.5)
        phase2_label.move_to(UP * 2.3)
        self.play(FadeOut(phase1_label))
        self.play(Write(phase2_label))
        self.wait(1.5)

        # Create 10 electrons in shell around molecule
        electrons = VGroup()
        n_electrons = 10
        radius = 2.2

        for i in range(n_electrons):
            angle = i * TAU / n_electrons + PI/2
            pos = center + np.array([
                radius * np.cos(angle),
                radius * np.sin(angle) * 0.6,  # Flatten vertically
                0
            ])
            electron = self.create_atom("e⁻", BLUE, radius=0.15, label_scale=0.25)
            electron.move_to(pos)
            electrons.add(electron)

        self.play(FadeIn(electrons))
        self.wait(1.5)

        # Clear previous calculation
        self.play(
            FadeOut(nn_calc_text),
            FadeOut(nn_formula)
        )

        # Calculate interactions
        n_nuclei = 3
        n_electrons = 10

        # Show Electron-Electron calculation
        ee_calc_text = Text(get_string("electron_calc_label"), color=BLUE_C).scale(0.45)
        ee_calc_text.move_to(RIGHT * 3 + UP * 2.2)
        self.play(Write(ee_calc_text))

        ee_formula = Tex(
            r"\frac{10 \times 9}{2} = 45~\text{WW}",
            color=BLUE_C
        ).scale(0.5)
        ee_formula.move_to(RIGHT * 3 + UP * 1.6)
        self.play(Write(ee_formula))
        self.wait(1)

        # Draw a few symbolic electron-electron lines (not all 45!)
        ee_lines = VGroup()
        electron_positions = [e.get_center() for e in electrons]
        # Draw first 8 connections as examples
        for i in range(min(4, len(electrons))):
            for j in range(i+1, min(i+8, len(electrons))):
                line = Line(electron_positions[i], electron_positions[j],
                          color=BLUE_C, stroke_width=1, stroke_opacity=0.4)
                ee_lines.add(line)

        self.play(ShowCreation(ee_lines), run_time=1.5)
        self.wait(1)

        # Show Nucleus-Electron calculation
        self.play(FadeOut(ee_calc_text), FadeOut(ee_formula))

        ne_calc_text = Text(get_string("mixed_calc_label"), color=PURPLE).scale(0.45)
        ne_calc_text.move_to(RIGHT * 3 + UP * 2.2)
        self.play(Write(ne_calc_text))

        # IMPORTANT: No division by 2 for nucleus-electron!
        ne_formula = Tex(
            r"3 \times 10 = 30~\text{WW}",
            color=PURPLE
        ).scale(0.5)
        ne_formula.move_to(RIGHT * 3 + UP * 1.6)
        self.play(Write(ne_formula))

        ne_explanation = Text(
            get_string("different_types"),
            color=PURPLE
        ).scale(0.35)
        ne_explanation.move_to(RIGHT * 3 + UP * 1.1)
        self.play(Write(ne_explanation))
        self.wait(1)

        # Draw a few symbolic nucleus-electron lines
        ne_lines = VGroup()
        for i in range(3):  # Each nucleus
            for j in range(min(3, len(electrons))):  # To a few electrons
                line = Line(nn_positions[i], electron_positions[j],
                          color=PURPLE, stroke_width=1, stroke_opacity=0.4)
                ne_lines.add(line)

        self.play(ShowCreation(ne_lines), run_time=1.5)
        self.wait(1.5)

        # Clear and show total sum
        self.play(
            FadeOut(ne_calc_text),
            FadeOut(ne_formula),
            FadeOut(ne_explanation)
        )

        # Summary
        summary_title = Text(get_string("summary"), color=WHITE).scale(0.5)
        summary_title.move_to(RIGHT * 3 + UP * 2.0)
        self.play(Write(summary_title))

        summary_lines = VGroup(
            Text(get_string("summary_nucleus_nucleus"), color=YELLOW).scale(0.4),
            Text(get_string("summary_electron_electron"), color=BLUE_C).scale(0.4),
            Text(get_string("summary_nucleus_electron"), color=PURPLE).scale(0.4),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        summary_lines.move_to(RIGHT * 3 + UP * 0.8)

        for line in summary_lines:
            self.play(Write(line), run_time=0.5)

        # Total
        total_line = Line(
            RIGHT * 2.2 + UP * 0.1,
            RIGHT * 3.8 + UP * 0.1,
            color=WHITE,
            stroke_width=2
        )
        self.play(ShowCreation(total_line))

        total_sum = Tex(
            r"3 + 45 + 30 = 78~\text{WW}",
            color=GREEN
        ).scale(0.55)
        total_sum.move_to(RIGHT * 3 + DOWN * 0.4)
        self.play(Write(total_sum))
        self.wait(2)

        # Alternative calculation: Total particles approach
        alt_title = Text(
            get_string("alternative_simple"),
            color=YELLOW
        ).scale(0.5)
        alt_title.move_to(RIGHT * 3 + DOWN * 1.3)
        self.play(Write(alt_title))
        self.wait(1)

        # Show total particle count
        total_particles_text = Text(
            get_string("total_particles_count"),
            color=YELLOW
        ).scale(0.45)
        total_particles_text.move_to(RIGHT * 3 + DOWN * 2.0)
        self.play(Write(total_particles_text))
        self.wait(0.5)

        # Show calculation steps
        # Step 1: 13 × 12
        step1 = Tex(
            r"13 \times 12 = 156",
            color=YELLOW
        ).scale(0.5)
        step1.move_to(RIGHT * 3 + DOWN * 2.7)
        self.play(Write(step1))
        self.wait(1)

        # Step 2: 156 / 2
        step2 = Tex(
            r"\frac{156}{2} = 78~\text{WW}",
            color=YELLOW
        ).scale(0.5)
        step2.move_to(RIGHT * 3 + DOWN * 3.4)
        self.play(Write(step2))
        self.wait(1.5)

        # Highlight that it's the same result
        same_result_text = Text(
            get_string("same_result"),
            color=GREEN,
            weight=BOLD
        ).scale(0.5)
        same_result_text.move_to(RIGHT * 3 + DOWN * 4.2)
        self.play(Write(same_result_text))
        self.wait(5.5)

        # Clean up
        self.play(
            FadeOut(scene_title),
            FadeOut(phase2_label),
            FadeOut(nuclei_group),
            FadeOut(electrons),
            FadeOut(nn_lines),
            FadeOut(ee_lines),
            FadeOut(ne_lines),
            FadeOut(summary_title),
            FadeOut(summary_lines),
            FadeOut(total_line),
            FadeOut(total_sum),
            FadeOut(alt_title),
            FadeOut(total_particles_text),
            FadeOut(step1),
            FadeOut(step2),
            FadeOut(same_result_text)
        )

    def scenario_4_scaling(self):
        """Scenario 4: O(N²) scaling problem"""
        self.clear_scene_except_title()

        # Scene title
        scene_title = Text(get_string("scene4_title"), color=BLUE_C).scale(0.6)
        scene_title.move_to(UP * 3.0)
        self.play(Write(scene_title))
        self.wait(1)

        # Create axes for graph
        axes = Axes(
            x_range=[0, 100, 20],
            y_range=[0, 5000, 1000],
            width=10,
            height=5,
            axis_config={
                "include_tip": True,
                "include_numbers": True
            },
        )
        axes.move_to(DOWN * 0.5)

        # Axis labels
        x_label = Text(get_string("number_of_particles"), color=WHITE).scale(0.4)
        x_label.next_to(axes.get_x_axis(), DOWN, buff=0.3)

        y_label = Text(get_string("number_of_interactions"), color=WHITE).scale(0.4)
        y_label.next_to(axes.get_y_axis(), LEFT, buff=0.3)
        y_label.rotate(90 * DEGREES)

        self.play(ShowCreation(axes), Write(x_label), Write(y_label))
        self.wait(1.5)

        # Plot the curve n(n-1)/2
        graph = axes.get_graph(
            lambda n: n * (n - 1) / 2,
            x_range=[1, 100],
            color=BLUE
        )

        self.play(ShowCreation(graph), run_time=3)
        self.wait(2)

        # Mark specific points
        examples = [
            (10, 45, get_string("example_10")),
            (50, 1225, get_string("example_50")),
            (100, 4950, get_string("example_100"))
        ]

        dots = VGroup()
        labels = VGroup()

        for n, interactions, label_text in examples:
            point = axes.coords_to_point(n, interactions)
            dot = Dot(point, color=YELLOW, radius=0.08)
            dots.add(dot)

            label = Text(label_text, color=YELLOW).scale(0.35)
            label.next_to(point, UP + RIGHT, buff=0.1)
            labels.add(label)

        self.play(FadeIn(dots), Write(labels))
        self.wait(2)

        # Add scaling notation
        scaling_text = Tex(
            get_string("scaling"),
            color=RED
        ).scale(0.7)
        scaling_text.move_to(UP * 2)
        self.play(Write(scaling_text))
        self.wait(3.5)

        # Clean up
        self.play(
            FadeOut(scene_title),
            FadeOut(axes),
            FadeOut(x_label),
            FadeOut(y_label),
            FadeOut(graph),
            FadeOut(dots),
            FadeOut(labels),
            FadeOut(scaling_text)
        )

    def scenario_5_optimization(self):
        """Scenario 5: Optimization strategies"""
        self.clear_scene_except_title()

        # Scene title
        scene_title = Text(get_string("scene5_title"), color=BLUE_C).scale(0.6)
        scene_title.move_to(UP * 3.0)
        self.play(Write(scene_title))
        self.wait(1)

        # List optimization strategies
        strategies = VGroup(
            Text(get_string("optimization"), color=YELLOW).scale(0.6),
            Text(get_string("strategy_symmetry"), color=WHITE).scale(0.45),
            Text(get_string("strategy_cutoff"), color=WHITE).scale(0.45),
            Text(get_string("strategy_neighborlist"), color=WHITE).scale(0.45)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        strategies.move_to(LEFT * 3.5 + UP * 0.5)

        self.play(Write(strategies))
        self.wait(2)

        # Visual demonstration: Cut-off radius
        cutoff_demo_center = RIGHT * 2.5

        # Create particles
        n_particles = 12
        particles = VGroup()
        positions = []

        np.random.seed(42)
        for i in range(n_particles):
            angle = i * TAU / n_particles
            r = 1.5 + 0.5 * np.random.random()
            pos = cutoff_demo_center + np.array([r * np.cos(angle), r * np.sin(angle), 0])
            positions.append(pos)

            particle = Circle(radius=0.12, fill_color=BLUE, fill_opacity=0.8, stroke_color=WHITE)
            particle.move_to(pos)
            particles.add(particle)

        self.play(FadeIn(particles))
        self.wait(1.5)

        # Show all interactions first
        all_lines = VGroup()
        for i in range(n_particles):
            for j in range(i + 1, n_particles):
                line = Line(positions[i], positions[j], stroke_width=1, color=GREY, stroke_opacity=0.3)
                all_lines.add(line)

        all_label = Text(get_string("all_interactions"), color=GREY).scale(0.4)
        all_label.move_to(cutoff_demo_center + DOWN * 2.5)

        self.play(ShowCreation(all_lines), Write(all_label))
        self.wait(2)

        # Now show cutoff radius
        cutoff_radius = 1.2
        cutoff_circle = Circle(
            radius=cutoff_radius,
            stroke_color=RED,
            stroke_width=3,
            fill_opacity=0
        )
        cutoff_circle.move_to(cutoff_demo_center)

        cutoff_label = Text(get_string("cutoff_radius"), color=RED).scale(0.4)
        cutoff_label.next_to(cutoff_circle, UP, buff=0.2)

        self.play(ShowCreation(cutoff_circle), Write(cutoff_label))
        self.wait(2)

        # Highlight only interactions within cutoff
        cutoff_lines = VGroup()
        center = cutoff_demo_center

        for i in range(n_particles):
            for j in range(i + 1, n_particles):
                dist = np.linalg.norm(positions[i] - positions[j])
                if dist < 2 * cutoff_radius:  # Both within cutoff region
                    line = Line(positions[i], positions[j], stroke_width=2, color=GREEN)
                    cutoff_lines.add(line)

        cutoff_int_label = Text(get_string("cutoff_interactions"), color=GREEN).scale(0.4)
        cutoff_int_label.move_to(cutoff_demo_center + DOWN * 2.5)

        self.play(
            FadeOut(all_lines),
            FadeOut(all_label),
            ShowCreation(cutoff_lines)
        )
        self.play(Write(cutoff_int_label))
        self.wait(2)

        # Show speedup
        total_interactions = n_particles * (n_particles - 1) // 2
        cutoff_interactions = len(cutoff_lines)
        speedup = total_interactions / max(cutoff_interactions, 1)

        speedup_text = Text(
            f"{get_string('speedup')}{speedup:.1f}x",
            color=YELLOW
        ).scale(0.5)
        speedup_text.move_to(cutoff_demo_center + DOWN * 3.2)

        self.play(Write(speedup_text))
        self.wait(3.5)

        # Clean up
        self.play(
            FadeOut(scene_title),
            FadeOut(strategies),
            FadeOut(particles),
            FadeOut(cutoff_lines),
            FadeOut(cutoff_circle),
            FadeOut(cutoff_label),
            FadeOut(cutoff_int_label),
            FadeOut(speedup_text)
        )

    # Helper methods

    def clear_scene_except_title(self):
        """Clear all objects except the main title at the top"""
        # Keep only the first object (title)
        if len(self.mobjects) > 1:
            to_remove = self.mobjects[1:]
            self.play(*[FadeOut(obj) for obj in to_remove])

    def create_particle_group(self, n, center, scale=0.6, radius_factor=1.5):
        """Create n particles arranged in a circle"""
        particles = VGroup()

        if n == 1:
            # Single particle at center
            particle = self.create_atom("1", BLUE, radius=0.2*scale, label_scale=0.4)
            particle.move_to(center)
            particles.add(particle)
        else:
            # Arrange in circle
            for i in range(n):
                angle = i * TAU / n - PI/2  # Start from top
                pos = center + radius_factor * scale * np.array([np.cos(angle), np.sin(angle), 0])
                particle = self.create_atom(str(i+1), BLUE, radius=0.2*scale, label_scale=0.4)
                particle.move_to(pos)
                particles.add(particle)

        return particles

    def create_interaction_lines(self, particles):
        """Create lines connecting all pairs of particles"""
        if len(particles) < 2:
            return None

        lines = VGroup()
        n = len(particles)

        for i in range(n):
            for j in range(i + 1, n):
                line = Line(
                    particles[i].get_center(),
                    particles[j].get_center(),
                    stroke_width=2,
                    color=YELLOW
                )
                lines.add(line)

        return lines

    def create_atom(self, label_text, color, radius=0.3, label_scale=0.35):
        """Create an atom with label"""
        circle = Circle(
            radius=radius,
            fill_color=color,
            fill_opacity=0.8,
            stroke_color=WHITE,
            stroke_width=2
        )
        label = Text(label_text, color=WHITE).scale(label_scale)
        atom = VGroup(circle, label)
        return atom


if __name__ == "__main__":
    # Run with: manimgl particle_interactions_combinatorics.py ParticleInteractionsCombinatorics
    pass
