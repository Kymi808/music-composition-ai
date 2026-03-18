# Music Composition AI - Implementation Plan

## Overview
A Python-based music composition engine that takes text prompts and generates professional-grade compositions with MIDI output and audio rendering. No AI/ML models - pure algorithmic composition using music theory rules.

## Tech Stack
- **Python 3.10+**
- **pretty_midi** - MIDI generation and manipulation
- **midi2audio** / **pyfluidsynth** - Audio rendering via FluidSynth + SoundFonts
- **pydub** - Audio format conversion (WAV → MP3)
- **numpy** - Audio sample processing
- **click** - CLI interface
- **pydantic** - Configuration/schema validation

## Directory Structure

```
music-composition-ai/
├── pyproject.toml                    # Project config, dependencies
├── setup.py                          # Package setup
├── LICENSE
├── .gitignore
├── composer/                         # Main package
│   ├── __init__.py
│   ├── __main__.py                   # CLI entry point
│   ├── cli.py                        # Click CLI commands
│   │
│   ├── core/                         # Core composition engine
│   │   ├── __init__.py
│   │   ├── prompt_parser.py          # Parse text prompts into composition params
│   │   ├── composition.py            # Main Composition class - orchestrates everything
│   │   ├── section.py                # Song section (intro, verse, chorus, etc.)
│   │   └── track.py                  # Individual instrument track
│   │
│   ├── theory/                       # Music theory engine
│   │   ├── __init__.py
│   │   ├── constants.py              # Note names, MIDI mappings, intervals
│   │   ├── scales.py                 # Scale definitions and operations
│   │   ├── chords.py                 # Chord types, voicings, inversions
│   │   ├── progressions.py           # Chord progression patterns and generation
│   │   ├── rhythm.py                 # Rhythm patterns, time signatures, grooves
│   │   └── harmony.py               # Voice leading, counterpoint rules
│   │
│   ├── generators/                   # Pattern generators for different roles
│   │   ├── __init__.py
│   │   ├── melody.py                 # Melody generation (motifs, phrases, contour)
│   │   ├── bass.py                   # Bass line generation
│   │   ├── drums.py                  # Drum pattern generation
│   │   ├── accompaniment.py          # Chordal accompaniment (arpeggios, pads, etc.)
│   │   └── orchestrator.py           # Assigns instruments, layers, dynamics
│   │
│   ├── instruments/                  # Instrument definitions
│   │   ├── __init__.py
│   │   ├── registry.py               # Instrument registry (MIDI programs, ranges)
│   │   └── presets.py                # Genre-specific instrument combinations
│   │
│   ├── styles/                       # Style/genre definitions
│   │   ├── __init__.py
│   │   ├── style.py                  # Style dataclass - bundles genre parameters
│   │   └── library.py                # Built-in style library (orchestral, jazz, etc.)
│   │
│   ├── moods/                        # Mood/vibe system
│   │   ├── __init__.py
│   │   └── mood.py                   # Mood definitions → theory parameter mappings
│   │
│   ├── structure/                    # Song structure
│   │   ├── __init__.py
│   │   └── arrangement.py            # Song form, section ordering, transitions
│   │
│   ├── rendering/                    # Audio output pipeline
│   │   ├── __init__.py
│   │   ├── midi_renderer.py          # Generate MIDI file from composition
│   │   └── audio_renderer.py         # MIDI → WAV/MP3 via FluidSynth
│   │
│   └── config.py                     # Global configuration, defaults
│
├── soundfonts/                       # SoundFont files (gitignored, downloaded)
│   └── .gitkeep
│
├── output/                           # Generated output (gitignored)
│   └── .gitkeep
│
└── tests/                            # Test suite
    ├── __init__.py
    ├── test_prompt_parser.py
    ├── test_theory.py
    ├── test_generators.py
    ├── test_composition.py
    └── test_rendering.py
```

## Key Classes & Data Flow

### 1. Prompt Parsing (`prompt_parser.py`)
```
"epic orchestral battle theme in D minor, fast tempo"
       ↓
CompositionParams:
  - mood: "epic"
  - genre: "orchestral"
  - theme: "battle"
  - key: D minor
  - tempo: 160 BPM
  - intensity: 0.85
```

**PromptParser** - Keyword matching to extract: mood, genre, key, tempo, instruments, structure hints, intensity, duration.

### 2. Style Resolution (`style.py`, `mood.py`)
CompositionParams → **StyleResolver** → full parameter set including:
- Chord progression templates
- Rhythm patterns
- Instrument palette
- Dynamic curve
- Section structure

### 3. Composition Engine (`composition.py`)
**Composition** orchestrates the generation:
1. Resolve style + mood → full parameters
2. Generate song structure (sections)
3. Generate chord progressions per section
4. For each section, generate:
   - Melody (melody.py)
   - Bass line (bass.py)
   - Drum patterns (drums.py)
   - Accompaniment (accompaniment.py)
