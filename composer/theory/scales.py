"""Scale definitions and operations."""

from __future__ import annotations

import random
from dataclasses import dataclass

from composer.theory.constants import (
    NOTE_NAMES,
    FLAT_TO_SHARP,
    SCALE_PATTERNS,
    SCALE_ALIASES,
    note_name_to_midi,
)


@dataclass
class Scale:
    """Represents a musical scale rooted on a specific note."""

    root: str
    scale_type: str

    def __post_init__(self) -> None:
        if self.root in FLAT_TO_SHARP:
            self.root = FLAT_TO_SHARP[self.root]
        resolved = SCALE_ALIASES.get(self.scale_type, self.scale_type)
        if resolved not in SCALE_PATTERNS:
            raise ValueError(
                f"Unknown scale type: {self.scale_type}. "
                f"Available: {list(SCALE_PATTERNS.keys())}"
            )
        self.scale_type = resolved

    @property
    def pattern(self) -> list[int]:
        return SCALE_PATTERNS[self.scale_type]

    @property
    def root_index(self) -> int:
        return NOTE_NAMES.index(self.root)

    def get_notes(self) -> list[str]:
        """Get the note names in this scale."""
        notes = []
        current = self.root_index
        notes.append(NOTE_NAMES[current % 12])
        for interval in self.pattern[:-1]:
            current += interval
            notes.append(NOTE_NAMES[current % 12])
        return notes

    def get_midi_notes(self, octave: int = 4, num_octaves: int = 1) -> list[int]:
        """Get MIDI note numbers for the scale across octaves."""
        midi_notes = []
        base = note_name_to_midi(self.root, octave)
        for oct in range(num_octaves):
            current = base + (12 * oct)
            midi_notes.append(current)
            for interval in self.pattern[:-1]:
                current += interval
                midi_notes.append(current)
        # Add final root
        midi_notes.append(base + 12 * num_octaves)
        return midi_notes

    def degree_to_midi(self, degree: int, octave: int = 4) -> int:
        """Convert a scale degree (1-based) to MIDI note number.

        Supports degrees beyond the octave (e.g., 9 = 2nd an octave up).
        """
        degree -= 1  # Convert to 0-based
        octave_offset = degree // len(self.pattern)
        step = degree % len(self.pattern)

        semitones = sum(self.pattern[:step])
        base = note_name_to_midi(self.root, octave)
        return base + semitones + (12 * octave_offset)

    def note_in_scale(self, midi_note: int) -> bool:
        """Check if a MIDI note belongs to this scale."""
        pitch_class = midi_note % 12
        scale_pcs = set()
        current = self.root_index
        scale_pcs.add(current % 12)
        for interval in self.pattern:
            current += interval
            scale_pcs.add(current % 12)
        return pitch_class in scale_pcs

    def get_pitch_classes(self) -> set[int]:
        """Get the set of pitch classes (0-11) in this scale."""
        pcs = set()
        current = self.root_index
        pcs.add(current % 12)
        for interval in self.pattern:
            current += interval
            pcs.add(current % 12)
        return pcs

    def nearest_scale_note(self, midi_note: int) -> int:
        """Snap a MIDI note to the nearest note in the scale."""
        if self.note_in_scale(midi_note):
            return midi_note
        # Check one semitone up and down
        if self.note_in_scale(midi_note - 1):
            return midi_note - 1
        if self.note_in_scale(midi_note + 1):
            return midi_note + 1
        if self.note_in_scale(midi_note - 2):
            return midi_note - 2
        return midi_note + 2

    def random_note(self, low: int = 48, high: int = 84) -> int:
        """Pick a random note from the scale within the given range."""
        candidates = [
            n for n in range(low, high + 1)
            if self.note_in_scale(n)
        ]
        return random.choice(candidates) if candidates else (low + high) // 2

    def is_minor(self) -> bool:
        """Check if this is a minor-type scale."""
        return self.scale_type in (
            "natural_minor", "harmonic_minor", "melodic_minor",
            "dorian", "phrygian", "locrian", "aeolian",
            "pentatonic_minor", "blues", "phrygian_dominant",
            "hungarian_minor", "hirajoshi", "in_scale",
        )

    def relative_major_or_minor(self) -> Scale:
        """Get the relative major/minor scale."""
        if self.is_minor():
            # Relative major is 3 semitones up
            new_root = NOTE_NAMES[(self.root_index + 3) % 12]
            return Scale(new_root, "major")
        else:
            # Relative minor is 3 semitones down
            new_root = NOTE_NAMES[(self.root_index - 3) % 12]
            return Scale(new_root, "natural_minor")

    def __repr__(self) -> str:
        return f"Scale({self.root} {self.scale_type})"
