from discord.sinks.core import Filters, Sink, default_filters
from pydub import AudioSegment
from queue import Queue


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
        self.buffer = StreamBuffer()

    def write(self, data, user):

        # if the data comes from the inviting user, we append it to buffer
        if user == self.user_id:
            self.buffer.write(data=data, user=user)

    def cleanup(self):
        self.finished = True

    def get_all_audio(self):
        # not applicable for streaming but will cause errors if not overwritten
        pass

    def get_user_audio(self, user):
        # not applicable for streaming but will cause errors if not overwritten
        pass

    def set_user(self, user_id: int):
        self.user_id = user_id
        print(f"Set user ID: {user_id}")


class StreamBuffer:
    def __init__(self) -> None:
        # holds byte-form audio data as it builds
        self.byte_buffer = bytearray()
        self.segment_buffer = Queue()

        # audio data specifications
        self.sample_width = 2
        self.channels = 2
        self.sample_rate = 48000
        self.bytes_ps = 192000
        self.block_len = 2  # in seconds
        self.buff_lim = self.bytes_ps * self.block_len

        # temp var for outputting audio
        self.ct = 1

    def write(self, data, user):

        self.byte_buffer += data  # data is a bytearray object
        # checking amount of data in the buffer
        if len(self.byte_buffer) > self.buff_lim:

            # grabbing slice from the buffer to work with
            byte_slice = self.byte_buffer[:self.buff_lim]

            # creating AudioSegment object with the slice
            audio_segment = AudioSegment(data=byte_slice,
                                         sample_width=self.sample_width,
                                         frame_rate=self.sample_rate,
                                         channels=self.channels,
                                         )

            # removing the old stinky trash data from buffer - ew get it out of there already
            self.byte_buffer = self.byte_buffer[self.buff_lim:]

            self.segment_buffer.put(audio_segment)

            # temporary for validating process
            audio_segment.export(f"output{self.ct}.mp3", format="mp3")
            self.ct += 1
