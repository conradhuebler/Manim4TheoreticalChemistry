# LiaScript Übungsaufgaben - Parameter-Variations-Analyse

> **Ziel**: Systematische Analyse aller 19 Animationsszenarien zur Identifikation geeigneter Parameter-Variationen für interaktive LiaScript-Übungsaufgaben.

**Legende**:
- 🎯 Eignung: ⭐ (niedrig) bis ⭐⭐⭐⭐⭐ (sehr hoch)
- 📚 Niveau: 🟢 Anfänger | 🟡 Fortgeschritten | 🔴 Experte
- ✨ = Besonders gut für Übungen geeignet

---

## 📊 Schnellübersicht - Kategorisierung

### Top-Priorität für LiaScript (⭐⭐⭐⭐⭐)
1. **bond_stretching.py** - Harmonisches vs. Morse-Potential ✨
2. **quantum_dynamics_manim.py** - Tunneling-Szenarien ✨
3. **h2_md_full_refactored.py** - H₂-Moleküldynamik ✨
4. **polymer_monte_carlo.py** - MC-Sampling mit Presets ✨
5. **metadynamics_visualization.py** - Enhanced Sampling ✨

### Hohe Priorität (⭐⭐⭐⭐)
6. **nh3_inversion.py** - Umbrella-Inversion
7. **h3_reaction_pathway.py** - Reaktionspfade
8. **geometry_optimization.py** - Optimierungsalgorithmen
9. **polarization_forcefield.py** - Forcefields vergleichen
10. **polymer_sampling_comparison.py** - Sampling-Methoden

### Mittlere Priorität (⭐⭐⭐)
11. **angle_bending.py** - Winkelpotentiale
12. **torsion_angle_optimized.py** - Torsionswinkel
13. **nonbonded_interactions.py** - Lennard-Jones
14. **variational_method.py** - Variationsprinzip
15. **monte_carlo_pi.py** - Monte Carlo Grundlagen

### Spezielle Anwendungen (⭐⭐)
16. **metropolis_animation.py** - Didaktisch fixiert
17. **particle_interactions_combinatorics.py** - Kombinatorik
18. **pca_molecular_dynamics.py** - PCA-Analyse
19. **quantum_nonlocality.py** - Quantenkorrelationen

---

## 📖 Detaillierte Analyse nach Dateien

---

### 1. bond_stretching.py ⭐⭐⭐⭐⭐ ✨

**Thema**: Molekulare Bindungsdehnungspotentiale (Harmonisch vs. Morse)

**Konfigurierbare Parameter**:
```python
"D_e": 4.478 eV          # Dissoziationsenergie
"r_e": 0.741 Å           # Gleichgewichtsabstand
"alpha": 1.9 Å⁻¹         # Morse-Parameter (Breite)
"k": 574.0 eV/Å²         # Harmonische Federkonstante
"amplitude": 0.3 Å       # Oszillationsamplitude
"oscillation_cycles": 3  # Anzahl Schwingungen
"fps": 30                # Animation fps
```

**Sinnvolle Parameter-Variationen für Übungen**:

| Parameter | Variation | Physikalischer Effekt | Niveau |
|-----------|-----------|----------------------|--------|
| `D_e` | 2.0 → 8.0 eV | Stärkere Bindung → kleinere Anharmonizität | 🟢 |
| `alpha` | 0.5 → 3.0 Å⁻¹ | Breitere/schmalere Potentialkurve | 🟡 |
| `amplitude` | 0.1 → 0.8 Å | Harmonisch → stark anharmonisch | 🟢 |
| `r_e` | 0.5 → 1.5 Å | Verändert Gleichgewichtslänge | 🟢 |
| `k` | 200 → 1000 eV/Å² | Steifere/weichere Bindung | 🟡 |

**Lernziele**:

🟢 **Anfänger**:
- Unterschied harmonisches vs. Morse-Potential verstehen
- Einfluss von D_e und r_e auf Bindungsstärke
- Konzept der Anharmonizität erkennen

🟡 **Fortgeschritten**:
- Quantitative Abweichung bei großen Amplituden
- Physikalische Bedeutung von alpha-Parameter
- Schwingungsfrequenz vs. Federkonstante

🔴 **Experte**:
- Beziehung k = 2·D_e·alpha² herleiten
- Grenzfall Dissoziation analysieren
- Morse-Potential aus quantenmechanischen Prinzipien

**LiaScript Übungsvorschläge**:

**Übung 1 (🟢)**: "Wann versagt die harmonische Näherung?"
- Variiere `amplitude` von 0.1 → 0.8 Å
- Beobachte Abweichung Morse vs. harmonisch
- Frage: Bei welcher Amplitude wird Fehler > 10%?

**Übung 2 (🟡)**: "Starke vs. schwache Bindungen"
- Vergleiche H-H (D_e=4.5 eV) mit hypothetischem He-He (D_e=0.01 eV)
- Variiere D_e und alpha entsprechend
- Frage: Wie ändert sich die Schwingungsfrequenz?

**Übung 3 (🔴)**: "Der alpha-Parameter"
- Zeige dass k = 2·D_e·alpha² gilt
- Variiere alpha bei konstantem D_e
- Frage: Wie verändert sich die Krümmung bei r_e?

**Empfohlene Ergänzungen**:
- ✅ Parameter für quantisierte Energieniveaus (E_n = ℏω(n+½))
- ✅ Optionale Anzeige der klassischen Umkehrpunkte
- ✅ Direkte Anzeige von ω = √(k/μ) für harmonischen Oszillator

---

### 2. quantum_dynamics_manim.py ⭐⭐⭐⭐⭐ ✨

**Thema**: Quantendynamik - Wellenpaket-Propagation im Doppeltopf-Potential

**Konfigurierbare Parameter**:
```python
"active_scenario": "TUNNELING"  # 5 Presets verfügbar
"barrier": 100.0 kcal/mol       # Barrierenhöhe
"alpha": 5.0                    # Wellenpaket-Breite
"x0": -1.5 Bohr                 # Startposition
"mass": 50 a.u.                 # Teilchenmasse
"width": 3.0 Bohr               # Doppeltopf-Breite
"duration": 15.0 s              # Animationsdauer
"snapshot_freq": 10             # Update-Frequenz
```

**Verfügbare Szenarien**:
1. `TUNNELING` - Quantentunneln durch Barriere
2. `CLASSICAL_TRAPPED` - Klassisch gefangen
3. `HIGH_ENERGY` - Über-Barriere-Bewegung
4. `DISPERSION` - Starke Wellenpaket-Aufstreuung
5. `COHERENT` - Kohärente Oszillation

**Sinnvolle Parameter-Variationen für Übungen**:

| Parameter | Variation | Quanteneffekt | Niveau |
|-----------|-----------|---------------|--------|
| `barrier` | 1 → 200 kcal/mol | Tunnelwahrscheinlichkeit ↓ | 🟢 |
| `alpha` | 0.2 → 10.0 | Lokalisierung vs. Dispersion | 🟡 |
| `mass` | 1 → 1836 a.u. | Elektron → Proton: weniger Tunneln | 🟡 |
| `x0` | -2.5 → -1.0 Bohr | Initiale kinetische Energie | 🟢 |
| `width` | 1.0 → 5.0 Bohr | Barrierenbreite ändert Tunneln | 🔴 |

