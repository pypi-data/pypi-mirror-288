from convert import ConvTempo
from pretty_midi import PrettyMIDI, Instrument

midi = PrettyMIDI("./AgeOfAquarius.mid")
conv = ConvTempo("./AgeOfAquarius.mid", 120)
conv.convert()

print(midi.instruments[0].notes[0:10])
print(conv.midi_data.instruments[0].notes[0:10])
