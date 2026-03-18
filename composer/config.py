"""Global configuration and defaults."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Config:
    """Application-wide configuration."""

    # Paths
    output_dir: Path = field(default_factory=lambda: Path("output"))
    soundfont_path: Path | None = None

    # Defaults
    default_tempo: int = 120
    default_key: str = "C"
    default_scale: str = "major"
    default_time_signature: tuple[int, int] = (4, 4)
    default_duration_seconds: int = 120
    default_velocity: int = 80

    # Audio rendering
    sample_rate: int = 44100

    # Composition
    min_tempo: int = 40
    max_tempo: int = 220

    def __post_init__(self) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        if self.soundfont_path is None:
            # Check common locations
            candidates = [
                Path("soundfonts/default.sf2"),
                Path(os.path.expanduser("~/.fluidsynth/default_sound_font.sf2")),
                Path("/usr/share/sounds/sf2/FluidR3_GM.sf2"),
                Path("/usr/share/soundfonts/FluidR3_GM.sf2"),
                Path("/usr/share/sounds/sf2/default-GM.sf2"),
            ]
            for candidate in candidates:
                if candidate.exists():
                    self.soundfont_path = candidate
                    break


# Global singleton
config = Config()