**Lernziele**:

🟢 **Anfänger**:
- Quantentunneln als nicht-klassisches Phänomen
- Rolle der Barrierenhöhe für Tunneln
- Wahrscheinlichkeitsdichte |ψ|²

🟡 **Fortgeschritten**:
- Einfluss der Masse auf Quanteneffekte
- Wellenpaket-Dispersion und Heisenberg-Unschärfe
- Tunnelrate vs. Barrierenparameter

🔴 **Experte**:
- WKB-Approximation für Tunnelwahrscheinlichkeit
- Split-step Fourier Propagation verstehen
- Quantenklassischer Übergang (Korrespondenzprinzip)

**LiaScript Übungsvorschläge**:

**Übung 1 (🟢)**: "Tunneln vs. klassische Barriere"
- Vergleiche `TUNNELING` (barrier=5) mit `CLASSICAL_TRAPPED` (barrier=100)
- Frage: Warum erreicht das Teilchen im ersten Fall die andere Seite?

**Übung 2 (🟡)**: "Elektron vs. Proton"
- Starte mit `TUNNELING` (mass=50 a.u.)
- Erhöhe mass auf 1836 a.u. (Protonenmasse)
- Frage: Wie ändert sich die Tunnelwahrscheinlichkeit? Warum?

**Übung 3 (🟡)**: "Schmales vs. breites Wellenpaket"
- Variiere `alpha`: 0.5 (breit) → 5.0 (schmal)
- Beobachte Dispersion über Zeit
- Frage: Welches Paket streut stärker? Warum? (Δp·Δx ≥ ℏ/2)

**Übung 4 (🔴)**: "WKB-Approximation testen"
- Berechne theoretische Tunnelrate mit WKB-Formel
- Variiere barrier und width systematisch
- Frage: Ab welcher Barriere gilt WKB gut?

**Empfohlene Ergänzungen**:
- ✅ Anzeige der durchschnittlichen kinetischen Energie <KE>
- ✅ Parameter für initiale Impulskomponente p₀
- ✅ Overlay: klassische Teilchentrajektorie zum Vergleich
- ✅ Quantitative Tunnelwahrscheinlichkeit berechnen und anzeigen

---

### 3. h2_md_full_refactored.py ⭐⭐⭐⭐⭐ ✨

**Thema**: H₂-Moleküldynamik - Von freien Atomen zur Born-Oppenheimer-Näherung

**Konfigurierbare Parameter** (22 Parameter!):
```python
# Physikalische Konstanten
"T": 1500 K              # Temperatur
"dt": 0.5 fs             # Zeitschritt
"k_B": 8.617e-5 eV/K     # Boltzmann-Konstante

# Morse-Potential (H₂)
"D_e": 4.478 eV          # Dissoziationsenergie
"r_e": 0.741 Å           # Gleichgewichtsbindungslänge
"alpha": 1.5 Å⁻¹         # Morse-Breite

# Lennard-Jones (Phase 2)
"epsilon": 0.1 eV        # LJ-Tiefe
"sigma": 1.5 Å           # LJ-Länge

# Phasen-Dauer (5 Phasen!)
"phase1_steps": 200      # Freie Atome
"phase2_steps": 800      # Zwei Atome mit Wechselwirkung
"phase4_steps": 200      # H₂-Formation
"phase5_steps": 200      # Dissoziation
# + entsprechende wait-Parameter
```

**5 Simulationsphasen**:
1. Phase 1: Freie H-Atome in Box
2. Phase 2: Zwei H-Atome mit LJ-Wechselwirkung
3. Phase 3: Born-Oppenheimer-Näherung (konzeptionell)
4. Phase 4: H₂-Molekül-Formation mit Morse-Potential
5. Phase 5: H₂-Dissoziation

**Sinnvolle Parameter-Variationen für Übungen**:

| Parameter | Variation | Physikalischer Effekt | Niveau |
|-----------|-----------|----------------------|--------|
| `T` | 300 → 3000 K | Kinetische Energie, Bindungsbildung | 🟢 |
| `epsilon` (LJ) | 0.01 → 0.5 eV | Stärke der Annäherung (Phase 2) | 🟡 |
| `D_e` | 2.0 → 6.0 eV | Bindungsstärke von H₂ | 🟡 |
| `phase2_steps` | 200 → 2000 | Zeit bis zur Begegnung | 🟢 |
| `phase5_steps` | 50 → 500 | Geschwindigkeit der Dissoziation | 🟢 |
| `box_size` | 2.0 → 10.0 Å | Einfluss des Einschlussvolumens | 🔴 |

**Lernziele**:

🟢 **Anfänger**:
- Molekülbildung aus Atomen verstehen
- Rolle der kinetischen Energie (Temperatur)
- Born-Oppenheimer-Näherung konzeptionell

🟡 **Fortgeschritten**:
- Lennard-Jones vs. Morse-Potential
- MD-Integration (Velocity Verlet)
- Energieerhaltung in Phasen 4-5

🔴 **Experte**:
- Thermodynamik der Bindungsbildung (ΔG = ΔH - TΔS)
- Übergangszustandstheorie
- Elektronische vs. nukleare Zeitskalen

**LiaScript Übungsvorschläge**:

**Übung 1 (🟢)**: "Temperatur und Bindungsbildung"
- Variiere T: 300 K (niedrig) → 3000 K (hoch)
- Beobachte Phase 4 (Formation)
- Frage: Bei welcher Temperatur vibriert H₂ stärker? Dissoziiert es spontan?

**Übung 2 (🟡)**: "Lennard-Jones Parameter"
- Phase 2: Variiere epsilon (0.05 → 0.3 eV)
- Beobachte Annäherungsverhalten
- Frage: Wie beeinflusst epsilon die Kollisionsfrequenz?

**Übung 3 (🟡)**: "Schwache vs. starke Bindungen"
- Variiere D_e (2.0 → 6.0 eV) in Phase 4
- Beobachte Vibrationsfrequenz
- Frage: Gilt ω ∝ √(D_e)? Warum?

**Übung 4 (🔴)**: "Dissoziation und Energiebilanz"
- Phase 5: Stelle sicher dass E_kin(initial) > D_e
- Variiere phase5_steps (schnell vs. langsam)
- Frage: Ist Energie erhalten? Wo geht sie hin?

**Empfohlene Ergänzungen**:
- ✅ Echtzeit-Anzeige von E_total, E_kin, E_pot
- ✅ Parameter für externe Kraft (z.B. optische Pinzette)
- ✅ Optionale Quantisierung der Schwingungsniveaus
- ✅ Thermostat-Option für konstante Temperatur

---

### 4. polymer_monte_carlo.py ⭐⭐⭐⭐⭐ ✨

**Thema**: Monte Carlo Polymer Coarse-Graining mit Presets

