
from pretty_midi import PrettyMIDI, Instrument, Note
from abc import abstractmethod, ABC
import music21 as m21
import music21


def get_key_number(key):
    if key == "C":
        return 0
    if key == "C#" or key == "D-":
        return 1
    if key == "D":
        return 2
    if key == "D#" or key == "E-":
        return 3
    if key == "E":
        return 4
    if key == "F":
        return 5
    if key == "F#" or key == "G-":
        return 6
    if key == "G":
        return 7
    if key == "G#" or key == "A-":
        return 8
    if key == "A":
        return 9
    if key == "A#" or key == "B-":
        return 10
    if key == "B":
        return 11


class _AbstractConvert:
    def __init__(self, directory: str, midi_data):
        self.dir = directory
        self.is_Error = False

        if midi_data is None:
            self.midi_data = PrettyMIDI(directory)
        else:
            self.midi_data = midi_data
        pass

    @abstractmethod
    def convert(self):
        pass


class ConvTempo(_AbstractConvert):
    def __init__(self, directory: str, change_tempo: int, midi_data=None):
        super().__init__(directory, midi_data)
        self.change_tempo = change_tempo

    def convert(self):
        origin = self.midi_data.get_tempo_changes()[1][0]

        tempo_ratio = origin / self.change_tempo
        for instrument in self.midi_data.instruments:
            for note in instrument.notes:
                note.start *= tempo_ratio
                note.end *= tempo_ratio


class ConvKey(_AbstractConvert):

    def __init__(self, directory: str, key, midi_data: PrettyMIDI = None):
        super().__init__(directory, midi_data)
        self.key = get_key_number(key)

    def convert(self):
        try:
            score = m21.converter.parse(self.dir)
            key = score.analyze("key").tonic.name
            now_key_number = get_key_number(key)
            transpose_number = abs(now_key_number - self.key)
            for inst in self.midi_data.instruments:
                if not inst.is_drum:
                    for note in inst.notes:
                        note.pitch -= transpose_number
        except AttributeError:
            print(f"{self.dir}が移調できませんでした。")
            self.is_Error = True
        except music21.midi.MidiException:
            self.is_Error = True
            print(f"{self.dir}が移調できませんでした。")
        except music21.converter.ConverterFileException:
            self.is_Error = True
            print(f"{self.dir}が移調できませんでした")
        except music21.exceptions21.StreamException:
            self.is_Error = True
            print(f"{self.dir}が移調できませんでした")
        pass

