"""Style dataclass - bundles all parameters for a genre/mood combination."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Style:
    """Complete style definition for composition generation."""

    name: str

    # Theory
    preferred_scales: list[str] = field(default_factory=lambda: ["major"])
    use_seventh_chords: bool = False
    use_extended_chords: bool = False
    chromatic_passing_tones: bool = False

    # Rhythm
    default_time_signature: tuple[int, int] = (4, 4)
    swing: float = 0.0
    syncopation: float = 0.0

    # Melody
    melody_contour: str = "arch"
    melody_range_octaves: int = 2
    melody_density: float = 0.7
    melody_variation: float = 0.3

    # Bass
    bass_style: str = "root"

    # Accompaniment
    accompaniment_style: str = "block"

    # Drums
    drum_genre: str = "rock"
    drum_intensity: float = 0.7
    use_drums: bool = True

    # Dynamics
    dynamic_curve: str = "arc"
    base_velocity: int = 80

    # Structure
    typical_sections: list[str] = field(
        default_factory=lambda: ["intro", "verse", "chorus", "verse", "chorus", "outro"]
    )
    measures_per_section: int = 8

    def __repr__(self) -> str:
        return f"Style({self.name})"
