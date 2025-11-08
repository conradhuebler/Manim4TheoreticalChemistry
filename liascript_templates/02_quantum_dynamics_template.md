<!--
author:   Computational Chemistry Course
email:
version:  1.0.0
language: de
narrator: Deutsch Female

comment:  LiaScript Template für quantum_dynamics_manim.py - Quantentunneln

@style
.lia-effect__circle {
  animation: none !important;
}
@end
-->

# Quantendynamik: Wellenpaket-Propagation & Tunneln

> **Lernziele:**
>
> - 🟢 Quantentunneln als nicht-klassisches Phänomen verstehen
> - 🟢 Rolle der Barrierenhöhe für Tunnelwahrscheinlichkeit
> - 🟡 Einfluss der Masse auf Quanteneffekte (Elektron vs. Proton)
> - 🟡 Wellenpaket-Dispersion und Heisenberg-Unschärfe
> - 🔴 WKB-Approximation für Tunnelwahrscheinlichkeit

## 📚 Theorie

Die **zeitabhängige Schrödinger-Gleichung** beschreibt die Dynamik von Quantensystemen:

$$i\hbar \frac{\partial \psi}{\partial t} = \hat{H} \psi = \left[-\frac{\hbar^2}{2m}\frac{\partial^2}{\partial x^2} + V(x)\right]\psi$$

Für ein **Doppeltopf-Potential** (double-well) mit Barriere:

$$V(x) = \begin{cases}
V_{\text{well}}(x) & \text{in den Töpfen} \\
V_{\text{barrier}} & \text{an der Barriere}
\end{cases}$$

### Quantentunneln

**Klassisch:** Teilchen mit E < V_barrier kann Barriere NICHT überwinden

**Quantenmechanisch:** Teilchen hat **endliche Wahrscheinlichkeit**, durch Barriere zu tunneln!

**Tunnelwahrscheinlichkeit (WKB-Approximation):**

$$T \approx e^{-2\gamma}, \quad \gamma = \frac{1}{\hbar}\int_{x_1}^{x_2} \sqrt{2m[V(x)-E]} \, dx$$

Je **höher die Barriere** oder **schwerer das Teilchen**, desto **geringer** die Tunnelrate.

---

## 🎬 Interaktive Animation: 5 Szenarien

### Szenario auswählen

Wähle eines der 5 vorkonfigurierten Szenarien:

[(TUNNELING)] 1. **TUNNELING** - Quantentunneln durch Barriere (barrier = 5 kcal/mol)
[( )] 2. **CLASSICAL_TRAPPED** - Klassisch gefangen (barrier = 100 kcal/mol)
[( )] 3. **HIGH_ENERGY** - Über-Barriere-Bewegung (E > V_barrier)
[( )] 4. **DISPERSION** - Starke Wellenpaket-Aufstreuung (breit, α = 0.2)
[( )] 5. **COHERENT** - Kohärente Oszillation (schmal, α = 5.0)

### Parameter anpassen (für fortgeschrittene Nutzer)

**Barrierenhöhe:**

<script input="range" value="5.0" output="barrier_val" min="1.0" max="200.0" step="1.0">@input</script>
barrier = <script>@input(`barrier_val`)</script> kcal/mol

**Wellenpaket-Breite (alpha):**

<script input="range" value="5.0" output="alpha_val" min="0.2" max="10.0" step="0.1">@input</script>
alpha = <script>@input(`alpha_val`)</script> (größer = schmaler)

**Teilchenmasse:**

<script input="range" value="50" output="mass_val" min="1" max="1836" step="10">@input</script>
mass = <script>@input(`mass_val`)</script> a.u. (1 = Elektron, 1836 = Proton)

**Startposition:**

<script input="range" value="-1.5" output="x0_val" min="-2.5" max="-1.0" step="0.1">@input</script>
x0 = <script>@input(`x0_val`)</script> Bohr

### Animation starten

```python
# Quantum wavepacket propagation
from quantum_dynamics_manim import QuantumDynamicsScene

# Szenario-basierte Parameter
SCENARIOS = {
    "TUNNELING": {"barrier": 5.0, "alpha": 5.0, "x0": -1.5, "mass": 50},
    "CLASSICAL_TRAPPED": {"barrier": 100.0, "alpha": 5.0, "x0": -1.5, "mass": 50},
    "HIGH_ENERGY": {"barrier": 1.0, "alpha": 3.0, "x0": -2.0, "mass": 20},
    "DISPERSION": {"barrier": 50.0, "alpha": 0.2, "x0": -1.5, "mass": 50},
    "COHERENT": {"barrier": 50.0, "alpha": 5.0, "x0": -1.5, "mass": 50}
}

# Animation mit gewählten Parametern
scene = QuantumDynamicsScene()
scene.PARAMETERS["active_scenario"]["value"] = "TUNNELING"  # Anpassen
scene.render()
```

