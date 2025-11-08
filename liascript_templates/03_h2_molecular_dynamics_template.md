<!--
author:   Computational Chemistry Course
email:
version:  1.0.0
language: de
narrator: Deutsch Female

comment:  LiaScript Template für h2_md_full_refactored.py - H₂ Moleküldynamik

@style
.lia-effect__circle {
  animation: none !important;
}
@end
-->

# H₂-Moleküldynamik: Von freien Atomen zur Born-Oppenheimer-Näherung

> **Lernziele:**
>
> - 🟢 Molekülbildung aus Atomen verstehen
> - 🟢 Rolle der kinetischen Energie (Temperatur) auf Bindungsbildung
> - 🟡 Lennard-Jones vs. Morse-Potential unterscheiden
> - 🟡 MD-Integration (Velocity Verlet) verstehen
> - 🔴 Born-Oppenheimer-Näherung konzeptionell erfassen
> - 🔴 Thermodynamik der Bindungsbildung (ΔG = ΔH - TΔS)

## 📚 Theorie

Diese Animation zeigt den **vollständigen Prozess** der H₂-Molekülbildung in **5 Phasen**:

### Phase 1: Freie H-Atome in MD-Box
Einzelne H-Atome bewegen sich frei mit thermaler Energie E_kin = (3/2)k_B T.

**Box-Einschluss:**
$$V_{\text{box}}(x) = \frac{1}{2}k_{\text{box}}(|x| - r_{\text{box}})^2 \cdot \Theta(|x| - r_{\text{box}})$$

### Phase 2: Zwei H-Atome mit Lennard-Jones-Wechselwirkung
**Lennard-Jones-Potential:**
$$V_{\text{LJ}}(r) = 4\epsilon\left[\left(\frac{\sigma}{r}\right)^{12} - \left(\frac{\sigma}{r}\right)^6\right]$$

- $r^{-12}$: Pauli-Abstoßung (Elektron-Elektron)
- $r^{-6}$: Van-der-Waals-Anziehung (induzierte Dipole)

### Phase 3: Born-Oppenheimer-Näherung
**Konzept:** Trennung von Elektronen- und Kernbewegung

**Begründung:**
- Elektronenmasse: $m_e = 9.109 \times 10^{-31}$ kg
- Protonenmasse: $m_p = 1.673 \times 10^{-27}$ kg
- Verhältnis: $m_p / m_e \approx 1836$

→ Elektronen folgen **instantan** den Kernpositionen (adiabatische Näherung)

### Phase 4: H₂-Molekül mit Morse-Potential
**Morse-Potential:**
$$V_{\text{Morse}}(r) = D_e[1-e^{-\alpha(r-r_e)}]^2 - D_e$$

**H₂-Parameter:**
- D_e = 4.478 eV (Dissoziationsenergie)
- r_e = 0.741 Å (Gleichgewichtslänge)
- α = 1.5 Å⁻¹ (Breite)

### Phase 5: H₂-Dissoziation
Bei hoher kinetischer Energie (E_kin > D_e) dissoziiert H₂ zurück in freie Atome.

---

## 🎬 Interaktive Animation

### Globale Parameter

**Temperatur:**

<script input="range" value="1500" output="T_val" min="300" max="3000" step="100">@input</script>
T = <script>@input(`T_val`)</script> K

**Zeitschritt (Integrator):**

<script input="range" value="0.5" output="dt_val" min="0.1" max="2.0" step="0.1">@input</script>
dt = <script>@input(`dt_val`)</script> fs

**Box-Größe:**

<script input="range" value="6.0" output="box_val" min="2.0" max="10.0" step="0.5">@input</script>
box_size = <script>@input(`box_val`)</script> Å

### Lennard-Jones-Parameter (Phase 2)

**Epsilon (Tiefe):**

<script input="range" value="0.1" output="epsilon_val" min="0.01" max="0.5" step="0.01">@input</script>
epsilon = <script>@input(`epsilon_val`)</script> eV

**Sigma (Länge):**

