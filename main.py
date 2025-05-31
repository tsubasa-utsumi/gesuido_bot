import discord
from discord.ext import commands
import os
from datetime import datetime
import pytz
from dotenv import load_dotenv
import random

# 環境変数を読み込み
load_dotenv()

# 日本時間のタイムゾーン
JST = pytz.timezone('Asia/Tokyo')

# リアクションルール
# TODO: ランダムも加えたい
REACTION_RULES = {
  'うんこ': {'random': ['<:blobpoop:1235236342594539581>', '<:poop_fairy:1377905879403335690>']},
  'んち': {'random': ['<:blobpoop:1235236342594539581>', '<:poop_fairy:1377905879403335690>']},
  '<:n_:1375806870543138927> <:ti:1375806832660058142>': {'random': ['<:blobpoop:1235236342594539581>', '<:poop_fairy:1377905879403335690>']},
  'まんこ': '🦪',
  'ちんちん': '🛎️',
  'はしもん': ['<:hashimon:1368619272372228269>', '💋'],
}

# Botの設定
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
  print(f'{bot.user} がログインしました！')
  print(f'Bot ID: {bot.user.id}')

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  
  await check_and_react(message)
  await bot.process_commands(message)

async def add_reaction(message, emoji):
  if emoji.startswith('<') and emoji.endswith('>'):
    emoji_parts = emoji.strip('<>').split(':')
    if len(emoji_parts) == 3:
      emoji_name = emoji_parts[1]
      custom_emoji = discord.utils.get(message.guild.emojis, name=emoji_name)
      if custom_emoji:
        await message.add_reaction(custom_emoji)
      else:
        print(f'カスタム絵文字が見つかりません: {emoji_name}')
  else:
    if len(emoji.strip()) > 0:
      await message.add_reaction(emoji)

async def check_and_react(message):
  """メッセージ内容をチェックして該当する場合リアクションを追加"""
  content = message.content.lower()
  
  for keyword, emoji in REACTION_RULES.items():
    if keyword in content or keyword.replace(" ", "") in content:
      try:
        if isinstance(emoji, list):
          for item in emoji:
            await add_reaction(message, item)
        if isinstance(emoji, dict):
          item = random.choice(emoji['random'])
          await add_reaction(message, item)
        else:
          await add_reaction(message, emoji)
        
        print(f'[{datetime.now(JST).strftime("%H:%M")}] リアクション追加: "{keyword}" -> {emoji}')
      except discord.HTTPException as e:
        print(f'リアクション追加エラー: {e}')
      except Exception as e:
        print(f'予期しないエラー: {e}')

@bot.command(name='reactions')
async def show_reactions(ctx):
  embed = discord.Embed(
    title='🎭 リアクションルール一覧',
    description='以下のキーワードが含まれるメッセージに自動でリアクションします',
    color=discord.Color.purple()
  )
  
  rules_text = '\n'.join([f'`{keyword}` → {emoji}' for keyword, emoji in REACTION_RULES.items()])
  embed.add_field(name='キーワード → 絵文字', value=rules_text, inline=False)
  embed.add_field(name='📝 注意', value='大文字小文字は区別しません', inline=False)
  
  await ctx.send(embed=embed)

if __name__ == '__main__':
  token = os.getenv('DISCORD_TOKEN')
  if token:
    # 追加の依存関係チェック
    try:
      bot.run(token)
    except Exception as e:
      print(f'Bot起動エラー: {e}')
  else:
    print('エラー: DISCORD_TOKENが設定されていません')