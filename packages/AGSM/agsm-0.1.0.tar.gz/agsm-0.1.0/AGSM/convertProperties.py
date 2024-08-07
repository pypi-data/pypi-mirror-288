import convert
from pretty_midi.pretty_midi import PrettyMIDI


class ConvertProperties:
    def __init__(self, directory: str):
        self.properties = []
        self.isError = False
        self.directory = directory
        try:
            self.midi_data = PrettyMIDI(directory)
        except OSError:
            print(f"{directory}を読み込むことができません")
            self.isError = True
        except IndexError:
            print(f"{directory}を読み込むことができません")
            self.isError = True
        except AttributeError:
            print(f"{directory}を読み込むことができません")
            self.isError = True

    def change_tempo(self, tempo):
        self.properties.append(convert.ConvTempo(directory=self.directory, midi_data=self.midi_data,  change_tempo=tempo))
        return self

    def change_key(self, key: str):
        self.properties.append(convert.ConvKey(directory=self.directory, midi_data=self.midi_data, key=key))
        return self

    def convert(self):
        for c in self.properties:
            c.convert()

        return self.midi_data
