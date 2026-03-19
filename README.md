# Music Composer

An algorithmic music composition engine that generates professional-grade MIDI compositions from text prompts.

## Features

- **Natural language prompts** — describe the music you want and the engine interprets mood, genre, key, tempo, and instrumentation
- **Deep music theory engine** — 17 scale types, 20 chord types, voice leading, and 30+ chord progression patterns
- **Multiple generators** — melody, bass, drums, and accompaniment with genre-appropriate styles
- **12 genre presets** — orchestral, cinematic, jazz, rock, electronic, ambient, and more
- **17 mood mappings** — epic, melancholic, heroic, serene, dark, playful, etc.
- **Song structure system** — section-based arrangement (intro, verse, chorus, bridge, outro)
- **Multi-format output** — MIDI, WAV, and MP3 rendering
- **Reproducible** — optional random seed for deterministic generation

## Installation

Requires Python 3.10+.

```bash
pip install -e .
```

For audio rendering (WAV/MP3), you also need [FluidSynth](https://www.fluidsynth.org/) and a SoundFont:

```bash
# macOS
brew install fluidsynth

# Ubuntu/Debian
sudo apt-get install fluidsynth
```

## Usage

```bash
# Basic usage
composer "epic orchestral battle theme"

# Specify format and options
composer "melancholic piano ballad in D minor" -f midi wav

# Jazz with custom tempo and duration
composer "jazz trio improvisation" --tempo 140 --duration 180

# Full control
composer "cinematic trailer music" -g cinematic -m epic -k C --tempo 100 -f wav mp3
```

### Options

| Flag | Description |
|---|---|
| `-k`, `--key` | Musical key (e.g., `C`, `Dm`, `F#`) |
| `-t`, `--tempo` | Tempo in BPM |
| `-d`, `--duration` | Duration in seconds (default: 120) |
| `-g`, `--genre` | Genre preset |
| `-m`, `--mood` | Mood/vibe |
| `-f`, `--format` | Output format(s): `midi`, `wav`, `mp3` |
| `--time-sig` | Time signature (e.g., `4/4`, `3/4`) |
| `--intensity` | Intensity from 0.0 to 1.0 |
| `--seed` | Random seed for reproducibility |

### Discovery commands

```bash
composer --list-moods        # Show available moods
composer --list-genres       # Show available genres
composer --list-instruments  # Show available instruments
composer --check-deps        # Check audio rendering dependencies
```

## Development

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT
