from __future__ import annotations

import os

import discord

from open_scrapers_desk.discord_bridge import run_prompt_to_preset_messages

TOKEN = os.environ["DISCORD_TOKEN"]
PREFIX = os.environ.get("DISCORD_PREFIX", "!scrape")
TOOLKIT_PATH = os.environ.get("OPEN_SCRAPERS_TOOLKIT_PATH", r"g:\Scrapers")
NODE = os.environ.get("OPEN_SCRAPERS_NODE", "node")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_message(message: discord.Message) -> None:
  if message.author.bot or not message.content.startswith(PREFIX):
    return

  prompt = message.content[len(PREFIX) :].strip()
  if not prompt:
    await message.reply("Use !scrape <question>, for example !scrape What is the weather in London")
    return

  messages = run_prompt_to_preset_messages(
    TOOLKIT_PATH,
    NODE,
    prompt,
    preset="rich",
    limit=3,
  )

  for payload in messages:
    embeds = [discord.Embed.from_dict(embed) for embed in payload.get("embeds", [])]
    await message.reply(content=payload.get("content"), embeds=embeds)


client.run(TOKEN)
