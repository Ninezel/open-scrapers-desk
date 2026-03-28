import os

import discord
from discord.ext import commands

from open_scrapers_desk.discord_bridge import run_scraper_to_discord_messages

TOKEN = os.environ["DISCORD_TOKEN"]
TOOLKIT_PATH = os.environ.get("OPEN_SCRAPERS_TOOLKIT_PATH", r"g:\Scrapers")
NODE_EXECUTABLE = os.environ.get("OPEN_SCRAPERS_NODE", "node")
PREFIX = os.environ.get("DISCORD_PREFIX", "!")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)


@bot.command(name="scrape")
async def scrape(ctx: commands.Context[commands.Bot], scraper_id: str) -> None:
  await ctx.typing()

  try:
    messages = run_scraper_to_discord_messages(
      TOOLKIT_PATH,
      NODE_EXECUTABLE,
      scraper_id,
      limit=3,
      max_records=3,
      max_embeds_per_message=3,
    )
  except Exception as error:  # noqa: BLE001
    await ctx.reply(f"Scraper run failed: {error}")
    return

  for payload in messages:
    embeds = [discord.Embed.from_dict(embed) for embed in payload.get("embeds", [])]
    await ctx.reply(payload.get("content"), embeds=embeds)


bot.run(TOKEN)
