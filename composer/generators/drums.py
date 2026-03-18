"""Drum pattern generation - genre-specific grooves, fills, and build-ups."""

from __future__ import annotations

import random
from dataclasses import dataclass, field

from composer.theory.constants import GM_DRUMS
from composer.theory.rhythm import TimeSignature
from composer.generators.melody import NoteEvent


# Pre-built drum patterns: dict of {position_in_beats: [(drum_name, velocity_scale)]}
# These are per-measure patterns for 4/4 time

ROCK_PATTERN = {
    0.0:  [("bass_drum_1", 1.2), ("closed_hi_hat", 1.0)],
    0.5:  [("closed_hi_hat", 0.8)],
    1.0:  [("snare_drum", 1.1), ("closed_hi_hat", 1.0)],
    1.5:  [("closed_hi_hat", 0.8)],
    2.0:  [("bass_drum_1", 1.1), ("closed_hi_hat", 1.0)],
    2.5:  [("closed_hi_hat", 0.8)],
    3.0:  [("snare_drum", 1.2), ("closed_hi_hat", 1.0)],
    3.5:  [("closed_hi_hat", 0.8)],
}

POP_PATTERN = {
    0.0:  [("bass_drum_1", 1.2), ("closed_hi_hat", 0.9)],
    0.5:  [("closed_hi_hat", 0.7)],
    1.0:  [("snare_drum", 1.0), ("closed_hi_hat", 0.9)],
    1.5:  [("closed_hi_hat", 0.7)],
    2.0:  [("bass_drum_1", 1.0), ("closed_hi_hat", 0.9)],
    2.5:  [("bass_drum_1", 0.8), ("closed_hi_hat", 0.7)],
    3.0:  [("snare_drum", 1.1), ("closed_hi_hat", 0.9)],
    3.5:  [("closed_hi_hat", 0.7)],
}

JAZZ_PATTERN = {
    0.0:  [("ride_cymbal_1", 1.1)],
    0.67: [("ride_cymbal_1", 0.7)],  # Swing triplet
    1.0:  [("ride_cymbal_1", 1.0)],
    1.5:  [("pedal_hi_hat", 0.6)],
    2.0:  [("ride_cymbal_1", 1.1)],
    2.67: [("ride_cymbal_1", 0.7)],
    3.0:  [("ride_cymbal_1", 1.0)],
    3.5:  [("pedal_hi_hat", 0.6)],
}

ELECTRONIC_PATTERN = {
    0.0:  [("bass_drum_1", 1.3)],
    0.5:  [("closed_hi_hat", 0.6)],
    1.0:  [("bass_drum_1", 1.1), ("snare_drum", 1.0)],
    1.5:  [("closed_hi_hat", 0.6)],
    2.0:  [("bass_drum_1", 1.3)],
    2.5:  [("closed_hi_hat", 0.6)],
    3.0:  [("bass_drum_1", 1.1), ("snare_drum", 1.0)],
    3.5:  [("closed_hi_hat", 0.6), ("open_hi_hat", 0.5)],
}

ORCHESTRAL_PATTERN = {
    0.0:  [("bass_drum_1", 1.2)],
    2.0:  [("bass_drum_1", 0.9)],
}

CINEMATIC_PATTERN = {
    0.0:  [("bass_drum_1", 1.3), ("crash_cymbal_1", 0.8)],
    1.0:  [("low_tom", 0.9)],
    2.0:  [("bass_drum_1", 1.1), ("low_mid_tom", 0.9)],
    3.0:  [("hi_mid_tom", 1.0), ("snare_drum", 0.7)],
}

AMBIENT_PATTERN = {
    0.0:  [("ride_cymbal_1", 0.5)],
    2.0:  [("ride_cymbal_1", 0.4)],
}

WALTZ_PATTERN = {
    0.0:  [("bass_drum_1", 1.2)],
    1.0:  [("closed_hi_hat", 0.7)],
    2.0:  [("closed_hi_hat", 0.7)],
}

METAL_PATTERN = {
    0.0:   [("bass_drum_1", 1.3), ("closed_hi_hat", 1.0)],
    0.25:  [("bass_drum_1", 1.0)],
    0.5:   [("closed_hi_hat", 0.9)],
    0.75:  [("bass_drum_1", 0.9)],
    1.0:   [("snare_drum", 1.2), ("closed_hi_hat", 1.0)],
    1.5:   [("closed_hi_hat", 0.9)],
    2.0:   [("bass_drum_1", 1.3), ("closed_hi_hat", 1.0)],
    2.25:  [("bass_drum_1", 1.0)],
    2.5:   [("closed_hi_hat", 0.9)],
    2.75:  [("bass_drum_1", 0.9)],
    3.0:   [("snare_drum", 1.2), ("closed_hi_hat", 1.0)],
    3.5:   [("closed_hi_hat", 0.9)],
}

