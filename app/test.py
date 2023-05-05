import discord
from discord.ext import commands
from custom_core import StreamSink


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

connections = {}

mysink = StreamSink()


@bot.command()
async def record(ctx):  # If you're using commands.Bot, this will also work.
    voice = ctx.author.voice

    if not voice:
        await ctx.reply("You aren't in a voice channel bro what the fuck do you want me to do lmao")

    # Connect to the voice channel the author is in.
    mysink.set_user(ctx.author.id)
    vc = await voice.channel.connect()
    # Updating the cache with the guild and channel.
    connections.update({ctx.guild.id: vc})

    vc.start_recording(
        mysink,  # The sink type to use.
        once_done,  # What to do once done.
        ctx.channel  # The channel to disconnect from.
    )

    await ctx.reply("Started recording!")


# Our voice client already passes these in.
async def once_done(sink: discord.sinks, channel: discord.TextChannel, *args):
    await sink.vc.disconnect()  # Disconnect from the voice channel.
    print("Recording stopped.")


@bot.command()
async def stop_recording(ctx):
    if ctx.guild.id in connections:  # Check if the guild is in the cache.
        vc = connections[ctx.guild.id]
        # Stop recording, and call the callback (once_done).
        vc.stop_recording()
        del connections[ctx.guild.id]  # Remove the guild from the cache.
    else:
        # Respond with this if we aren't recording.
        await ctx.reply("I am currently not recording here.")

key = open("key.pw", "r").read()
bot.run(key)
