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
  'ンチ': nti,
  'んㄘ': nti,
  '<:n_:1375806870543138927><:ti:1375806832660058142>': nti,
  'まんこ': '🦪',
  'ちんちん': timpo,
  'ちんこ': timpo,
  'ちんぽ': timpo,
  'ㄘんㄘん': timpo,
  '<:ti:1375806832660058142><:n_:1375806870543138927><:ko:1375807359267377172>': timpo,
  '<:ti:1375806832660058142><:n_:1375806870543138927><:po:1375806918177718333>': timpo,
  '<:ti:1375806832660058142><:n_:1375806870543138927><:ti:1375806832660058142><:n_:1375806870543138927>': timpo,
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
  content = content.replace(" ", "").replace("　", "")
  
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
        
        # print(f'[{datetime.now(JST).strftime("%H:%M")}] リアクション追加: "{keyword}" -> {emoji}')
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
  
  # print(f'[{datetime.now(JST).strftime("%H:%M")}] あだ名決定: {interaction.user.display_name} -> {nickname} (固定)')

@bot.tree.command(name='spice', description='調味料スロット！')
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
    'コンソメ',
    'めんつゆ',
    '白だし',
    'トマト',
    'マヨネーズ',
    'ケチャップ',
    '鶏ガラ',
    'にんにく',
    'しょうが',
    'オリーブオイル',
    '味覇',
  ]
  s1 = random.choice(spices)
  s2 = random.choice(spices)
  s3 = random.choice(spices)

  # 3つの要素をリストにまとめる
  selected_spices = [s1, s2, s3]
  # Counterを使って各要素の出現回数を数える
  counts = Counter(selected_spices)
  v = ""

  if len(counts) == 1:
    v = f"全部{s1}！！！ 濃い味で死！"
  elif len(counts) == 2:
    v = f"2個も一緒！！！ それなりに濃い味で死！"
  else:
    v = "らしいよ"

  if 'パクチー' in selected_spices:
    v = f"{v} パクチーが入ってるから完全に死！！！！！"

  # 特定のユーザに1/2でトマト
  if str(interaction.user.id) == os.getenv('TOMATO_USER'):
    if random.random() < 0.5:
      s1 = "ト"
      s2 = "マ"
      s3 = "ト"
      v = "トマトトマトトマトトマトトマトトマトトマトトマトトマト"

  # 結果を表示
  embed = discord.Embed(
    title='調味料スロット',
    description=f'{interaction.user.mention} がこれから使う調味料は',
    color=discord.Color.gold()
  )
  embed.add_field(
    name=f'{s1}　{s2}　{s3}',
    value=v,
    inline=False
  )
  embed.set_footer(text='ほら、使え')

  await interaction.response.send_message(embed=embed)

@bot.tree.command(name='sex', description='ちんぽスロット')
async def slash_mynick(interaction: discord.Interaction):
  words = [
    "ち",
    "ん",
    "こ",
    "ぽ",
    "ま",
    "う"
  ]
  s1 = random.choice(words)
  s2 = random.choice(words)
  s3 = random.choice(words)
  ss = s1 + s2 + s3

  v = "だってさ"
  if "んち" in ss or "うんこ" == ss:
    v = "うわ、くっせ:poop:"
  elif "ちんぽ" == ss or "ちんこ" == ss or "ちちん" == ss:
    v = ":bell:"
  elif "まんこ" == ss:
    v = ":oyster:"
  elif "まま" in ss:
    v = "ママー！<:donburicat_ota:1226872163278127205>"
  elif "ぽぽぽ" == ss:
    v = "八尺様かよｗ"
  elif "ちちち" == ss:
    v = "鼠先輩かよｗ"
  elif "んんん" == ss:
    v = "拙者はオタクではないですゾ～！"
  elif "こここ" == ss:
    v = "王騎かよｗ"
  elif "ううう" == ss:
    v = "どうした？具合悪い？ｗ"

  # 特定のユーザに1/2でトマト
  if str(interaction.user.id) == os.getenv('TOMATO_USER'):
    if random.random() < 0.5:
      s1 = "ト"
      s2 = "マ"
      s3 = "ト"
      v = "トマトトマトトマトトマトトマトトマトトマトトマトトマト"

  # 結果を表示
  embed = discord.Embed(
    title='ちんぽスロット',
    description=f'{interaction.user.mention} は',
    color=discord.Color.gold()
  )
  embed.add_field(
    name=f'{s1}　{s2}　{s3}',
    value=v,
    inline=False
  )
  embed.set_footer(text='うへぇ')

  await interaction.response.send_message(embed=embed)

@bot.tree.command(name='negitoro', description='ねぎとろスロット')
async def slash_mynick(interaction: discord.Interaction):
  tomato = "<a:negitoro_yoke:1379052510932635768>"
  negitoro = "<:tomatoski:1379057098511351878>"
  words = [
    tomato,
    negitoro,
  ]
  s1 = random.choice(words)
  s2 = random.choice(words)
  s3 = random.choice(words)

  v = "さぁいくぞ！"
  if s1 == s3 == tomato and s2 == negitoro:
    v = "オラ！トマト食え！"
  elif s1 == s2 == s3 == tomato:
    v = "チッ、逃げられたか"
  elif s1 == s2 == s3 == negitoro:
    v = "トマトがなくて今だけは平和だね＾＾"
  elif s1 == s3 == negitoro and s2 == tomato:
    v = "仲良く分けて食べなさい＾＾"

  # 特定のユーザに1/2でトマト
  if str(interaction.user.id) == os.getenv('TOMATO_USER'):
    s1 = tomato
    s2 = negitoro
    s3 = tomato
    v = "お前は常にこれだ"

  # 結果を表示
  embed = discord.Embed(
    title='ねぎとろスロット',
    description=f'みんな大好きなねぎとろさん',
    color=discord.Color.gold()
  )
  embed.add_field(
    name=v,
    value=f'{s1}　{s2}　{s3}',
    inline=False
  )
  embed.set_footer(text='ヤッホオオオオオオオウ！！！')

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