<script input="range" value="1.5" output="sigma_val" min="1.0" max="3.0" step="0.1">@input</script>
sigma = <script>@input(`sigma_val`)</script> Å

### Morse-Parameter (Phase 4)

**Dissoziationsenergie:**

<script input="range" value="4.478" output="De_val" min="2.0" max="6.0" step="0.1">@input</script>
D_e = <script>@input(`De_val`)</script> eV

**Morse-Breite:**

<script input="range" value="1.5" output="alpha_morse_val" min="1.0" max="2.5" step="0.1">@input</script>
alpha = <script>@input(`alpha_morse_val`)</script> Å⁻¹

### Phasen-Dauern konfigurieren

**Phase 1 (Freie Atome):**

<script input="range" value="200" output="phase1_steps" min="50" max="1000" step="50">@input</script>
Schritte: <script>@input(`phase1_steps`)</script> (~<script>@input(`phase1_steps`) * @input(`dt_val`) / 1000</script> ps)

**Phase 2 (LJ-Wechselwirkung):**

<script input="range" value="800" output="phase2_steps" min="200" max="2000" step="100">@input</script>
Schritte: <script>@input(`phase2_steps`)</script> (~<script>@input(`phase2_steps`) * @input(`dt_val`) / 1000</script> ps)

**Phase 4 (H₂-Formation):**

<script input="range" value="200" output="phase4_steps" min="50" max="1000" step="50">@input</script>
Schritte: <script>@input(`phase4_steps`)</script> (~<script>@input(`phase4_steps`) * @input(`dt_val`) / 1000</script> ps)

**Phase 5 (Dissoziation):**

<script input="range" value="200" output="phase5_steps" min="50" max="1000" step="50">@input</script>
Schritte: <script>@input(`phase5_steps`)</script> (~<script>@input(`phase5_steps`) * @input(`dt_val`) / 1000</script> ps)

### Animation starten

```python
from h2_md_full_refactored import H2MDFullRefactored

# Parameter setzen
scene = H2MDFullRefactored()
scene.PARAMETERS["T"]["value"] = @input(`T_val`)
scene.PARAMETERS["dt"]["value"] = @input(`dt_val`)
scene.PARAMETERS["epsilon"]["value"] = @input(`epsilon_val`)
scene.PARAMETERS["sigma"]["value"] = @input(`sigma_val`)
scene.PARAMETERS["D_e"]["value"] = @input(`De_val`)
scene.PARAMETERS["alpha"]["value"] = @input(`alpha_morse_val`)
scene.PARAMETERS["phase1_steps"]["value"] = @input(`phase1_steps`)
scene.PARAMETERS["phase2_steps"]["value"] = @input(`phase2_steps`)
scene.PARAMETERS["phase4_steps"]["value"] = @input(`phase4_steps`)
scene.PARAMETERS["phase5_steps"]["value"] = @input(`phase5_steps`)

# Velocity Verlet Integration
scene.render()
```

---

## ✏️ Übung 1: Temperatur und Bindungsbildung (🟢 Anfänger)

**Aufgabe:**
Variiere die Temperatur: 300 K (niedrig) → 3000 K (hoch) und beobachte Phase 4 (H₂-Formation).

**Frage 1:** Bei welcher Temperatur vibriert H₂ am stärksten?

[[ ]] 300 K
[[ ]] 1000 K
[[ ]] 1500 K
[[X]] 3000 K
***********************************************************************

**Erklärung:**

Die **kinetische Energie** ist direkt proportional zur Temperatur:

$$\langle E_{\text{kin}} \rangle = \frac{3}{2}k_B T$$

Bei höheren Temperaturen:
- **Größere Schwingungsamplitude** um r_e
- **Höhere Vibrationsfrequenz** (mehr Energie in Schwingungsmoden)
- **Höhere Wahrscheinlichkeit** für Anregung in höhere Vibrationszustände

**Numerisch:**
- T = 300 K: $\langle E_{\text{kin}} \rangle \approx 0.04$ eV → Vibration um r_e ± 0.05 Å
- T = 3000 K: $\langle E_{\text{kin}} \rangle \approx 0.4$ eV → Vibration um r_e ± 0.2 Å

