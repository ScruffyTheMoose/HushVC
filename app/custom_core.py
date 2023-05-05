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
    def __init__(self) -> None:
        # holds byte-form audio data as it builds
        self.byte_buffer = bytearray()  # bytes
        self.segment_buffer = Queue()  # pydub.AudioSegments

        # audio data specifications
        self.sample_width = 2
        self.channels = 2
        self.sample_rate = 48000
        self.bytes_ps = 192000  # bytes added to buffer per second
        self.block_len = 2  # how long you want each audio block to be in seconds
        # min len to pull bytes from buffer
        self.buff_lim = self.bytes_ps * self.block_len

        # var for tracking order of exported audio
        self.ct = 1

    # will need 'user' param if tracking multiple peoples voices - TBD
    def write(self, data, user) -> None:

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
            # ok much better now

            # adding AudioSegment to the queue
            self.segment_buffer.put(audio_segment)

            # temporary for validating process
            self.export_mp3(audio_segment=audio_segment)

    def export_mp3(self, audio_segment: AudioSegment, directory: str = '') -> None:
        audio_segment.export(f"{directory}output{self.ct}.mp3", format="mp3")
        self.ct += 1
