"""Accompaniment generation - arpeggios, block chords, pads, Alberti bass."""

from __future__ import annotations

import random
from dataclasses import dataclass

from composer.theory.scales import Scale
from composer.theory.chords import Chord
from composer.theory.harmony import VoiceLeader
from composer.generators.melody import NoteEvent


@dataclass
class AccompanimentGenerator:
    """Generates chordal accompaniment patterns."""

    scale: Scale
    velocity_base: int = 70
    note_range: tuple[int, int] = (48, 72)  # C3 to C5
    style: str = "block"  # block, arpeggio, alberti, tremolo, pad, strum

    def generate(
        self,
        chords: list[Chord],
        beats_per_chord: float = 4.0,
    ) -> list[NoteEvent]:
        """Generate accompaniment over a chord progression."""
        if self.style == "arpeggio":
            return self._arpeggiated(chords, beats_per_chord)
        elif self.style == "alberti":
            return self._alberti(chords, beats_per_chord)
        elif self.style == "tremolo":
            return self._tremolo(chords, beats_per_chord)
        elif self.style == "pad":
            return self._pad(chords, beats_per_chord)
        elif self.style == "strum":
            return self._strum(chords, beats_per_chord)
        else:
            return self._block_chords(chords, beats_per_chord)

    def _block_chords(
        self,
        chords: list[Chord],
        beats_per_chord: float,
    ) -> list[NoteEvent]:
        """Block chord accompaniment - chords on beats."""
        notes = []
        voice_leader = VoiceLeader()
        prev_voicing = []

        for i, chord in enumerate(chords):
            start = i * beats_per_chord
            voicing = self._get_voicing(chord)

            if prev_voicing:
                voicing = voice_leader.smooth_transition(prev_voicing, chord)

            voicing = self._constrain_range(voicing)

            # Play chord on beats 1 and 3 (or each beat depending on density)
            beat_positions = [0.0, 2.0] if beats_per_chord >= 4 else [0.0]
            for beat_pos in beat_positions:
                for pitch in voicing:
                    dur = beats_per_chord / len(beat_positions) * 0.9
                    accent = 1.1 if beat_pos == 0 else 0.95
                    notes.append(NoteEvent(
                        pitch=pitch,
                        start=start + beat_pos,
                        duration=dur,
                        velocity=int(self.velocity_base * accent),
                    ))

            prev_voicing = voicing
        return notes

    def _arpeggiated(
        self,
        chords: list[Chord],
        beats_per_chord: float,
    ) -> list[NoteEvent]:
        """Arpeggiated accompaniment - broken chords."""
        notes = []
        patterns = [
            [0, 1, 2, 1],         # Up and back
            [0, 1, 2, 3],         # Straight up
            [0, 2, 1, 2],         # Skip pattern
            [2, 1, 0, 1],         # Down and back
        ]
        arp_pattern = random.choice(patterns)
        note_dur = beats_per_chord / (len(arp_pattern) * 2)  # Eighth-note arpeggios

        for i, chord in enumerate(chords):
            start = i * beats_per_chord
            voicing = self._get_voicing(chord)
            voicing = self._constrain_range(voicing)

            # Repeat pattern to fill the measure
            repetitions = int(beats_per_chord / (len(arp_pattern) * note_dur))
            repetitions = max(1, repetitions)

            pos = 0.0
            for rep in range(repetitions):
                for idx in arp_pattern:
                    if pos >= beats_per_chord:
                        break
                    note_idx = idx % len(voicing)
                    accent = 1.1 if pos == 0 else 0.9
                    notes.append(NoteEvent(
                        pitch=voicing[note_idx],
                        start=start + pos,
                        duration=note_dur * 0.85,
                        velocity=int(self.velocity_base * accent),
                    ))
                    pos += note_dur

        return notes

    def _alberti(
        self,
        chords: list[Chord],
        beats_per_chord: float,
    ) -> list[NoteEvent]:
        """Alberti bass pattern (low-high-mid-high)."""
        notes = []
        note_dur = 0.5  # Eighth notes

        for i, chord in enumerate(chords):
            start = i * beats_per_chord
            voicing = self._get_voicing(chord)
            voicing = self._constrain_range(voicing)

            if len(voicing) < 3:
                voicing = voicing + [voicing[-1] + 12]

            # Alberti pattern: bottom, top, middle, top
            pattern_notes = [voicing[0], voicing[-1], voicing[1], voicing[-1]]
            num_notes = int(beats_per_chord / note_dur)

            for j in range(num_notes):
                idx = j % len(pattern_notes)
                accent = 1.1 if j % 4 == 0 else 0.85
                notes.append(NoteEvent(
                    pitch=pattern_notes[idx],
                    start=start + j * note_dur,
                    duration=note_dur * 0.8,
                    velocity=int(self.velocity_base * accent),
                ))

        return notes

    def _tremolo(
        self,
        chords: list[Chord],
        beats_per_chord: float,
    ) -> list[NoteEvent]:
        """Tremolo - rapid repetition of chord tones (orchestral style)."""
        notes = []
        note_dur = 0.25  # Sixteenth notes

        for i, chord in enumerate(chords):
            start = i * beats_per_chord
            voicing = self._get_voicing(chord)
            voicing = self._constrain_range(voicing)
            num_repeats = int(beats_per_chord / note_dur)

            for j in range(num_repeats):
                for pitch in voicing:
                    vel_variation = random.uniform(0.85, 1.15)
                    notes.append(NoteEvent(
                        pitch=pitch,
                        start=start + j * note_dur,
                        duration=note_dur * 0.7,
                        velocity=int(self.velocity_base * 0.7 * vel_variation),
                    ))

        return notes

    def _pad(
        self,
        chords: list[Chord],
        beats_per_chord: float,
    ) -> list[NoteEvent]:
        """Sustained pad - long held chords."""
        notes = []
        voice_leader = VoiceLeader()
        prev_voicing = []

        for i, chord in enumerate(chords):
            start = i * beats_per_chord
            voicing = self._get_voicing(chord)

            if prev_voicing:
                voicing = voice_leader.smooth_transition(prev_voicing, chord)
            voicing = self._constrain_range(voicing)

            for pitch in voicing:
                notes.append(NoteEvent(
                    pitch=pitch,
                    start=start,
                    duration=beats_per_chord * 0.98,
                    velocity=int(self.velocity_base * 0.8),
                ))
            prev_voicing = voicing

        return notes

    def _strum(
        self,
        chords: list[Chord],
        beats_per_chord: float,
    ) -> list[NoteEvent]:
        """Guitar-style strumming pattern."""
        notes = []
        # Down-up strumming pattern
        strum_times = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]
        is_down = [True, False, True, False, True, False, True, False]

        for i, chord in enumerate(chords):
            start = i * beats_per_chord
            voicing = self._get_voicing(chord)
            voicing = self._constrain_range(voicing)

            for j, (strum_time, down) in enumerate(zip(strum_times, is_down)):
                if strum_time >= beats_per_chord:
                    break
                # Strum effect: slight time offset between notes
                order = voicing if down else list(reversed(voicing))
                for k, pitch in enumerate(order):
                    strum_offset = k * 0.02  # Slight stagger
                    vel = self.velocity_base + (5 if down else -5)
                    vel += random.randint(-8, 8)
                    # Skip some upstrums randomly
                    if not down and random.random() < 0.3:
                        continue
                    notes.append(NoteEvent(
                        pitch=pitch,
                        start=start + strum_time + strum_offset,
                        duration=0.45 if down else 0.35,
                        velocity=max(1, min(127, vel)),
                    ))

        return notes

    def _get_voicing(self, chord: Chord) -> list[int]:
        """Get MIDI notes for a chord, respecting the note range."""
        return chord.get_midi_notes()

    def _constrain_range(self, notes: list[int]) -> list[int]:
        """Constrain notes to the generator's range."""
        low, high = self.note_range
        result = []
        for note in notes:
            while note < low:
                note += 12
            while note > high:
                note -= 12
            if low <= note <= high:
                result.append(note)
        return sorted(set(result)) if result else [low]
