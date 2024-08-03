from pretty_midi import PrettyMIDI, Instrument, Note
from abc import abstractmethod
import pretty_midi


class _AbstractConvert:
    def __init__(self, directory: str, midi_data: PrettyMIDI = None):
        self.dir = directory
        self.isError = False

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