**Konfigurierbare Parameter**:
```python
"active_preset": "DEMO"   # 8 Presets!
"steps": 10000            # MC-Schritte

# Polymer-Geometrie
"n_beads": 20             # Anzahl Beads
"r0_bond": 1.5 Å          # Gleichgewichtsbindung
"k_bond": 300 kcal/(mol·Å²)  # Bindungsstärke

# Lennard-Jones
"epsilon_lj": 1.5 kcal/mol    # Van-der-Waals
"sigma_lj": 1.2 Å             # Bead-Größe
"cutoff_lj": 100 Å            # Reichweite

# Monte Carlo
"temperature": 300 K          # Temperatur
"max_displacement": 0.15 Å    # MC-Schrittweite

# Phasen
"phase1_steps": 10        # Slow demo
"phase2_steps": 80        # Medium speed
"phase3_wait": 0.0001 s   # Fast thermalization
```

**8 verfügbare Presets**:
1. `REALISTIC` - Physikalisch realistische Parameter
2. `DEMO` - Optimiert für schnelle visuelle Demo
3. `SLOW` - Langsame Relaxation
4. `EDUCATIONAL` - Mit ausführlichen Erklärungen
5. `NO_LJ` - Nur Bindungen (keine Van-der-Waals)
6. `NO_BONDS` - Nur LJ (keine Bindungen)
7. `BOTH` - Beide Potentiale stark
8. `NONE` - Brownian Diffusion (keine Potentiale)

**Sinnvolle Parameter-Variationen für Übungen**:

| Parameter | Variation | Physikalischer Effekt | Niveau |
|-----------|-----------|----------------------|--------|
| `active_preset` | NO_LJ ↔ BOTH | Rolle von VdW-Kräften | 🟢 |
| `temperature` | 100 → 600 K | Thermale Fluktuationen, Kollaps | 🟡 |
| `epsilon_lj` | 0.5 → 30 kcal/mol | Stärke des Kollapses | 🟡 |
| `k_bond` | 0 → 300 kcal/(mol·Å²) | Steifheit der Kette | 🟡 |
| `max_displacement` | 0.05 → 0.5 Å | Akzeptanzrate, Ergodizität | 🔴 |
| `n_beads` | 10 → 50 | Kettenlänge, Entropie | 🟡 |

**Lernziele**:

🟢 **Anfänger**:
- Monte Carlo Sampling Prinzip
- Metropolis-Kriterium verstehen
- Polymer-Kollaps durch VdW-Anziehung

🟡 **Fortgeschritten**:
- Akzeptanzrate optimieren (20-40%)
- Coarse-Graining Konzept
- Harmonic bonds vs. LJ competition

🔴 **Experte**:
- Detailed Balance beweisen
- Autocorrelation time analysieren
- Theta-Punkt bestimmen (T_theta)

**LiaScript Übungsvorschläge**:

**Übung 1 (🟢)**: "Rolle der Van-der-Waals-Kräfte"
- Vergleiche Presets: `NO_LJ` vs. `NO_BONDS` vs. `BOTH`
- Beobachte Radius of Gyration R_g
- Frage: Welches Potential sorgt für Kollaps?

**Übung 2 (🟡)**: "Gute vs. schlechte Lösungsmittel"
- `SLOW` Preset mit epsilon_lj: 0.5 (schlechtes LM) → 5.0 (gutes LM)
- Beobachte finalen R_g
- Frage: Wie ändert sich die Polymergröße?

**Übung 3 (🟡)**: "Optimale Schrittweite"
- Variiere `max_displacement`: 0.05 → 0.5 Å
- Beobachte Akzeptanzrate
- Frage: Welche Schrittweite ist optimal (30-40% Akzeptanz)?

**Übung 4 (🔴)**: "Theta-Temperatur"
- Variiere systematisch T bei konstantem epsilon_lj
- Messe R_g vs. T
- Frage: Bei welcher T_theta gilt R_g ∝ N^0.5?

**Empfohlene Ergänzungen**:
- ✅ Echtzeit-Anzeige der Akzeptanzrate
- ✅ End-to-end Distanz zusätzlich zu R_g
- ✅ Autocorrelation Funktion berechnen
- ✅ Preset "THETA_POINT" hinzufügen

---

### 5. metadynamics_visualization.py ⭐⭐⭐⭐⭐ ✨

**Thema**: Metadynamik - Enhanced Sampling für Reaktionspfade

**Konfigurierbare Parameter** (31 Parameter!):
```python
# Doppeltopf-Potential
"barrier_height": 8.0 kcal/mol   # Barrierenhöhe
"well_separation": 2.0 Å         # Abstand der Minima
"well_depth_A": -5.0 kcal/mol    # Tiefe Well A
"well_depth_B": -4.0 kcal/mol    # Tiefe Well B

# Metadynamik
"gaussian_height": 0.2 kcal/mol  # Höhe der Gaussians
"gaussian_width": 0.1 Å          # Breite der Gaussians
"deposition_frequency": 10 steps # Wie oft Gaussian hinzufügen

# Temperatur-Rampen (3 Phasen!)
"phase1_temp_start": 300 K
"phase1_temp_end": 600 K
"phase1_duration": 50 steps

"phase2_temp_start": 600 K
"phase2_temp_end": 300 K
"phase2_duration": 100 steps

"phase3_temp_start": 300 K
"phase3_temp_end": 300 K
"phase3_duration": 150 steps

# Animation
"fps": 30
"slow_motion_factor": 1.0
```

**3 Simulationsphasen mit Temperatur-Rampen**:
1. **Phase 1**: Exploration (300K → 600K) - Hohe T zum Überwinden der Barriere
2. **Phase 2**: Cooldown (600K → 300K) - Abkühlen zur Stabilisierung
3. **Phase 3**: Metadynamics (300K const.) - Gaussians füllen FES auf

**Sinnvolle Parameter-Variationen für Übungen**:

| Parameter | Variation | Physikalischer Effekt | Niveau |
|-----------|-----------|----------------------|--------|
| `barrier_height` | 2 → 20 kcal/mol | Schwierigkeit des Übergangs | 🟢 |
| `gaussian_height` | 0.05 → 0.5 kcal/mol | Geschwindigkeit des FES-Aufbaus | 🟡 |
| `gaussian_width` | 0.05 → 0.3 Å | Auflösung der FES | 🔴 |
| `deposition_frequency` | 5 → 50 steps | Balance Exploration/Exploitation | 🔴 |
| `phase1_temp_end` | 300 → 1000 K | Thermale Aktivierung | 🟡 |
| `well_depth_A` vs `B` | -10/-2 ↔ -2/-10 | Asymmetrie der Wells | 🟡 |

**Lernziele**:

🟢 **Anfänger**:
- Konzept von Free Energy Surfaces (FES)
- Metadynamik als Enhanced Sampling
- Rolle der Temperatur für Barrierenüberwindung

🟡 **Fortgeschritten**:
- Gaussian-Parameter tunen
- Konvergenz der FES beurteilen
- Well-tempered Metadynamik

🔴 **Experte**:
- Multiple Collective Variables (CVs)
- Bias-Potential korrekt interpretieren
- Übergang zu Umbrella Sampling

**LiaScript Übungsvorschläge**:

**Übung 1 (🟢)**: "Niedrige vs. hohe Barriere"
- Variiere `barrier_height`: 4 kcal/mol → 16 kcal/mol
- Beobachte Anzahl erfolgreicher Übergänge
- Frage: Wie oft muss Gaussian deponiert werden bis Übergang?

**Übung 2 (🟡)**: "Temperatur-Rampe optimieren"
- Variiere `phase1_temp_end`: 400K → 800K
- Beobachte Exploration in Phase 1
- Frage: Welche T_max ist optimal für barrier=8 kcal/mol?

**Übung 3 (🟡)**: "Asymmetrische Wells"
- Setze `well_depth_A = -8`, `well_depth_B = -4`
- Beobachte Populationsverteilung
- Frage: Wie lange dauert es Well B zu finden?

**Übung 4 (🔴)**: "Gaussians tunen"
- Finde optimales Verhältnis gaussian_height/barrier_height
- Teste: 0.025, 0.05, 0.1, 0.2 (relativ zu barrier)
- Frage: Ab welchem Ratio ist FES in <200 steps konvergiert?

**Übung 5 (🔴)**: "Deposition Frequency"
- Variiere `deposition_frequency`: 5 → 50 steps
- Messe Zeit bis zur FES-Konvergenz
- Frage: Welche Frequency ist optimal? (Trade-off!)

**Empfohlene Ergänzungen**:
- ✅ Well-tempered Metadynamik (bias-factor Parameter)
- ✅ Anzeige der aktuellen bias-Energie
- ✅ Konvergenzmetrik für FES
- ✅ Option für multiple Collective Variables (2D-FES)

---

### 6. nh3_inversion.py ⭐⭐⭐⭐

**Thema**: NH₃ Umbrella-Inversion durch Doppeltopf-Potential

**Konfigurierbare Parameter** (14 Parameter):
```python
# Doppeltopf-Parameter
"barrier_height": 5.0 kcal/mol   # Inversionbarriere
"well_distance": 1.0 Å           # Asymmetrie
"curvature_a": 200 kcal/(mol·Å²) # Well A Krümmung
"curvature_b": 200 kcal/(mol·Å²) # Well B Krümmung

# Phase Dauer (4 Phasen + Oszillation)
"phase1_steps": 30    # Initiale Ruhe
"phase2_steps": 60    # Annäherung Barriere
"phase3_steps": 40    # Überwindung
"phase4_steps": 60    # Relaxation Well B
"phase5_cycles": 3    # Oszillationen

# Animation
"phase1_wait": 0.1 s
"phase2_wait": 0.08 s
...
```

**Simulationsphasen**:
1. Phase 1: NH₃ in Well A (Ruhe)
2. Phase 2: Annäherung an Barriere
3. Phase 3: Tunneln/Überwindung
4. Phase 4: Relaxation in Well B
5. Phase 5: Oszillationen zwischen Wells

**Sinnvolle Parameter-Variationen für Übungen**:

| Parameter | Variation | Physikalischer Effekt | Niveau |
|-----------|-----------|----------------------|--------|
| `barrier_height` | 1 → 10 kcal/mol | Inversionsfrequenz | 🟢 |
| `well_distance` | 0.0 → 2.0 Å | Symmetrie → Asymmetrie | 🟡 |
| `curvature_a` vs `b` | 100 ↔ 400 | Schwingungsfrequenz in Wells | 🟡 |
| `phase5_cycles` | 1 → 10 | Beobachtungszeit | 🟢 |

**Lernziele**:

🟢 **Anfänger**:
- Umbrella-Inversion als molekulare Bewegung
- Doppeltopf-Potential verstehen
- Barrierenhöhe und Inversionsrate

🟡 **Fortgeschritten**:
- Asymmetrische Doppeltöpfe
- Quantenmechanisches Tunneln bei niedriger T
- NH₃ Chirality (wenn asymmetrisch)

🔴 **Experte**:
- Inversion-Splitting in Spektroskopie
- Semi-classical approximation
- Temperature-dependent rate constant k(T)

**LiaScript Übungsvorschläge**:

**Übung 1 (🟢)**: "Barrierenhöhe und Inversionsrate"
- Variiere `barrier_height`: 2 → 8 kcal/mol
- Zähle Oszillationen in Phase 5
- Frage: Wie ändert sich die Inversionsfrequenz?

**Übung 2 (🟡)**: "Symmetrisches vs. asymmetrisches NH₃"
- Setze `well_distance`: 0.0 (symmetrisch) → 1.5 (asymmetrisch)
- Beobachte Oszillationsamplituden
- Frage: In welchem Well verbringt NH₃ mehr Zeit?

**Übung 3 (🔴)**: "Spektroskopisches Inversion-Splitting"
- Berechne ΔE_splitting = E(antisym) - E(sym) aus barrier_height
- Variiere barrier systematisch
- Frage: Wie hängt ΔE von barrier ab? (exponentiell!)

**Empfohlene Ergänzungen**:
- ✅ Quantenmechanisches Energieniveau-Diagramm
- ✅ Parameter für Masse (N-Isotope)
- ✅ Anzeige der Inversionsfrequenz ν_inv

---

### 7. h3_reaction_pathway.py ⭐⭐⭐⭐

**Thema**: H + H₂ → H₂ + H Reaktionspfad mit Übergangszustand

**Konfigurierbare Parameter** (15 Parameter):
```python
# Reaktionsbarriere
"barrier_height": 9.8 kcal/mol   # Aktivierungsenergie
"reactant_energy": 0.0 kcal/mol  # Edukt-Energie
"product_energy": 0.0 kcal/mol   # Produkt-Energie

# Geometrie
"r_reactant": 2.5 Å              # H...H-H Abstand initial
"r_ts": 0.92 Å                   # Übergangszustand H-H-H
"r_product": 2.5 Å               # H-H...H Abstand final

# Phase Dauer (5 Phasen)
"phase1_steps": 30    # Initiale Config
"phase2_steps": 60    # H₂ approaching
"phase3_steps": 40    # TS Formation
"phase4_steps": 60    # Product Formation
"phase5_steps": 50    # Product Separation

# Animation
"phase1_wait": 0.15 s
"phase2_wait": 0.08 s
...
```

**Simulationsphasen**:
1. Phase 1: H + H₂ weit entfernt
2. Phase 2: H₂ nähert sich H
3. Phase 3: Übergangszustand H-H-H
4. Phase 4: H₂ Produkt bildet sich
5. Phase 5: H₂ + H trennen sich

**Sinnvolle Parameter-Variationen für Übungen**:

| Parameter | Variation | Physikalischer Effekt | Niveau |
|-----------|-----------|----------------------|--------|
| `barrier_height` | 5 → 15 kcal/mol | Reaktionsgeschwindigkeit | 🟢 |
| `reactant_energy` | -5 → +5 kcal/mol | Exotherm ↔ Endotherm | 🟡 |
| `r_ts` | 0.8 → 1.1 Å | Früher/später ÜZ (Hammond) | 🔴 |
| `product_energy` | -10 → +10 kcal/mol | Thermodynamik vs. Kinetik | 🟡 |

**Lernziele**:

🟢 **Anfänger**:
- Reaktionskoordinate verstehen
- Übergangszustand visualisieren
- Aktivierungsenergie E_a

