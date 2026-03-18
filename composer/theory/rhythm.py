"""Rhythm patterns, time signatures, and groove templates."""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import NamedTuple


class TimeSignature(NamedTuple):
    """Time signature representation."""
    numerator: int
    denominator: int

    @property
    def beats_per_measure(self) -> int:
        return self.numerator

    @property
    def beat_duration(self) -> float:
        """Duration of one beat in quarter notes."""
        return 4.0 / self.denominator

    @property
    def measure_duration(self) -> float:
        """Duration of one measure in quarter notes."""
        return self.beats_per_measure * self.beat_duration


# Common time signatures
TIME_SIGNATURES = {
    "4/4": TimeSignature(4, 4),
    "3/4": TimeSignature(3, 4),
    "2/4": TimeSignature(2, 4),
    "6/8": TimeSignature(6, 8),
    "5/4": TimeSignature(5, 4),
    "7/8": TimeSignature(7, 8),
    "2/2": TimeSignature(2, 2),
    "12/8": TimeSignature(12, 8),
}


@dataclass
class RhythmEvent:
    """A single rhythmic event."""
    position: float       # Position in beats (0-based within measure)
    duration: float       # Duration in beats
    velocity_scale: float = 1.0  # Velocity multiplier (accent = > 1.0)
    is_rest: bool = False


