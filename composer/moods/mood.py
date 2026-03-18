"""Mood definitions and their musical parameter mappings."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Mood:
    """Maps a mood/vibe to musical parameters."""

    name: str
    preferred_modes: list[str] = field(default_factory=lambda: ["major"])
    tempo_range: tuple[int, int] = (100, 130)
    velocity_range: tuple[str, str] = ("mf", "f")  # Dynamic range
    intensity: float = 0.6
    preferred_contours: list[str] = field(default_factory=lambda: ["arch"])
    preferred_bass_styles: list[str] = field(default_factory=lambda: ["root"])
    preferred_acc_styles: list[str] = field(default_factory=lambda: ["block"])
    dynamic_curve: str = "arc"
    description: str = ""


class MoodLibrary:
    """Collection of mood definitions."""

    MOODS: dict[str, Mood] = {
        "epic": Mood(
            name="epic",
            preferred_modes=["natural_minor", "harmonic_minor"],
            tempo_range=(120, 160),
            velocity_range=("f", "fff"),
            intensity=0.85,
            preferred_contours=["climbing", "arch"],
            preferred_bass_styles=["root", "ostinato"],
            preferred_acc_styles=["pad", "tremolo"],
            dynamic_curve="crescendo",
            description="Grand, sweeping, powerful",
        ),
        "melancholic": Mood(
            name="melancholic",
            preferred_modes=["natural_minor", "dorian"],
            tempo_range=(55, 80),
            velocity_range=("pp", "mp"),
            intensity=0.35,
            preferred_contours=["falling", "valley"],
            preferred_bass_styles=["pedal", "root"],
            preferred_acc_styles=["arpeggio", "pad"],
            dynamic_curve="decrescendo",
            description="Sad, sorrowful, reflective",
        ),
        "heroic": Mood(
            name="heroic",
            preferred_modes=["major", "mixolydian"],
            tempo_range=(120, 150),
            velocity_range=("f", "ff"),
            intensity=0.8,
            preferred_contours=["climbing", "arch"],
            preferred_bass_styles=["root"],
            preferred_acc_styles=["block", "pad"],
            dynamic_curve="arc",
            description="Brave, bold, triumphant",
        ),
        "mysterious": Mood(
            name="mysterious",
            preferred_modes=["dorian", "phrygian", "whole_tone"],
            tempo_range=(65, 100),
            velocity_range=("pp", "p"),
            intensity=0.45,
            preferred_contours=["wave", "plateau"],
            preferred_bass_styles=["pedal"],
            preferred_acc_styles=["arpeggio", "pad"],
            dynamic_curve="wave",
            description="Enigmatic, eerie, curious",
        ),
        "romantic": Mood(
            name="romantic",
            preferred_modes=["major", "lydian"],
            tempo_range=(65, 90),
            velocity_range=("mp", "mf"),
            intensity=0.5,
            preferred_contours=["arch", "wave"],
            preferred_bass_styles=["root"],
            preferred_acc_styles=["arpeggio", "alberti"],
            dynamic_curve="arc",
            description="Tender, gentle, passionate",
        ),
        "dark": Mood(
            name="dark",
            preferred_modes=["phrygian", "locrian", "harmonic_minor"],
            tempo_range=(75, 120),
            velocity_range=("mp", "f"),
            intensity=0.7,
            preferred_contours=["falling", "valley"],
            preferred_bass_styles=["ostinato", "pedal"],
            preferred_acc_styles=["tremolo", "pad"],
            dynamic_curve="crescendo",
            description="Sinister, ominous, foreboding",
        ),
        "joyful": Mood(
            name="joyful",
            preferred_modes=["major", "lydian", "pentatonic_major"],
            tempo_range=(115, 145),
            velocity_range=("mf", "f"),
            intensity=0.7,
            preferred_contours=["ascending", "arch"],
            preferred_bass_styles=["root", "walking"],
            preferred_acc_styles=["arpeggio", "strum"],
            dynamic_curve="flat",
            description="Happy, cheerful, bright",
        ),
        "tense": Mood(
            name="tense",
            preferred_modes=["locrian", "phrygian", "harmonic_minor"],
            tempo_range=(95, 140),
            velocity_range=("mp", "ff"),
            intensity=0.75,
            preferred_contours=["climbing", "wave"],
            preferred_bass_styles=["ostinato"],
            preferred_acc_styles=["tremolo"],
            dynamic_curve="crescendo",
            description="Anxious, urgent, suspenseful",
        ),
        "triumphant": Mood(
            name="triumphant",
            preferred_modes=["major"],
            tempo_range=(110, 140),
            velocity_range=("f", "fff"),
            intensity=0.9,
            preferred_contours=["ascending", "climbing"],
            preferred_bass_styles=["root"],
            preferred_acc_styles=["block", "pad"],
            dynamic_curve="crescendo",
            description="Victorious, majestic, glorious",
        ),
        "peaceful": Mood(
            name="peaceful",
            preferred_modes=["major", "lydian", "pentatonic_major"],
            tempo_range=(55, 80),
            velocity_range=("pp", "mp"),
            intensity=0.25,
            preferred_contours=["plateau", "wave"],
            preferred_bass_styles=["pedal"],
            preferred_acc_styles=["pad", "arpeggio"],
            dynamic_curve="flat",
            description="Calm, serene, tranquil",
        ),
        "adventurous": Mood(
            name="adventurous",
            preferred_modes=["major", "mixolydian", "dorian"],
            tempo_range=(110, 145),
            velocity_range=("mf", "f"),
            intensity=0.75,
            preferred_contours=["climbing", "wave"],
            preferred_bass_styles=["root", "walking"],
            preferred_acc_styles=["arpeggio", "strum"],
            dynamic_curve="arc",
            description="Exciting, exploration, quest",
        ),
        "nostalgic": Mood(
            name="nostalgic",
            preferred_modes=["major", "dorian"],
            tempo_range=(70, 100),
            velocity_range=("mp", "mf"),
            intensity=0.45,
            preferred_contours=["arch", "falling"],
            preferred_bass_styles=["root"],
            preferred_acc_styles=["arpeggio", "block"],
            dynamic_curve="decrescendo",
            description="Wistful, bittersweet, memories",
        ),
        "angry": Mood(
            name="angry",
            preferred_modes=["phrygian", "natural_minor", "locrian"],
            tempo_range=(130, 175),
            velocity_range=("f", "fff"),
            intensity=0.9,
            preferred_contours=["descending", "valley"],
            preferred_bass_styles=["ostinato", "pumping"],
            preferred_acc_styles=["tremolo", "block"],
            dynamic_curve="flat",
            description="Rage, fury, aggression",
        ),
        "dreamy": Mood(
            name="dreamy",
            preferred_modes=["lydian", "major", "pentatonic_major"],
            tempo_range=(60, 85),
            velocity_range=("pp", "p"),
            intensity=0.3,
            preferred_contours=["plateau", "wave"],
            preferred_bass_styles=["pedal"],
            preferred_acc_styles=["pad", "arpeggio"],
            dynamic_curve="wave",
            description="Ethereal, floating, surreal",
        ),
        "suspenseful": Mood(
            name="suspenseful",
            preferred_modes=["phrygian", "locrian", "chromatic"],
            tempo_range=(80, 110),
            velocity_range=("pp", "f"),
            intensity=0.6,
            preferred_contours=["climbing"],
            preferred_bass_styles=["pedal", "ostinato"],
            preferred_acc_styles=["tremolo", "pad"],
            dynamic_curve="crescendo",
            description="Creepy, thriller, chilling",
        ),
        "uplifting": Mood(
            name="uplifting",
            preferred_modes=["major", "lydian"],
            tempo_range=(108, 138),
            velocity_range=("mf", "f"),
            intensity=0.7,
            preferred_contours=["ascending", "climbing"],
            preferred_bass_styles=["root"],
            preferred_acc_styles=["arpeggio", "strum"],
            dynamic_curve="crescendo",
            description="Inspiring, hopeful, soaring",
        ),
        "neutral": Mood(
            name="neutral",
            preferred_modes=["major"],
            tempo_range=(100, 130),
            velocity_range=("mp", "mf"),
            intensity=0.6,
            preferred_contours=["arch"],
            preferred_bass_styles=["root"],
            preferred_acc_styles=["block"],
            dynamic_curve="flat",
            description="Default balanced mood",
        ),
    }

    @classmethod
    def get(cls, mood_name: str) -> Mood:
        return cls.MOODS.get(mood_name, cls.MOODS["neutral"])

    @classmethod
    def list_moods(cls) -> list[str]:
        return sorted(cls.MOODS.keys())
