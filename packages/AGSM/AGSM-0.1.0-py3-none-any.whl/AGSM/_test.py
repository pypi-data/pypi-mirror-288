from convert import ConvTempo, ConvKey
from pretty_midi import PrettyMIDI, Instrument

midi = PrettyMIDI("./4thAvenueTheme.mid")
conv = ConvKey("./4thAvenueTheme.mid", "C")
conv.convert()

print(midi.instruments[0].notes[0:10])
print(conv.midi_data.instruments[0].notes[0:10])