**Dissoziation:**
Wenn $\langle E_{\text{kin}} \rangle > D_e = 4.478$ eV (entspricht T ~ 52000 K), dissoziiert H₂ spontan!

***********************************************************************

**Frage 2:** Kann H₂ bei 3000 K spontan dissoziieren?

[[ ]] Ja, immer
[[X]] Nein, E_kin(3000K) << D_e
[[ ]] Nur bei sehr langen Zeiten
[[ ]] Nur wenn alpha groß ist
***********************************************************************

**Erklärung:**

Bei T = 3000 K:
$$\langle E_{\text{kin}} \rangle = \frac{3}{2} \times 8.617 \times 10^{-5} \times 3000 \approx 0.39 \, \text{eV}$$

Verglichen mit D_e = 4.478 eV:
$$\frac{\langle E_{\text{kin}} \rangle}{D_e} \approx 0.09 \approx 9\%$$

→ **Viel zu wenig Energie** für spontane Dissoziation!

**Für Dissoziation notwendig:**
$$T_{\text{diss}} \approx \frac{2 D_e}{3 k_B} \approx \frac{2 \times 4.478}{3 \times 8.617 \times 10^{-5}} \approx 34600 \, \text{K}$$

**Aber:** Bei hohen T können **thermale Fluktuationen** einzelne Moleküle über D_e bringen (Boltzmann-Tail)!

$$P(E > D_e) \propto e^{-D_e / k_B T}$$

Bei 3000 K: P ≈ 10⁻²³ (extrem selten)

***********************************************************************

---

## ✏️ Übung 2: Lennard-Jones-Parameter (🟡 Fortgeschritten)

**Aufgabe:**
In Phase 2 variiere epsilon: 0.05 eV → 0.3 eV und beobachte das Annäherungsverhalten.

**Frage 3:** Wie beeinflusst epsilon die Kollisionsfrequenz?

[[X]] Größeres epsilon → mehr Anziehung → häufigere Annäherung
[[ ]] Größeres epsilon → mehr Abstoßung → seltenere Annäherung
[[ ]] Epsilon hat keinen Einfluss auf Dynamik
[[ ]] Nur sigma beeinflusst Kollisionen
***********************************************************************

**Erklärung:**

Das Lennard-Jones-Potential hat:
- **Anziehung** bei mittleren Abständen (r ~ σ bis 2.5σ)
- **Abstoßung** bei kurzen Abständen (r < σ)

**Epsilon bestimmt:**
- **Potentialtiefe** bei r_min = 2^(1/6)·σ
- **Anziehungsstärke** für Van-der-Waals-Kräfte

**Effekt auf Dynamik:**

Kleines epsilon (0.05 eV):
- Schwache Anziehung
- Atome "ignorieren" einander weitgehend
- Seltene, kurze Begegnungen

Großes epsilon (0.3 eV):
- Starke Anziehung
- Atome bilden **temporäres Cluster**
- Lange Verweildauer bei r ≈ r_min
- **Häufige Rekollisionen**

**Vergleich mit Morse:**
In Phase 4 wird LJ durch **Morse** ersetzt, weil:
- Morse beschreibt **echte chemische Bindung** (kovalent)
- LJ beschreibt nur **Van-der-Waals** (physikalische Wechselwirkung)
- Morse hat **Dissoziation** eingebaut (V → 0 bei r → ∞)

***********************************************************************

---

## ✏️ Übung 3: Schwache vs. starke Bindungen (🟡 Fortgeschritten)

**Aufgabe:**
In Phase 4 variiere D_e: 2.0 eV → 6.0 eV und beobachte die Vibrationsfrequenz.

**Frage 4:** Gilt ω ∝ √D_e? Überprüfe experimentell!

Für D_e = 2.0 eV: ω₁ = [[_____]] cm⁻¹
Für D_e = 4.0 eV: ω₂ = [[_____]] cm⁻¹

Verhältnis ω₂/ω₁ = [[1.41]]
[[?]] Tipp: √(4.0/2.0) = √2 ≈ 1.41
***********************************************************************

