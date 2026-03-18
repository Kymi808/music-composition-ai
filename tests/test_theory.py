"""Tests for the music theory engine."""

import pytest

from composer.theory.constants import (
    NOTE_NAMES, note_name_to_midi, midi_to_note_name,
    SCALE_PATTERNS, GM_INSTRUMENTS, GM_DRUMS,
)
from composer.theory.scales import Scale
from composer.theory.chords import Chord, ChordType
from composer.theory.progressions import ChordProgression
from composer.theory.rhythm import RhythmPattern, TimeSignature
from composer.theory.harmony import VoiceLeader


class TestConstants:
    def test_note_names_count(self):
        assert len(NOTE_NAMES) == 12

    def test_note_name_to_midi_middle_c(self):
        assert note_name_to_midi("C", 4) == 60

    def test_note_name_to_midi_a440(self):
        assert note_name_to_midi("A", 4) == 69

    def test_midi_to_note_name_middle_c(self):
        note, octave = midi_to_note_name(60)
        assert note == "C"
        assert octave == 4

    def test_midi_to_note_name_roundtrip(self):
        for midi_num in [36, 48, 60, 72, 84]:
            note, octave = midi_to_note_name(midi_num)
            assert note_name_to_midi(note, octave) == midi_num

    def test_gm_instruments_range(self):
        for name, program in GM_INSTRUMENTS.items():
            assert 0 <= program <= 127, f"{name} has invalid program {program}"

    def test_gm_drums_range(self):
        for name, note in GM_DRUMS.items():
            assert 35 <= note <= 81, f"{name} has invalid note {note}"


class TestScales:
    def test_c_major_notes(self):
        scale = Scale("C", "major")
        notes = scale.get_notes()
        assert notes == ["C", "D", "E", "F", "G", "A", "B"]

    def test_a_minor_notes(self):
        scale = Scale("A", "natural_minor")
        notes = scale.get_notes()
        assert notes == ["A", "B", "C", "D", "E", "F", "G"]

    def test_scale_alias(self):
        scale = Scale("A", "minor")
        assert scale.scale_type == "natural_minor"

    def test_flat_root_conversion(self):
        scale = Scale("Bb", "major")
        assert scale.root == "A#"

    def test_midi_notes_c_major(self):
        scale = Scale("C", "major")
        midi = scale.get_midi_notes(octave=4, num_octaves=1)
        assert midi[0] == 60  # C4
        assert midi[-1] == 72  # C5
        assert len(midi) == 8

    def test_note_in_scale(self):
        scale = Scale("C", "major")
        assert scale.note_in_scale(60)  # C
        assert scale.note_in_scale(62)  # D
        assert not scale.note_in_scale(61)  # C#

    def test_degree_to_midi(self):
        scale = Scale("C", "major")
        assert scale.degree_to_midi(1, 4) == 60  # C4
        assert scale.degree_to_midi(3, 4) == 64  # E4
        assert scale.degree_to_midi(5, 4) == 67  # G4

    def test_is_minor(self):
        assert Scale("A", "natural_minor").is_minor()
        assert Scale("A", "harmonic_minor").is_minor()
        assert not Scale("C", "major").is_minor()

    def test_relative_major_minor(self):
        a_minor = Scale("A", "natural_minor")
        relative = a_minor.relative_major_or_minor()
        assert relative.root == "C"
        assert relative.scale_type == "major"

    def test_pitch_classes(self):
        scale = Scale("C", "major")
        pcs = scale.get_pitch_classes()
        assert 0 in pcs   # C
        assert 1 not in pcs  # C#
        assert 2 in pcs   # D

    def test_unknown_scale_raises(self):
        with pytest.raises(ValueError):
            Scale("C", "nonexistent_scale")

    def test_all_scale_patterns_valid(self):
        for name, pattern in SCALE_PATTERNS.items():
            assert sum(pattern) == 12 or name == "pentatonic_major" or name == "pentatonic_minor" or name == "blues", \
                f"Scale {name} intervals don't sum to 12: {sum(pattern)}"


