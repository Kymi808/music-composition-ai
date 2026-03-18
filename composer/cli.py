"""Command-line interface for the music composer."""

from __future__ import annotations

import sys
from pathlib import Path

import click

from composer import __version__


@click.command()
@click.argument("prompt", required=False)
@click.option("--key", "-k", default=None, help="Musical key (e.g., C, Dm, F#)")
@click.option("--tempo", "-t", type=int, default=None, help="Tempo in BPM")
@click.option("--duration", "-d", type=int, default=120, help="Duration in seconds")
@click.option("--genre", "-g", default=None, help="Genre (orchestral, jazz, electronic, etc.)")
@click.option("--mood", "-m", default=None, help="Mood/vibe (epic, melancholic, heroic, etc.)")
@click.option("--output", "-o", default=None, help="Output file path (without extension)")
@click.option(
    "--format", "-f", "formats",
    multiple=True,
    default=("midi",),
    type=click.Choice(["midi", "wav", "mp3"], case_sensitive=False),
    help="Output format(s)",
)
@click.option("--time-sig", default=None, help="Time signature (e.g., 4/4, 3/4)")
@click.option("--intensity", type=float, default=None, help="Intensity 0.0-1.0")
@click.option("--seed", type=int, default=None, help="Random seed for reproducibility")
@click.option("--list-moods", is_flag=True, help="List available moods")
@click.option("--list-genres", is_flag=True, help="List available genres")
@click.option("--list-instruments", is_flag=True, help="List available instruments")
@click.option("--check-deps", is_flag=True, help="Check audio rendering dependencies")
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
@click.version_option(__version__)
def main(
    prompt: str | None,
    key: str | None,
    tempo: int | None,
    duration: int,
    genre: str | None,
    mood: str | None,
    output: str | None,
    formats: tuple[str, ...],
    time_sig: str | None,
    intensity: float | None,
    seed: int | None,
    list_moods: bool,
    list_genres: bool,
    list_instruments: bool,
    check_deps: bool,
    verbose: bool,
) -> None:
    """Generate music from text prompts.

    PROMPT is a text description of the music you want to create.

    Examples:

    \b
      composer "epic orchestral battle theme"
      composer "melancholic piano ballad in D minor" -f midi wav
      composer "jazz trio improvisation" --tempo 140 --duration 180
      composer "cinematic trailer music" -g cinematic -m epic -f wav mp3
    """
    # Handle list commands
    if list_moods:
        from composer.moods.mood import MoodLibrary
        click.echo("Available moods:")
        for mood_name in MoodLibrary.list_moods():
            m = MoodLibrary.get(mood_name)
            click.echo(f"  {mood_name:15s} - {m.description}")
        return

    if list_genres:
        from composer.styles.library import StyleLibrary
        click.echo("Available genres:")
        for genre_name in StyleLibrary.list_styles():
            click.echo(f"  {genre_name}")
        return

    if list_instruments:
        from composer.instruments.registry import InstrumentRegistry
        click.echo("Available instruments:")
        for name in InstrumentRegistry.list_all():
            click.echo(f"  {name.replace('_', ' ')}")
        return

    if check_deps:
        from composer.rendering.audio_renderer import AudioRenderer
        deps = AudioRenderer.check_dependencies()
        click.echo("Audio rendering dependencies:")
        for dep, available in deps.items():
            status = click.style("OK", fg="green") if available else click.style("MISSING", fg="red")
            click.echo(f"  {dep:20s} {status}")
        return

    if not prompt:
        click.echo("Error: Please provide a prompt or use --help for options.", err=True)
        click.echo('Example: composer "epic orchestral battle theme"', err=True)
        sys.exit(1)

    # Set random seed
    if seed is not None:
        import random
        random.seed(seed)

    # Build overrides
    overrides: dict = {}
    if key:
        # Parse key like "Dm" or "F# minor"
        key_str = key.rstrip("m").rstrip(" ")
        if key.endswith("m") or "minor" in key.lower():
            overrides["key"] = key_str
            overrides["scale_type"] = "natural_minor"
        else:
            overrides["key"] = key_str
    if tempo:
        overrides["tempo"] = tempo
    if duration:
        overrides["duration_seconds"] = duration
    if genre:
        overrides["genre"] = genre
    if mood:
        overrides["mood"] = mood
    if intensity is not None:
        overrides["intensity"] = intensity
    if time_sig:
        parts = time_sig.split("/")
        if len(parts) == 2:
            overrides["time_signature"] = (int(parts[0]), int(parts[1]))

    # Generate composition
    click.echo(f"Composing: {prompt}")
    if verbose:
        click.echo(f"  Overrides: {overrides}")

    from composer.core.composition import Composition
    composition = Composition.from_prompt(prompt, **overrides)

    if verbose:
        click.echo(composition.summary())

    # Determine output path
    if output is None:
        # Generate from prompt
        safe_name = "".join(c if c.isalnum() or c in " -_" else "" for c in prompt)
        safe_name = safe_name.strip().replace(" ", "_")[:50]
        output = f"output/{safe_name}"

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Render outputs
    from composer.rendering.midi_renderer import MidiRenderer
    from composer.rendering.audio_renderer import AudioRenderer

    rendered_files = []

    if "midi" in formats:
        midi_path = MidiRenderer.render(
            tracks=composition.tracks,
            tempo=composition.tempo,
            time_signature=composition.time_signature,
            output_path=output_path.with_suffix(".mid"),
        )
        rendered_files.append(midi_path)
        click.echo(f"  MIDI: {midi_path}")

    if "wav" in formats or "mp3" in formats:
        # Need MIDI file first
        midi_path = output_path.with_suffix(".mid")
        if not midi_path.exists():
            midi_path = MidiRenderer.render(
                tracks=composition.tracks,
                tempo=composition.tempo,
                time_signature=composition.time_signature,
                output_path=midi_path,
            )

        renderer = AudioRenderer()

        if "wav" in formats:
            try:
                wav_path = renderer.render_wav(midi_path, output_path.with_suffix(".wav"))
                rendered_files.append(wav_path)
                click.echo(f"  WAV:  {wav_path}")
            except Exception as e:
                click.echo(f"  WAV:  Failed - {e}", err=True)

        if "mp3" in formats:
            try:
                mp3_path = renderer.render_mp3(midi_path, output_path.with_suffix(".mp3"))
                rendered_files.append(mp3_path)
                click.echo(f"  MP3:  {mp3_path}")
            except Exception as e:
                click.echo(f"  MP3:  Failed - {e}", err=True)

    # Print summary
    click.echo()
    click.echo(composition.summary())
    click.echo()
    click.echo(f"Generated {len(rendered_files)} file(s).")


if __name__ == "__main__":
    main()
