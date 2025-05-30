import discord
from discord.ext import commands, tasks
import os
import asyncio
from datetime import datetime, time
import pytz
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

# 日本時間のタイムゾーン
JST = pytz.timezone('Asia/Tokyo')

# リアクションルール
REACTION_RULES = {
  'うんこ': '<:blobpoop:1235236342594539581>',
  'んち': '<:blobpoop:1235236342594539581>',
  ':n_: :ti: ': '<:blobpoop:1235236342594539581>',
  
}

def validate_emoji(emoji_str):
  """絵文字が有効かどうかを検証"""
  if not emoji_str or len(emoji_str.strip()) == 0:
    return False, "空の絵文字"
  
  if emoji_str.startswith('<') and emoji_str.endswith('>'):
    parts = emoji_str.strip('<>').split(':')
    if len(parts) != 3:
      return False, "無効なカスタム絵文字形式"
    return True, "カスタム絵文字"
  
  return True, "Unicode絵文字"

def is_active_hours():
  """現在が稼働時間かどうかを判定（JST AM10:00-AM2:00）"""
  now_jst = datetime.now(JST)
  current_time = now_jst.time()
  
  # AM10:00-翌日AM2:00が稼働時間
  start_time = time(10, 0)  # AM10:00
  end_time = time(2, 0)     # AM2:00
  
  if start_time <= current_time or current_time < end_time:
    return True
  return False

def get_next_wake_time():
  """次の起動時刻を取得"""
  now_jst = datetime.now(JST)
  current_time = now_jst.time()
  
  if current_time < time(2, 0):
    # 現在AM0:00-AM2:00の場合、同日AM10:00まで待機
    next_wake = now_jst.replace(hour=10, minute=0, second=0, microsecond=0)
  elif current_time < time(10, 0):
    # 現在AM2:00-AM10:00の場合、同日AM10:00まで待機
    next_wake = now_jst.replace(hour=10, minute=0, second=0, microsecond=0)
  else:
    # 現在AM10:00以降の場合、翌日AM10:00まで待機
    next_wake = now_jst.replace(hour=10, minute=0, second=0, microsecond=0)
    next_wake = next_wake.replace(day=next_wake.day + 1)
  
  return next_wake

# Botの設定
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
  print(f'{bot.user} がログインしました！')
  print(f'Bot ID: {bot.user.id}')
  print(f'現在時刻（JST）: {datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S")}')
  
  # 稼働時間チェック開始
  if not schedule_checker.is_running():
    schedule_checker.start()
  
  # 稼働状況を報告
  if is_active_hours():
    print('✅ 稼働時間内です - Botは正常に動作します')
  else:
    print('⏰ 停止時間内です - Botは停止準備中...')
    next_wake = get_next_wake_time()
    print(f'次回起動予定: {next_wake.strftime("%Y-%m-%d %H:%M:%S JST")}')
  
  print('------')

@tasks.loop(minutes=5)
async def schedule_checker():
  """5分ごとに稼働時間をチェック"""
  now_jst = datetime.now(JST)
  
  if not is_active_hours():
    print(f'[{now_jst.strftime("%H:%M")}] 停止時間に入りました - Botを停止します')
    
    # 管理者に通知（設定されている場合）
    admin_channel_id = os.getenv('ADMIN_CHANNEL_ID')
    if admin_channel_id:
      try:
        channel = bot.get_channel(int(admin_channel_id))
        if channel:
          next_wake = get_next_wake_time()
          embed = discord.Embed(
            title='🌙 Bot 定期停止',
            description=f'節電のため停止します\n次回起動: {next_wake.strftime("%m/%d %H:%M JST")}',
            color=discord.Color.blue()
          )
          await channel.send(embed=embed)
      except:
        pass
    
    # Botを停止
    await bot.close()

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  
  # 稼働時間外はリアクションしない
  if not is_active_hours():
    return
  
  await check_and_react(message)
  await bot.process_commands(message)

async def check_and_react(message):
  """メッセージ内容をチェックして該当する場合リアクションを追加"""
  content = message.content.lower()
  
  for keyword, emoji in REACTION_RULES.items():
    if keyword in content or keyword.replace(" ", "") in content:
      try:
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
        
        print(f'[{datetime.now(JST).strftime("%H:%M")}] リアクション追加: "{keyword}" -> {emoji}')
      except discord.HTTPException as e:
        print(f'リアクション追加エラー: {e}')
      except Exception as e:
        print(f'予期しないエラー: {e}')
    else:
      print(f"対応外: {content}")

@bot.command(name='schedule_status')
async def schedule_status(ctx):
  """現在のスケジュール状況を表示"""
  now_jst = datetime.now(JST)
  is_active = is_active_hours()
  
  embed = discord.Embed(
    title='⏰ Bot スケジュール状況',
    color=discord.Color.green() if is_active else discord.Color.orange()
  )
  
  embed.add_field(
    name='現在時刻（JST）',
    value=now_jst.strftime('%Y-%m-%d %H:%M:%S'),
    inline=False
  )
  
  embed.add_field(
    name='稼働状況',
    value='🟢 稼働中' if is_active else '🟡 停止予定',
    inline=True
  )
  
  embed.add_field(
    name='稼働時間',
    value='毎日 AM10:00 - AM2:00（JST）',
    inline=True
  )
  
  if not is_active:
    next_wake = get_next_wake_time()
    embed.add_field(
      name='次回起動予定',
      value=next_wake.strftime('%m/%d %H:%M JST'),
      inline=False
    )
  
  embed.add_field(
    name='月間稼働時間',
    value='約480時間（500時間以内）',
    inline=False
  )
  
  await ctx.send(embed=embed)

@bot.command(name='hello')
async def hello(ctx):
  if not is_active_hours():
    await ctx.send('現在は停止時間です。AM10:00-AM2:00の間にお試しください。')
    return
  await ctx.send(f'こんにちは、{ctx.author.mention}さん！')

@bot.command(name='reactions')
async def show_reactions(ctx):
  if not is_active_hours():
    await ctx.send('現在は停止時間です。AM10:00-AM2:00の間にお試しください。')
    return
    
  embed = discord.Embed(
    title='🎭 リアクションルール一覧',
    description='以下のキーワードが含まれるメッセージに自動でリアクションします',
    color=discord.Color.purple()
  )
  
  rules_text = '\n'.join([f'`{keyword}` → {emoji}' for keyword, emoji in REACTION_RULES.items()])
  embed.add_field(name='キーワード → 絵文字', value=rules_text, inline=False)
  embed.add_field(name='📝 注意', value='大文字小文字は区別しません', inline=False)
  embed.add_field(name='⏰ 稼働時間', value='AM10:00-AM2:00（JST）のみ', inline=False)
  
  await ctx.send(embed=embed)

if __name__ == '__main__':
  # 起動時に稼働時間をチェック
  if not is_active_hours():
    next_wake = get_next_wake_time()
    sleep_seconds = (next_wake - datetime.now(JST)).total_seconds()
    
    print(f'現在は停止時間です（JST: {datetime.now(JST).strftime("%H:%M")}）')
    print(f'次回起動まで {sleep_seconds/3600:.1f} 時間待機...')
    print(f'起動予定時刻: {next_wake.strftime("%Y-%m-%d %H:%M:%S JST")}')
    
    # 起動時刻まで待機
    import time
    time.sleep(sleep_seconds)
  
  token = os.getenv('DISCORD_TOKEN')
  if token:
    # 追加の依存関係チェック
    try:
      bot.run(token)
    except Exception as e:
      print(f'Bot起動エラー: {e}')
  else:
    print('エラー: DISCORD_TOKENが設定されていません')