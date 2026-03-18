"""Parse text prompts into composition parameters."""

from __future__ import annotations

import re
from dataclasses import dataclass, field


# Keyword mappings for mood detection
MOOD_KEYWORDS = {
    "epic": ["epic", "grand", "massive", "powerful", "sweeping"],
    "melancholic": ["melancholic", "melancholy", "sad", "sorrowful", "mournful", "heartbreak", "lonely", "grief"],
    "heroic": ["heroic", "hero", "brave", "courageous", "triumphant", "victory", "glorious"],
    "mysterious": ["mysterious", "mystery", "enigmatic", "eerie", "strange", "curious", "haunting"],
    "romantic": ["romantic", "love", "tender", "gentle", "sweet", "affectionate", "passionate"],
    "dark": ["dark", "sinister", "ominous", "evil", "menacing", "grim", "foreboding", "doom"],
    "joyful": ["joyful", "happy", "cheerful", "bright", "upbeat", "playful", "fun", "celebratory"],
    "tense": ["tense", "tension", "suspense", "anxious", "urgent", "nervous", "intense"],
    "triumphant": ["triumphant", "triumph", "victorious", "majestic", "regal"],
    "peaceful": ["peaceful", "calm", "serene", "tranquil", "relaxing", "soothing", "gentle", "quiet"],
    "adventurous": ["adventure", "adventurous", "quest", "journey", "explore", "discovery"],
    "nostalgic": ["nostalgic", "nostalgia", "memories", "remembrance", "bittersweet", "wistful"],
    "angry": ["angry", "rage", "fury", "aggressive", "violent", "fierce", "brutal"],
    "dreamy": ["dreamy", "dream", "ethereal", "floating", "surreal", "hazy", "misty"],
    "suspenseful": ["suspenseful", "creepy", "thriller", "horror", "spooky", "chilling"],
    "uplifting": ["uplifting", "inspiring", "hopeful", "optimistic", "soaring", "elevating"],
}

# Genre keywords
GENRE_KEYWORDS = {
    "orchestral": ["orchestral", "orchestra", "symphonic", "symphony", "philharmonic"],
    "cinematic": ["cinematic", "film", "movie", "soundtrack", "ost", "score", "trailer"],
    "electronic": ["electronic", "edm", "synth", "synthwave", "techno", "house", "trance", "dubstep"],
    "jazz": ["jazz", "swing", "bebop", "smooth jazz", "fusion", "bossa nova"],
    "rock": ["rock", "alternative", "indie rock", "punk"],
    "metal": ["metal", "heavy metal", "death metal", "progressive metal", "thrash"],
    "classical": ["classical", "baroque", "romantic era", "concerto", "sonata", "fugue"],
    "ambient": ["ambient", "atmospheric", "soundscape", "drone", "new age", "meditation"],
    "folk": ["folk", "acoustic", "celtic", "country", "bluegrass"],
    "blues": ["blues", "delta blues", "chicago blues", "soul"],
    "rnb": ["r&b", "rnb", "rhythm and blues", "neo-soul", "motown"],
    "pop": ["pop", "dance pop", "synth pop", "indie pop"],
}

# Theme/setting keywords
THEME_KEYWORDS = {
    "battle": ["battle", "fight", "combat", "war", "clash", "duel"],
    "nature": ["nature", "forest", "ocean", "mountain", "river", "garden", "rain", "storm", "wind", "sea"],
    "space": ["space", "cosmic", "galaxy", "stellar", "nebula", "astral", "interstellar"],
    "medieval": ["medieval", "castle", "knight", "kingdom", "dungeon", "dragon", "fantasy"],
    "urban": ["urban", "city", "street", "downtown", "metropolitan", "neon"],
    "romance": ["romance", "wedding", "love story", "heartfelt"],
    "chase": ["chase", "pursuit", "running", "escape", "flight"],
    "celebration": ["celebration", "party", "festival", "carnival", "dance"],
    "lullaby": ["lullaby", "cradle", "nursery", "bedtime", "sleeping"],
    "march": ["march", "military", "parade", "procession"],
    "requiem": ["requiem", "funeral", "mourning", "memorial", "elegy"],
}

# Key detection patterns
KEY_PATTERN = re.compile(
    r'\b(?:key\s+(?:of\s+)?|in\s+)'
    r'([A-Ga-g][#b]?)\s*(major|minor|maj|min|m)?\b',
    re.IGNORECASE,
)

# Tempo keywords
TEMPO_KEYWORDS = {
    "very slow": (40, 60),
    "slow": (60, 80),
    "moderate": (80, 110),
    "medium": (90, 120),
    "fast": (120, 160),
    "very fast": (160, 200),
    "upbeat": (110, 140),
    "brisk": (120, 150),
    "lively": (130, 160),
    "frantic": (170, 220),
    "largo": (40, 60),
    "adagio": (55, 75),
    "andante": (73, 100),
    "allegro": (120, 156),
    "vivace": (156, 176),
    "presto": (176, 200),
}

# Instrument keywords
INSTRUMENT_KEYWORDS = {
    "piano": "acoustic_grand_piano",
    "guitar": "acoustic_guitar_nylon",
    "electric guitar": "electric_guitar_clean",
    "violin": "violin",
    "cello": "cello",
    "flute": "flute",
    "trumpet": "trumpet",
    "saxophone": "alto_sax",
    "sax": "alto_sax",
    "organ": "church_organ",
    "harp": "orchestral_harp",
    "strings": "string_ensemble_1",
    "brass": "brass_section",
    "choir": "choir_aahs",
    "synth": "lead_sawtooth",
    "pad": "pad_warm",
    "bass": "acoustic_bass",
    "electric bass": "electric_bass_finger",
    "oboe": "oboe",
    "clarinet": "clarinet",
    "bassoon": "bassoon",
    "trombone": "trombone",
    "tuba": "tuba",
    "french horn": "french_horn",
    "horn": "french_horn",
    "timpani": "timpani",
    "marimba": "marimba",
    "vibraphone": "vibraphone",
    "celesta": "celesta",
    "harpsichord": "harpsichord",
    "harmonica": "harmonica",
    "banjo": "banjo",
    "sitar": "sitar",
}

# Time signature patterns
TIME_SIG_PATTERN = re.compile(r'\b(\d)/(\d)\b')

# Duration patterns
DURATION_PATTERN = re.compile(
    r'(\d+)\s*(?:seconds?|secs?|s|minutes?|mins?|m)\b',
    re.IGNORECASE,
)


@dataclass
class CompositionParams:
    """Parameters extracted from a text prompt."""

    prompt: str = ""
    mood: str = "neutral"
    genre: str = "cinematic"
    theme: str = ""
    key: str = "C"
    scale_type: str = "major"
    tempo: int = 120
    time_signature: tuple[int, int] = (4, 4)
    duration_seconds: int = 120
    intensity: float = 0.7
    instruments: list[str] = field(default_factory=list)
    sections: list[str] = field(default_factory=list)

    # Derived parameters set by the style system
    use_seventh_chords: bool = False
    bass_style: str = "root"
    accompaniment_style: str = "block"
    melody_contour: str = "arch"
    drum_intensity: float = 0.7
    dynamic_curve: str = "arc"


