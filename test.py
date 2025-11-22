import discord
from discord.ui import Button, View
from discord.ext import commands
import requests
import os
import webserver
from pytube import Playlist, YouTube

DISCORD_API = os.environ["discordapi"]
TENOR_API = os.environ["tenorapi"]
STUDY_CHANNEL = os.evironment["study_channel"]
GIF_CHANNEL = os.evironment["gif_channel"]
# Bot
bot = commands.Bot(
    command_prefix="!",
    intents=discord.Intents.all(),
    case_insensitive=True,
    self_bot=True,
)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True


@bot.event
async def on_ready():
    print(f"{bot.user.name} has turned on")


@bot.command()
async def gif(ctx, *, msg):
    url = f"https://tenor.googleapis.com/v2/search?q={msg}&key={TENOR_API}&client_key=my_test_app&limit=10"
    response = requests.get(url)
    if response.status_code == 200:
        gifs = response.json()
        gif_urls = [gif["media_formats"]["gif"]["url"] for gif in gifs["results"]]
        gif_no = 0
        embed = discord.Embed(title=msg)
        embed.set_image(url=gif_urls[gif_no])

        button = Button(label="Next", emoji="➡️")

        async def button_callback(interaction):
            nonlocal gif_no
            gif_no = (gif_no + 1) % len(gif_urls)
            embed = discord.Embed(title=msg)
            embed.set_image(url=gif_urls[gif_no])
            await message.edit(embed=embed)
            await interaction.response.defer()

        button.callback = button_callback
        view = View(timeout=None)
        view.add_item(button)

        channel = bot.get_channel(GIF_CHANNEL)
        message = await channel.send(embed=embed, view=view)
    else:
        await ctx.send(f"No gifs found for {msg}")


@bot.command()
async def pl(ctx, url: str, utitle: str):
    pl_url = "https://youtube.com/playlist?list=PL"
    yt1_url = "https://www.youtube.com/watch?v"
    yt2_url = "https://youtu.be/"
    response = requests.get(url)
    if response.status_code == 200:
        if url[:36] == pl_url:
            playlist = Playlist(url)
            links = playlist.video_urls
            c = 1
            des = ""
            for link in links:
                des += f"[Video Number {c}](<{link}>)" + " \n"
                c += 1
                if c == len(links):
                    break
            des += f"[Video Number {c}](<{links[-1]}>)"
            embed = discord.Embed(
                title=utitle,
                description=des,
            )
            channel = bot.get_channel(STUDY_CHANNEL)
            await channel.send(embed=embed)
        elif url[:31] == yt1_url or url[:17] == yt2_url:
            await ctx.send(f"[{utitle}](<{url}>)")
    else:
        await ctx.send("Your given link is wrong")


webserver.keep_alive()
bot.run(DISCORD_API)