5. Orchestrate: assign instruments, set dynamics
6. Return list of Track objects with Note events

### 4. Music Theory Engine

**Scales** (`scales.py`):
- Major, minor (natural/harmonic/melodic), modes, pentatonic, blues, whole tone, chromatic
- Scale degree operations, transposition

**Chords** (`chords.py`):
- Triads, 7ths, 9ths, 11ths, 13ths, sus, aug, dim
- Voicings: close, open, drop-2, drop-3, spread
- Inversions

**Progressions** (`progressions.py`):
- Common patterns: I-IV-V-I, ii-V-I, I-vi-IV-V, i-iv-v, etc.
- Genre-specific libraries (jazz: ii-V-I turnarounds; cinematic: chromatic mediants)
- Modulation support

**Rhythm** (`rhythm.py`):
- Time signatures: 4/4, 3/4, 6/8, 5/4, 7/8
- Beat patterns, syncopation levels
- Genre-specific grooves

**Harmony** (`harmony.py`):
- Voice leading rules (minimize motion, avoid parallel 5ths/octaves)
- Resolution tendencies
- Tension/release curves

### 5. Generators

**MelodyGenerator** - Generates melodies using:
- Contour shapes (ascending, arch, descending, wave)
- Motif development (repetition, sequence, inversion, augmentation)
- Scale-degree tendencies
- Rhythmic variation
- Range constraints per instrument

**BassGenerator** - Root motion, walking bass, ostinato, pedal tones

**DrumGenerator** - Kit-based patterns, fills, build-ups, genre-specific grooves

**AccompanimentGenerator** - Arpeggios, block chords, Alberti bass, tremolo, pads

**Orchestrator** - Selects instruments from palette, assigns octaves, sets velocity curves, handles layering and doubling

### 6. Rendering Pipeline

**MidiRenderer** - Converts Track/Note objects → pretty_midi PrettyMIDI object → .mid file

**AudioRenderer** - Uses midi2audio (FluidSynth wrapper) to render .mid → .wav, then pydub for .wav → .mp3

## Mood/Vibe Mappings (examples)

| Mood       | Mode      | Tempo   | Dynamics | Progressions       | Instruments            |
|------------|-----------|---------|----------|--------------------|------------------------|
| Epic       | Minor     | 130-170 | ff       | i-VII-VI-V         | Full orchestra + choir |
| Melancholic| Minor     | 60-80   | pp-mp    | i-iv-VI-III        | Piano, strings         |
| Heroic     | Major     | 120-150 | f-ff     | I-V-vi-IV          | Brass, timpani, strings|
| Mysterious | Dorian    | 70-100  | pp-p     | i-IV-bVII-i        | Woodwinds, harp, celesta|
| Romantic   | Major     | 70-90   | mp-mf    | I-vi-ii-V          | Piano, violin, cello   |
| Dark       | Phrygian  | 80-120  | mp-f     | i-bII-i-v          | Low strings, organ     |
| Joyful     | Major     | 120-140 | mf-f     | I-IV-V-I           | Bright winds, guitar   |
| Tense      | Locrian   | 100-140 | crescendo| dim-based, clusters | Tremolo strings, perc  |

## Genre Instrument Palettes

- **Orchestral**: Strings (vln, vla, vc, cb), Woodwinds (fl, ob, cl, bn), Brass (hn, tpt, tbn, tuba), Percussion (timp, cymbals), Harp
- **Electronic**: Synth leads, pads, sub bass, drum machine, arpeggiated synth
- **Jazz**: Piano, upright bass, drum kit (brushes), saxophone, trumpet
- **Rock**: Electric guitar, bass guitar, drum kit, keys
- **Ambient**: Pads, reverb textures, sparse piano, atmospheric synths
- **Cinematic**: Full orchestra + synth hybrid, choir, epic percussion

## CLI Interface

```bash
# Basic usage
composer "epic orchestral battle theme"

# With options
composer "melancholic piano piece" --key "C minor" --tempo 72 --duration 180 --output my_piece

# Export formats
composer "jazz trio improvisation" --format midi wav mp3

# List available options
composer --list-moods
composer --list-genres
composer --list-instruments
```

## Implementation Order

1. **Phase 1: Foundation** - theory/constants, scales, chords, config, basic types
2. **Phase 2: Theory Engine** - progressions, rhythm, harmony
3. **Phase 3: Generators** - melody, bass, drums, accompaniment
4. **Phase 4: Composition Core** - prompt parser, composition engine, orchestrator
5. **Phase 5: Styles & Moods** - style library, mood mappings, instrument presets
6. **Phase 6: Structure** - song sections, arrangement, transitions
7. **Phase 7: Rendering** - MIDI output, audio rendering
8. **Phase 8: CLI** - Click interface, configuration
9. **Phase 9: Tests** - Unit tests for all modules
