#!/usr/bin/env python3
"""
Metropolis-Algorithmus Animation
Didaktische Visualisierung der Akzeptanzwahrscheinlichkeit und Metropolis-Schritte
bei verschiedenen Temperaturen mit zweisprachiger Unterstützung.
"""

from manimlib import *
import numpy as np
import random

# Konstanten
R = 8.314  # J/(mol·K)
T_values = [198, 298, 398]  # Temperaturen in K
colors_temp = [GREEN, BLUE, RED]

# Spracheinstellung
LANGUAGE = "EN"  # "DE" oder "EN"

STRINGS = {
    "DE": {
        "title": "Metropolis-Algorithmus (T = {} K)",
        "temp_title": "Temperatureffekt auf Akzeptanzwahrscheinlichkeit",
        "x_axis": "ΔE [kJ/mol]",
        "y_axis": "P(akzeptiert)",
        "step": "Schritt {}/{}",
        "delta_e": "ΔE = {} kJ/mol",
        "probability": "P = ",
        "random": "r = ",
        "accepted": "AKZEPTIERT ✓",
        "rejected": "ABGELEHNT ✗",
        "always_accept": "ΔE < 0 → energetisch günstig\n→ immer akzeptiert (P = 1)",
        "formula_positive": "ΔE > 0 → P = exp(-ΔE/kT)",
        "comparison_accept": "r < P → Schritt wird akzeptiert",
        "comparison_reject": "r ≥ P → Schritt wird abgelehnt",
        "acceptance_zone": "Akzeptanzzone",
        "rejection_zone": "Ablehnungszone",
        "higher_temp": "Höhere Temperatur\n→ mehr Akzeptanz unfavoribler Konfigurationen",
        "sweep_intro": "Bei ΔE > 0: Akzeptanzwahrscheinlichkeit hängt von ΔE ab",
        "sweep_explanation": "Größeres ΔE\n→ kleinere Akzeptanzzone (grün) → geringere Wahrscheinlichkeit",
        "observe_ratio": "Beobachte: Verhältnis zwischen grün und rot ändert sich!",
    },
    "EN": {
        "title": "Metropolis Algorithm (T = {} K)",
        "temp_title": "Temperature Effect on Acceptance Probability",
        "x_axis": "ΔE [kJ/mol]",
        "y_axis": "P(accepted)",
        "step": "Step {}/{}",
        "delta_e": "ΔE = {} kJ/mol",
        "probability": "P = ",
        "random": "r = ",
        "accepted": "ACCEPTED ✓",
        "rejected": "REJECTED ✗",
        "always_accept": "ΔE < 0 → energetically favorable\n→ always accepted (P = 1)",
        "formula_positive": "ΔE > 0 → P = exp(-ΔE/kT)",
        "comparison_accept": "r < P → step accepted",
        "comparison_reject": "r ≥ P → step rejected",
        "acceptance_zone": "Acceptance zone",
        "rejection_zone": "Rejection zone",
        "higher_temp": "Higher temperature\n→ more acceptance of unfavorable configurations",
        "sweep_intro": "For ΔE > 0: Acceptance probability depends on ΔE",
        "sweep_explanation": "Larger ΔE\n→ smaller acceptance zone (green) → lower probability",
        "observe_ratio": "Observe: Ratio between green and red changes!",
    }
}

def get_string(key):
    return STRINGS[LANGUAGE].get(key, key)


