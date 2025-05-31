import discord
from discord.ext import commands
from discord import app_commands
import os
from datetime import datetime
import pytz
from dotenv import load_dotenv
import random
import hashlib
from collections import Counter

# 環境変数を読み込み
load_dotenv()

# 日本時間のタイムゾーン
JST = pytz.timezone('Asia/Tokyo')

# リアクションルール
nti = {'random': ['<:blobpoop:1235236342594539581>', '<:poop_fairy:1377905879403335690>']}
timpo = '🛎️'
REACTION_RULES = {
  'うんこ': nti,
  'んち': nti,
  '<:n_:1375806870543138927> <:ti:1375806832660058142>': nti,
  'まんこ': '🦪',
  'ちんちん': timpo,
  'ちんこ': timpo,
  'ちんぽ': timpo,
  'はしもん': ['<:hashimon:1368619272372228269>', '💋'],
}

# Botの設定
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True  # ギルド（サーバー）情報取得用
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
  print(f'{bot.user} がログインしました！')
  print(f'Bot ID: {bot.user.id}')
  
  # スラッシュコマンドを同期
  try:
    synced = await bot.tree.sync()
    print(f'{len(synced)} 個のスラッシュコマンドを同期しました')
  except Exception as e:
    print(f'スラッシュコマンドの同期に失敗: {e}')

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  
  await check_and_react(message)
  await bot.process_commands(message)

def get_today_key():
  """今日の日付キーを取得"""
  return datetime.now(JST).strftime('%Y-%m-%d')

def get_daily_role_index(user_id, today_date, role_count):
  """ユーザーIDと日付から決定論的にロールインデックスを生成"""
  # ユーザーIDと日付を組み合わせてハッシュ化
  seed_string = f"{user_id}-{today_date}"
  hash_object = hashlib.md5(seed_string.encode())
  hash_hex = hash_object.hexdigest()
  
  # ハッシュの最初の8文字を16進数として解釈し、ロール数で割った余りを返す
  hash_int = int(hash_hex[:8], 16)
  return hash_int % role_count

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
        elif isinstance(emoji, dict):
          item = random.choice(emoji['random'])
          await add_reaction(message, item)
        else:
          await add_reaction(message, emoji)
        
        print(f'[{datetime.now(JST).strftime("%H:%M")}] リアクション追加: "{keyword}" -> {emoji}')
      except discord.HTTPException as e:
        print(f'リアクション追加エラー: {e}')
      except Exception as e:
        print(f'予期しないエラー: {e}')

# スラッシュコマンド: リアクションルール一覧
@bot.tree.command(name='reactions', description='自動リアクションのルール一覧を表示します')
async def slash_reactions(interaction: discord.Interaction):
  embed = discord.Embed(
    title='🎭 リアクションルール一覧',
    description='以下のキーワードが含まれるメッセージに自動でリアクションします',
    color=discord.Color.purple()
  )
  
  rules_text = '\n'.join([f'`{keyword}` → {emoji}' for keyword, emoji in REACTION_RULES.items()])
  embed.add_field(name='キーワード → 絵文字', value=rules_text, inline=False)
  embed.add_field(name='📝 注意', value='大文字小文字は区別しません', inline=False)
  
  await interaction.response.send_message(embed=embed)

# スラッシュコマンド: 1日固定のあだ名決定
@bot.tree.command(name='mynick', description='今日のあだ名を決定します（1日固定）')
async def slash_mynick(interaction: discord.Interaction):
  """1日固定のあだ名を決定（データ保存なし・決定論的）"""
  
  # サーバーのロール一覧を取得（@everyoneを除く）
  guild_roles = [role for role in interaction.guild.roles if role.name != '@everyone']
  
  if not guild_roles:
    await interaction.response.send_message('😅 このサーバーにはロールがありません！')
    return
  
  # ユーザーIDと今日の日付から決定論的にロールを選択
  today = get_today_key()
  user_id = interaction.user.id
  role_index = get_daily_role_index(user_id, today, len(guild_roles))
  selected_role = guild_roles[role_index]
  nickname = selected_role.name
  
  # 結果を表示
  embed = discord.Embed(
    title='🏷️ 今日のあだ名',
    description=f'{interaction.user.mention} の今日のあだ名は...',
    color=discord.Color.gold()
  )
  embed.add_field(
    name='✨ あだ名',
    value=f'**{nickname}**',
    inline=False
  )
  embed.set_footer(text=f'全{len(guild_roles)}個のロールから選出（1日固定）')
  
  await interaction.response.send_message(embed=embed)
  
  print(f'[{datetime.now(JST).strftime("%H:%M")}] あだ名決定: {interaction.user.display_name} -> {nickname} (固定)')


@bot.tree.command(name='mynick', description='今日のあだ名を決定します（1日固定）')
async def slash_mynick(interaction: discord.Interaction):
  spices = [
    '砂糖',
    '塩',
    '酢',
    '醤油',
    '味噌',
    '豆板醤',
    '甜麺醤',
    'オイスターソース',
    'ごま油',
    'バジル',
    'パクチー',
    '味の素',
    'ほんだし',
    'コンソメ'
  ]
  s1 = random.choice(spices)
  s2 = random.choice(spices)
  s3 = random.choice(spices)

  # 3つの要素をリストにまとめる
  selected_spices = [s1, s2, s3]
  # Counterを使って各要素の出現回数を数える
  counts = Counter(selected_spices)
  v = ""

  if counts == 1:
    v = f"全部{s1}！！！ 濃い味で死！"
  elif counts == 2:
    v = f"2個も一緒！！！ それなりに濃い味で死！"
  else:
    v = "らしいよ"

  if 'パクチー' in selected_spices:
    v = f"{v} パクチーが入ってるから完全に死！！！！！"
  
  # 結果を表示
  embed = discord.Embed(
    title='調味料スロット',
    description=f'{interaction.user.mention} がこれから使う調味料は',
    color=discord.Color.gold()
  )
  embed.add_field(
    name=f'{s1} {s2} {s3}',
    value=v,
    inline=False
  )
  embed.set_footer(text=f'ほら、使え<:blobcat_watchyou:1237029431680438273>')
  
  await interaction.response.send_message(embed=embed)

# 従来のプレフィックスコマンドも残す（互換性のため）
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