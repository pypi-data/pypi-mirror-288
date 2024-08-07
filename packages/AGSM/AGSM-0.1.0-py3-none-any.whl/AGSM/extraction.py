from abc import abstractmethod
from pretty_midi import PrettyMIDI, Instrument, Note


class _AbstractExtraction:
    def __init__(self, directory: str, midi_data: PrettyMIDI = None):
        self.directory = directory
        self.isError = False

        if midi_data is None:
            self.midi_data = PrettyMIDI(directory)
        else:
            self.midi_data = midi_data

    @abstractmethod
    def extract(self):
        pass


class CodeExtraction(_AbstractExtraction):

    def __init__(self, directory: str, calc_beat: int):
        super().__init__(directory)
        self.cb = calc_beat

    def extract(self):
        pass
