"""Melody generation using contour shapes, motif development, and scale-degree tendencies."""

from __future__ import annotations

import random
from dataclasses import dataclass, field

from composer.theory.scales import Scale
from composer.theory.chords import Chord
from composer.theory.rhythm import RhythmPattern, RhythmEvent, TimeSignature
from composer.theory.harmony import VoiceLeader


# Contour shapes define the general melodic direction
CONTOUR_SHAPES = {
    "ascending":  [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 0.9, 0.8],
    "descending": [1.0, 0.8, 0.6, 0.4, 0.2, 0.0, 0.1, 0.2],
    "arch":       [0.0, 0.3, 0.6, 0.9, 1.0, 0.8, 0.5, 0.2],
    "valley":     [1.0, 0.7, 0.4, 0.1, 0.0, 0.2, 0.5, 0.8],
    "wave":       [0.5, 0.8, 1.0, 0.7, 0.3, 0.0, 0.3, 0.5],
    "plateau":    [0.2, 0.5, 0.8, 0.8, 0.8, 0.8, 0.5, 0.2],
    "climbing":   [0.0, 0.15, 0.3, 0.25, 0.5, 0.45, 0.7, 0.85],
    "falling":    [1.0, 0.85, 0.7, 0.75, 0.5, 0.55, 0.3, 0.15],
}


@dataclass
class NoteEvent:
    """A single note in the melody."""
    pitch: int          # MIDI note number
    start: float        # Start time in beats
    duration: float     # Duration in beats
    velocity: int = 80  # MIDI velocity