🟡 **Fortgeschritten**:
- Hammond-Postulat (ÜZ ähnelt höherem Energiezustand)
- Exotherme vs. endotherme Reaktionen
- Arrhenius-Gleichung k = A·exp(-E_a/RT)

🔴 **Experte**:
- Transition State Theory
- Marcus-Theorie (wenn ΔG_rxn variiert)
- Bell-Evans-Polanyi Prinzip

**LiaScript Übungsvorschläge**:

**Übung 1 (🟢)**: "Aktivierungsenergie variieren"
- Variiere `barrier_height`: 5 → 15 kcal/mol
- Berechne k(T) mit Arrhenius bei T=300K
- Frage: Um welchen Faktor ändert sich k?

**Übung 2 (🟡)**: "Exotherme vs. endotherme Reaktion"
- Setze `product_energy`: -8 kcal/mol (exotherm) vs. +8 (endotherm)
- Beobachte finalen Zustand
- Frage: Wie ändert sich die Rückreaktion-Barriere?

**Übung 3 (🔴)**: "Hammond-Postulat testen"
- Exotherm (ΔG = -10): Erwarte r_ts < 0.92 Å (früher ÜZ)
- Endotherm (ΔG = +10): Erwarte r_ts > 0.92 Å (später ÜZ)
- Frage: Stimmt die Geometrie mit Hammond?

**Empfohlene Ergänzungen**:
- ✅ Temperatur-Parameter für Arrhenius k(T)
- ✅ Anzeige der Rückreaktion-Barriere
- ✅ Tunneling-Korrektur für leichte Atome (H)

---

### 8. geometry_optimization.py ⭐⭐⭐⭐

**Thema**: Geometrie-Optimierung mit Gradient Descent und BFGS

**Konfigurierbare Parameter**:
```python
"method": "GD"             # GD oder BFGS
"learning_rate": 0.1       # Schrittweite (GD)
"max_iterations": 100      # Max Optimierungsschritte
"convergence_threshold": 0.01  # Konvergenzkriterium
"fps": 30                  # Animation fps
```

**Zwei Methoden**:
1. **GD** (Gradient Descent) - Einfacher, aber langsamer
2. **BFGS** (Broyden-Fletcher-Goldfarb-Shanno) - Quasi-Newton, schneller

**Sinnvolle Parameter-Variationen für Übungen**:

| Parameter | Variation | Effekt | Niveau |
|-----------|-----------|--------|--------|
| `method` | GD ↔ BFGS | Konvergenzgeschwindigkeit | 🟢 |
| `learning_rate` | 0.01 → 0.5 | GD: Oszillation vs. Konvergenz | 🟡 |
| `max_iterations` | 20 → 200 | Beobachtungszeit | 🟢 |
| `convergence_threshold` | 0.001 → 0.1 | Genauigkeit | 🟡 |

**Lernziele**:

🟢 **Anfänger**:
- Konzept der Optimierung verstehen
- Gradient Descent Prinzip
- Konvergenz vs. Oszillation

🟡 **Fortgeschritten**:
- Learning rate tuning
- Quasi-Newton vs. first-order methods
- BFGS Update-Formel

🔴 **Experte**:
- Hessian-Approximation in BFGS
- Line search vs. trust region
- Saddle points und second-order optimization

**LiaScript Übungsvorschläge**:

**Übung 1 (🟢)**: "GD vs. BFGS"
- Vergleiche beide Methoden bei gleichen Startbedingungen
- Zähle Iterationen bis Konvergenz
- Frage: Um welchen Faktor ist BFGS schneller?

**Übung 2 (🟡)**: "Learning Rate tuning"
- GD mit learning_rate: 0.01 (zu klein), 0.1 (gut), 0.4 (zu groß)
- Beobachte Oszillationen
- Frage: Welche LR ist optimal? Warum oszilliert 0.4?

**Übung 3 (🔴)**: "Konvergenz-Kriterien"
- Variiere `convergence_threshold`: 0.001 → 0.1
- Messe finale Energie und Gradienten-Norm
- Frage: Welches Kriterium ist sinnvoll für Chemie?

**Empfohlene Ergänzungen**:
- ✅ Anzeige der Gradienten-Norm |∇E|
- ✅ Energy vs. Iteration Plot
- ✅ Line Search Parameter (Armijo, Wolfe)
- ✅ Mehr Optimierungsalgorithmen (L-BFGS, CG)

---

### 9. polarization_forcefield.py ⭐⭐⭐⭐

**Thema**: Vergleich Fixed vs. Polarizable Forcefields in MD

**Konfigurierbare Parameter** (15 Parameter):
```python
# Fixed Forcefield
"fixed_charge": 1.0 e     # Feste Ladung
"fixed_dipole": 2.0 D     # Festes Dipolmoment

# Polarizable Forcefield
"polarizability": 1.5 Å³  # Polarisierbarkeit α
"damping_factor": 0.5     # Dämpfung

# MD Simulation
"n_atoms": 20             # Anzahl Atome
"temperature": 300 K      # Temperatur
"dt": 0.001 ps            # Zeitschritt
"box_size": 15.0 Å        # Box

# Animation
"total_time": 10.0 s
"fps": 30
```

**Vergleich**: Zwei parallele Simulationen (Fixed links, Polarizable rechts)

**Sinnvolle Parameter-Variationen für Übungen**:

| Parameter | Variation | Physikalischer Effekt | Niveau |
|-----------|-----------|----------------------|--------|
| `polarizability` | 0.5 → 3.0 Å³ | Stärke der Rückkopplung | 🟡 |
| `temperature` | 100 → 600 K | Thermale Effekte | 🟢 |
| `damping_factor` | 0.1 → 0.9 | Oszillation vs. Dämpfung | 🔴 |
| `n_atoms` | 10 → 50 | Many-body Polarization | 🟡 |

**Lernziele**:

🟢 **Anfänger**:
- Fixed vs. polarizable Forcefields
- Induzierte Dipole verstehen
- Warum polarizable genauer ist

🟡 **Fortgeschritten**:
- Self-consistent Field (SCF) für Dipole
- Computational Cost: O(N) vs. O(N³)
- Wann ist polarizable notwendig?

🔴 **Experte**:
- Drude oscillator model
- AMOEBA Forcefield
- QM/MM Hybrid-Ansätze

**LiaScript Übungsvorschläge**:

**Übung 1 (🟢)**: "Fixed vs. Polarizable"
- Vergleiche beide Simulationen visuell
- Beobachte Clusterbildung
- Frage: Welches System zeigt mehr Struktur?

**Übung 2 (🟡)**: "Polarisierbarkeit variieren"
- Polarizable FF mit α: 0.5 → 2.5 Å³
- Beobachte induzierte Dipole
- Frage: Ab welchem α weicht Verhalten stark ab?

**Übung 3 (🔴)**: "Computational Cost"
- Messe Rechenzeit bei n_atoms: 10 → 50
- Vergleiche Fixed (linear) vs. Polarizable (cubic?)
- Frage: Wie skaliert die Zeit? (Hinweis: SCF-Iterationen)

