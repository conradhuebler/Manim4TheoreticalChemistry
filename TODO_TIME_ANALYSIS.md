# 🔍 Zeit/FPS/Phasenlängen-Parameter Analyse

**Datum:** 2025-11-06
**Ziel:** Identifizierung aller hardcodierten Zeitparameter, FPS-Werte, wait()-Calls, und Phasenlängen für potenzielle Konfigurierbarkeit.

---

## ✅ Dateien MIT konfigurierbaren Zeit-Parametern

| Datei | Zeit-Parameter | Status |
|-------|---------------|--------|
| `bond_stretching.py` | `duration`, `fps` | ✅ Vollständig konfigurierbar |
| `angle_bending.py` | `duration`, `fps` | ✅ Vollständig konfigurierbar |
| `torsion_angle_optimized.py` | `duration`, `fps` | ✅ Vollständig konfigurierbar |
| `nonbonded_interactions.py` | `duration`, `fps` | ✅ Vollständig konfigurierbar |
| `quantum_dynamics_manim.py` | `duration` (per scenario), `fps` | ✅ Vollständig konfigurierbar |
| `metadynamics_visualization.py` | `phase0-4_steps`, `morph_steps`, `temp_*` | ✅ Vollständig konfigurierbar (NEU 2025-11-06!) |

---

## ⚠️ Dateien MIT hardcodierten Zeitwerten

### **Forcefield Animation Series**

#### `nh3_inversion.py` (5 Parameter, KEINE Zeit-Konfiguration)
**Zeilen mit hardcodierten Werten:**
- Zeile 407: `for step in range(60)` - Phase 1 (Approaching transition state)
- Zeile 435: `for step in range(40)` - Phase 2 (Transition state)
- Zeile 463: `for step in range(60)` - Phase 3 (Inversion complete)
- Zeile 494-514: `for cycle in range(3)` - 3 Inversionszyklen
  - Zeile 496: `for step in range(80)` - Cycle up
  - Zeile 514: `for step in range(80)` - Cycle down
- Zeile 422, 450, 478: `self.wait(0.05)`
- Zeile 511, 529: `self.wait(0.03)`

**💡 Empfehlung:** Füge 6 neue Parameter hinzu:
```python
"inversion_cycles": {
    "value": 3,
    "type": int,
    "unit": "-",
    "description": "Number of inversion cycles to animate",
    "min": 1,
    "max": 10
},
"phase1_steps": {
    "value": 60,
    "type": int,
    "unit": "steps",
    "description": "Phase 1: Approaching transition state",
    "min": 20,
    "max": 200
},
"phase2_steps": {
    "value": 40,
    "type": int,
    "unit": "steps",
    "description": "Phase 2: At transition state",
    "min": 10,
    "max": 100
},
"phase3_steps": {
    "value": 60,
    "type": int,
    "unit": "steps",
    "description": "Phase 3: Inversion complete",
    "min": 20,
    "max": 200
},
"cycle_up_steps": {
    "value": 80,
    "type": int,
    "unit": "steps",
    "description": "Cycling animation: upward movement",
    "min": 20,
    "max": 200
},
"cycle_down_steps": {
    "value": 80,
    "type": int,
    "unit": "steps",
    "description": "Cycling animation: downward movement",
    "min": 20,
    "max": 200
},
"animation_wait_fast": {
    "value": 0.03,
    "type": float,
    "unit": "s",
    "description": "Wait time for fast animation phases",
    "min": 0.001,
    "max": 0.1
},
"animation_wait_slow": {
    "value": 0.05,
    "type": float,
    "unit": "s",
    "description": "Wait time for slower animation phases",
    "min": 0.001,
    "max": 0.2
}
```

---

### **Monte Carlo & Sampling**

#### `monte_carlo_pi.py` (6 Parameter, TEILWEISE Zeit-Konfiguration)
- ✅ Hat bereits `animation_speed` Parameter (line 126)
- ❌ Hardcodierte wait() calls: `wait(0.5)`, `wait(1)`, `wait(2)`, `wait(3)`
- **Status:** animation_speed wird bereits für batch processing verwendet
- **💡 Empfehlung:** Wait() calls sind für didaktische Pausen OK (Scene-Übergänge)

---

