# H₂ Born-Oppenheimer Animation Project

## Übersicht

Dieses Projekt enthält Animationen für die Vorlesung "Theoretische Chemie" zur Born-Oppenheimer-Näherung bei der H₂-Molekülbildung.

## Dateien

### h2_born_oppenheimer.py
**Einfache Born-Oppenheimer MD-Simulation**

- 4-Quadranten Layout: Links H₂-Molekül, rechts Energie/Abstand-Plots
- Morse-Potential für H₂: V(r) = De(1-e^(-α(r-re)))² - De
- Parameter: De=4.478 eV, re=0.741 Å, α=1.5 Å⁻¹
- Velocity Verlet Integration für zeitliche Entwicklung
- 300K Temperatur-Initialisierung mit Maxwell-Boltzmann-Verteilung
- Mehrsprachigkeitsunterstützung (DE/EN)

**Verbesserungen gegenüber ursprünglicher h2.py:**
- Richtige Molekulardynamik statt parametrischer Bewegung
- Realistische Physik mit korrekten Einheiten (eV, Å, fs)
- Anti-Überlappungs Design mit optimierten Schriftgrößen
- Numerische Stabilität durch Clamping und Overflow-Schutz

### h2_md_full.py
**Erweiterte 4-Phasen Animation: Von freien Atomen zur H₂-Bindung**

#### Phase 1: Freie H-Atome in MD-Box
- Ein H-Atom bewegt sich frei in harmonisch begrenzter Box
- Velocity Verlet Integration mit Box-Confinement (V = k(r-rwall)²)
- Elektron folgt instantan mit kreisförmiger Orbitalbewegung
- Live-Tracking von kinetischer und potentieller Energie

#### Phase 2: Zwei H-Atome mit Wechselwirkung
- Zweites H-Atom wird eingeführt
- H-H Wechselwirkung: repulsiv bei kurzen, attraktiv bei mittleren Abständen
- Beide Atome mit eigener MD und Elektronenbewegung
- Tracking von Abstand und Wechselwirkungsenergie

#### Phase 3: Born-Oppenheimer-Übergang
- Erklärung der Born-Oppenheimer-Näherung als Text-Overlay
- Elektronen und Orbits verschwinden (FadeOut)
- Fokus auf Kernbewegung durch Vergrößerung der Nuklear-Symbole
- Theoretische Begründung der Trennung von Kern- und Elektronenbewegung

#### Phase 4: H₂-Molekül Formation
- Übergang zu H₂-Koordinate (Kernabstand)
- Morse-Potential Dynamik wie im ursprünglichen h2.py
- Vibrationsanalyse mit Bindungsvisualisierung
- Integration der molekularen Dynamik

#### Innovative Features:

1. **Adaptive Zeitachsen:**
   - Konstante Plot-Breite bei wachsendem Zeitbereich
   - Automatische Skalierung: mehr Zeit auf gleiche Pixelanzahl
   - `time_scale_factor` passt sich dynamisch an

2. **Realistische Box-MD:**
   - Harmonische Wandpotentiale bei Boxgrenzen
   - Korrektes Kraft-Feedback für Confinement
   - Physikalisch konsistente Reflektion

3. **Instantane Elektronenbewegung:**
   - Elektronen folgen Kernen ohne Verzögerung
   - Kreisbahn-Simulation mit Phasendifferenz
   - Visuell ansprechende Darstellung der adiabatischen Näherung

4. **Sequenzielle Physik:**
   - Freie Atome → Wechselwirkung → BO-Näherung → Molekül
   - Nahtlose Übergänge zwischen Konzepten
   - Pädagogisch aufgebaute Erklärungssequenz

## Ausführung

### Voraussetzungen
- Python 3.13 mit ManimGL


## Technische Details

### Numerische Stabilität
- Kleine Zeitschritte (0.05-0.1 fs) für stabile Integration
- Clamping von Positionen und Geschwindigkeiten
- Overflow-Schutz in Exponentialfunktionen
- Endlichkeitsprüfungen für alle Werte

### Performance-Optimierung
- Begrenzte Datenpunkte in Plots (200 max)
- Selektive Visualisierungs-Updates
- Sichere MD-Integration mit Kraftbegrenzung

### 4-Quadranten Layout-Prinzipien
- Linke Seite: Molekulare Visualisierung (großer Bereich)
- Rechts oben: Energie vs Zeit
- Rechts unten: Distanz/andere Parameter vs Zeit
- Klare Bereichtrennung mit angemessenen Abständen
- Optimierte Schriftgrößen (8-14px)
- Farbkodierung zur besseren Unterscheidung

## Anpassungen

### Mehrsprachigkeit
Variable `LANGUAGE = "DE"/"EN"` am Dateianfang ändern.

### Physikalische Parameter
Morse-Parameter, Temperatur und Zeitschritte in `setup_parameters()` anpassbar.

### Visualisierung
Layout-Parameter in `setup_layout()` konfigurierbar.
