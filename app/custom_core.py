from discord.sinks.core import Filters, Sink, default_filters
from pydub import AudioSegment
from queue import Queue
import numpy as np


from transcription.model import Whisper

# for testing purpose only
wm = Whisper()


class StreamSink(Sink):
    def __init__(self, *, filters=None):
        if filters is None:
            filters = default_filters
        self.filters = filters
        Filters.__init__(self, **self.filters)
        self.vc = None
        self.audio_data = {}

        # user id for parsing their specific audio data
        self.user_id = None

        # obj to store our super sweet awesome audio data
        self.buffer = StreamBuffer()

    def write(self, data, user):
        # we overload the write method to take advantage of the already running thread for recording

        # if the data comes from the inviting user, we append it to buffer
        if user == self.user_id:
            self.buffer.write(data=data, user=user)

    def cleanup(self):
        self.finished = True

    def get_all_audio(self):
        # not applicable for streaming but may cause errors if not overloaded
        pass

    def get_user_audio(self, user):
        # not applicable for streaming but will def cause errors if not overloaded called
        pass

    def set_user(self, user_id: int):
        self.user_id = user_id
        print(f"Set user ID: {user_id}")


class StreamBuffer:
    def __init__(self, sample_width: int = 2, channels: int = 2, sample_rate: int = 48000, block_len: int = 2) -> None:
        # holds byte-form audio data as it builds
        self.byte_buffer = bytearray()  # bytes
        self.segment_buffer = Queue()  # pydub.AudioSegments - temporary

        # audio data specifications
        self.sample_width = sample_width
        self.channels = channels
        self.sample_rate = sample_rate

        self.block_len = block_len  # how long you want each audio block to be in seconds

        # min len to pull bytes from buffer
        self.buff_lim = sample_width * channels * sample_rate * block_len

        # var for tracking order of exported audio
        self.ct = 1  # temporary

    # will need 'user' param if tracking multiple peoples voices - TBD
    def write(self, data, user) -> None:

        self.byte_buffer += data  # data is a bytearray object
        # checking amount of data in the buffer
        if len(self.byte_buffer) > self.buff_lim:

            # grabbing slice from the buffer to work with
            byte_slice = self.byte_buffer[:self.buff_lim]

            # # creating AudioSegment object with the slice
            # audio_segment = AudioSegment(data=byte_slice,
            #                              sample_width=self.sample_width,
            #                              frame_rate=self.sample_rate,
            #                              channels=self.channels,
            #                              )

            byte_nda = self.byte_to_nda(byte_array=byte_slice)

            print(wm.generate(byte_nda))

            # removing the old stinky trash data from buffer - ew get it out of there already
            self.byte_buffer = self.byte_buffer[self.buff_lim:]
            # ok much better now

            # # adding AudioSegment to the queue
            # self.segment_buffer.put(audio_segment)

            # # temporary for validating process
            # self.export_mp3(audio_segment=audio_segment)

    def byte_to_nda(self, byte_array: bytearray) -> np.ndarray(dtype=np.float32):

        # Convert the audio data bytearray to a NumPy array
        audio_array = np.frombuffer(byte_array, dtype=np.int16)

        # Reshape the audio array to match the number of channels
        audio_array = audio_array.reshape((-1, self.channels))

        # Normalize the audio data to the range [-1.0, 1.0]
        audio_array = audio_array.astype(np.float32) / 32768.0

        return audio_array

    def export_mp3(self, audio_segment: AudioSegment, directory: str = '') -> None:
        audio_segment.export(f"{directory}output{self.ct}.mp3", format="mp3")
        self.ct += 1
