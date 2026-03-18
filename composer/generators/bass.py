"""Bass line generation - root motion, walking bass, ostinato patterns."""

from __future__ import annotations

import random
from dataclasses import dataclass

from composer.theory.scales import Scale
from composer.theory.chords import Chord
from composer.theory.rhythm import RhythmPattern, RhythmEvent
from composer.generators.melody import NoteEvent


@dataclass
class BassGenerator:
    """Generates bass lines that follow chord progressions."""

    scale: Scale
    velocity_base: int = 85
    note_range: tuple[int, int] = (28, 55)  # E1 to G3
    style: str = "root"  # root, walking, ostinato, pedal, pumping

    def generate(
        self,
        chords: list[Chord],
        beats_per_chord: float = 4.0,
        rhythm: RhythmPattern | None = None,
    ) -> list[NoteEvent]:
        """Generate a bass line over a chord progression."""
        if self.style == "walking":
            return self._walking_bass(chords, beats_per_chord)
        elif self.style == "ostinato":
            return self._ostinato_bass(chords, beats_per_chord)
        elif self.style == "pedal":
            return self._pedal_bass(chords, beats_per_chord)
        elif self.style == "pumping":
            return self._pumping_bass(chords, beats_per_chord)
        else:
            return self._root_bass(chords, beats_per_chord, rhythm)

    def _root_bass(
        self,
        chords: list[Chord],
        beats_per_chord: float,
        rhythm: RhythmPattern | None = None,
    ) -> list[NoteEvent]:
        """Simple root note bass on each chord."""
        notes = []
        for i, chord in enumerate(chords):
            root = self._find_bass_note(chord)
            start = i * beats_per_chord

            if rhythm:
                for event in rhythm.events:
                    if not event.is_rest:
                        vel = int(self.velocity_base * event.velocity_scale)
                        notes.append(NoteEvent(
                            pitch=root,
                            start=start + event.position,
                            duration=event.duration * 0.85,
                            velocity=max(1, min(127, vel)),
                        ))
            else:
                # Root on beat 1, fifth on beat 3
                fifth = self.scale.nearest_scale_note(root + 7)
                fifth = max(self.note_range[0], min(self.note_range[1], fifth))

                notes.append(NoteEvent(
                    pitch=root, start=start,
                    duration=beats_per_chord / 2 * 0.9,
                    velocity=self.velocity_base + 10,
                ))
                if beats_per_chord >= 3:
                    notes.append(NoteEvent(
                        pitch=fifth,
                        start=start + beats_per_chord / 2,
                        duration=beats_per_chord / 2 * 0.9,
                        velocity=self.velocity_base,
                    ))
        return notes

    def _walking_bass(
        self,
        chords: list[Chord],
        beats_per_chord: float,
    ) -> list[NoteEvent]:
        """Jazz-style walking bass - quarter notes approaching next chord."""
        notes = []
        prev_note = None

        for i, chord in enumerate(chords):
            root = self._find_bass_note(chord)
            next_root = None
            if i + 1 < len(chords):
                next_root = self._find_bass_note(chords[i + 1])

            beats = int(beats_per_chord)
            start = i * beats_per_chord

            for beat in range(beats):
                if beat == 0:
                    pitch = root
                elif beat == beats - 1 and next_root is not None:
                    # Approach note to next chord
                    approach = next_root + random.choice([-1, -2, 1, 2])
                    pitch = self.scale.nearest_scale_note(approach)
                else:
                    # Scale-wise motion between root and fifth
                    chord_tones = chord.get_midi_notes()
                    target = random.choice([root, root + 7, root + 5, root + 3])
                    pitch = self.scale.nearest_scale_note(target)
                    if prev_note:
                        # Prefer stepwise
                        step = 1 if pitch > prev_note else -1
                        pitch = self.scale.nearest_scale_note(prev_note + step * random.randint(1, 3))

                pitch = max(self.note_range[0], min(self.note_range[1], pitch))

                vel = self.velocity_base + (5 if beat == 0 else -5)
                notes.append(NoteEvent(
                    pitch=pitch,
                    start=start + beat,
                    duration=0.9,
                    velocity=max(1, min(127, vel)),
                ))
                prev_note = pitch

        return notes

    def _ostinato_bass(
        self,
        chords: list[Chord],
        beats_per_chord: float,
    ) -> list[NoteEvent]:
        """Repeating rhythmic pattern adapted to each chord."""
        notes = []
        # Define a repeating pattern (eighth notes)
        pattern_offsets = [0, 0, 7, 0, 5, 0, 7, 12]  # Semitone offsets from root
        dur = beats_per_chord / len(pattern_offsets)

        for i, chord in enumerate(chords):
            root = self._find_bass_note(chord)
            start = i * beats_per_chord

            for j, offset in enumerate(pattern_offsets):
                pitch = self.scale.nearest_scale_note(root + offset)
                pitch = max(self.note_range[0], min(self.note_range[1], pitch))
                accent = 1.15 if j == 0 else (1.05 if j % 2 == 0 else 0.9)
                notes.append(NoteEvent(
                    pitch=pitch,
                    start=start + j * dur,
                    duration=dur * 0.8,
                    velocity=int(self.velocity_base * accent),
                ))
        return notes

    def _pedal_bass(
        self,
        chords: list[Chord],
        beats_per_chord: float,
    ) -> list[NoteEvent]:
        """Sustained pedal tone (tonic) with occasional movement."""
        notes = []
        tonic = self._find_bass_note(chords[0]) if chords else 36

        for i, chord in enumerate(chords):
            start = i * beats_per_chord
            # Use tonic most of the time, move to chord root for dominant chords
            use_root = random.random() < 0.3
            pitch = self._find_bass_note(chord) if use_root else tonic

            notes.append(NoteEvent(
                pitch=pitch,
                start=start,
                duration=beats_per_chord * 0.95,
                velocity=self.velocity_base,
            ))
        return notes

    def _pumping_bass(
        self,
        chords: list[Chord],
        beats_per_chord: float,
    ) -> list[NoteEvent]:
        """Electronic/dance pumping eighth-note bass."""
        notes = []
        for i, chord in enumerate(chords):
            root = self._find_bass_note(chord)
            start = i * beats_per_chord
            eighth_count = int(beats_per_chord * 2)

            for j in range(eighth_count):
                # Sidechain-like velocity pattern
                vel_mult = 1.2 if j % 2 == 0 else 0.7
                notes.append(NoteEvent(
                    pitch=root,
                    start=start + j * 0.5,
                    duration=0.4,
                    velocity=int(self.velocity_base * vel_mult),
                ))
        return notes

    def _find_bass_note(self, chord: Chord) -> int:
        """Find the best bass note for a chord within the bass range."""
        from composer.theory.constants import note_name_to_midi

        low, high = self.note_range
        # Try octaves from low to high
        for octave in range(1, 5):
            note = note_name_to_midi(chord.root, octave)
            if low <= note <= high:
                return note
        # Fallback
        return max(low, min(high, note_name_to_midi(chord.root, 2)))
