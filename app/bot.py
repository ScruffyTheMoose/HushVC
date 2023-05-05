import discord

# opening all intents except for privilaged
intents = discord.Intents.all()
intents.members = False
intents.presences = False

# instantiating discord client
client = discord.Client(intents=intents)


async def handle_transcription(transcription):
    print(transcription)


async def transcribe_audio(audio_data):
    # initialize WhisperAI
    # ai = whisper.load_model("tiny")

    # stream the audio data and transcribe in real-time
    async with ai.streaming_transcribe(audio_data) as result_stream:
        async for result in result_stream:
            # handle the transcription in real-time
            await handle_transcription(result.transcription)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message):
    if message.content.startswith("~!join"):
        # need error catching here incase user not in channel
        channel = message.author.voice.channel

        vc = await channel.connect()
        while vc.is_connected():
            audiostrean = (
                discord.AudioSource()
            )  # read audio data from the voice channel
            audio_data = discord.PCMAudio(audiostrean)

            chunk = audio_data.read()

            print(type(chunk))

            await transcribe_audio(
                audio_data
            )  # send audio data to WhisperAI for live transcription

        await vc.disconnect()

    elif message.content.startswith("~!leave"):
        if message.guild.voice_client:
            await message.guild.voice_client.disconnect()


# reading bot token from outside file
key = open("key.pw", "r").read()

if __name__ == "__main__":
    client.run(key)
