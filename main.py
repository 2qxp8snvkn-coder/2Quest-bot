import discord
from discord.ext import commands
import sqlite3

# Discord Bot Setup
intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix="!", intents=intents)

# SQLite Database Setup
conn = sqlite3.connect("tokens.db")
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS tokens (
 token text,
 owner text,
 balance integer DEFAULT 0,
 PRIMARY KEY (token)
 )""")

def validate_token(token):
 c.execute("SELECT * FROM tokens WHERE token=?", (token,))
 return c.fetchone() is not None

@bot.event
async def on_ready():
 print(f"{bot.user} has connected to Discord!")

@bot.command()
async def submit_token(ctx, token: str):
 """Submits a new token."""
 if validate_token(token):
 await ctx.send("Token already registered!")
 else:
 c.execute("INSERT INTO tokens VALUES (?, ?, ?)", (token, ctx.author.name, 10))
 conn.commit()
 await ctx.send("Token submitted! You have 10 credits.")

@bot.command()
async def do_quest(ctx, quest_name: str):
 """Executes a quest using stored credits."""
 user_data = c.execute("SELECT * FROM tokens WHERE owner=?", (ctx.author.name,))
 
 if user_data.fetchone() and user_data.fetchone()[2] > 0:
 # Simulate quest execution here-replace with actual API calls or actions.
 print(f"Executing {quest_name} for {ctx.author.name}")
 
 # Decrement credits after successful execution.
 c.execute("UPDATE tokens SET balance=balance-1 WHERE owner=?", (ctx.author.name,))
 conn.commit()
 
 await ctx.send(f"Quest '{quest_name}' executed successfully!")
 else:
 await ctx.send("Insufficient credits or invalid request.")

# Run the bot with your Discord app token from https://discord.com/developers/applications/
if __name__ == "__main__":
 import os
 bot.run(os.environ.get('MTUyMDAwNDY2NDMyMDU5Mzk2MA.GYItPZ.rPpIc0vRrwEc5EVzzMGduFQzcZzk4ig6e4l6DE'))