@dataclass
class MelodyGenerator:
    """Generates melodies based on scale, chords, contour, and rhythm."""

    scale: Scale
    tempo: int = 120
    velocity_base: int = 80
    note_range: tuple[int, int] = (60, 84)  # C4 to C6

    def generate(
        self,
        chords: list[Chord],
        beats_per_chord: float = 4.0,
        rhythm: RhythmPattern | None = None,
        contour: str = "arch",
        variation: float = 0.3,
        density: float = 0.7,
    ) -> list[NoteEvent]:
        """Generate a melodic line over a chord progression.

        Args:
            chords: Chord progression to follow.
            beats_per_chord: Beats per chord.
            rhythm: Rhythm pattern per measure (if None, auto-generate).
            contour: Melodic contour shape name.
            variation: Amount of randomness (0-1).
            density: Note density (0-1), controls rests.
        """
        contour_shape = CONTOUR_SHAPES.get(contour, CONTOUR_SHAPES["arch"])
        melody: list[NoteEvent] = []
        current_time = 0.0
        prev_note = None

        low, high = self.note_range
        voice_leader = VoiceLeader()

        for chord_idx, chord in enumerate(chords):
            # Get chord tones and scale tones for this section
            chord_tones = set(n % 12 for n in chord.get_midi_notes())
            measure_events = self._get_rhythm_events(rhythm, beats_per_chord)

            for event_idx, event in enumerate(measure_events):
                if event.is_rest or random.random() > density:
                    current_time = (chord_idx * beats_per_chord) + event.position + event.duration
                    continue

                # Determine target pitch from contour
                progress = (chord_idx * len(measure_events) + event_idx) / max(
                    len(chords) * len(measure_events) - 1, 1
                )
                contour_val = self._interpolate_contour(contour_shape, progress)
                target_midi = low + contour_val * (high - low)

                # Choose pitch
                pitch = self._choose_pitch(
                    target_midi, chord_tones, prev_note, variation, event, low, high
                )

                # Apply velocity with accent from rhythm
                vel = int(self.velocity_base * event.velocity_scale)
                vel = max(1, min(127, vel))

                note_start = (chord_idx * beats_per_chord) + event.position
                note = NoteEvent(
                    pitch=pitch,
                    start=note_start,
                    duration=event.duration * 0.9,  # Slight gap between notes
                    velocity=vel,
                )
                melody.append(note)
                prev_note = pitch

            current_time = (chord_idx + 1) * beats_per_chord

        return melody

    def generate_motif(self, length: int = 4) -> list[NoteEvent]:
        """Generate a short melodic motif that can be developed."""
        notes = []
        current_pitch = self.scale.degree_to_midi(
            random.choice([1, 3, 5]), octave=4
        )
        for i in range(length):
            # Prefer stepwise motion with occasional leaps
            if random.random() < 0.7:
                step = random.choice([-1, 1])
                current_pitch = self.scale.nearest_scale_note(current_pitch + step * random.randint(1, 2))
            else:
                leap = random.choice([-1, 1]) * random.choice([3, 4, 5, 7])
                current_pitch = self.scale.nearest_scale_note(current_pitch + leap)

            current_pitch = max(self.note_range[0], min(self.note_range[1], current_pitch))

            dur = random.choice([0.5, 1.0, 1.0, 1.5, 2.0])
            notes.append(NoteEvent(
                pitch=current_pitch,
                start=sum(n.duration for n in notes),
                duration=dur,
                velocity=self.velocity_base + random.randint(-10, 10),
            ))
        return notes

    def develop_motif(
        self,
        motif: list[NoteEvent],
        technique: str = "sequence",
        interval: int = 2,
    ) -> list[NoteEvent]:
        """Apply motivic development techniques.

        Techniques: sequence, inversion, retrograde, augmentation, diminution.
        """
        if not motif:
            return []

        start_time = motif[-1].start + motif[-1].duration

        if technique == "sequence":
            # Transpose the motif up/down by scale degrees
            developed = []
            for note in motif:
                new_pitch = self.scale.nearest_scale_note(note.pitch + interval)
                new_pitch = max(self.note_range[0], min(self.note_range[1], new_pitch))
                developed.append(NoteEvent(
                    pitch=new_pitch,
                    start=start_time + (note.start - motif[0].start),
                    duration=note.duration,
                    velocity=note.velocity,
                ))
            return developed

        elif technique == "inversion":
            # Mirror intervals around the first note
            pivot = motif[0].pitch
            developed = []
            for note in motif:
                interval_from_root = note.pitch - pivot
                new_pitch = pivot - interval_from_root
                new_pitch = self.scale.nearest_scale_note(new_pitch)
                new_pitch = max(self.note_range[0], min(self.note_range[1], new_pitch))
                developed.append(NoteEvent(
                    pitch=new_pitch,
                    start=start_time + (note.start - motif[0].start),
                    duration=note.duration,
                    velocity=note.velocity,
                ))
            return developed

        elif technique == "retrograde":
            # Reverse the motif
            developed = []
            for i, note in enumerate(reversed(motif)):
                orig = motif[i]
                developed.append(NoteEvent(
                    pitch=note.pitch,
                    start=start_time + (orig.start - motif[0].start),
                    duration=note.duration,
                    velocity=note.velocity,
                ))
            return developed

        elif technique == "augmentation":
            # Double the durations
            developed = []
            cum_time = 0.0
            for note in motif:
                developed.append(NoteEvent(
                    pitch=note.pitch,
                    start=start_time + cum_time,
                    duration=note.duration * 2,
                    velocity=note.velocity,
                ))
                cum_time += note.duration * 2
            return developed

        elif technique == "diminution":
            # Halve the durations
            developed = []
            cum_time = 0.0
            for note in motif:
                developed.append(NoteEvent(
                    pitch=note.pitch,
                    start=start_time + cum_time,
                    duration=note.duration * 0.5,
                    velocity=note.velocity,
                ))
                cum_time += note.duration * 0.5
            return developed

        return motif

    def _choose_pitch(
        self,
        target: float,
        chord_tones: set[int],
        prev_note: int | None,
        variation: float,
        event: RhythmEvent,
        low: int,
        high: int,
    ) -> int:
        """Choose a pitch considering target contour, chord tones, and smooth motion."""
        target_int = int(round(target))
        candidates = []

        # Prioritize chord tones on strong beats
        is_strong = event.velocity_scale >= 1.0
        search_range = 8 if is_strong else 12

        for pitch in range(target_int - search_range, target_int + search_range + 1):
            if pitch < low or pitch > high:
                continue
            if not self.scale.note_in_scale(pitch):
                continue

            score = 0.0
            pc = pitch % 12

            # Closeness to contour target
            dist = abs(pitch - target_int)
            score -= dist * 0.5

            # Chord tone preference (stronger on strong beats)
            if pc in chord_tones:
                score += 5.0 if is_strong else 2.0

            # Smooth motion from previous note
            if prev_note is not None:
                step = abs(pitch - prev_note)
                if step <= 2:
                    score += 3.0  # Stepwise motion preferred
                elif step <= 4:
                    score += 1.0
                elif step <= 7:
                    score += 0.0
                else:
                    score -= 2.0  # Penalize large leaps

            # Add randomness
            score += random.uniform(-variation * 3, variation * 3)

            candidates.append((pitch, score))

        if not candidates:
            return self.scale.nearest_scale_note(target_int)

        candidates.sort(key=lambda x: x[1], reverse=True)
        # Pick from top candidates with some randomness
        top_n = max(1, int(len(candidates) * 0.3))
        return random.choice(candidates[:top_n])[0]

    def _get_rhythm_events(
        self,
        rhythm: RhythmPattern | None,
        beats: float,
    ) -> list[RhythmEvent]:
        """Get rhythm events for one chord, auto-generating if needed."""
        if rhythm is not None:
            return rhythm.events

        # Auto-generate a simple rhythm
        events = []
        pos = 0.0
        while pos < beats:
            dur = random.choice([0.5, 0.5, 1.0, 1.0, 1.0, 1.5, 2.0])
            dur = min(dur, beats - pos)
            if dur <= 0:
                break
            accent = 1.15 if pos == 0 else 1.0
            # Occasional rest
            is_rest = random.random() < 0.1
            events.append(RhythmEvent(
                position=pos, duration=dur,
                velocity_scale=accent, is_rest=is_rest,
            ))
            pos += dur

        return events

    def _interpolate_contour(self, shape: list[float], progress: float) -> float:
        """Interpolate a contour shape at a given progress (0-1)."""
        if not shape:
            return 0.5
        idx = progress * (len(shape) - 1)
        lower = int(idx)
        upper = min(lower + 1, len(shape) - 1)
        frac = idx - lower
        return shape[lower] * (1 - frac) + shape[upper] * frac
