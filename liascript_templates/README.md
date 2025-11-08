# LiaScript Interactive Exercise Templates

Dieses Verzeichnis enthält **interaktive LiaScript-Templates** für die Manim4TheoreticalChemistry-Animationen.

## 📚 Was ist LiaScript?

[LiaScript](https://liascript.github.io/) ist eine Markdown-basierte E-Learning-Plattform, die:
- ✅ Interaktive Slider und Eingabefelder unterstützt
- ✅ Quiz-Fragen mit automatischer Bewertung ermöglicht
- ✅ Code-Ausführung direkt im Browser erlaubt
- ✅ Komplett Open Source und kostenlos ist
- ✅ Keine Server-Installation benötigt (statisches Hosting)

## 📁 Verfügbare Templates

### 1. `01_bond_stretching_template.md` ⭐⭐⭐⭐⭐
**Thema:** Harmonisches vs. Morse-Potential für Bindungsdehnungen

**Lernziele:**
- 🟢 Unterschied harmonisches vs. Morse-Potential verstehen
- 🟡 Quantitative Abweichung bei großen Amplituden
- 🔴 Beziehung k = 2·D_e·alpha² herleiten

**Parameter:**
- D_e (Dissoziationsenergie): 2.0 - 8.0 eV
- alpha (Morse-Breite): 0.5 - 3.0 Å⁻¹
- amplitude (Oszillation): 0.1 - 0.8 Å
- r_e (Gleichgewichtslänge): 0.5 - 1.5 Å

**Übungen:** 3 Aufgaben (🟢🟡🔴)

**Bearbeitungszeit:** ~30-45 Minuten

---

### 2. `02_quantum_dynamics_template.md` ⭐⭐⭐⭐⭐
**Thema:** Quantentunneln & Wellenpaket-Propagation

**Lernziele:**
- 🟢 Quantentunneln als nicht-klassisches Phänomen
- 🟡 Wellenpaket-Dispersion und Heisenberg-Unschärfe
- 🔴 WKB-Approximation für Tunnelwahrscheinlichkeit

**Szenarien:**
1. TUNNELING - Quantentunneln durch Barriere
2. CLASSICAL_TRAPPED - Klassisch gefangen
3. HIGH_ENERGY - Über-Barriere-Bewegung
4. DISPERSION - Starke Wellenpaket-Aufstreuung
5. COHERENT - Kohärente Oszillation

**Parameter:**
- barrier (Barrierenhöhe): 1 - 200 kcal/mol
- alpha (Paket-Breite): 0.2 - 10.0
- mass (Teilchenmasse): 1 - 1836 a.u. (Elektron → Proton)
- x0 (Startposition): -2.5 - -1.0 Bohr

**Übungen:** 4 Aufgaben (🟢🟡🔴)

**Bearbeitungszeit:** ~45-60 Minuten

---

### 3. `03_h2_molecular_dynamics_template.md` ⭐⭐⭐⭐⭐
**Thema:** H₂-Moleküldynamik - Von freien Atomen zur Born-Oppenheimer-Näherung

**Lernziele:**
- 🟢 Molekülbildung aus Atomen verstehen
- 🟡 Lennard-Jones vs. Morse-Potential
- 🔴 Thermodynamik der Bindungsbildung

**5 Simulationsphasen:**
1. Freie H-Atome in MD-Box
2. Zwei H-Atome mit LJ-Wechselwirkung
3. Born-Oppenheimer-Näherung (konzeptionell)
4. H₂-Molekül-Formation (Morse-Potential)
5. H₂-Dissoziation

**Parameter:**
- T (Temperatur): 300 - 3000 K
- epsilon (LJ-Tiefe): 0.01 - 0.5 eV
- D_e (Dissoziationsenergie): 2.0 - 6.0 eV
- phase1-5_steps (Phasendauern): 50 - 2000 Schritte

**Übungen:** 4 Aufgaben (🟢🟡🔴)

**Bearbeitungszeit:** ~60-90 Minuten

---

## 🚀 Wie nutze ich die Templates?

### Option 1: Online mit LiaScript (Empfohlen)

1. **Lade das Template auf GitHub hoch:**
   ```bash
   git add liascript_templates/*.md
   git commit -m "Add LiaScript templates"
   git push
   ```

2. **Öffne mit LiaScript:**
   ```
   https://liascript.github.io/course/?https://raw.githubusercontent.com/DEIN_USERNAME/Manim4TheoreticalChemistry/main/liascript_templates/01_bond_stretching_template.md
   ```

3. **Ersetze:** `DEIN_USERNAME` durch Deinen GitHub-Nutzernamen

### Option 2: Lokal mit LiaScript Dev-Server

1. **Installiere den LiaScript Dev-Server:**
   ```bash
   npm install -g @liascript/devserver
   ```

2. **Starte den Server:**
   ```bash
   cd liascript_templates
   liascript-devserver --input 01_bond_stretching_template.md --port 3000
   ```

3. **Öffne im Browser:**
   ```
   http://localhost:3000
   ```

### Option 3: Integration mit QManimPlayer

Die Templates sind so gestaltet, dass sie mit dem **QManimPlayer** (PyQt6-GUI) integriert werden können:

```python
# In QManimPlayer
from bond_stretching import BondStretching

# Lese Parameter aus LiaScript-Slidern
D_e = liascript_slider_value("D_e_val")
alpha = liascript_slider_value("alpha_val")

# Setze PARAMETERS
BondStretching.PARAMETERS["D_e"]["value"] = D_e
BondStretching.PARAMETERS["alpha"]["value"] = alpha

# Render Animation
scene = BondStretching()
scene.render()
```

---

## 📖 Template-Struktur

Jedes Template folgt dieser Struktur:

```markdown
# Titel

> Lernziele

## 📚 Theorie
- Mathematische Grundlagen
- Physikalische Konzepte
- Relevante Formeln

## 🎬 Interaktive Animation
- Parameter-Slider
- Szenario-Auswahl
- Code-Integration

## ✏️ Übung 1-N
- Aufgabenbeschreibung
- Multiple-Choice-Fragen
- Numerische Eingaben
- Ausführliche Erklärungen

## 📊 Zusammenfassung
- Checkboxen für Lernziele

## 🔬 Weiterführende Themen
- Vertiefende Konzepte
- Literaturhinweise
```

---

## 🎨 LiaScript-Syntax-Beispiele

### Interaktive Slider

```markdown
<script input="range" value="4.478" output="D_e_val" min="2.0" max="8.0" step="0.1">@input</script>
D_e = <script>@input(`D_e_val`)</script> eV
```

### Multiple-Choice-Fragen

```markdown
Welche Aussage ist richtig?

[[ ]] Falsche Antwort
[[X]] Richtige Antwort
[[ ]] Falsche Antwort
***
Erklärung hier...
***
```

### Numerische Eingaben

```markdown
Berechne k = 2·D_e·alpha²:

[[36.0]]
[[?]] Tipp: D_e = 4.5 eV, alpha = 2.0 Å⁻¹
```

### Checkboxen

```markdown
Was hast Du gelernt?

- [[X]] Konzept A verstanden
- [[X]] Konzept B verstanden
- [[ ]] Optionales Konzept C
```

---

## 📊 Schwierigkeitsgrade

Die Übungen sind nach Schwierigkeit kategorisiert:

- 🟢 **Anfänger:** Grundlegende Konzepte, qualitativ
- 🟡 **Fortgeschritten:** Quantitative Analyse, Zusammenhänge
- 🔴 **Experte:** Herleitungen, WKB-Approximation, numerisch

---

## 🔗 Weitere Ressourcen

- **LiaScript Dokumentation:** https://liascript.github.io/course/
- **LiaScript Editor:** https://code.visualstudio.com/ + Extension "LiaScript Preview"
- **Manim4TheoreticalChemistry Repo:** https://github.com/conradhuebler/Manim4TheoreticalChemistry
- **LIASCRIPT_EXERCISE_ANALYSIS.md:** Vollständige Analyse aller 19 Szenarien

---

## 🎯 Nächste Schritte

Basierend auf **LIASCRIPT_EXERCISE_ANALYSIS.md** können weitere Templates erstellt werden:

### Hohe Priorität (⭐⭐⭐⭐)
- `04_polymer_monte_carlo_template.md` - MC-Sampling mit 8 Presets
- `05_metadynamics_template.md` - Enhanced Sampling (31 Parameter!)
- `06_nh3_inversion_template.md` - Umbrella-Inversion
- `07_h3_reaction_pathway_template.md` - Transition State Theory

### Mittlere Priorität (⭐⭐⭐)
- `08_angle_bending_template.md` - Winkelpotentiale
- `09_torsion_angle_template.md` - Dihedral Angles
- `10_nonbonded_template.md` - Lennard-Jones
- `11_geometry_optimization_template.md` - Optimierungsalgorithmen

---

**Stand:** 2025-11-08

**Erstellt von:** Claude Code

**Basis:** LIASCRIPT_EXERCISE_ANALYSIS.md (Top 5 Prioritäten)

**Lizenz:** MIT (oder entsprechend Projekt-Lizenz)
