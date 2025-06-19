import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
if not DISCORD_TOKEN:
    raise Exception("DISCORD_TOKEN environment variable not set")

# Set up Discord bot with all necessary intents
intents = discord.Intents.default()
intents.message_content = True  # Required to read messages
intents.messages = True         # Required for purge/delete
intents.guilds = True           # Good to have

bot = commands.Bot(command_prefix="doom ", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot is online as {bot.user}')

# Command: delete messages safely
@bot.command(name="delete")
@commands.has_permissions(manage_messages=True)
async def delete(ctx):
    try:
        deleted = await ctx.channel.purge(limit=100)  # Try with 50 to avoid old message limit
        await ctx.send(f"✅ Deleted {len(deleted)} messages!", delete_after=5)
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to delete messages.")
    except Exception as e:
        await ctx.send(f"⚠️ Error: {str(e)}")

# Command: debug current permissions
@bot.command(name="debug_perms")
async def debug_perms(ctx):
    perms = ctx.channel.permissions_for(ctx.guild.me)
    await ctx.send(
        f"🔍 Permissions for me in this channel:\n"
        f"- Manage Messages: {perms.manage_messages}\n"
        f"- Read Message History: {perms.read_message_history}\n"
        f"- View Channel: {perms.view_channel}\n"
        f"- Send Messages: {perms.send_messages}"
    )

# Flask app for keeping alive on Render
app = Flask("")

@app.route("/")
def home():
    return "🌐 Doom Bot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

def run_bot():
    bot.run(DISCORD_TOKEN)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    run_bot()
