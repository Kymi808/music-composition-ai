"""Instrument registry - MIDI program numbers, ranges, and roles."""

from __future__ import annotations

from dataclasses import dataclass

from composer.theory.constants import GM_INSTRUMENTS, INSTRUMENT_RANGES


@dataclass
class InstrumentInfo:
    """Information about an instrument."""
    name: str
    midi_program: int
    low_note: int = 21
    high_note: int = 108
    family: str = "keyboard"  # keyboard, strings, woodwinds, brass, percussion, synth, guitar

    @property
    def range(self) -> tuple[int, int]:
        return (self.low_note, self.high_note)


class InstrumentRegistry:
    """Registry of all available instruments."""

    _instruments: dict[str, InstrumentInfo] = {}

    @classmethod
    def initialize(cls) -> None:
        """Build the instrument registry from constants."""
        if cls._instruments:
            return

        families = {
            "keyboard": range(0, 8),
            "chromatic_percussion": range(8, 16),
            "organ": range(16, 24),
            "guitar": range(24, 32),
            "bass": range(32, 40),
            "strings": range(40, 48),
            "ensemble": range(48, 56),
            "brass": range(56, 64),
            "reed": range(64, 72),
            "pipe": range(72, 80),
            "synth_lead": range(80, 88),
            "synth_pad": range(88, 96),
            "synth_effects": range(96, 104),
            "ethnic": range(104, 112),
            "percussive": range(112, 120),
            "sound_effects": range(120, 128),
        }

        for name, program in GM_INSTRUMENTS.items():
            family = "other"
            for fam_name, fam_range in families.items():
                if program in fam_range:
                    family = fam_name
                    break

            low, high = INSTRUMENT_RANGES.get(name, (21, 108))
            cls._instruments[name] = InstrumentInfo(
                name=name,
                midi_program=program,
                low_note=low,
                high_note=high,
                family=family,
            )

    @classmethod
    def get(cls, name: str) -> InstrumentInfo:
        """Get instrument info by name."""
        cls.initialize()
        if name in cls._instruments:
            return cls._instruments[name]
        # Try fuzzy match
        name_lower = name.lower().replace(" ", "_")
        for iname, info in cls._instruments.items():
            if name_lower in iname:
                return info
        raise KeyError(f"Unknown instrument: {name}")

    @classmethod
    def get_program(cls, name: str) -> int:
        """Get MIDI program number for an instrument."""
        return cls.get(name).midi_program

    @classmethod
    def get_by_family(cls, family: str) -> list[InstrumentInfo]:
        """Get all instruments in a family."""
        cls.initialize()
        return [i for i in cls._instruments.values() if i.family == family]

    @classmethod
    def list_all(cls) -> list[str]:
        """List all instrument names."""
        cls.initialize()
        return sorted(cls._instruments.keys())