**Empfohlene Ergänzungen**:
- ✅ Anzeige der SCF-Iterationen pro Schritt
- ✅ Energiedifferenz Fixed vs. Polarizable
- ✅ Visualisierung der induzierten Dipole (Pfeile)

---

### 10. polymer_sampling_comparison.py ⭐⭐⭐⭐

**Thema**: Vergleich von 4 Sampling-Methoden (MC, NAIVE, MD, OPT)

**Konfigurierbare Parameter**:
```python
"sampling_method": "MC"    # MC, NAIVE, MD, OPT
"initial_config": "LINEAR"  # LINEAR oder RANDOM
"n_steps": 40000           # Sampling-Schritte

# Gemeinsame Physik
"n_beads": 20              # Polymer-Länge
"k_bond": 0.0              # Harmonische Bindungen
"epsilon_lj": 0.0          # Lennard-Jones
"sigma_lj": 2.5 Å          # LJ-Größe

# MC-spezifisch
"mc_temperature": 300 K
"mc_max_displacement": 0.2 Å

# NAIVE-spezifisch
"naive_perturbation_strength": 0.3 Å
"naive_opt_max_steps": 50

# MD-spezifisch
"md_dt": 0.0001 ps
"md_temperature": 300 K
"md_berendsen_tau": 0.1 ps

# OPT-spezifisch
"opt_max_steps": 500
"opt_alpha_init": 0.05 Å
```

**4 Methoden im Vergleich**:
1. **MC** - Metropolis Monte Carlo
2. **NAIVE** - Random Perturbation + Gradient Descent
3. **MD** - Molecular Dynamics mit Berendsen Thermostat
4. **OPT** - Pure Gradient Descent

**Sinnvolle Parameter-Variationen für Übungen**:

| Parameter | Variation | Effekt | Niveau |
|-----------|-----------|--------|--------|
| `sampling_method` | MC/NAIVE/MD/OPT | Konvergenzverhalten | 🟢 |
| `initial_config` | LINEAR vs. RANDOM | Startbedingung | 🟢 |
| `k_bond` + `epsilon_lj` | 0/0 → 30/5 | Potentiale aktivieren | 🟡 |
| `mc_max_displacement` | 0.05 → 0.5 Å | MC Akzeptanzrate | 🔴 |
| `md_dt` | 0.00001 → 0.001 ps | MD Stabilität | 🔴 |

**Lernziele**:

🟢 **Anfänger**:
- Unterschiede: Stochastisch vs. Deterministisch
- Monte Carlo Konzept
- Molecular Dynamics Basics

🟡 **Fortgeschritten**:
- Sampling Efficiency vergleichen
- Ergodicity und Equilibration
- Thermostat-Algorithmen (Berendsen)

🔴 **Experte**:
- Detailed Balance (MC)
- Symplektische Integratoren (MD)
- Convergence Diagnostics (Autocorrelation)

**LiaScript Übungsvorschläge**:

**Übung 1 (🟢)**: "Vier Methoden vergleichen"
- Führe alle 4 aus mit gleichen Parametern
- Beobachte R_g vs. Time
- Frage: Welche Methode konvergiert am schnellsten?

**Übung 2 (🟡)**: "LINEAR vs. RANDOM Start"
- MC mit initial_config: LINEAR vs. RANDOM
- Vergleiche Equilibration Time
- Frage: Welcher Start ist "schwieriger"?

**Übung 3 (🔴)**: "MD Zeitschritt optimieren"
- Variiere md_dt: 0.00001 → 0.001 ps
- Beobachte Energieerhaltung
- Frage: Welches dt ist maximal stabil?

**Übung 4 (🔴)**: "MC Schrittweite tunen"
- Variiere mc_max_displacement: 0.05 → 0.5 Å
- Messe Autocorrelation Time
- Frage: Welche Schrittweite ist effizienteste?

**Empfohlene Ergänzungen**:
- ✅ Autocorrelation Function anzeigen
- ✅ Accepted/Total Moves für MC
- ✅ Temperature vs. Time für MD
- ✅ Convergence Metrik (z.B. R_g Varianz)

---

### 11. angle_bending.py ⭐⭐⭐

**Thema**: Winkelpotentiale (Harmonisch vs. Cosinus)

**Konfigurierbare Parameter**:
```python
"k_theta": 100 kcal/(mol·rad²)  # Harmonische Federkonstante
"theta_0": 109.5°                # Gleichgewichtswinkel
"amplitude": 20.0°               # Oszillationsamplitude
"oscillation_cycles": 3          # Anzahl Schwingungen
"fps": 30
```

**Sinnvolle Parameter-Variationen für Übungen**:

| Parameter | Variation | Physikalischer Effekt | Niveau |
|-----------|-----------|----------------------|--------|
| `theta_0` | 90° → 180° | sp³, sp², sp Hybridisierung | 🟢 |
| `k_theta` | 50 → 300 kcal/(mol·rad²) | Steifheit der Winkelbiegung | 🟡 |
| `amplitude` | 5° → 40° | Harmonisch → Anharmonisch | 🟢 |

**Lernziele**:

🟢 **Anfänger**:
- Winkel-Potentiale in Kraftfeldern
- Gleichgewichtswinkel θ₀ verstehen
- Unterschied harmonisch vs. cosinus

🟡 **Fortgeschritten**:
- Anharmonizität bei großen Auslenkungen
- Vergleich mit Torsionswinkel
- Energieskalen von Winkelbiegung

🔴 **Experte**:
- Cross-terms (Urey-Bradley)
- AMOEBA-Winkel-Terme
- Quantisierung der Biegeschwingung

**LiaScript Übungsvorschläge**:

**Übung 1 (🟢)**: "Hybridisierung erkennen"
- Variiere θ₀: 109.5° (sp³), 120° (sp²), 180° (sp)
- Beobachte Molekülform
- Frage: Welche Hybridisierung bei welchem Winkel?

**Übung 2 (🟡)**: "Steife vs. weiche Winkel"
- Variiere k_theta: 50 → 300 kcal/(mol·rad²)
- Beobachte Oszillationsfrequenz
- Frage: Wie hängt ω von k_theta ab?

**Empfohlene Ergänzungen**:
- ✅ Cosinus-Potential zum Vergleich
- ✅ Urey-Bradley cross-term

---

### 12. torsion_angle_optimized.py ⭐⭐⭐

**Thema**: Torsionswinkel-Potential (Dihedral Angles)

**Konfigurierbare Parameter**:
```python
"V_n": [2.0, 1.5, 0.5] kcal/mol  # Fourier-Koeffizienten
"n": [1, 2, 3]                   # Periodizität
"gamma": [0°, 180°, 0°]          # Phase
"rotation_cycles": 2             # Vollrotationen
"fps": 30
```

**Sinnvolle Parameter-Variationen für Übungen**:

| Parameter | Variation | Physikalischer Effekt | Niveau |
|-----------|-----------|----------------------|--------|
| `V_n[0]` (V₁) | 0 → 5 kcal/mol | Barriere zwischen staggered/eclipsed | 🟢 |
| `V_n[1]` (V₂) | 0 → 3 kcal/mol | Preferenz trans vs. gauche | 🟡 |
| `rotation_cycles` | 1 → 4 | Beobachtungszeit | 🟢 |