GENRE_PATTERNS = {
    "rock": ROCK_PATTERN,
    "pop": POP_PATTERN,
    "jazz": JAZZ_PATTERN,
    "electronic": ELECTRONIC_PATTERN,
    "orchestral": ORCHESTRAL_PATTERN,
    "cinematic": CINEMATIC_PATTERN,
    "ambient": AMBIENT_PATTERN,
    "waltz": WALTZ_PATTERN,
    "metal": METAL_PATTERN,
    "folk": POP_PATTERN,
    "classical": ORCHESTRAL_PATTERN,
    "blues": ROCK_PATTERN,
    "rnb": POP_PATTERN,
}


@dataclass
class DrumGenerator:
    """Generates drum patterns for various genres."""

    genre: str = "rock"
    velocity_base: int = 90
    swing: float = 0.0  # 0.0 = straight, 1.0 = full swing
    intensity: float = 0.7  # Controls density of hits

    def generate(
        self,
        num_measures: int,
        time_sig: TimeSignature | None = None,
        fill_every: int = 4,
    ) -> list[NoteEvent]:
        """Generate drum patterns for the specified number of measures.

        Args:
            num_measures: Number of measures to generate.
            time_sig: Time signature.
            fill_every: Add a fill every N measures.
        """
        ts = time_sig or TimeSignature(4, 4)
        pattern = GENRE_PATTERNS.get(self.genre, ROCK_PATTERN)
        notes: list[NoteEvent] = []
        measure_dur = ts.measure_duration

        for measure in range(num_measures):
            measure_start = measure * measure_dur
            is_fill = fill_every > 0 and (measure + 1) % fill_every == 0

            if is_fill:
                fill_notes = self._generate_fill(measure_start, measure_dur)
                notes.extend(fill_notes)
            else:
                for pos, hits in pattern.items():
                    if pos >= measure_dur:
                        continue
                    for drum_name, vel_scale in hits:
                        # Apply intensity filter
                        if vel_scale < 0.7 and random.random() > self.intensity:
                            continue

                        midi_note = GM_DRUMS.get(drum_name)
                        if midi_note is None:
                            continue

                        # Apply swing to off-beats
                        actual_pos = pos
                        if self.swing > 0 and pos % 1.0 == 0.5:
                            actual_pos += self.swing * 0.16  # Slight delay

                        vel = int(self.velocity_base * vel_scale)
                        vel += random.randint(-5, 5)  # Humanize
                        vel = max(1, min(127, vel))

                        notes.append(NoteEvent(
                            pitch=midi_note,
                            start=measure_start + actual_pos,
                            duration=0.1,  # Drums are short
                            velocity=vel,
                        ))

                # Add ghost notes for more groove
                if self.intensity > 0.5 and random.random() < 0.3:
                    ghost_pos = random.choice([0.75, 1.75, 2.75, 3.75])
                    if ghost_pos < measure_dur:
                        notes.append(NoteEvent(
                            pitch=GM_DRUMS["snare_drum"],
                            start=measure_start + ghost_pos,
                            duration=0.1,
                            velocity=int(self.velocity_base * 0.35),
                        ))

        return notes

    def _generate_fill(self, start: float, duration: float) -> list[NoteEvent]:
        """Generate a drum fill for transitions."""
        notes = []
        fill_drums = ["snare_drum", "high_tom", "hi_mid_tom", "low_mid_tom", "low_tom"]

        # Start with a crash
        notes.append(NoteEvent(
            pitch=GM_DRUMS["crash_cymbal_1"],
            start=start,
            duration=0.1,
            velocity=int(self.velocity_base * 1.2),
        ))

        # Fill in the last 2 beats with descending toms
        fill_start = start + duration - 2.0
        num_hits = random.choice([4, 6, 8])
        hit_dur = 2.0 / num_hits

        for i in range(num_hits):
            drum_idx = min(i * len(fill_drums) // num_hits, len(fill_drums) - 1)
            drum = fill_drums[drum_idx]
            vel = int(self.velocity_base * (1.0 + i * 0.05))
            notes.append(NoteEvent(
                pitch=GM_DRUMS[drum],
                start=fill_start + i * hit_dur,
                duration=0.1,
                velocity=max(1, min(127, vel)),
            ))

        # Crash on the last beat
        notes.append(NoteEvent(
            pitch=GM_DRUMS["crash_cymbal_1"],
            start=start + duration - 0.01,
            duration=0.1,
            velocity=int(self.velocity_base * 1.3),
        ))

        return notes

    def generate_buildup(self, start: float, duration: float) -> list[NoteEvent]:
        """Generate an intensity buildup (e.g., snare roll into crash)."""
        notes = []
        num_hits = int(duration * 8)  # 32nd notes
        hit_dur = duration / num_hits if num_hits > 0 else duration

        for i in range(num_hits):
            vel = int(self.velocity_base * (0.4 + 0.6 * (i / max(num_hits - 1, 1))))
            notes.append(NoteEvent(
                pitch=GM_DRUMS["snare_drum"],
                start=start + i * hit_dur,
                duration=0.05,
                velocity=max(1, min(127, vel)),
            ))

        # Final crash
        notes.append(NoteEvent(
            pitch=GM_DRUMS["crash_cymbal_1"],
            start=start + duration,
            duration=0.1,
            velocity=min(127, int(self.velocity_base * 1.4)),
        ))

        return notes