@dataclass
class RhythmPattern:
    """A rhythmic pattern for one measure."""

    events: list[RhythmEvent] = field(default_factory=list)
    time_signature: TimeSignature = field(default_factory=lambda: TimeSignature(4, 4))

    @property
    def measure_length(self) -> float:
        return self.time_signature.measure_duration

    @staticmethod
    def straight_quarters(time_sig: TimeSignature | None = None) -> RhythmPattern:
        """Simple quarter note pattern."""
        ts = time_sig or TimeSignature(4, 4)
        events = []
        for beat in range(ts.beats_per_measure):
            pos = beat * ts.beat_duration
            accent = 1.2 if beat == 0 else (1.1 if beat == 2 else 1.0)
            events.append(RhythmEvent(position=pos, duration=ts.beat_duration, velocity_scale=accent))
        return RhythmPattern(events=events, time_signature=ts)

    @staticmethod
    def straight_eighths(time_sig: TimeSignature | None = None) -> RhythmPattern:
        """Eighth note pattern."""
        ts = time_sig or TimeSignature(4, 4)
        events = []
        total_eighths = int(ts.measure_duration / 0.5)
        for i in range(total_eighths):
            pos = i * 0.5
            accent = 1.2 if i == 0 else (1.05 if i % 2 == 0 else 0.9)
            events.append(RhythmEvent(position=pos, duration=0.5, velocity_scale=accent))
        return RhythmPattern(events=events, time_signature=ts)

    @staticmethod
    def whole_notes(time_sig: TimeSignature | None = None) -> RhythmPattern:
        """One note per measure (sustained)."""
        ts = time_sig or TimeSignature(4, 4)
        return RhythmPattern(
            events=[RhythmEvent(position=0, duration=ts.measure_duration, velocity_scale=1.0)],
            time_signature=ts,
        )

    @staticmethod
    def half_notes(time_sig: TimeSignature | None = None) -> RhythmPattern:
        """Two notes per measure."""
        ts = time_sig or TimeSignature(4, 4)
        dur = ts.measure_duration / 2
        return RhythmPattern(
            events=[
                RhythmEvent(position=0, duration=dur, velocity_scale=1.1),
                RhythmEvent(position=dur, duration=dur, velocity_scale=1.0),
            ],
            time_signature=ts,
        )

    @staticmethod
    def syncopated(time_sig: TimeSignature | None = None) -> RhythmPattern:
        """Syncopated rhythm with off-beat accents."""
        ts = time_sig or TimeSignature(4, 4)
        events = [
            RhythmEvent(position=0, duration=0.75, velocity_scale=1.1),
            RhythmEvent(position=0.75, duration=0.75, velocity_scale=1.15),
            RhythmEvent(position=1.5, duration=0.5, velocity_scale=0.9),
            RhythmEvent(position=2.0, duration=0.75, velocity_scale=1.0),
            RhythmEvent(position=2.75, duration=0.75, velocity_scale=1.15),
            RhythmEvent(position=3.5, duration=0.5, velocity_scale=0.9),
        ]
        return RhythmPattern(events=events, time_signature=ts)

    @staticmethod
    def dotted(time_sig: TimeSignature | None = None) -> RhythmPattern:
        """Dotted quarter + eighth pattern."""
        ts = time_sig or TimeSignature(4, 4)
        events = [
            RhythmEvent(position=0, duration=1.5, velocity_scale=1.1),
            RhythmEvent(position=1.5, duration=0.5, velocity_scale=0.9),
            RhythmEvent(position=2.0, duration=1.5, velocity_scale=1.0),
            RhythmEvent(position=3.5, duration=0.5, velocity_scale=0.9),
        ]
        return RhythmPattern(events=events, time_signature=ts)

    @staticmethod
    def waltz(time_sig: TimeSignature | None = None) -> RhythmPattern:
        """3/4 waltz pattern (strong-weak-weak)."""
        ts = time_sig or TimeSignature(3, 4)
        events = [
            RhythmEvent(position=0, duration=1.0, velocity_scale=1.3),
            RhythmEvent(position=1.0, duration=1.0, velocity_scale=0.8),
            RhythmEvent(position=2.0, duration=1.0, velocity_scale=0.8),
        ]
        return RhythmPattern(events=events, time_signature=ts)

    @staticmethod
    def arpeggiated(notes_per_beat: int = 4, time_sig: TimeSignature | None = None) -> RhythmPattern:
        """Fast arpeggiated pattern (sixteenths)."""
        ts = time_sig or TimeSignature(4, 4)
        dur = 1.0 / notes_per_beat
        events = []
        total = int(ts.measure_duration * notes_per_beat)
        for i in range(total):
            pos = i * dur
            accent = 1.15 if i % notes_per_beat == 0 else 0.85
            events.append(RhythmEvent(position=pos, duration=dur, velocity_scale=accent))
        return RhythmPattern(events=events, time_signature=ts)

    @staticmethod
    def triplet(time_sig: TimeSignature | None = None) -> RhythmPattern:
        """Triplet pattern."""
        ts = time_sig or TimeSignature(4, 4)
        events = []
        dur = 1.0 / 3.0
        for beat in range(ts.beats_per_measure):
            for tri in range(3):
                pos = beat + tri * dur
                accent = 1.1 if tri == 0 else 0.85
                events.append(RhythmEvent(position=pos, duration=dur, velocity_scale=accent))
        return RhythmPattern(events=events, time_signature=ts)


# Named rhythm patterns for different roles
MELODY_RHYTHMS = {
    "simple": RhythmPattern.straight_quarters,
    "flowing": RhythmPattern.straight_eighths,
    "sustained": RhythmPattern.whole_notes,
    "syncopated": RhythmPattern.syncopated,
    "dotted": RhythmPattern.dotted,
    "waltz": RhythmPattern.waltz,
}

ACCOMPANIMENT_RHYTHMS = {
    "block": RhythmPattern.straight_quarters,
    "arpeggiated": RhythmPattern.arpeggiated,
    "sustained": RhythmPattern.whole_notes,
    "half": RhythmPattern.half_notes,
    "waltz": RhythmPattern.waltz,
    "tremolo": lambda ts=None: RhythmPattern.arpeggiated(8, ts),
}

BASS_RHYTHMS = {
    "whole": RhythmPattern.whole_notes,
    "half": RhythmPattern.half_notes,
    "quarter": RhythmPattern.straight_quarters,
    "walking": RhythmPattern.straight_quarters,
    "eighth": RhythmPattern.straight_eighths,
    "syncopated": RhythmPattern.syncopated,
}