#### `metropolis_animation.py` (2/3 Parameter, KEINE Zeit-Konfiguration)
**Zeilen mit hardcodierten Werten:**
- Zeile 252: `run_time=8` (langer Plot-Aufbau)
- Viele wait() calls: 0.4, 0.5, 0.8, 1.0, 1.5, 2, 3, 4.5

**💡 Empfehlung:** Füge 1 Parameter hinzu:
```python
"animation_speed_factor": {
    "value": 1.0,
    "type": float,
    "unit": "-",
    "description": "Multiplier for all animation timings (wait/run_time)",
    "min": 0.1,
    "max": 5.0
}
```
Dann alle `wait(x)` → `wait(x * self.animation_speed_factor)`

---

#### `polymer_monte_carlo.py` (2 Parameter, KEINE Zeit-Konfiguration)
**Zeilen mit hardcodierten Werten:**
- Zeile 928: `for i in range(10)` - Initial display steps
- Zeile 960: `for step_count in range(80)` - Warmup steps
- Zeile 969: `self.wait(0.02)` - Warmup animation
- Zeile 939, 949: `self.wait(3.5)` - Preset comparison pause
- Zeile 988: `self.wait(0.0001)` - Fast simulation

**💡 Empfehlung:** Füge 5 neue Parameter hinzu:
```python
"init_display_steps": {
    "value": 10,
    "type": int,
    "unit": "steps",
    "description": "Initial display steps before simulation",
    "min": 1,
    "max": 50
},
"warmup_steps": {
    "value": 80,
    "type": int,
    "unit": "steps",
    "description": "Warmup/equilibration steps",
    "min": 10,
    "max": 500
},
"animation_wait_warmup": {
    "value": 0.02,
    "type": float,
    "unit": "s",
    "description": "Wait time during warmup",
    "min": 0.001,
    "max": 0.1
},
"animation_wait_pause": {
    "value": 3.5,
    "type": float,
    "unit": "s",
    "description": "Pause between preset comparisons",
    "min": 0.5,
    "max": 10.0
},
"animation_wait_simulation": {
    "value": 0.0001,
    "type": float,
    "unit": "s",
    "description": "Wait time during fast simulation",
    "min": 0.0,
    "max": 0.01
}
```

---

#### `polymer_sampling_comparison.py` (29 Parameter, KEINE Zeit-Konfiguration)
**Zeilen mit hardcodierten Werten:**
- Zeilen 932, 1006, 1087, 1145: `self.wait(0.001)` (alle 4 Methoden)

**💡 Empfehlung:** Füge 1 Parameter hinzu:
```python
"animation_wait": {
    "value": 0.001,
    "type": float,
    "unit": "s",
    "description": "Wait time between simulation frames",
    "min": 0.0,
    "max": 0.1
}
```

---

### **Molecular Dynamics & Quantum**

#### `h2_md_full_refactored.py` (14 Parameter, KEINE Zeit-Konfiguration)
**Zeilen mit hardcodierten Werten:**

**Phasenlängen:**
- Zeile 735: `for step in range(200)` - Phase 1 (heating) ≈ 20 fs
- Zeile 794: `for step in range(800)` - Phase 2 (dissociation) ≈ 150 fs
- Zeile 948: `for step in range(200)` - Phase 3 (cooling)
- Zeile 1035: `for step in range(200)` - Phase 4 (equilibration)
- Zeile 1114: `for step in range(200)` - Phase 5 (second dissociation)

**Animation wait times:**
- Zeile 763: `wait(0.004)` - Phase 1
- Zeile 844: `wait(0.001)` - Phase 2
- Zeile 1004: `wait(0.02)` - Phase 3
- Zeile 1091: `wait(0.02)` - Phase 4
- Zeile 1173: `wait(0.005)` - Phase 5