---

## ✏️ Übung 1: Tunneln vs. klassische Barriere (🟢 Anfänger)

**Aufgabe:**
Vergleiche Szenario 1 (TUNNELING, barrier = 5 kcal/mol) mit Szenario 2 (CLASSICAL_TRAPPED, barrier = 100 kcal/mol).

**Frage 1:** Warum erreicht das Wellenpaket im ersten Fall die andere Seite?

[[ ]] Weil die kinetische Energie höher ist
[[X]] Weil Quantentunneln durch die Barriere möglich ist
[[ ]] Weil die Barriere zu breit ist
[[ ]] Weil das Wellenpaket schmaler ist
***********************************************************************

**Erklärung:**

Im **TUNNELING**-Szenario ist die Barriere niedrig (5 kcal/mol), sodass:

$$T \approx e^{-2\gamma} \approx 0.1 \quad (\text{ca. 10% Tunnelwahrscheinlichkeit})$$

Die Wellenfunktion ψ(x,t) **penetriert** die Barriere:
- In der Barriere: ψ(x) ∝ e^{-κx} (exponentieller Abfall, aber ≠ 0!)
- Nach der Barriere: Endliche Amplitude → **Teilchen tunnelt**

Im **CLASSICAL_TRAPPED**-Szenario ist barrier = 100 kcal/mol:

$$T \approx e^{-40} \approx 10^{-17} \quad (\text{praktisch null})$$

→ Das Wellenpaket wird **reflektiert** (klassisches Verhalten)

**Merke:** Quantentunneln ist ein **rein quantenmechanisches** Phänomen ohne klassisches Analogon!

***********************************************************************

---

## ✏️ Übung 2: Elektron vs. Proton (🟡 Fortgeschritten)

**Aufgabe:**
Starte mit TUNNELING (mass = 50 a.u.), dann erhöhe mass auf 1836 a.u. (Protonenmasse).

**Frage 2:** Wie ändert sich die Tunnelwahrscheinlichkeit?

[[X]] Nimmt stark ab (Proton tunnelt fast nicht)
[[ ]] Bleibt gleich (Masse spielt keine Rolle)
[[ ]] Nimmt zu (schwerere Teilchen tunneln besser)
[[ ]] Oszilliert periodisch
***********************************************************************

**Erklärung:**

Die Tunnelrate hängt **exponentiell** von der Masse ab:

$$T \propto e^{-2\gamma}, \quad \gamma \propto \sqrt{m}$$

**Faktor:** $\frac{m_{\text{Proton}}}{m_{\text{Elektron}}} = 1836$

→ $\gamma_{\text{Proton}} \approx 43 \times \gamma_{\text{Elektron}}$

**Ergebnis:**
- **Elektron** (m = 1 a.u.): T ≈ 10⁻² (tunnelt leicht!)
- **Proton** (m = 1836 a.u.): T ≈ 10⁻⁸⁶ (tunnelt praktisch nicht)

**Anwendung:**
- H-Tunneln in Enzymen (z.B. Alkohol-Dehydrogenase)
- Elektronentransfer-Reaktionen (Marcus-Theorie)
- Rastertunnelmikroskopie (STM)

***********************************************************************

---

## ✏️ Übung 3: Schmales vs. breites Wellenpaket (🟡 Fortgeschritten)

**Aufgabe:**
Variiere alpha: 0.5 (breit) → 5.0 (schmal) und beobachte Dispersion über Zeit.

**Frage 3:** Welches Wellenpaket streut stärker? Warum?

[[ ]] Schmales Paket (α = 5.0) streut stärker
[[X]] Breites Paket (α = 0.5) streut stärker
[[ ]] Beide streuen gleich
[[ ]] Keine Streuung erkennbar
***********************************************************************

**Erklärung:**

**Heisenberg-Unschärferelation:**

$$\Delta x \cdot \Delta p \geq \frac{\hbar}{2}$$

Ein **breites Wellenpaket** (α klein) hat:
- Große Ortsunschärfe: Δx groß
- **Kleine Impulsunschärfe:** Δp klein
- Aber: Viele Impulskomponenten p = ℏk

Ein **schmales Wellenpaket** (α groß) hat:
- Kleine Ortsunschärfe: Δx klein
- **Große Impulsunschärfe:** Δp groß → **starke Dispersion!**

**Zeitentwicklung:**

$$\Delta x(t) = \Delta x(0) \sqrt{1 + \left(\frac{\hbar t}{2m\Delta x(0)^2}\right)^2}$$

→ Je kleiner Δx(0), desto schneller wächst Δx(t)!

**Dispersion breites Paket (α = 0.5):**
- Δx(0) groß → langsame Ausbreitung
- Bleibt kompakt über längere Zeit

