# Reimportar las bibliotecas necesarias para asegurar la funcionalidad
from mido import MidiFile, MidiTrack, Message

# Crear un archivo MIDI básico con un patrón rítmico constante basado en un tempo estimado
tempo = 105  # Tempo en BPM
ticks_per_beat = 480  # Resolución MIDI típica
microseconds_per_beat = int(60 * 1e6 / tempo)

# Crear el archivo MIDI
simple_midi = MidiFile(ticks_per_beat=ticks_per_beat)
track = MidiTrack()
simple_midi.tracks.append(track)

# Configurar el tempo en el archivo MIDI
track.append(Message('set_tempo', tempo=microseconds_per_beat, time=0))

# Crear un patrón básico de batería (kick y snare alternados)
pattern_duration = 240  # Duración de cada nota en ticks (1/2 de un beat)
kick_note = 36  # Nota MIDI para el kick drum
snare_note = 38  # Nota MIDI para el snare drum

# Generar 4 compases de ritmo básico
for i in range(16):  # 4 compases con 4 beats cada uno
    # Kick en los beats 1 y 3
    if i % 4 == 0 or i % 4 == 2:
        track.append(Message('note_on', note=kick_note, velocity=100, time=0))
        track.append(Message('note_off', note=kick_note, velocity=100, time=pattern_duration))
    # Snare en los beats 2 y 4
    elif i % 4 == 1 or i % 4 == 3:
        track.append(Message('note_on', note=snare_note, velocity=100, time=0))
        track.append(Message('note_off', note=snare_note, velocity=100, time=pattern_duration))

# Guardar el archivo MIDI
simple_midi_output_path = "/mnt/data/simple_beat.mid"
simple_midi.save(simple_midi_output_path)

simple_midi_output_path