**💡 Empfehlung:** Füge 10 neue Parameter hinzu (analog zu metadynamics):
```python
"phase1_steps": {
    "value": 200,
    "type": int,
    "unit": "steps",
    "description": "Phase 1 duration: Heating (~20 fs)",
    "min": 50,
    "max": 1000
},
"phase2_steps": {
    "value": 800,
    "type": int,
    "unit": "steps",
    "description": "Phase 2 duration: Dissociation (~150 fs)",
    "min": 200,
    "max": 3000
},
"phase3_steps": {
    "value": 200,
    "type": int,
    "unit": "steps",
    "description": "Phase 3 duration: Cooling",
    "min": 50,
    "max": 1000
},
"phase4_steps": {
    "value": 200,
    "type": int,
    "unit": "steps",
    "description": "Phase 4 duration: Equilibration",
    "min": 50,
    "max": 1000
},
"phase5_steps": {
    "value": 200,
    "type": int,
    "unit": "steps",
    "description": "Phase 5 duration: Second dissociation",
    "min": 50,
    "max": 1000
},
"animation_wait_phase1": {
    "value": 0.004,
    "type": float,
    "unit": "s",
    "description": "Animation wait time for Phase 1",
    "min": 0.0,
    "max": 0.1
},
"animation_wait_phase2": {
    "value": 0.001,
    "type": float,
    "unit": "s",
    "description": "Animation wait time for Phase 2",
    "min": 0.0,
    "max": 0.1
},
"animation_wait_phase3": {
    "value": 0.02,
    "type": float,
    "unit": "s",
    "description": "Animation wait time for Phase 3",
    "min": 0.0,
    "max": 0.1
},
"animation_wait_phase4": {
    "value": 0.02,
    "type": float,
    "unit": "s",
    "description": "Animation wait time for Phase 4",
    "min": 0.0,
    "max": 0.1
},
"animation_wait_phase5": {
    "value": 0.005,
    "type": float,
    "unit": "s",
    "description": "Animation wait time for Phase 5",
    "min": 0.0,
    "max": 0.1
}
```

---

#### `h3_reaction_pathway.py` (9 Parameter, KEINE Zeit-Konfiguration)
**Zeilen mit hardcodierten Werten:**
- Zeile 620: `for step in range(60)` - Phase 1
- Zeile 653: `for step in range(40)` - Phase 2
- Zeile 684: `for step in range(60)` - Phase 3
- Zeile 644: `wait(0.08)` - Phase 1
- Zeile 672: `wait(0.1)` - Phase 2
- Zeile 704: `wait(0.08)` - Phase 3

**💡 Empfehlung:** Füge 6 neue Parameter hinzu:
```python
"phase1_steps": {
    "value": 60,
    "type": int,
    "unit": "steps",
    "description": "Phase 1: H2 approaching",
    "min": 20,
    "max": 200
},
"phase2_steps": {
    "value": 40,
    "type": int,
    "unit": "steps",
    "description": "Phase 2: Transition state",
    "min": 10,
    "max": 200
},
"phase3_steps": {
    "value": 60,
    "type": int,
    "unit": "steps",
    "description": "Phase 3: Product formation",
    "min": 20,
    "max": 200
},
"animation_wait_phase1": {
    "value": 0.08,
    "type": float,
    "unit": "s",
    "description": "Wait time for Phase 1 animation",
    "min": 0.0,
    "max": 0.3
},
"animation_wait_phase2": {
    "value": 0.1,
    "type": float,
    "unit": "s",
    "description": "Wait time for Phase 2 animation",
    "min": 0.0,
    "max": 0.3
},
"animation_wait_phase3": {
    "value": 0.08,
    "type": float,
    "unit": "s",
    "description": "Wait time for Phase 3 animation",
    "min": 0.0,
    "max": 0.3
}
```

---

#### `geometry_optimization.py` (9 Parameter, KEINE Zeit-Konfiguration)
**Zeilen mit hardcodierten Werten:**
- Zeile 345: `self.wait(10)` - Sehr lange Pause (wahrscheinlich für manuelle Eingabe/Prüfung)
- Viele wait() calls: 0.2, 0.3, 0.5, 1.5, 2
- run_time values: 0.3, 0.4, 0.5

**💡 Empfehlung:** Füge 2 Parameter hinzu:
```python
"manual_input_wait": {
    "value": 10.0,
    "type": float,
    "unit": "s",
    "description": "Wait time for manual user input/inspection",
    "min": 0.0,
    "max": 60.0
},
"animation_speed_factor": {
    "value": 1.0,
    "type": float,
    "unit": "-",
    "description": "Multiplier for all animation timings",
    "min": 0.1,
    "max": 5.0
}
```

---

#### `quantum_nonlocality.py` (1 Parameter, KEINE Zeit-Konfiguration)
**Zeilen mit hardcodierten Werten:**
- Sehr viele wait() calls: 2×`wait(1)`, 5×`wait(2)`, 5×`wait(3)`, `wait(4)`, `wait(5)`
- Viele run_time values: `run_time=2`, `run_time=3`, `run_time=4`
- Loops über n_points, range(8), n_bars

