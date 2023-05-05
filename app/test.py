import discord
from discord.ext import commands
from custom_core import StreamSink


# test module since I keep breaking everything while updating custom implementations of core classes from Pycord

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

connections = {}

mysink = StreamSink()


@bot.command()
async def record(ctx):  # if you're using commands.Bot, this will also work.
    voice = ctx.author.voice

    if not voice:
        # someone had to say it my guy
        await ctx.reply("You aren't in a voice channel bro what the fuck do you want me to do lmao")

    # connect to the voice channel the author is in.
    mysink.set_user(ctx.author.id)
    vc = await voice.channel.connect()
    # updating the cache with the guild and channel.
    connections.update({ctx.guild.id: vc})

    vc.start_recording(
        mysink,  # the sink type to use.
        once_done,  # what to do once done.
        ctx.channel  # the channel to disconnect from.
    )

    await ctx.reply("Started recording!")


# our voice client already passes these in.
async def once_done(sink: discord.sinks, channel: discord.TextChannel, *args):
    await sink.vc.disconnect()  # disconnect from the voice channel.
    print("Recording stopped.")


@bot.command()
async def stop_recording(ctx):
    if ctx.guild.id in connections:  # check if the guild is in the cache.
        vc = connections[ctx.guild.id]
        # stop recording, and call the callback (once_done).
        vc.stop_recording()
        del connections[ctx.guild.id]  # remove the guild from the cache.
    else:
        # respond with this if we aren't recording.
        await ctx.reply("I am currently not recording here.")

key = open("key.pw", "r").read()
bot.run(key)
