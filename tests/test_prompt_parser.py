"""Tests for the prompt parser."""

from composer.core.prompt_parser import PromptParser, CompositionParams


class TestPromptParser:
    def setup_method(self):
        self.parser = PromptParser()

    def test_basic_parse(self):
        params = self.parser.parse("epic orchestral battle theme")
        assert params.mood == "epic"
        assert params.genre == "orchestral"
        assert params.theme == "battle"

    def test_key_detection(self):
        params = self.parser.parse("piano piece in D minor")
        assert params.key == "D"
        assert params.scale_type == "natural_minor"

    def test_key_detection_major(self):
        params = self.parser.parse("song in key of G major")
        assert params.key == "G"
        assert params.scale_type == "major"

    def test_tempo_bpm(self):
        params = self.parser.parse("fast piece at 160 bpm")
        assert params.tempo == 160

    def test_tempo_keyword(self):
        params = self.parser.parse("slow melancholic ballad")
        assert params.tempo <= 100

    def test_genre_detection(self):
        params = self.parser.parse("jazz trio improvisation")
        assert params.genre == "jazz"

    def test_electronic_genre(self):
        params = self.parser.parse("electronic synth dance track")
        assert params.genre == "electronic"

    def test_mood_detection(self):
        params = self.parser.parse("dark sinister theme")
        assert params.mood == "dark"

    def test_peaceful_mood(self):
        params = self.parser.parse("peaceful calm meditation music")
        assert params.mood == "peaceful"

    def test_instrument_detection(self):
        params = self.parser.parse("piano and violin duet")
        assert "acoustic_grand_piano" in params.instruments
        assert "violin" in params.instruments

    def test_time_signature(self):
        params = self.parser.parse("waltz in 3/4")
        assert params.time_signature == (3, 4)

    def test_intensity_soft(self):
        params = self.parser.parse("soft gentle lullaby")
        assert params.intensity < 0.5

    def test_intensity_loud(self):
        params = self.parser.parse("loud powerful anthem")
        assert params.intensity > 0.7

    def test_theme_detection(self):
        params = self.parser.parse("medieval castle fantasy theme")
        assert params.theme == "medieval"

    def test_space_theme(self):
        params = self.parser.parse("cosmic space exploration soundtrack")
        assert params.theme == "space"

    def test_defaults(self):
        params = self.parser.parse("some music")
        assert params.duration_seconds == 120
        assert params.time_signature == (4, 4)

    def test_duration_seconds(self):
        params = self.parser.parse("30 second jingle")
        assert params.duration_seconds == 30

    def test_duration_minutes(self):
        params = self.parser.parse("3 minute song")
        assert params.duration_seconds == 180