**💡 Empfehlung:** **NICHT ändern**
- Didaktische Animation mit sehr fester Erzählstruktur
- Timing ist Teil des Storytellings (Pausen für Verständnis)
- Würde durch Konfigurierbarkeit an Wirkung verlieren

---

#### `variational_method.py` (6 Parameter, TEILWEISE Zeit-Konfiguration)
**Zeilen mit hardcodierten Werten:**
- Zeile 555: `duration = 10.0` (Hardcoded!)
- Zeile 556: `fps = 30` (Hardcoded!)
- Zeile 594: `self.wait(1/fps)`
- Viele wait() calls: 1.5, 2, 3

**💡 Empfehlung:** Füge 2 Parameter hinzu:
```python
"animation_duration": {
    "value": 10.0,
    "type": float,
    "unit": "s",
    "description": "Duration of optimization animation",
    "min": 1.0,
    "max": 60.0
},
"animation_fps": {
    "value": 30,
    "type": int,
    "unit": "frames/s",
    "description": "Animation frames per second",
    "min": 10,
    "max": 120
}
```

---

### **Specialized Topics**

#### `pca_molecular_dynamics.py` (9 Parameter, KEINE Zeit-Konfiguration)
**Zeilen mit hardcodierten Werten:**
- Sehr viele wait() calls: 8×`wait(0.5)`, 5×`wait(1)`, `wait(0.3)`, `wait(0.8)`, 2×`wait(1.5)`, `wait(2.0)`, `wait(3)`
- run_time values: `run_time=1`, `run_time=1.5`, `run_time=2`, `run_time=3`

**💡 Empfehlung:** Füge 1 Parameter hinzu:
```python
"animation_speed_factor": {
    "value": 1.0,
    "type": float,
    "unit": "-",
    "description": "Multiplier for all animation timings",
    "min": 0.1,
    "max": 5.0
}
```
Oder: Behalte feste Timings für didaktische Präsentation (Storytelling)

---

#### `particle_interactions_combinatorics.py` (7 Parameter, KEINE Zeit-Konfiguration)
**Zeilen mit hardcodierten Werten:**
- Viele wait() calls: 0.3, 0.5, 0.6, 1, 1.5, 2, 2.5
- run_time values: 0.5, 1
- Loop: `for n in range(2, 5)` (zeigt 2, 3, 4 Teilchen)

**💡 Empfehlung:** **NICHT ändern**
- Didaktische Animation mit festem Aufbau (2→3→4 Teilchen)
- Timing ist Teil der pädagogischen Struktur
- n=2,3,4 ist didaktisch gewählt (keine Konfiguration nötig)

---

#### `polarization_forcefield.py` (13 Parameter, KEINE Zeit-Konfiguration)
**Zeilen mit hardcodierten Werten:**
- Zeile 838: `frame_dt = 1/30` (FPS hardcoded)
- Zeile 839: `total_time = 10.0` (Duration hardcoded)
- Zeile 843: `frames = int(total_time / frame_dt)`

**💡 Empfehlung:** Füge 2 Parameter hinzu:
```python
"simulation_duration": {
    "value": 10.0,
    "type": float,
    "unit": "s",
    "description": "Total simulation/animation duration",
    "min": 1.0,
    "max": 60.0
},
"animation_fps": {
    "value": 30,
    "type": int,
    "unit": "frames/s",
    "description": "Animation frames per second",
    "min": 10,
    "max": 120
}
```

---

## 📊 Zusammenfassung & Empfehlungen

### Statistik

| Kategorie | Mit Zeit-Config | Ohne Zeit-Config | Anteil konfigurierbar |
|-----------|----------------|------------------|----------------------|
| **Forcefield Animation** | 4/5 (80%) | `nh3_inversion.py` | Sehr gut |
| **Monte Carlo & Sampling** | 1/4 (25%) | 3 Dateien | Verbesserungspotential |
| **MD & Quantum** | 1/6 (17%) | 5 Dateien | Hohes Potential |
| **Specialized Topics** | 1/4 (25%) | 3 Dateien | Optional (didaktisch) |
| **GESAMT** | **7/19 (37%)** | **12/19 (63%)** | - |

---

### 🎯 Prioritäten für weitere Konfigurierbarkeit

#### **Hohe Priorität** ⭐⭐⭐ (wissenschaftliche Simulationen mit variablen Phasen)