**Erklärung:**

Die Vibrationsfrequenz nahe dem Minimum folgt aus:

$$\omega = \sqrt{\frac{k}{\mu}}$$

Mit der Beziehung $k = 2D_e\alpha^2$ (aus Morse-Potential):

$$\omega = \sqrt{\frac{2D_e\alpha^2}{\mu}} \propto \sqrt{D_e}$$

**Experimentelle Verifikation:**

Aus der Animation kann man die Schwingungsperiode T ablesen:
- T = Zeit für eine volle Oszillation (r_max → r_min → r_max)
- ω = 2π/T (in rad/s)
- Oder in Spektroskopie: ν̃ = ω/(2πc) (in cm⁻¹)

**Beispiel H₂:**
- D_e = 4.478 eV, α = 1.5 Å⁻¹, μ = 0.5 a.u.
- k = 2 × 4.478 × 1.5² ≈ 20.2 eV/Å²
- ω = √(20.2 / 0.5) ≈ 6.4 rad/fs
- ν̃ ≈ 4400 cm⁻¹ ✓ (experimentell: 4401 cm⁻¹)

**Test der Proportionalität:**
- D_e × 2 → ω × √2 ≈ 1.41
- D_e × 4 → ω × 2

***********************************************************************

---

## ✏️ Übung 4: Dissoziation und Energiebilanz (🔴 Experte)

**Aufgabe:**
In Phase 5 stelle sicher, dass E_kin(initial) > D_e. Variiere phase5_steps (schnell vs. langsam).

**Frage 5:** Ist die Gesamtenergie E_total = E_kin + E_pot erhalten?

[[ ]] Nein, Energie geht verloren
[[ ]] Nur wenn dt sehr klein ist
[[X]] Ja, Velocity Verlet ist symplektisch (Energie-erhaltend)
[[ ]] Nur bei adiabatischen Prozessen
***********************************************************************

**Erklärung:**

**Velocity Verlet-Integrator:**

$$x(t+dt) = x(t) + v(t) \cdot dt + \frac{1}{2}a(t) \cdot dt^2$$
$$v(t+dt) = v(t) + \frac{1}{2}[a(t) + a(t+dt)] \cdot dt$$

**Eigenschaften:**
- **Symplektisch:** Erhält Phasenraumvolumen (Liouville-Theorem)
- **Zeitumkehr-invariant:** T-symmetrisch
- **Energie-Drift:** O(dt²) über kurze Zeit, **beschränkt** über lange Zeit

**Energieerhaltung testen:**

Plot E_total(t) = E_kin(t) + E_pot(t) während Phase 5:

```python
import matplotlib.pyplot as plt

# Während MD-Simulation
E_total = []
for step in range(phase5_steps):
    # Velocity Verlet step
    # ...
    E_kin = 0.5 * mass * v**2
    E_pot = morse_potential(r)
    E_total.append(E_kin + E_pot)

plt.plot(E_total)
plt.ylabel("E_total (eV)")
plt.xlabel("Step")
plt.title("Energy Conservation Check")
plt.show()
```

**Erwartung:**
- **Perfekte Erhaltung:** E_total = const. (flache Linie)
- **Realität:** Kleine Fluktuationen um Mittelwert (Drift < 0.1% über 1000 steps)

**Wenn Energie NICHT erhalten:**
- dt zu groß → reduziere auf 0.1 fs
- Numerische Instabilität → Force-Clipping nötig
- Cutoff-Probleme → Smoothing bei r_cut

***********************************************************************

**Frage 6:** Wohin geht die potentielle Energie bei Dissoziation?

[[X]] Wird in kinetische Energie umgewandelt
[[ ]] Wird abgestrahlt als Licht
[[ ]] Geht verloren durch Reibung
[[ ]] Bleibt konstant
***********************************************************************

**Erklärung:**

**Energiebilanz:**

Initial (gebundener Zustand bei r = r_e):
$$E_{\text{pot}}(r_e) = -D_e = -4.478 \, \text{eV}$$
$$E_{\text{kin}}(\text{initial}) = E_0 > D_e$$

