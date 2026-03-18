"""Chord types, voicings, and inversions."""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import Enum

from composer.theory.constants import NOTE_NAMES, FLAT_TO_SHARP, note_name_to_midi


class ChordType(Enum):
    """Common chord types defined by interval structure (semitones from root)."""

    MAJOR = (0, 4, 7)
    MINOR = (0, 3, 7)
    DIMINISHED = (0, 3, 6)
    AUGMENTED = (0, 4, 8)
    SUS2 = (0, 2, 7)
    SUS4 = (0, 5, 7)
    DOMINANT_7 = (0, 4, 7, 10)
    MAJOR_7 = (0, 4, 7, 11)
    MINOR_7 = (0, 3, 7, 10)
    MINOR_MAJOR_7 = (0, 3, 7, 11)
    DIMINISHED_7 = (0, 3, 6, 9)
    HALF_DIMINISHED_7 = (0, 3, 6, 10)
    AUGMENTED_7 = (0, 4, 8, 10)
    DOMINANT_9 = (0, 4, 7, 10, 14)
    MAJOR_9 = (0, 4, 7, 11, 14)
    MINOR_9 = (0, 3, 7, 10, 14)
    DOMINANT_11 = (0, 4, 7, 10, 14, 17)
    DOMINANT_13 = (0, 4, 7, 10, 14, 17, 21)
    ADD9 = (0, 4, 7, 14)
    POWER = (0, 7)

    @property
    def intervals(self) -> tuple[int, ...]:
        return self.value

    def is_minor(self) -> bool:
        return self in (
            ChordType.MINOR, ChordType.MINOR_7, ChordType.MINOR_MAJOR_7,
            ChordType.MINOR_9, ChordType.DIMINISHED, ChordType.DIMINISHED_7,
            ChordType.HALF_DIMINISHED_7,
        )


# Map scale degrees to chord types for major scale harmonization
MAJOR_SCALE_CHORDS = {
    1: ChordType.MAJOR,
    2: ChordType.MINOR,
    3: ChordType.MINOR,
    4: ChordType.MAJOR,
    5: ChordType.MAJOR,
    6: ChordType.MINOR,
    7: ChordType.DIMINISHED,
}

MAJOR_SCALE_CHORDS_7TH = {
    1: ChordType.MAJOR_7,
    2: ChordType.MINOR_7,
    3: ChordType.MINOR_7,
    4: ChordType.MAJOR_7,
    5: ChordType.DOMINANT_7,
    6: ChordType.MINOR_7,
    7: ChordType.HALF_DIMINISHED_7,
}

# For natural minor
MINOR_SCALE_CHORDS = {
    1: ChordType.MINOR,
    2: ChordType.DIMINISHED,
    3: ChordType.MAJOR,
    4: ChordType.MINOR,
    5: ChordType.MINOR,
    6: ChordType.MAJOR,
    7: ChordType.MAJOR,
}

MINOR_SCALE_CHORDS_7TH = {
    1: ChordType.MINOR_7,
    2: ChordType.HALF_DIMINISHED_7,
    3: ChordType.MAJOR_7,
    4: ChordType.MINOR_7,
    5: ChordType.MINOR_7,
    6: ChordType.MAJOR_7,
    7: ChordType.DOMINANT_7,
}

# Harmonic minor gives dominant V
HARMONIC_MINOR_CHORDS = {
    1: ChordType.MINOR,
    2: ChordType.DIMINISHED,
    3: ChordType.AUGMENTED,
    4: ChordType.MINOR,
    5: ChordType.MAJOR,
    6: ChordType.MAJOR,
    7: ChordType.DIMINISHED,
}


@dataclass
class Chord:
    """Represents a specific chord with root, type, and voicing."""

    root: str
    chord_type: ChordType
    inversion: int = 0
    octave: int = 4
    voicing: str = "close"  # close, open, drop2, drop3, spread

    def __post_init__(self) -> None:
        if self.root in FLAT_TO_SHARP:
            self.root = FLAT_TO_SHARP[self.root]

    @property
    def root_midi(self) -> int:
        return note_name_to_midi(self.root, self.octave)

    def get_midi_notes(self) -> list[int]:
        """Get MIDI note numbers for this chord with voicing applied."""
        base = self.root_midi
        notes = [base + interval for interval in self.chord_type.intervals]

        # Apply inversion
        for i in range(self.inversion):
            if i < len(notes):
                notes[i] += 12

        notes.sort()

        # Apply voicing
        if self.voicing == "open" and len(notes) >= 3:
            # Move middle note(s) up an octave
            notes[1] += 12
            notes.sort()
        elif self.voicing == "drop2" and len(notes) >= 4:
            # Drop second-from-top note down an octave
            notes[-2] -= 12
            notes.sort()
        elif self.voicing == "drop3" and len(notes) >= 4:
            # Drop third-from-top note down an octave
            notes[-3] -= 12
            notes.sort()
        elif self.voicing == "spread":
            # Spread notes across wide range
            result = [notes[0]]
            for i, note in enumerate(notes[1:], 1):
                result.append(note + (12 * (i // 2)))
            notes = result

        return notes

    def get_note_names(self) -> list[str]:
        """Get note names in this chord."""
        root_idx = NOTE_NAMES.index(self.root)
        return [NOTE_NAMES[(root_idx + interval) % 12]
                for interval in self.chord_type.intervals]

    @property
    def name(self) -> str:
        """Human-readable chord name."""
        type_names = {
            ChordType.MAJOR: "",
            ChordType.MINOR: "m",
            ChordType.DIMINISHED: "dim",
            ChordType.AUGMENTED: "aug",
            ChordType.SUS2: "sus2",
            ChordType.SUS4: "sus4",
            ChordType.DOMINANT_7: "7",
            ChordType.MAJOR_7: "maj7",
            ChordType.MINOR_7: "m7",
            ChordType.MINOR_MAJOR_7: "mMaj7",
            ChordType.DIMINISHED_7: "dim7",
            ChordType.HALF_DIMINISHED_7: "m7b5",
            ChordType.AUGMENTED_7: "aug7",
            ChordType.DOMINANT_9: "9",
            ChordType.MAJOR_9: "maj9",
            ChordType.MINOR_9: "m9",
            ChordType.DOMINANT_11: "11",
            ChordType.DOMINANT_13: "13",
            ChordType.ADD9: "add9",
            ChordType.POWER: "5",
        }
        suffix = type_names.get(self.chord_type, "?")
        return f"{self.root}{suffix}"

    @staticmethod
    def from_scale_degree(
        scale_root: str,
        degree: int,
        is_minor: bool = False,
        use_seventh: bool = False,
        octave: int = 4,
    ) -> Chord:
        """Build a diatonic chord from a scale degree."""
        from composer.theory.scales import Scale

        scale_type = "natural_minor" if is_minor else "major"
        scale = Scale(scale_root, scale_type)
        notes = scale.get_notes()

        chord_root = notes[degree - 1]

        if is_minor:
            chord_map = MINOR_SCALE_CHORDS_7TH if use_seventh else MINOR_SCALE_CHORDS
        else:
            chord_map = MAJOR_SCALE_CHORDS_7TH if use_seventh else MAJOR_SCALE_CHORDS

        return Chord(
            root=chord_root,
            chord_type=chord_map[degree],
            octave=octave,
        )

    def __repr__(self) -> str:
        return f"Chord({self.name})"