**Lernziele**:

🟢 **Anfänger**:
- Torsionswinkel in Molekülen
- Eclipsed vs. staggered
- Rotationsbarrieren

🟡 **Fortgeschritten**:
- Fourier-Entwicklung V(φ) = Σ V_n·[1+cos(n·φ-γ)]
- Trans/gauche Isomere
- n-fold Symmetrie

🔴 **Experte**:
- Elektronische Ursache der Barrieren
- Hyperkonjugation (Ethan)
- Coupled torsions

**LiaScript Übungsvorschläge**:

**Übung 1 (🟢)**: "Ethan-Rotation"
- V₁=0, V₂=0, V₃=2.9 kcal/mol (realistisch)
- Vollrotation beobachten
- Frage: Wie viele Minima/Maxima pro 360°?

**Übung 2 (🟡)**: "Fourier-Term isolieren"
- V₁=2.0, V₂=0, V₃=0 (nur n=1)
- Dann V₁=0, V₂=2.0, V₃=0 (nur n=2)
- Frage: Wie ändert sich die Periodizität?

**Empfohlene Ergänzungen**:
- ✅ Mehr Fourier-Terms (n=4,5,6)
- ✅ Coupled torsions (2D-Surface)

---

### 13. nonbonded_interactions.py ⭐⭐⭐

**Thema**: Lennard-Jones Potential (Van-der-Waals)

**Konfigurierbare Parameter**:
```python
"epsilon": 0.238 kcal/mol   # LJ Tiefe
"sigma": 3.4 Å              # LJ Null-Crossing
"r_start": 7.0 Å            # Startabstand
"r_end": 2.5 Å              # Endabstand
"approach_duration": 5.0 s  # Annäherungsdauer
"fps": 30
```

**Sinnvolle Parameter-Variationen für Übungen**:

| Parameter | Variation | Physikalischer Effekt | Niveau |
|-----------|-----------|----------------------|--------|
| `epsilon` | 0.05 → 1.0 kcal/mol | Stärke der Anziehung | 🟢 |
| `sigma` | 2.5 → 4.5 Å | Atomgröße | 🟡 |
| `r_start` / `r_end` | Verschiedene Trajektorien | Repulsion/Attraction Balance | 🟡 |

**Lernziele**:

🟢 **Anfänger**:
- LJ-Potential V(r) = 4ε[(σ/r)¹² - (σ/r)⁶]
- Abstoßung vs. Anziehung
- Van-der-Waals Minimum

🟡 **Fortgeschritten**:
- Combining rules (Lorentz-Berthelot)
- Cutoff vs. Truncated & Shifted
- LJ als Coarse-Graining

🔴 **Experte**:
- Mie-Potential (m-n statt 12-6)
- Buckingham Potential
- Dispersion + Exchange-Repulsion

**LiaScript Übungsvorschläge**:

**Übung 1 (🟢)**: "Gleichgewichtsabstand"
- Variiere sigma: 3.0 → 4.0 Å
- Lese r_min ab (wo V minimal)
- Frage: Gilt r_min = 2^(1/6)·σ? Berechne!

**Übung 2 (🟡)**: "Schwache vs. starke VdW"
- Variiere epsilon: 0.1 → 0.5 kcal/mol
- Beobachte Potentialtiefe
- Frage: Wie ändert sich die "Bindungsstärke"?

**Empfohlene Ergänzungen**:
- ✅ Buckingham-Potential Option
- ✅ Combining Rules visualisieren

---

### 14. variational_method.py ⭐⭐⭐

**Thema**: Variationsmethode für Harmonischen Oszillator

**Konfigurierbare Parameter**:
```python
"alpha_start": 0.5     # Initiale Variationsparameter
"alpha_end": 2.0       # Finale Variationsparameter
"n_steps": 50          # Optimierungsschritte
"omega": 1.0           # Oszillator-Frequenz
"duration": 10.0 s     # Animation
"fps": 30
```

**Sinnvolle Parameter-Variationen für Übungen**:

| Parameter | Variation | Physikalischer Effekt | Niveau |
|-----------|-----------|----------------------|--------|
| `alpha_start` | 0.1 → 3.0 | Startpunkt im Parameter-Raum | 🟡 |
| `omega` | 0.5 → 2.0 | Oszillator-Frequenz | 🟡 |
| `n_steps` | 20 → 100 | Konvergenzgeschwindigkeit | 🟢 |

**Lernziele**:

🟢 **Anfänger**:
- Variationsprinzip E[ψ] ≥ E₀
- Trial Wavefunction ψ_trial
- Parameter-Optimierung

🟡 **Fortgeschritten**:
- Gaussche Wellenfunktionen
- Variational Monte Carlo
- Basis-Set-Konvergenz

🔴 **Experte**:
- Ritz-Variationsprinzip
- Multi-configurational Ansatz
- Size-Consistency

**LiaScript Übungsvorschläge**:

**Übung 1 (🟢)**: "Konvergenz zum Grundzustand"
- Starte mit alpha_start = 0.2 (schlecht)
- Beobachte Optimierung
- Frage: Was ist finale Energie? Vergleiche mit E₀ = ½ℏω

**Übung 2 (🟡)**: "Verschiedene Startpunkte"
- Variiere alpha_start: 0.1, 0.5, 1.0, 2.0
- Beobachte Konvergenz
- Frage: Konvergieren alle zum gleichen Minimum?

**Empfohlene Ergänzungen**:
- ✅ Mehrere Variationsparameter
- ✅ Excited States (orthogonalisiert)

---

### 15. monte_carlo_pi.py ⭐⭐⭐

**Thema**: Monte Carlo Integration (π berechnen)

**Konfigurierbare Parameter**:
```python
"n_samples": 1000      # Anzahl MC-Samples
"animation_speed": 0.01 s  # Delay pro Sample
"show_estimate": True  # π-Schätzung anzeigen
"fps": 30
```

**Sinnvolle Parameter-Variationen für Übungen**:

| Parameter | Variation | Effekt | Niveau |
|-----------|-----------|--------|--------|
| `n_samples` | 100 → 10000 | Konvergenz von π | 🟢 |
| `animation_speed` | 0.001 → 0.1 s | Visualisierungsgeschwindigkeit | 🟢 |

**Lernziele**:

🟢 **Anfänger**:
- Monte Carlo Prinzip
- Law of Large Numbers
- Fehler ∝ 1/√N

🟡 **Fortgeschritten**:
- Importance Sampling
- Variance Reduction
- Quasi-Monte Carlo

🔴 **Experte**:
- Markov Chain Monte Carlo
- Metropolis-Hastings
- Detailed Balance

**LiaScript Übungsvorschläge**:

**Übung 1 (🟢)**: "Konvergenz beobachten"
- Variiere n_samples: 100 → 5000
- Beobachte π-Schätzung
- Frage: Ab welchem N ist Fehler < 1%?

**Übung 2 (🟡)**: "Fehlerabschätzung"
- Wiederhole mit n_samples = 1000 mehrfach
- Berechne Standardabweichung
- Frage: Gilt σ ∝ 1/√N?