class MetropolisBasic(Scene):
    """Szene 1: Metropolis-Algorithmus Grundprinzip bei T=298K"""

    # ✅ Central parameter dictionary for GUI tool compatibility
    PARAMETERS = {
        # Physical parameters
        "T": {
            "value": 298,
            "type": int,
            "unit": "K",
            "description": "Temperature for Metropolis acceptance probability",
            "min": 100,
            "max": 500
        },
        "R": {
            "value": 8.314,
            "type": float,
            "unit": "J/(mol·K)",
            "description": "Gas constant",
            "min": 8.0,
            "max": 9.0
        }
    }

    def construct(self):
        # Extract parameters from central dictionary
        self.T = self.PARAMETERS["T"]["value"]
        self.R = self.PARAMETERS["R"]["value"]
        self.ax = None
        self.curve = None

        # Setup
        self.setup_axes_and_curve()
        self.wait(2)

        # Schritt 1: ΔE < 0 (energetisch günstig, immer akzeptiert)
        self.metropolis_step(-2, 1, 6)
        self.wait(1)

        # Kontinuierliches Sweep: Zeige Verhältnis grün/rot bei verschiedenen ΔE > 0
        self.continuous_sweep_demonstration()

        # Weitere diskrete Schritte mit Zufallszahlen (ΔE > 0 und ΔE < 0)
        delta_E_values = [1, 3, -1, 8, 2]
        for i, delta_E in enumerate(delta_E_values):
            self.metropolis_step(delta_E, i + 2, 6)

        self.wait(3)

    def setup_axes_and_curve(self):
        """Setup: Achsen und Akzeptanzwahrscheinlichkeitskurve"""
        # Koordinatensystem
        self.ax = Axes(
            x_range=[-5, 20, 5],
            y_range=[0, 1.1, 0.2],
            width=10,
            height=6
        )

        # Achsen-Zahlen manuell hinzufügen
        get_x_axis = self.ax.get_x_axis()
        get_x_axis.add_numbers(font_size=20, num_decimal_places=1)

        get_y_axis = self.ax.get_y_axis()
        get_y_axis.add_numbers(font_size=20, num_decimal_places=1)

        # Achsenlabels
        x_label = Text(get_string("x_axis"), color=WHITE).scale(0.4)
        x_label.next_to(self.ax.get_x_axis(), DOWN, buff=0.3)

        y_label = Text(get_string("y_axis"), color=WHITE).scale(0.4)
        y_label.next_to(self.ax.get_y_axis(), LEFT + UP , buff=0.1)
        #y_label.rotate(90 * DEGREES)

        # Kurve der Akzeptanzwahrscheinlichkeit für ΔE > 0
        def acceptance_prob_positive(x):
            """P(akzeptiert) = exp(-ΔE/RT) für ΔE > 0"""
            return np.exp(-x * 1000 / (self.R * self.T))

        self.curve = self.ax.get_graph(
            acceptance_prob_positive,
            x_range=[-5, 20],
            color=BLUE
        )
        self.curve.set_stroke(width=3)

        # Horizontale Linie bei P=1 für ΔE < 0
        point_left = self.ax.coords_to_point(-5, 1)
        point_zero = self.ax.coords_to_point(0, 1)

        self.flat_line = DashedLine(point_left, point_zero, color=BLUE, stroke_width=3)

        # Titel
        title = Text(get_string("title").format(self.T), color=YELLOW)
        title.scale(0.7)
        title.to_edge(UP)

        # Alles hinzufügen
        self.add(self.ax, x_label, y_label, self.curve, self.flat_line, title)

    def continuous_sweep_demonstration(self):
        """Kontinuierliches Abfahren der Kurve von ΔE=0 bis ΔE=10 mit dynamischen Zonen"""

        # Einführungstext
        intro_text = Text(get_string("sweep_intro"), color=YELLOW)
        intro_text.scale(0.5)
        intro_text.to_corner(UP + RIGHT).shift(LEFT * 0.3 + DOWN * 0.5)

        observe_text = Text(get_string("observe_ratio"), color=WHITE)
        observe_text.scale(0.4)
        observe_text.to_corner(DOWN + RIGHT).shift(LEFT * 0.3 + UP * 1.0)

        self.play(FadeIn(intro_text), FadeIn(observe_text))
        self.wait(1.5)

        # ValueTracker für ΔE (von 0.1 bis 10)
        delta_e_tracker = ValueTracker(0.1)

        # Rechteckbreite für Zonen
        rect_width = 0.5

        # Dynamische vertikale Linie
        delta_e_line = always_redraw(lambda: Line(
            self.ax.coords_to_point(delta_e_tracker.get_value(), 0),
            self.ax.coords_to_point(delta_e_tracker.get_value(), 1.1),
            color=YELLOW,
            stroke_width=3
        ))

        # Dynamisches ΔE-Label
        delta_e_label = always_redraw(lambda: Text(
            get_string("delta_e").format(round(delta_e_tracker.get_value(), 1)),
            color=YELLOW
        ).scale(0.4).next_to(
            self.ax.coords_to_point(delta_e_tracker.get_value(), 0.5),
            RIGHT,
            buff=0.2
        ))

        # Akzeptanzwahrscheinlichkeit als Funktion
        def get_acceptance_prob(delta_e):
            return np.exp(-delta_e * 1000 / (self.R * self.T))

        # Dynamische Akzeptanzzone (grün)
        acceptance_zone = always_redraw(lambda: self._create_acceptance_zone(
            delta_e_tracker.get_value(),
            get_acceptance_prob(delta_e_tracker.get_value()),
            rect_width
        ))

        # Dynamische Ablehnungszone (rot)
        rejection_zone = always_redraw(lambda: self._create_rejection_zone(
            delta_e_tracker.get_value(),
            get_acceptance_prob(delta_e_tracker.get_value()),
            rect_width
        ))

        # Dynamischer Punkt auf der Kurve
        curve_point = always_redraw(lambda: Dot(
            self.ax.coords_to_point(
                delta_e_tracker.get_value(),
                get_acceptance_prob(delta_e_tracker.get_value())
            ),
            radius=0.08,
            color=YELLOW
        ))

        # Dynamisches P-Label
        p_label = always_redraw(lambda: Text(
            f"P = {get_acceptance_prob(delta_e_tracker.get_value()):.3f}",
            color=BLUE
        ).scale(0.45).move_to(
            self.ax.coords_to_point(12, 0.85)
        ))

        # Alle dynamischen Objekte hinzufügen
        self.add(delta_e_line, delta_e_label, acceptance_zone, rejection_zone, curve_point, p_label)

        # Kontinuierliche Animation von ΔE = 0.1 bis 10
        self.play(
            delta_e_tracker.animate.set_value(10),
            run_time=8,
            rate_func=linear
        )

        self.wait(1)

        # Erklärungstext am Ende
        explanation_text = Text(get_string("sweep_explanation"), color=GREEN)
        explanation_text.scale(0.4)
        explanation_text.next_to(observe_text, UP, buff=0.3)

        self.play(FadeIn(explanation_text))
        self.wait(2)

        # Aufräumen
        self.play(
            FadeOut(intro_text),
            FadeOut(observe_text),
            FadeOut(explanation_text),
            FadeOut(delta_e_line),
            FadeOut(delta_e_label),
            FadeOut(acceptance_zone),
            FadeOut(rejection_zone),
            FadeOut(curve_point),
            FadeOut(p_label)
        )
        self.wait(0.5)

    def _create_acceptance_zone(self, delta_e, p_accept, rect_width):
        """Hilfsmethode: Erstellt grüne Akzeptanzzone"""
        bottom_left = self.ax.coords_to_point(delta_e, 0)
        top_right = self.ax.coords_to_point(delta_e + rect_width, p_accept)

        zone = Rectangle(
            width=top_right[0] - bottom_left[0],
            height=max(0.001, top_right[1] - bottom_left[1]),  # Verhindere negative Höhe
            fill_color=GREEN,
            fill_opacity=0.4,
            stroke_width=0
        )
        zone.move_to([
            (bottom_left[0] + top_right[0]) / 2,
            (bottom_left[1] + top_right[1]) / 2,
            0
        ])
        return zone

    def _create_rejection_zone(self, delta_e, p_accept, rect_width):
        """Hilfsmethode: Erstellt rote Ablehnungszone"""
        bottom_left = self.ax.coords_to_point(delta_e, p_accept)
        top_right = self.ax.coords_to_point(delta_e + rect_width, 1)

        zone = Rectangle(
            width=top_right[0] - bottom_left[0],
            height=max(0.001, top_right[1] - bottom_left[1]),  # Verhindere negative Höhe
            fill_color=RED,
            fill_opacity=0.4,
            stroke_width=0
        )
        zone.move_to([
            (bottom_left[0] + top_right[0]) / 2,
            (bottom_left[1] + top_right[1]) / 2,
            0
        ])
        return zone

    def metropolis_step(self, delta_E, step_num, total_steps):
        """Einzelner Metropolis-Schritt animieren mit Entscheidungszonen"""

        # Berechne Akzeptanzwahrscheinlichkeit
        if delta_E <= 0:
            p_accept = 1.0
        else:
            p_accept = np.exp(-delta_E * 1000 / (self.R * self.T))

        # Zufallszahl generieren
        r = random.random()
        accepted = r < p_accept

        # Farben und Text für Entscheidung
        decision_color = GREEN if accepted else RED
        decision_text = get_string("accepted") if accepted else get_string("rejected")

        # 1. Schritt-Nummer anzeigen
        step_info = Text(get_string("step").format(step_num, total_steps), color=YELLOW)
        step_info.scale(0.5)
        step_info.to_edge(UP).shift(DOWN * 0.7)
        self.play(FadeIn(step_info))
        self.wait(0.8)

        # 2. Vertikale Linie für ΔE
        x_coord = self.ax.coords_to_point(delta_E, 0)[0]
        y_top = self.ax.coords_to_point(delta_E, 1.1)[1]
        y_bottom = self.ax.coords_to_point(delta_E, 0)[1]

        delta_E_line = Line(
            [x_coord, y_bottom, 0],
            [x_coord, y_top, 0],
            color=YELLOW,
            stroke_width=3
        )

        # ΔE-Label neben der vertikalen Linie (rechts daneben)
        delta_E_label = Text(get_string("delta_e").format(delta_E), color=YELLOW)
        delta_E_label.scale(0.4)
        delta_E_label.next_to(delta_E_line, LEFT, buff=0.2)

        self.play(FadeIn(delta_E_line), FadeIn(delta_E_label))
        self.wait(0.8)

        # 3. Entscheidungszonen als farbige Rechtecke
        rect_width = 0.5  # Breite des Entscheidungsrechtecks

        # Akzeptanzzone (grün): von 0 bis P
        accept_rect_bottom_left = self.ax.coords_to_point(delta_E, 0)
        accept_rect_top_right = self.ax.coords_to_point(delta_E + rect_width, p_accept)

        acceptance_zone = Rectangle(
            width=accept_rect_top_right[0] - accept_rect_bottom_left[0],
            height=accept_rect_top_right[1] - accept_rect_bottom_left[1],
            fill_color=GREEN,
            fill_opacity=0.3,
            stroke_width=0
        )
        acceptance_zone.move_to(
            [(accept_rect_bottom_left[0] + accept_rect_top_right[0])/2,
             (accept_rect_bottom_left[1] + accept_rect_top_right[1])/2,
             0]
        )

        # Ablehnungszone (rot): von P bis 1
        reject_rect_bottom_left = self.ax.coords_to_point(delta_E, p_accept)
        reject_rect_top_right = self.ax.coords_to_point(delta_E + rect_width, 1)

        rejection_zone = Rectangle(
            width=reject_rect_top_right[0] - reject_rect_bottom_left[0],
            height=reject_rect_top_right[1] - reject_rect_bottom_left[1],
            fill_color=RED,
            fill_opacity=0.3,
            stroke_width=0
        )
        rejection_zone.move_to(
            [(reject_rect_bottom_left[0] + reject_rect_top_right[0])/2,
             (reject_rect_bottom_left[1] + reject_rect_top_right[1])/2,
             0]
        )

        self.play(FadeIn(acceptance_zone), FadeIn(rejection_zone))
        self.wait(0.8)

        # 4. Punkt auf Kurve
        point_y = self.ax.coords_to_point(delta_E, p_accept)[1]
        point = Dot(
            [x_coord, point_y, 0],
            radius=0.08,
            color=YELLOW
        )
        self.play(FadeIn(point))
        self.wait(0.4)

        # 5. Info-Box rechts vom Chart: P-Wert, Formel, r-Wert, Entscheidung
        info_box_pos = self.ax.coords_to_point(12, 0.75)

        # P-Label rechts
        p_label_text = Text(f"P = {p_accept:.3f}", color=YELLOW).scale(0.4)
        p_label_text.move_to(info_box_pos + UP * 1.2)

        # Formel rechts
        if delta_E < 0:
            # Sonderbehandlung für ΔE < 0: Nur Erklärung zeigen, keine Zufallszahl
            formula_text = Text(get_string("always_accept"), color=GREEN).scale(0.35)
            formula_text.move_to(info_box_pos + UP * 0.4)

            # Einblenden von P-Wert und Erklärung
            self.play(FadeIn(p_label_text), FadeIn(formula_text))
            self.wait(4.5)

            # Alles ausblenden
            self.play(
                FadeOut(step_info),
                FadeOut(delta_E_line), FadeOut(delta_E_label),
                FadeOut(acceptance_zone), FadeOut(rejection_zone),
                FadeOut(point),
                FadeOut(p_label_text), FadeOut(formula_text)
            )
            self.wait(0.5)
            return
        else:
            formula_text = Text(get_string("formula_positive"), color=BLUE).scale(0.35)
            formula_text.move_to(info_box_pos + UP * 0.4)

        self.play(FadeIn(p_label_text), FadeIn(formula_text))
        self.wait(1.0)

        # 6. Horizontale Linie für Zufallszahl r
        x_left = self.ax.coords_to_point(-5, 0)[0]
        x_right = self.ax.coords_to_point(20, 0)[0]
        y_r = self.ax.coords_to_point(0, r)[1]

        r_line = DashedLine(
            [x_left, y_r, 0],
            [x_right, y_r, 0],
            color=ORANGE,
            stroke_width=2
        )

        # r-Label rechts
        r_label_text = Text(f"r = {r:.3f}", color=ORANGE).scale(0.4)
        r_label_text.move_to(info_box_pos - UP * 0.4)

        self.play(FadeIn(r_line), FadeIn(r_label_text))
        self.wait(1.0)

        # 7. Entscheidungstext rechts
        if accepted:
            comparison_text = Text(get_string("comparison_accept"), color=GREEN).scale(0.35)
        else:
            comparison_text = Text(get_string("comparison_reject"), color=RED).scale(0.35)

        comparison_text.move_to(info_box_pos - UP * 1.2)

        decision_final = Text(decision_text, color=decision_color).scale(0.5)
        decision_final.move_to(info_box_pos - UP * 1.8)

        self.play(FadeIn(comparison_text), FadeIn(decision_final))
        self.wait(2)

        # Cleanup: Alles ausblenden
        self.play(
            FadeOut(step_info),
            FadeOut(delta_E_line), FadeOut(delta_E_label),
            FadeOut(acceptance_zone), FadeOut(rejection_zone),
            FadeOut(point),
            FadeOut(p_label_text), FadeOut(formula_text),
            FadeOut(r_line), FadeOut(r_label_text),
            FadeOut(comparison_text), FadeOut(decision_final)
        )
        self.wait(0.5)