1. **`h2_md_full_refactored.py`** - 5 Phasen mit je 200-800 Schritten
   - **Impact:** Sehr hoch - ermöglicht detaillierte vs. schnelle Demos
   - **Aufwand:** +10 Parameter (5 phase_steps + 5 animation_wait)
   - **Nutzen:** Kürzere Demos (50 steps) oder längere Studien (2000 steps)

2. **`nh3_inversion.py`** - 4 Phasen + Zyklen
   - **Impact:** Hoch - 3 Inversionszyklen sind lang für Präsentationen
   - **Aufwand:** +8 Parameter (6 step counts + 2 wait times)
   - **Nutzen:** Schnelle Demo (1 Zyklus) vs. vollständige Darstellung (5+ Zyklen)

3. **`h3_reaction_pathway.py`** - 3 Phasen
   - **Impact:** Mittel-hoch - kürzere/längere Reaktionspfade
   - **Aufwand:** +6 Parameter (3 phase_steps + 3 animation_wait)
   - **Nutzen:** Flexibilität für verschiedene Detailstufen

#### **Mittlere Priorität** ⭐⭐ (würde Flexibilität erhöhen)

4. **`polymer_monte_carlo.py`** - warmup + simulation steps
   - **Impact:** Mittel - 80 warmup steps sind oft zu viel für Demos
   - **Aufwand:** +5 Parameter
   - **Nutzen:** Schnellere Demos ohne lange Warmup-Phase

5. **`variational_method.py`** - Animation duration/fps
   - **Impact:** Mittel - 10s Optimierung manchmal zu lang
   - **Aufwand:** +2 Parameter (duration, fps)
   - **Nutzen:** Kürzere (5s) oder längere (20s) Optimierungs-Animation

6. **`metropolis_animation.py`** - viele wait() calls
   - **Impact:** Mittel - lange didaktische Pausen
   - **Aufwand:** +1 Parameter (animation_speed_factor)
   - **Nutzen:** Schnellere Präsentationen (2x Geschwindigkeit)

7. **`geometry_optimization.py`** - wait(10) + timings
   - **Impact:** Niedrig-mittel - `wait(10)` ist für manuelle Inspektion
   - **Aufwand:** +2 Parameter
   - **Nutzen:** Anpassbare Inspektionszeit

8. **`polarization_forcefield.py`** - simulation duration/fps
   - **Impact:** Mittel - 10s Standard-Dauer
   - **Aufwand:** +2 Parameter (duration, fps)
   - **Nutzen:** Flexibilität für Demos vs. Studien

#### **Niedrige Priorität** ⭐ (didaktische Animationen, feste Timings oft besser)

9. **`quantum_nonlocality.py`** - Storytelling-Tempo wichtig
   - **Empfehlung:** NICHT ändern - Timing ist Teil der Erzählstruktur

10. **`pca_molecular_dynamics.py`** - didaktische Präsentation
    - **Empfehlung:** Optional - `animation_speed_factor` könnte helfen

11. **`particle_interactions_combinatorics.py`** - didaktische Präsentation
    - **Empfehlung:** NICHT ändern - n=2,3,4 Sequenz ist pädagogisch optimal

12. **`polymer_sampling_comparison.py`** - nur wait(0.001)
    - **Empfehlung:** Low priority - einfacher +1 Parameter

---

### 🚀 Nächste Schritte

**Kurzfristig (High Priority):**
1. `h2_md_full_refactored.py` - +10 Parameter
2. `nh3_inversion.py` - +8 Parameter
3. `h3_reaction_pathway.py` - +6 Parameter

**Mittelfristig (Medium Priority):**
4. `polymer_monte_carlo.py` - +5 Parameter
5. `variational_method.py` - +2 Parameter
6. `polarization_forcefield.py` - +2 Parameter

**Optional (Low Priority):**
7. `metropolis_animation.py` - +1 Parameter
8. `polymer_sampling_comparison.py` - +1 Parameter
9. `pca_molecular_dynamics.py` - +1 Parameter

**Total neue Parameter bei vollständiger Umsetzung:** +36 Parameter über 9 Dateien

---

**Status:** Dokumentation erstellt am 2025-11-06
**Analysiert:** 19/19 Dateien
**Empfohlene Ergänzungen:** 36 neue Zeit/FPS-Parameter in 9 High/Medium-Priority Dateien