**Empfohlene Ergänzungen**:
- ✅ Fehlerbalken anzeigen
- ✅ Konvergenz-Plot (N vs. π_est)

---

### 16. metropolis_animation.py ⭐⭐

**Thema**: Metropolis-Algorithmus (Didaktisch fixiert)

**Konfigurierbare Parameter**:
```python
"n_steps": 50          # MC-Schritte (didaktisch fixiert)
"temperature": 300 K   # Temperatur
"step_delay": 1.0 s    # Zeit pro Schritt (didaktisch)
```

**Hinweis**: Diese Animation ist **didaktisch optimiert** mit festen Timings für langsame Erklärung. Parameter-Variation weniger sinnvoll.

**Lernziele**:

🟢 **Anfänger**:
- Metropolis-Kriterium verstehen
- Accept/Reject Entscheidung
- Boltzmann-Faktor exp(-ΔE/kT)

**LiaScript Übungsvorschläge**:

**Übung 1 (🟢)**: "Akzeptanzrate vs. Temperatur"
- Variiere temperature: 100 → 600 K
- Zähle Akzeptierte/Abgelehnte
- Frage: Bei welcher T ist Akzeptanzrate am höchsten?

**Empfohlene Ergänzungen**:
- ✅ Parametrisierbare Timings (trotz didaktischem Fokus)

---

### 17. particle_interactions_combinatorics.py ⭐⭐

**Thema**: Kombinatorik von Teilchen-Wechselwirkungen

**Konfigurierbare Parameter**:
```python
"n_particles": 5       # Anzahl Teilchen
"show_all_pairs": True # Alle Paare zeigen
"delay_per_pair": 0.5 s  # Zeit pro Paar-Visualisierung
```

**Hinweis**: Mehr ein kombinatorisches/didaktisches Tool als physikalische Simulation.

**Lernziele**:

🟢 **Anfänger**:
- N(N-1)/2 Paare bei N Teilchen
- Kombinatorik verstehen
- Computational Complexity

🟡 **Fortgeschritten**:
- Cutoff-Strategien (Verlet-Listen)
- Cell-Lists und Neighbor-Lists
- O(N²) → O(N)

**LiaScript Übungsvorschläge**:

**Übung 1 (🟢)**: "Paar-Anzahl berechnen"
- Variiere n_particles: 3 → 10
- Zähle gezeigte Paare
- Frage: Bestätige Formel N(N-1)/2

**Übung 2 (🟡)**: "Computational Cost"
- Berechne für N=100, 1000, 10000
- Frage: Warum brauchen wir Cutoffs?

**Empfohlene Ergänzungen**:
- ✅ Verlet-Listen Visualisierung
- ✅ Cell-Decomposition zeigen

---

### 18. pca_molecular_dynamics.py ⭐⭐

**Thema**: Principal Component Analysis für MD-Trajektorien

**Konfigurierbare Parameter**:
```python
"n_atoms": 10          # Anzahl Atome
"n_frames": 100        # Trajektorien-Länge
"temperature": 300 K   # MD-Temperatur
"dt": 0.001 ps         # Zeitschritt
"fps": 30
```

**Hinweis**: Spezialisiert auf PCA-Konzept, weniger auf Physik-Variation.

**Lernziele**:

🟢 **Anfänger**:
- PCA als Dimensionsreduktion
- Hauptkomponenten verstehen
- Variance Explained

🟡 **Fortgeschritten**:
- Covariance Matrix
- Essential Dynamics
- Collective Variables aus PCA

🔴 **Experte**:
- Kernel PCA für Nonlinear Manifolds
- Time-lagged PCA
- Markov State Models

**LiaScript Übungsvorschläge**:

**Übung 1 (🟢)**: "Hauptkomponenten"
- Beobachte PC1, PC2
- Frage: Wieviel Varianz erklärt PC1?

**Übung 2 (🟡)**: "Temperatur-Effekt"
- Variiere temperature: 100 → 500 K
- Beobachte Varianz
- Frage: Wie ändert sich die Amplitude von PC1?

**Empfohlene Ergänzungen**:
- ✅ Scree Plot (Varianz vs. PC)
- ✅ 2D Projektion (PC1 vs. PC2)

---

### 19. quantum_nonlocality.py ⭐⭐

**Thema**: Quantenkorrelationen und Bell-Ungleichung

**Konfigurierbare Parameter**:
```python
"n_measurements": 100  # Anzahl Messungen
"entanglement_strength": 1.0  # Verschränkungsstärke
"detector_angle_a": 0°     # Alice Detektor
"detector_angle_b": 45°    # Bob Detektor
```

**Hinweis**: Mehr Quanteninformations-Theorie als Chemie.

**Lernziele**:

🟢 **Anfänger**:
- Quantenverschränkung
- EPR-Paradoxon
- Nichtlokalität

🟡 **Fortgeschritten**:
- Bell-Ungleichung S ≤ 2
- CHSH-Test
- Quantenkorrelationen vs. klassisch

🔴 **Experte**:
- Loopholes (Detection, Locality)
- GHZ-Zustände
- Quantum Key Distribution

**LiaScript Übungsvorschläge**:

**Übung 1 (🟢)**: "Bell-Test"
- Variiere detector_angle_b: 0°, 22.5°, 45°, 67.5°
- Berechne S-Parameter
- Frage: Ist S > 2? (Quantenkorrelation!)

**Übung 2 (🔴)**: "Maximale Verletzung"
- Finde optimale Winkel für max. S
- Theoretisch: S_max = 2√2 ≈ 2.83
- Frage: Welche Winkel erreichen S_max?

**Empfohlene Ergänzungen**:
- ✅ S-Parameter live berechnen
- ✅ Klassische Grenze (S=2) markieren

---

## 🎯 Zusammenfassung: Top 10 Empfehlungen

### ⭐⭐⭐⭐⭐ Höchste Priorität

1. **bond_stretching.py** - Perfekt für harmonisch/Morse Vergleich
2. **quantum_dynamics_manim.py** - 5 Szenarien, reich an Quanteneffekten
3. **h2_md_full_refactored.py** - Vollständiger MD-Workflow, 5 Phasen
4. **polymer_monte_carlo.py** - 8 Presets, ideal für MC-Lernen
5. **metadynamics_visualization.py** - Advanced Sampling, 31 Parameter!

### ⭐⭐⭐⭐ Hohe Priorität

6. **nh3_inversion.py** - Klassisches Tunneling-Beispiel
7. **h3_reaction_pathway.py** - Transition State Theory
8. **geometry_optimization.py** - Algorithmen-Vergleich
9. **polarization_forcefield.py** - Forcefield-Vergleich
10. **polymer_sampling_comparison.py** - 4 Methoden-Vergleich

---

## 📝 Nächste Schritte

1. ✅ Für Top 5 detaillierte LiaScript-Templates erstellen
2. ⏸ Interaktive Slider für Parameter implementieren
3. ⏸ Quiz-Fragen mit automatischer Bewertung
4. ⏸ Erweiterte Parametrierung wo sinnvoll

---

**Erstellt**: 2025-11-08
**Dateien analysiert**: 19/19
**Übungsszenarien identifiziert**: 40+