class MetropolisTemperatures(Scene):
    """Szene 2: Temperatureffekte zeigen"""

    # ✅ Central parameter dictionary for GUI tool compatibility
    PARAMETERS = {
        # Physical parameters
        "R": {
            "value": 8.314,
            "type": float,
            "unit": "J/(mol·K)",
            "description": "Gas constant",
            "min": 8.0,
            "max": 9.0
        }
        # Note: T_values and colors_temp are lists, handled separately below
    }

    def construct(self):
        # Extract parameters from central dictionary
        self.R = self.PARAMETERS["R"]["value"]
        # Use module-level T_values and colors_temp (could be made configurable)
        self.T_values = T_values
        self.colors_temp = colors_temp

        self.ax = None
        self.curves = []

        # Setup
        self.setup_multi_temperature_plot()
        self.wait(2)

        # Demonstration mit verschiedenen ΔE-Werten
        delta_E_demos = [2, 5, 10]

        for delta_E in delta_E_demos:
            self.demonstrate_temperature_effect(delta_E)

        self.wait(3)

    def setup_multi_temperature_plot(self):
        """Setup: Achsen und Kurven für alle Temperaturen"""
        # Koordinatensystem
        self.ax = Axes(
            x_range=[-5, 20, 5],
            y_range=[0, 1.1, 0.2],
            width=10,
            height=6,
            axis_config={"color": GREY_A},
        )

        # Achsenlabels
        x_label = Text(get_string("x_axis"), color=WHITE).scale(0.4)
        x_label.next_to(self.ax.get_x_axis(), DOWN, buff=0.3)

        y_label = Text(get_string("y_axis"), color=WHITE).scale(0.4)
        y_label.next_to(self.ax.get_y_axis(), LEFT, buff=0.3)
        y_label.rotate(90 * DEGREES)

        # Titel
        title = Text(get_string("temp_title"), color=YELLOW)
        title.scale(0.6)
        title.to_edge(UP)

        # Kurven für verschiedene Temperaturen
        legend_entries = []

        for T, color in zip(self.T_values, self.colors_temp):
            # Positive Seite
            def acceptance_prob(x, T=T, R=self.R):
                """P(akzeptiert) = exp(-ΔE/RT) für ΔE > 0"""
                return np.exp(-x * 1000 / (R * T))

            curve = self.ax.get_graph(acceptance_prob, x_range=[0, 20], color=color)
            curve.set_stroke(width=3)
            self.curves.append(curve)

            # Horizontale Linie für ΔE < 0
            point_left = self.ax.coords_to_point(-5, 1)
            point_zero = self.ax.coords_to_point(0, 1)
            flat_line = DashedLine(point_left, point_zero, color=color, stroke_width=3)
            self.curves.append(flat_line)

            # Legende mit farbiger Box
            color_box = Rectangle(
                width=0.2, height=0.15,
                fill_color=color, fill_opacity=1,
                stroke_width=0
            )
            legend_text = Text(f"T = {T} K", color=WHITE).scale(0.35)
            legend_entry = VGroup(color_box, legend_text).arrange(RIGHT, buff=0.1)
            legend_entries.append(legend_entry)

        # Legende positionieren
        legend = VGroup(*legend_entries)
        legend.arrange(DOWN, buff=0.4)
        legend.to_corner(UP + RIGHT)

        # Animation aufbauen
        self.add(self.ax, x_label, y_label)
        for curve in self.curves:
            self.add(curve)
        self.add(legend, title)

        # Text-Erklärung
        explanation = Text(get_string("higher_temp"), color=WHITE)
        explanation.scale(0.4)
        explanation.to_edge(DOWN)
        self.add(explanation)

    def demonstrate_temperature_effect(self, delta_E):
        """Vergleiche Akzeptanzwahrscheinlichkeiten bei verschiedenen Temperaturen mit Zonen"""

        # Berechne P für jede Temperatur
        probs = []
        for T in T_values:
            if delta_E <= 0:
                p = 1.0
            else:
                p = np.exp(-delta_E * 1000 / (R * T))
            probs.append(p)

        # Vertikale Linie für ΔE
        x_coord = self.ax.coords_to_point(delta_E, 0)[0]
        y_top = self.ax.coords_to_point(delta_E, 1.1)[1]
        y_bottom = self.ax.coords_to_point(delta_E, 0)[1]

        delta_E_line = Line(
            [x_coord, y_bottom, 0],
            [x_coord, y_top, 0],
            color=YELLOW,
            stroke_width=2
        )

        # ΔE-Label neben der Linie
        label = Text(get_string("delta_e").format(delta_E), color=YELLOW)
        label.scale(0.4)
        label.next_to(delta_E_line, RIGHT, buff=0.2)

        self.play(FadeIn(delta_E_line), FadeIn(label))
        self.wait(0.8)

        # Entscheidungszonen nebeneinander für jede Temperatur
        rect_width = 0.22  # Breite pro Temperatur
        zones_to_animate = []

        for i, (T, color, p) in enumerate(zip(T_values, colors_temp, probs)):
            # Akzeptanzzone (grün-Variante für diese Temperatur)
            x_start = delta_E + i * rect_width
            accept_rect_bottom_left = self.ax.coords_to_point(x_start, 0)
            accept_rect_top_right = self.ax.coords_to_point(x_start + rect_width * 0.95, p)

            acceptance_zone = Rectangle(
                width=accept_rect_top_right[0] - accept_rect_bottom_left[0],
                height=accept_rect_top_right[1] - accept_rect_bottom_left[1],
                fill_color=color,
                fill_opacity=0.4,
                stroke_width=0
            )
            acceptance_zone.move_to(
                [(accept_rect_bottom_left[0] + accept_rect_top_right[0])/2,
                 (accept_rect_bottom_left[1] + accept_rect_top_right[1])/2,
                 0]
            )
            zones_to_animate.append(acceptance_zone)

            # Ablehnungszone (dunklere Variante)
            reject_rect_bottom_left = self.ax.coords_to_point(x_start, p)
            reject_rect_top_right = self.ax.coords_to_point(x_start + rect_width * 0.95, 1)

            rejection_zone = Rectangle(
                width=reject_rect_top_right[0] - reject_rect_bottom_left[0],
                height=reject_rect_top_right[1] - reject_rect_bottom_left[1],
                fill_color=color,
                fill_opacity=0.15,
                stroke_width=0
            )
            rejection_zone.move_to(
                [(reject_rect_bottom_left[0] + reject_rect_top_right[0])/2,
                 (reject_rect_bottom_left[1] + reject_rect_top_right[1])/2,
                 0]
            )
            zones_to_animate.append(rejection_zone)

        # Punkte auf den Kurven für jede Temperatur
        dots = []
        for T, color, p in zip(T_values, colors_temp, probs):
            y_coord = self.ax.coords_to_point(delta_E, p)[1]
            dot = Dot([x_coord, y_coord, 0], radius=0.08, color=color)
            dots.append(dot)
            zones_to_animate.append(dot)

        # Alle Zonen und Punkte animieren
        self.play(*[FadeIn(zone) for zone in zones_to_animate])
        self.wait(0.8)

        # Info-Box rechts
        info_box_pos = self.ax.coords_to_point(12, 0.7)

        info_texts = []
        for i, (T, color, p) in enumerate(zip(T_values, colors_temp, probs)):
            p_text = Text(f"T={T}K: P={p:.3f}", color=color).scale(0.35)
            p_text.move_to(info_box_pos + UP * (1 - i * 0.5))
            info_texts.append(p_text)

        self.play(*[FadeIn(text) for text in info_texts])
        self.wait(1.5)

        # Ausblenden
        self.play(
            FadeOut(delta_E_line), FadeOut(label),
            *[FadeOut(zone) for zone in zones_to_animate],
            *[FadeOut(text) for text in info_texts]
        )
        self.wait(0.5)


if __name__ == "__main__":
    # Render mit:
    #   manimgl metropolis_animation.py MetropolisBasic
    # oder:
    #   manimgl metropolis_animation.py MetropolisTemperatures
    pass
