"""Audio rendering - MIDI to WAV/MP3 via FluidSynth."""

from __future__ import annotations

import subprocess
import shutil
from pathlib import Path

from composer.config import config


class AudioRenderer:
    """Renders MIDI files to audio using FluidSynth."""

    def __init__(self, soundfont_path: str | Path | None = None):
        self.soundfont_path = Path(soundfont_path) if soundfont_path else config.soundfont_path

    def render_wav(self, midi_path: str | Path, output_path: str | Path) -> Path:
        """Render a MIDI file to WAV.

        Tries multiple methods in order:
        1. midi2audio (Python library)
        2. fluidsynth CLI
        3. pretty_midi built-in synthesizer (fallback, lower quality)
        """
        midi_path = Path(midi_path)
        output_path = Path(output_path)
        if not output_path.suffix:
            output_path = output_path.with_suffix(".wav")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Try midi2audio first
        if self.soundfont_path and self.soundfont_path.exists():
            try:
                return self._render_midi2audio(midi_path, output_path)
            except Exception:
                pass

            # Try fluidsynth CLI
            try:
                return self._render_fluidsynth_cli(midi_path, output_path)
            except Exception:
                pass

        # Fallback: pretty_midi synthesize (sine wave, low quality but always works)
        return self._render_pretty_midi(midi_path, output_path)

    def render_mp3(self, midi_path: str | Path, output_path: str | Path) -> Path:
        """Render a MIDI file to MP3 (requires WAV first, then converts)."""
        output_path = Path(output_path)
        if not output_path.suffix:
            output_path = output_path.with_suffix(".mp3")

        # First render WAV
        wav_path = output_path.with_suffix(".wav")
        self.render_wav(midi_path, wav_path)

        # Convert WAV to MP3 using pydub
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_wav(str(wav_path))
            audio.export(str(output_path), format="mp3")
            wav_path.unlink(missing_ok=True)  # Clean up WAV
            return output_path
        except Exception as e:
            # Try ffmpeg directly
            if shutil.which("ffmpeg"):
                subprocess.run(
                    ["ffmpeg", "-y", "-i", str(wav_path), "-q:a", "2", str(output_path)],
                    capture_output=True,
                    check=True,
                )
                wav_path.unlink(missing_ok=True)
                return output_path
            raise RuntimeError(
                f"Cannot convert to MP3. Install pydub + ffmpeg. WAV saved at {wav_path}"
            ) from e

    def _render_midi2audio(self, midi_path: Path, output_path: Path) -> Path:
        """Render using midi2audio library."""
        from midi2audio import FluidSynth
        fs = FluidSynth(str(self.soundfont_path), sample_rate=config.sample_rate)
        fs.midi_to_audio(str(midi_path), str(output_path))
        return output_path

    def _render_fluidsynth_cli(self, midi_path: Path, output_path: Path) -> Path:
        """Render using fluidsynth command line."""
        if not shutil.which("fluidsynth"):
            raise RuntimeError("fluidsynth not found in PATH")

        cmd = [
            "fluidsynth",
            "-ni",
            str(self.soundfont_path),
            str(midi_path),
            "-F", str(output_path),
            "-r", str(config.sample_rate),
        ]
        subprocess.run(cmd, capture_output=True, check=True)
        return output_path

    def _render_pretty_midi(self, midi_path: Path, output_path: Path) -> Path:
        """Fallback: render using pretty_midi's built-in synthesizer (sine waves)."""
        import numpy as np
        import pretty_midi

        midi = pretty_midi.PrettyMIDI(str(midi_path))
        audio = midi.synthesize(fs=config.sample_rate)

        # Normalize
        if audio.max() > 0:
            audio = audio / audio.max() * 0.9

        # Convert to 16-bit PCM WAV
        import wave
        audio_16bit = (audio * 32767).astype(np.int16)

        with wave.open(str(output_path), "w") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(config.sample_rate)
            wav_file.writeframes(audio_16bit.tobytes())

        return output_path

    @staticmethod
    def check_dependencies() -> dict[str, bool]:
        """Check which audio rendering dependencies are available."""
        available = {}

        try:
            import midi2audio  # noqa: F401
            available["midi2audio"] = True
        except ImportError:
            available["midi2audio"] = False

        available["fluidsynth_cli"] = shutil.which("fluidsynth") is not None

        try:
            import pydub  # noqa: F401
            available["pydub"] = True
        except ImportError:
            available["pydub"] = False

        available["ffmpeg"] = shutil.which("ffmpeg") is not None

        return available
