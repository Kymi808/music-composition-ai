"""Chord progression patterns and generation."""

from __future__ import annotations

import random
from dataclasses import dataclass

from composer.theory.chords import Chord, ChordType
from composer.theory.constants import NOTE_NAMES
from composer.theory.scales import Scale


# Chord progressions defined as scale degrees (1-based)
# Each entry: (name, degrees, typical_genre)
PROGRESSION_LIBRARY = {
    # Major key progressions
    "pop_classic": [1, 5, 6, 4],         # I-V-vi-IV (most common pop)
    "pop_emotional": [1, 6, 4, 5],       # I-vi-IV-V
    "pop_uplifting": [1, 4, 5, 4],       # I-IV-V-IV
    "pop_four_chord": [6, 4, 1, 5],      # vi-IV-I-V
    "rock_classic": [1, 4, 5, 1],        # I-IV-V-I
    "rock_bluesy": [1, 1, 4, 4, 5, 4, 1, 1],  # 12-bar blues pattern
    "jazz_ii_v_i": [2, 5, 1],            # ii-V-I
    "jazz_turnaround": [1, 6, 2, 5],     # I-vi-ii-V
    "jazz_rhythm": [1, 6, 2, 5],         # Rhythm changes A section
    "classical_authentic": [4, 5, 1],     # IV-V-I (authentic cadence)
    "classical_plagal": [1, 4, 1],        # I-IV-I (plagal/amen cadence)
    "classical_circle": [6, 2, 5, 1],    # Circle of fifths
    "folk_simple": [1, 4, 1, 5],         # I-IV-I-V
    "doo_wop": [1, 6, 4, 5],            # Classic 50s
    "pachelbel": [1, 5, 6, 3, 4, 1, 4, 5],  # Canon progression
    "andalusian": [6, 5, 4, 3],          # Descending
    "royal_road": [4, 5, 3, 6],          # IV-V-iii-vi (J-pop)

    # Minor key progressions (degrees relative to minor scale)
    "minor_epic": [1, 7, 6, 5],          # i-VII-VI-V
    "minor_dramatic": [1, 4, 5, 1],      # i-iv-V-i
    "minor_cinematic": [1, 6, 3, 7],     # i-VI-III-VII
    "minor_dark": [1, 2, 5, 1],          # i-ii°-V-i (with dim ii)
    "minor_pop": [1, 6, 3, 7],           # i-VI-III-VII
    "minor_descending": [1, 7, 6, 5],    # Natural minor descent
    "minor_tense": [1, 4, 7, 1],         # i-iv-VII-i
    "minor_heroic": [1, 3, 4, 5],        # i-III-iv-V
    "minor_lament": [1, 7, 6, 7],        # Lament bass

    # Chromatic / modal
    "chromatic_mediant_major": [1, 6, 4, 1],   # With chromatic mediants
    "modal_dorian": [1, 4, 1, 4],              # i-IV-i-IV (Dorian)
    "modal_mixolydian": [1, 7, 4, 1],          # I-bVII-IV-I
}

# Genre-specific progression preferences
GENRE_PROGRESSIONS = {
    "pop": ["pop_classic", "pop_emotional", "pop_uplifting", "doo_wop", "pop_four_chord"],
    "rock": ["rock_classic", "rock_bluesy", "pop_classic", "modal_mixolydian"],
    "jazz": ["jazz_ii_v_i", "jazz_turnaround", "jazz_rhythm", "classical_circle"],
    "classical": ["classical_authentic", "classical_plagal", "classical_circle", "pachelbel"],
    "cinematic": ["minor_epic", "minor_cinematic", "minor_heroic", "pachelbel", "minor_dramatic"],
    "orchestral": ["minor_epic", "minor_cinematic", "classical_circle", "pachelbel", "minor_heroic"],
    "electronic": ["pop_classic", "minor_pop", "pop_uplifting", "modal_mixolydian"],
    "ambient": ["modal_dorian", "pop_uplifting", "minor_lament"],
    "folk": ["folk_simple", "rock_classic", "classical_plagal"],
    "metal": ["minor_dark", "minor_tense", "minor_epic"],
    "rnb": ["jazz_turnaround", "pop_emotional", "doo_wop"],
    "blues": ["rock_bluesy", "rock_classic"],
}

