"""Tests for music generators."""

import random

from composer.theory.scales import Scale
from composer.theory.chords import Chord, ChordType
from composer.theory.rhythm import TimeSignature
from composer.generators.melody import MelodyGenerator
from composer.generators.bass import BassGenerator
from composer.generators.drums import DrumGenerator
from composer.generators.accompaniment import AccompanimentGenerator
from composer.generators.orchestrator import Orchestrator


class TestMelodyGenerator:
    def setup_method(self):
        random.seed(42)
        self.scale = Scale("C", "major")
        self.gen = MelodyGenerator(scale=self.scale)

    def test_generate_produces_notes(self):
        chords = [
            Chord("C", ChordType.MAJOR, octave=4),
            Chord("G", ChordType.MAJOR, octave=4),
            Chord("A", ChordType.MINOR, octave=4),
            Chord("F", ChordType.MAJOR, octave=4),
        ]
        melody = self.gen.generate(chords, beats_per_chord=4.0)
        assert len(melody) > 0

    def test_notes_in_range(self):
        chords = [Chord("C", ChordType.MAJOR, octave=4)]
        melody = self.gen.generate(chords, beats_per_chord=4.0)
        for note in melody:
            assert self.gen.note_range[0] <= note.pitch <= self.gen.note_range[1]

    def test_notes_mostly_in_scale(self):
        chords = [
            Chord("C", ChordType.MAJOR, octave=4),
            Chord("F", ChordType.MAJOR, octave=4),
        ]
        melody = self.gen.generate(chords, beats_per_chord=4.0)
        in_scale = sum(1 for n in melody if self.scale.note_in_scale(n.pitch))
        assert in_scale / len(melody) > 0.8  # At least 80% in scale

    def test_generate_motif(self):
        motif = self.gen.generate_motif(length=4)
        assert len(motif) == 4

    def test_develop_motif_sequence(self):
        motif = self.gen.generate_motif(length=4)
        developed = self.gen.develop_motif(motif, technique="sequence", interval=2)
        assert len(developed) == len(motif)

    def test_develop_motif_inversion(self):
        motif = self.gen.generate_motif(length=4)
        developed = self.gen.develop_motif(motif, technique="inversion")
        assert len(developed) == len(motif)

    def test_develop_motif_retrograde(self):
        motif = self.gen.generate_motif(length=4)
        developed = self.gen.develop_motif(motif, technique="retrograde")
        assert len(developed) == len(motif)

    def test_velocity_range(self):
        chords = [Chord("C", ChordType.MAJOR, octave=4)]
        melody = self.gen.generate(chords, beats_per_chord=4.0)
        for note in melody:
            assert 1 <= note.velocity <= 127


class TestBassGenerator:
    def setup_method(self):
        random.seed(42)
        self.scale = Scale("C", "major")

    def test_root_bass(self):
        gen = BassGenerator(scale=self.scale, style="root")
        chords = [Chord("C", ChordType.MAJOR, octave=3)]
        notes = gen.generate(chords, beats_per_chord=4.0)
        assert len(notes) > 0

    def test_walking_bass(self):
        gen = BassGenerator(scale=self.scale, style="walking")
        chords = [
            Chord("C", ChordType.MAJOR, octave=3),
            Chord("G", ChordType.MAJOR, octave=3),
        ]
        notes = gen.generate(chords, beats_per_chord=4.0)
        assert len(notes) >= 8  # At least quarter notes

    def test_ostinato_bass(self):
        gen = BassGenerator(scale=self.scale, style="ostinato")
        chords = [Chord("C", ChordType.MAJOR, octave=3)]
        notes = gen.generate(chords, beats_per_chord=4.0)
        assert len(notes) > 4

    def test_bass_in_range(self):
        gen = BassGenerator(scale=self.scale, style="root")
        chords = [Chord("C", ChordType.MAJOR, octave=3)]
        notes = gen.generate(chords, beats_per_chord=4.0)
        for note in notes:
            assert gen.note_range[0] <= note.pitch <= gen.note_range[1]


class TestDrumGenerator:
    def setup_method(self):
        random.seed(42)

    def test_rock_drums(self):
        gen = DrumGenerator(genre="rock")
        notes = gen.generate(num_measures=4)
        assert len(notes) > 0

    def test_jazz_drums(self):
        gen = DrumGenerator(genre="jazz")
        notes = gen.generate(num_measures=4)
        assert len(notes) > 0

    def test_electronic_drums(self):
        gen = DrumGenerator(genre="electronic")
        notes = gen.generate(num_measures=4)
        assert len(notes) > 0

    def test_drum_fill(self):
        gen = DrumGenerator(genre="rock")
        notes = gen.generate(num_measures=4, fill_every=4)
        assert len(notes) > 0

    def test_drum_velocity_range(self):
        gen = DrumGenerator(genre="rock")
        notes = gen.generate(num_measures=4)
        for note in notes:
            assert 1 <= note.velocity <= 127

    def test_buildup(self):
        gen = DrumGenerator(genre="rock")
        notes = gen.generate_buildup(start=0.0, duration=4.0)
        assert len(notes) > 0
        # Velocities should generally increase
        velocities = [n.velocity for n in notes]
        assert velocities[-1] >= velocities[0]


class TestAccompanimentGenerator:
    def setup_method(self):
        random.seed(42)
        self.scale = Scale("C", "major")

    def test_block_chords(self):
        gen = AccompanimentGenerator(scale=self.scale, style="block")
        chords = [Chord("C", ChordType.MAJOR, octave=4)]
        notes = gen.generate(chords, beats_per_chord=4.0)
        assert len(notes) > 0

    def test_arpeggiated(self):
        gen = AccompanimentGenerator(scale=self.scale, style="arpeggio")
        chords = [Chord("C", ChordType.MAJOR, octave=4)]
        notes = gen.generate(chords, beats_per_chord=4.0)
        assert len(notes) > 3  # More notes than block chords

    def test_alberti(self):
        gen = AccompanimentGenerator(scale=self.scale, style="alberti")
        chords = [Chord("C", ChordType.MAJOR, octave=4)]
        notes = gen.generate(chords, beats_per_chord=4.0)
        assert len(notes) >= 4

    def test_pad(self):
        gen = AccompanimentGenerator(scale=self.scale, style="pad")
        chords = [Chord("C", ChordType.MAJOR, octave=4)]
        notes = gen.generate(chords, beats_per_chord=4.0)
        # Pad notes should be sustained
        for note in notes:
            assert note.duration >= 3.0


class TestOrchestrator:
    def setup_method(self):
        random.seed(42)

    def test_orchestrate_creates_tracks(self):
        orch = Orchestrator(intensity=0.7)
        melody = [__import__("composer.generators.melody", fromlist=["NoteEvent"]).NoteEvent(60, 0, 1, 80)]
        bass = [__import__("composer.generators.melody", fromlist=["NoteEvent"]).NoteEvent(36, 0, 1, 80)]
        drums = [__import__("composer.generators.melody", fromlist=["NoteEvent"]).NoteEvent(36, 0, 0.1, 90)]
        acc = [__import__("composer.generators.melody", fromlist=["NoteEvent"]).NoteEvent(60, 0, 4, 70)]

        palette = {"melody": 0, "accompaniment": 48, "bass": 32}
        tracks = orch.orchestrate(melody, bass, drums, acc, palette, 4.0)
        assert len(tracks) >= 3  # Melody, bass, drums at minimum