Final (dissoziiert bei r → ∞):
$$E_{\text{pot}}(r \to \infty) = 0$$
$$E_{\text{kin}}(\text{final}) = E_0 + D_e$$

→ Die **Bindungsenergie D_e wird freigesetzt** und erhöht E_kin!

**Experimentelle Analogie:**
- Photodissoziation: hν > D_e → Fragmente mit E_kin = hν - D_e
- Thermische Dissoziation: k_B T ~ D_e → Gleichverteilung über Freiheitsgrade

***********************************************************************

---

## 📊 Zusammenfassung

Was Du gelernt hast:

- [[X]] Molekülbildung verläuft in mehreren Phasen
- [[X]] Temperatur bestimmt kinetische Energie und Vibrationen
- [[X]] Lennard-Jones beschreibt Van-der-Waals, Morse chemische Bindungen
- [[X]] Velocity Verlet ist symplektisch (energie-erhaltend)
- [[X]] Vibrationsfrequenz ω ∝ √D_e
- [[X]] Born-Oppenheimer-Näherung trennt Elektronen-/Kernbewegung
- [[X]] Bei Dissoziation wird E_pot in E_kin umgewandelt

---

## 🔬 Weiterführende Konzepte

### 1. Statistische Mechanik
**Maxwell-Boltzmann-Verteilung:**
$$P(v) = \left(\frac{m}{2\pi k_B T}\right)^{3/2} 4\pi v^2 e^{-mv^2/(2k_BT)}$$

→ Initialisierung der Geschwindigkeiten in Phase 1

### 2. Thermodynamik der Bindungsbildung
**Freie Energie:**
$$\Delta G = \Delta H - T\Delta S$$

- Bei niedriger T: ΔH dominiert → Bindung bevorzugt (exotherm)
- Bei hoher T: -TΔS dominiert → Dissoziation bevorzugt (Entropie!)

**Gleichgewichtskonstante:**
$$K_{\text{eq}}(T) = e^{-\Delta G / (k_B T)}$$

### 3. Nicht-adiabatische Effekte
**Wann versagt Born-Oppenheimer?**
- Konische Durchschneidungen (conical intersections)
- Ultraschnelle Prozesse (< 10 fs)
- Elektronisch angeregte Zustände

→ Surface hopping (Tully), Ehrenfest-Dynamik, MCTDH

### 4. Enhanced Sampling
**Problem:** Barriere zwischen freien Atomen und gebundenem H₂

**Lösungen:**
- **Umbrella Sampling:** Künstliches Potential entlang Reaktionskoordinate
- **Metadynamik:** Gaussians füllen FES auf (siehe Template 5!)
- **Replica Exchange:** Parallele Simulationen bei verschiedenen T

---

## 🎓 Quiz: Verständnistest

Teste Dein Wissen!

**Frage 1:** Welche Phasen durchläuft die Simulation?

- [[X]] Freie Atome
- [[X]] LJ-Wechselwirkung
- [[X]] Born-Oppenheimer-Übergang
- [[X]] H₂-Formation
- [[X]] Dissoziation
- [[ ]] Ionisation

**Frage 2:** Was ist die Born-Oppenheimer-Näherung?

- [[ ]] Elektronen und Kerne bewegen sich gleich schnell
- [[X]] Elektronen folgen Kernen instantan (adiabatisch)
- [[ ]] Nur Kerne werden quantenmechanisch behandelt
- [[ ]] Nur Elektronen werden quantenmechanisch behandelt

**Frage 3:** Was passiert bei T → ∞?

- [[ ]] H₂ wird stabiler
- [[X]] Alle Moleküle dissoziieren
- [[ ]] Keine Änderung
- [[ ]] Elektronen trennen sich

---

**Schwierigkeitsgrad:** 🟢 Anfänger bis 🔴 Experte

**Geschätzte Bearbeitungszeit:** 60-90 Minuten

**Voraussetzungen:** Moleküldynamik, Statistische Mechanik, Quantenchemie (Grundlagen)

**Software:** ManimGL, NumPy, SciPy