**Dispersion schmales Paket (α = 5.0):**
- Δx(0) klein → **schnelle Ausbreitung**
- Zerläuft rasch (typisch: Verdopplung in ~10 fs)

***********************************************************************

---

## ✏️ Übung 4: WKB-Approximation testen (🔴 Experte)

**Aufgabe:**
Berechne die theoretische Tunnelrate mit der WKB-Formel und vergleiche mit der Simulation.

**Gegeben:**
- Rechteckbarriere: V = V₀ für 0 < x < a
- Teilchenenergie: E < V₀
- WKB-Formel: $T \approx e^{-2\kappa a}$ mit $\kappa = \sqrt{2m(V_0-E)}/\hbar$

**Frage 4:** Für V₀ = 10 kcal/mol, E = 2 kcal/mol, a = 1.0 Å, m = 50 a.u., berechne T.

[[ ]] T ≈ 0.5 (50%)
[[ ]] T ≈ 0.1 (10%)
[[X]] T ≈ 0.01 (1%)
[[ ]] T ≈ 0.001 (0.1%)
***********************************************************************

**Berechnung:**

1. Konvertiere Einheiten:
   - V₀ - E = 8 kcal/mol = 0.347 eV = 0.0128 a.u.
   - a = 1.0 Å = 1.89 Bohr
   - m = 50 a.u.

2. Berechne κ:
   $$\kappa = \sqrt{2 \times 50 \times 0.0128} = \sqrt{1.28} \approx 1.13 \, \text{Bohr}^{-1}$$

3. Exponent:
   $$2\kappa a = 2 \times 1.13 \times 1.89 \approx 4.27$$

4. Tunnelwahrscheinlichkeit:
   $$T \approx e^{-4.27} \approx 0.014 \approx 1\%$$

**Vergleich mit Simulation:**
- WKB-Näherung: T ≈ 1%
- Numerische Propagation (Split-Step Fourier): T ≈ 1.2%
- **Abweichung:** < 20% → WKB ist gut!

**Gültigkeitsgrenzen der WKB:**
- Barriere muss "langsam variieren": $\lambda_{\text{deBroglie}} \ll $ Barrierenbreite
- Nicht gültig bei sehr dünnen Barrieren (a < 0.5 Å)
- Nicht gültig bei Resonanzen

***********************************************************************

---

## 📊 Zusammenfassung

Was Du gelernt hast:

- [[X]] Quantentunneln ist ein nicht-klassisches Phänomen
- [[X]] Tunnelwahrscheinlichkeit T ∝ e^(-√m·V)
- [[X]] Schwerere Teilchen (Protonen) tunneln viel weniger als leichte (Elektronen)
- [[X]] Breite Wellenpakete dispergieren langsamer als schmale
- [[X]] Heisenberg-Unschärfe: Δx·Δp ≥ ℏ/2
- [[X]] WKB-Approximation liefert gute Tunnelraten

---

## 🔬 Physikalische Anwendungen

### 1. Rastertunnelmikroskopie (STM)
- Elektronen tunneln zwischen Spitze und Probe (~ 1 nm Abstand)
- Tunnelstrom I ∝ e^(-2κd) extrem abstandsabhängig
- Auflösung: einzelne Atome sichtbar!

### 2. Chemische Reaktionen
- H-Atom-Transfer: Tunneln beschleunigt Reaktion bei tiefen T
- Kinetische Isotopieeffekte: k_H / k_D ≈ 7 (klassisch) vs. > 100 (Tunneln)
- Enzyme nutzen Tunneln: Glucose-Oxidase, Methylamin-Dehydrogenase

### 3. Kernfusion
- Coulomb-Barriere bei Proton-Proton-Fusion: ~ 1 MeV
- Sonnentemperatur: k_B T ~ 1 keV → E << V
- Ohne Tunneln: keine Fusion! Sonne existiert nur wegen Quantentunneln

### 4. Tunneldioden (Esaki-Diode)
- Negative differentielle Resistanz bei forward bias
- Ultra-schnelles Schalten (~ THz)
- Anwendung: Oszillatoren, Mischer in der Mikrowellentechnik

---

## 🎓 Weiterführende Themen

1. **Instanton-Theorie:** Tunneln bei endlicher Temperatur
2. **Multidimensionales Tunneln:** Reaktionspfade in der Chemie
3. **Dissipatives Tunneln:** Einfluss der Umgebung (Caldeira-Leggett)
4. **Coulomb-Blockade:** Tunneln einzelner Elektronen in Quantenpunkten
5. **Makroskopisches Quantentunneln:** SQUIDs, Josephson-Kontakte

---

**Schwierigkeitsgrad:** 🟢 Anfänger bis 🔴 Experte

**Geschätzte Bearbeitungszeit:** 45-60 Minuten

**Voraussetzungen:** Quantenmechanik-Grundlagen, Wellenfunktionen, Schrödinger-Gleichung