class PromptParser:
    """Parses text prompts into CompositionParams."""

    def parse(self, prompt: str) -> CompositionParams:
        """Parse a text prompt into composition parameters."""
        params = CompositionParams(prompt=prompt)
        text = prompt.lower().strip()

        # Detect mood
        params.mood = self._detect_mood(text)

        # Detect genre
        params.genre = self._detect_genre(text)

        # Detect theme
        params.theme = self._detect_theme(text)

        # Detect key
        key_match = KEY_PATTERN.search(prompt)
        if key_match:
            params.key = key_match.group(1).upper()
            quality = (key_match.group(2) or "").lower()
            if quality in ("minor", "min", "m"):
                params.scale_type = "natural_minor"
            else:
                params.scale_type = "major"
        else:
            # Infer from mood
            params.scale_type = self._infer_scale(params.mood)
            if params.scale_type in ("natural_minor", "harmonic_minor", "dorian", "phrygian"):
                params.key = self._pick_minor_key()
            else:
                params.key = self._pick_major_key()

        # Detect tempo
        params.tempo = self._detect_tempo(text, params.mood, params.genre)

        # Detect time signature
        ts_match = TIME_SIG_PATTERN.search(text)
        if ts_match:
            params.time_signature = (int(ts_match.group(1)), int(ts_match.group(2)))
        elif "waltz" in text or "3/4" in text:
            params.time_signature = (3, 4)
        elif "6/8" in text or "compound" in text:
            params.time_signature = (6, 8)

        # Detect duration
        dur_match = DURATION_PATTERN.search(text)
        if dur_match:
            val = int(dur_match.group(1))
            unit = dur_match.group(0).lower()
            if "min" in unit or "m" == unit[-1]:
                params.duration_seconds = val * 60
            else:
                params.duration_seconds = val

        # Detect instruments
        params.instruments = self._detect_instruments(text)

        # Detect intensity
        params.intensity = self._detect_intensity(text, params.mood)

        return params

    def _detect_mood(self, text: str) -> str:
        best_mood = "neutral"
        best_score = 0
        for mood, keywords in MOOD_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text)
            if score > best_score:
                best_score = score
                best_mood = mood
        return best_mood

    def _detect_genre(self, text: str) -> str:
        best_genre = "cinematic"
        best_score = 0
        for genre, keywords in GENRE_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text)
            if score > best_score:
                best_score = score
                best_genre = genre
        return best_genre

    def _detect_theme(self, text: str) -> str:
        for theme, keywords in THEME_KEYWORDS.items():
            if any(kw in text for kw in keywords):
                return theme
        return ""

    def _detect_tempo(self, text: str, mood: str, genre: str) -> int:
        import random

        # Check for explicit BPM
        bpm_match = re.search(r'(\d{2,3})\s*bpm', text, re.IGNORECASE)
        if bpm_match:
            return int(bpm_match.group(1))

        # Check tempo keywords
        for keyword, (low, high) in TEMPO_KEYWORDS.items():
            if keyword in text:
                return random.randint(low, high)

        # Infer from mood
        mood_tempos = {
            "epic": (120, 160),
            "melancholic": (60, 80),
            "heroic": (120, 150),
            "mysterious": (70, 100),
            "romantic": (70, 90),
            "dark": (80, 120),
            "joyful": (120, 140),
            "tense": (100, 140),
            "triumphant": (110, 140),
            "peaceful": (60, 80),
            "adventurous": (110, 140),
            "nostalgic": (75, 100),
            "angry": (130, 170),
            "dreamy": (65, 85),
            "suspenseful": (80, 110),
            "uplifting": (110, 135),
        }

        if mood in mood_tempos:
            low, high = mood_tempos[mood]
            return random.randint(low, high)

        return 120

    def _detect_instruments(self, text: str) -> list[str]:
        found = []
        # Check longer keywords first to avoid partial matches
        sorted_keywords = sorted(INSTRUMENT_KEYWORDS.keys(), key=len, reverse=True)
        for keyword in sorted_keywords:
            if keyword in text:
                found.append(INSTRUMENT_KEYWORDS[keyword])
        return found

    def _detect_intensity(self, text: str, mood: str) -> float:
        if any(w in text for w in ["soft", "quiet", "gentle", "delicate", "subtle"]):
            return 0.3
        if any(w in text for w in ["loud", "powerful", "massive", "intense", "heavy"]):
            return 0.9
        if any(w in text for w in ["moderate", "medium"]):
            return 0.6

        mood_intensity = {
            "epic": 0.85, "angry": 0.9, "tense": 0.75, "heroic": 0.8,
            "dark": 0.7, "joyful": 0.7, "melancholic": 0.4, "peaceful": 0.3,
            "romantic": 0.5, "mysterious": 0.5, "dreamy": 0.35,
            "triumphant": 0.85, "adventurous": 0.75, "suspenseful": 0.6,
        }
        return mood_intensity.get(mood, 0.6)

    def _infer_scale(self, mood: str) -> str:
        minor_moods = {
            "melancholic", "dark", "mysterious", "tense", "angry",
            "suspenseful", "epic",
        }
        modal_moods = {
            "mysterious": "dorian",
            "dreamy": "lydian",
        }
        if mood in modal_moods:
            return modal_moods[mood]
        if mood in minor_moods:
            return "natural_minor"
        return "major"

    def _pick_minor_key(self) -> str:
        import random
        return random.choice(["A", "D", "E", "C", "G", "B", "F#"])

    def _pick_major_key(self) -> str:
        import random
        return random.choice(["C", "G", "D", "F", "A", "Bb", "Eb"])
