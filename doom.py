import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# Load env vars (optional locally, for Render it's automatic)
from dotenv import load_dotenv
load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
if not DISCORD_TOKEN:
    raise Exception("DISCORD_TOKEN environment variable not set")

# Set up Discord bot with intents to read messages and manage messages
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix="doom ", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot logged in as {bot.user}')

@bot.command(name="delete")
@commands.has_permissions(manage_messages=True)  # Optional: restrict to mods/admins
async def delete(ctx):
    # Delete 100 messages from the channel where command was issued
    deleted = await ctx.channel.purge(limit=100)
    await ctx.send(f"Deleted {len(deleted)} messages!", delete_after=5)

# Flask app to keep the service alive on Render
app = Flask("")

@app.route("/")
def home():
    return "Bot is running"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

def run_bot():
    bot.run(DISCORD_TOKEN)

if __name__ == "__main__":
    # Run Flask in a separate thread
    Thread(target=run_flask).start()
    run_bot()
