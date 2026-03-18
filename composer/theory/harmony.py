"""Voice leading and harmony rules."""

from __future__ import annotations

from dataclasses import dataclass

from composer.theory.chords import Chord
from composer.theory.scales import Scale


@dataclass
class VoiceLeader:
    """Applies voice leading rules to smooth chord transitions."""

    max_voice_jump: int = 7  # Maximum interval in semitones for smooth motion

    def smooth_transition(
        self,
        current_notes: list[int],
        target_chord: Chord,
    ) -> list[int]:
        """Find the smoothest voicing of target_chord given current notes.

        Minimizes total voice movement while avoiding parallel fifths/octaves.
        """
        target_pitches = target_chord.get_midi_notes()

        if not current_notes:
            return target_pitches

        # Try to match the number of voices
        while len(target_pitches) < len(current_notes):
            # Double the lowest note an octave up
            target_pitches.append(target_pitches[0] + 12)
        while len(target_pitches) > len(current_notes):
            target_pitches = target_pitches[:len(current_notes)]

        # For each target pitch, find the closest octave to the current voice
        result = []
        used_targets = set()

        for curr_note in current_notes:
            best_target = None
            best_distance = float("inf")

            for i, tp in enumerate(target_pitches):
                if i in used_targets:
                    continue
                # Check all octave transpositions within range
                for octave_shift in [-24, -12, 0, 12, 24]:
                    candidate = tp + octave_shift
                    dist = abs(candidate - curr_note)
                    if dist < best_distance and 24 <= candidate <= 108:
                        best_distance = dist
                        best_target = (i, candidate)

            if best_target is not None:
                used_targets.add(best_target[0])
                result.append(best_target[1])
            else:
                result.append(curr_note)

        result.sort()
        return result

    def check_parallel_fifths(
        self,
        prev_notes: list[int],
        curr_notes: list[int],
    ) -> bool:
        """Check if there are parallel fifths between two voicings.

        Returns True if parallel fifths exist (which is usually undesirable).
        """
        if len(prev_notes) < 2 or len(curr_notes) < 2:
            return False

        for i in range(len(prev_notes)):
            for j in range(i + 1, len(prev_notes)):
                if i >= len(curr_notes) or j >= len(curr_notes):
                    continue
                prev_interval = abs(prev_notes[j] - prev_notes[i]) % 12
                curr_interval = abs(curr_notes[j] - curr_notes[i]) % 12

                # Both are perfect fifths and both voices moved
                if (prev_interval == 7 and curr_interval == 7
                        and prev_notes[i] != curr_notes[i]
                        and prev_notes[j] != curr_notes[j]):
                    return True
        return False

    def resolve_tension(self, note: int, scale: Scale) -> int:
        """Resolve a tension note downward to the nearest scale tone."""
        if scale.note_in_scale(note):
            return note
        # Try resolving down by semitone
        if scale.note_in_scale(note - 1):
            return note - 1
        # Try resolving up by semitone
        if scale.note_in_scale(note + 1):
            return note + 1
        return note

    def generate_passing_tones(
        self,
        note_a: int,
        note_b: int,
        scale: Scale,
        max_passing: int = 2,
    ) -> list[int]:
        """Generate passing tones between two notes."""
        if abs(note_b - note_a) <= 2:
            return []

        direction = 1 if note_b > note_a else -1
        passing = []
        current = note_a + direction

        while current != note_b and len(passing) < max_passing:
            if scale.note_in_scale(current):
                passing.append(current)
            current += direction

        return passing

    def add_neighbor_tone(self, note: int, scale: Scale, upper: bool = True) -> int:
        """Get a neighbor tone (upper or lower) from the scale."""
        direction = 1 if upper else -1
        candidate = note + direction
        while not scale.note_in_scale(candidate) and abs(candidate - note) < 4:
            candidate += direction
        return candidate