# Mood-specific progression preferences
MOOD_PROGRESSIONS = {
    "epic": ["minor_epic", "minor_heroic", "minor_cinematic"],
    "melancholic": ["minor_lament", "minor_descending", "minor_pop"],
    "heroic": ["minor_heroic", "pop_classic", "minor_epic"],
    "mysterious": ["minor_dark", "modal_dorian", "minor_tense"],
    "romantic": ["pop_emotional", "jazz_turnaround", "doo_wop"],
    "dark": ["minor_dark", "minor_tense", "minor_dramatic"],
    "joyful": ["pop_classic", "pop_uplifting", "rock_classic"],
    "tense": ["minor_tense", "minor_dark", "minor_dramatic"],
    "triumphant": ["minor_heroic", "rock_classic", "classical_authentic"],
    "peaceful": ["folk_simple", "classical_plagal", "modal_dorian"],
    "adventurous": ["minor_cinematic", "minor_epic", "pachelbel"],
    "nostalgic": ["doo_wop", "pop_emotional", "pachelbel"],
    "angry": ["minor_dark", "minor_tense", "minor_dramatic"],
    "dreamy": ["modal_dorian", "jazz_turnaround", "pop_emotional"],
    "suspenseful": ["minor_tense", "minor_dark", "minor_dramatic"],
    "uplifting": ["pop_uplifting", "pop_classic", "rock_classic"],
}


@dataclass
class ChordProgression:
    """A sequence of chords forming a progression."""

    chords: list[Chord]
    degrees: list[int]
    name: str = ""

    @staticmethod
    def from_pattern(
        key: str,
        pattern_name: str,
        is_minor: bool = False,
        use_seventh: bool = False,
        octave: int = 4,
    ) -> ChordProgression:
        """Create a progression from a named pattern."""
        if pattern_name not in PROGRESSION_LIBRARY:
            raise ValueError(f"Unknown progression: {pattern_name}")

        degrees = PROGRESSION_LIBRARY[pattern_name]
        chords = []
        for degree in degrees:
            chord = Chord.from_scale_degree(
                key, degree, is_minor=is_minor,
                use_seventh=use_seventh, octave=octave,
            )
            chords.append(chord)

        return ChordProgression(chords=chords, degrees=degrees, name=pattern_name)

    @staticmethod
    def for_genre(
        key: str,
        genre: str,
        is_minor: bool = False,
        use_seventh: bool = False,
        octave: int = 4,
    ) -> ChordProgression:
        """Pick a genre-appropriate progression."""
        patterns = GENRE_PROGRESSIONS.get(genre, ["pop_classic"])
        pattern_name = random.choice(patterns)
        return ChordProgression.from_pattern(
            key, pattern_name, is_minor, use_seventh, octave
        )

    @staticmethod
    def for_mood(
        key: str,
        mood: str,
        is_minor: bool | None = None,
        use_seventh: bool = False,
        octave: int = 4,
    ) -> ChordProgression:
        """Pick a mood-appropriate progression."""
        patterns = MOOD_PROGRESSIONS.get(mood, ["pop_classic"])
        pattern_name = random.choice(patterns)

        # Determine if minor based on pattern name if not specified
        if is_minor is None:
            is_minor = pattern_name.startswith("minor_")

        return ChordProgression.from_pattern(
            key, pattern_name, is_minor, use_seventh, octave
        )

    def transpose(self, semitones: int) -> ChordProgression:
        """Transpose the entire progression by semitones."""
        new_chords = []
        for chord in self.chords:
            root_idx = NOTE_NAMES.index(chord.root)
            new_root = NOTE_NAMES[(root_idx + semitones) % 12]
            new_chords.append(Chord(
                root=new_root,
                chord_type=chord.chord_type,
                octave=chord.octave,
                inversion=chord.inversion,
                voicing=chord.voicing,
            ))
        return ChordProgression(chords=new_chords, degrees=self.degrees, name=self.name)

    def __len__(self) -> int:
        return len(self.chords)

    def __iter__(self):
        return iter(self.chords)

    def __repr__(self) -> str:
        chord_names = " → ".join(c.name for c in self.chords)
        return f"ChordProgression({chord_names})"