class TestChords:
    def test_c_major_chord(self):
        chord = Chord("C", ChordType.MAJOR, octave=4)
        notes = chord.get_midi_notes()
        assert 60 in notes  # C
        assert 64 in notes  # E
        assert 67 in notes  # G

    def test_chord_name(self):
        assert Chord("C", ChordType.MAJOR).name == "C"
        assert Chord("A", ChordType.MINOR).name == "Am"
        assert Chord("G", ChordType.DOMINANT_7).name == "G7"
        assert Chord("D", ChordType.MINOR_7).name == "Dm7"

    def test_inversion(self):
        chord = Chord("C", ChordType.MAJOR, octave=4, inversion=1)
        notes = chord.get_midi_notes()
        # First inversion: E should be lowest
        assert notes[0] < notes[-1]

    def test_from_scale_degree(self):
        # I chord in C major = C major
        chord = Chord.from_scale_degree("C", 1, is_minor=False)
        assert chord.root == "C"
        assert chord.chord_type == ChordType.MAJOR

        # ii chord in C major = D minor
        chord = Chord.from_scale_degree("C", 2, is_minor=False)
        assert chord.root == "D"
        assert chord.chord_type == ChordType.MINOR

    def test_flat_root(self):
        chord = Chord("Bb", ChordType.MAJOR)
        assert chord.root == "A#"

    def test_chord_type_is_minor(self):
        assert ChordType.MINOR.is_minor()
        assert ChordType.MINOR_7.is_minor()
        assert not ChordType.MAJOR.is_minor()
        assert not ChordType.DOMINANT_7.is_minor()

    def test_open_voicing(self):
        chord = Chord("C", ChordType.MAJOR, octave=4, voicing="open")
        notes = chord.get_midi_notes()
        assert len(notes) == 3
        # Open voicing spreads notes wider
        assert notes[-1] - notes[0] > 7


class TestProgressions:
    def test_from_pattern(self):
        prog = ChordProgression.from_pattern("C", "pop_classic")
        assert len(prog.chords) == 4
        assert prog.degrees == [1, 5, 6, 4]

    def test_for_genre(self):
        prog = ChordProgression.for_genre("C", "jazz")
        assert len(prog.chords) >= 2

    def test_for_mood(self):
        prog = ChordProgression.for_mood("A", "epic")
        assert len(prog.chords) >= 2

    def test_transpose(self):
        prog = ChordProgression.from_pattern("C", "pop_classic")
        transposed = prog.transpose(7)  # Up a fifth
        assert transposed.chords[0].root == "G"

    def test_unknown_pattern_raises(self):
        with pytest.raises(ValueError):
            ChordProgression.from_pattern("C", "nonexistent_progression")


class TestRhythm:
    def test_time_signature(self):
        ts = TimeSignature(4, 4)
        assert ts.beats_per_measure == 4
        assert ts.measure_duration == 4.0

    def test_waltz_time(self):
        ts = TimeSignature(3, 4)
        assert ts.beats_per_measure == 3
        assert ts.measure_duration == 3.0

    def test_straight_quarters(self):
        pattern = RhythmPattern.straight_quarters()
        assert len(pattern.events) == 4
        assert pattern.events[0].position == 0.0
        assert pattern.events[0].duration == 1.0

    def test_straight_eighths(self):
        pattern = RhythmPattern.straight_eighths()
        assert len(pattern.events) == 8

    def test_whole_notes(self):
        pattern = RhythmPattern.whole_notes()
        assert len(pattern.events) == 1
        assert pattern.events[0].duration == 4.0


class TestHarmony:
    def test_smooth_transition(self):
        vl = VoiceLeader()
        current = [60, 64, 67]  # C major
        target = Chord("G", ChordType.MAJOR, octave=4)
        result = vl.smooth_transition(current, target)
        assert len(result) == 3
        # Notes should be close to original
        for c, r in zip(current, result):
            assert abs(c - r) <= 12

    def test_resolve_tension(self):
        vl = VoiceLeader()
        scale = Scale("C", "major")
        # C# should resolve to C or D
        resolved = vl.resolve_tension(61, scale)
        assert resolved in (60, 62)

    def test_passing_tones(self):
        vl = VoiceLeader()
        scale = Scale("C", "major")
        passing = vl.generate_passing_tones(60, 67, scale, max_passing=3)
        assert all(scale.note_in_scale(n) for n in passing)
