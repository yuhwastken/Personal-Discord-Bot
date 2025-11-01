import discord
from discord.ui import Button, View
from discord.ext import commands
import requests
import os
import webserver

DISCORD_API = os.environ["discordapi"]
GIPHY_API = os.environ["giphyapi"]
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
    url = f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_API}&q={msg}&limit=10"
    response = requests.get(url)
    gifs = response.json()
    if gifs["data"] == []:
        await ctx.send(f"No gifs found for {msg}")
    else:
        gif_urls = [gif["images"]["original"]["url"] for gif in gifs["data"]]
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

        channel = bot.get_channel(1434190691621146735)
        message = await channel.send(embed=embed, view=view)


webserver.keep_alive()
bot.run(DISCORD_API)
