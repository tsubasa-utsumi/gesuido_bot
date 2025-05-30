import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

# リアクションルールを外部ファイルで管理するためのグローバル変数
REACTION_RULES = {
  'うんこ': '<:blobpoop:1235236342594539581>',
}

# Botの設定
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
  print(f'{bot.user} がログインしました！')
  print(f'Bot ID: {bot.user.id}')
  print('------')

@bot.event
async def on_message(message):
  # Bot自身のメッセージは無視
  if message.author == bot.user:
    return
  
  # 特定の文字列を含むメッセージにリアクションを追加
  await check_and_react(message)
  
  # コマンドの処理を継続
  await bot.process_commands(message)

async def check_and_react(message):
  """メッセージ内容をチェックして該当する場合リアクションを追加"""
  content = message.content.lower()  # 大文字小文字を区別しない
  
  # 各ルールをチェック
  for keyword, emoji in REACTION_RULES.items():
    if keyword in content:
      try:
        await message.add_reaction(emoji)
        print(f'リアクション追加: "{keyword}" -> {emoji} (by {message.author})')
      except discord.HTTPException as e:
        print(f'リアクション追加エラー: {e}')

@bot.command(name='hello')
async def hello(ctx):
  """挨拶コマンド"""
  await ctx.send(f'こんにちは、{ctx.author.mention}さん！')

@bot.command(name='ping')
async def ping(ctx):
  """レイテンシを確認するコマンド"""
  latency = round(bot.latency * 1000)
  await ctx.send(f'Pong! レイテンシ: {latency}ms')

@bot.command(name='info')
async def info(ctx):
  """サーバー情報を表示するコマンド"""
  guild = ctx.guild
  embed = discord.Embed(
    title=f'{guild.name} の情報',
    color=discord.Color.blue()
  )
  embed.add_field(name='メンバー数', value=guild.member_count, inline=True)
  embed.add_field(name='作成日', value=guild.created_at.strftime('%Y/%m/%d'), inline=True)
  embed.add_field(name='サーバーID', value=guild.id, inline=True)
  
  await ctx.send(embed=embed)

@bot.command(name='reactions')
async def show_reactions(ctx):
  """現在のリアクションルールを表示"""
  embed = discord.Embed(
    title='🎭 リアクションルール一覧',
    description='以下のキーワードが含まれるメッセージに自動でリアクションします',
    color=discord.Color.purple()
  )
  
  rules_text = '\n'.join([f'`{keyword}` → {emoji}' for keyword, emoji in REACTION_RULES.items()])
  embed.add_field(name='キーワード → 絵文字', value=rules_text, inline=False)
  embed.add_field(name='📝 注意', value='大文字小文字は区別しません', inline=False)
  
  await ctx.send(embed=embed)

@bot.command(name='test_reaction')
async def test_reaction(ctx, *, text: str):
  """リアクションテスト用コマンド"""
  # テスト用の仮想メッセージオブジェクトを作成
  class MockMessage:
    def __init__(self, content, author):
      self.content = content
      self.author = author
      self.reactions_added = []
    
    async def add_reaction(self, emoji):
      self.reactions_added.append(emoji)
  
  mock_msg = MockMessage(text, ctx.author)
  await check_and_react(mock_msg)
  
  if mock_msg.reactions_added:
    reaction_list = ' '.join(mock_msg.reactions_added)
    embed = discord.Embed(
      title='🧪 リアクションテスト結果',
      description=f'テキスト: `{text}`\nリアクション: {reaction_list}',
      color=discord.Color.green()
    )
  else:
    embed = discord.Embed(
      title='🧪 リアクションテスト結果',
      description=f'テキスト: `{text}`\n該当するリアクションはありませんでした',
      color=discord.Color.orange()
    )
  
  await ctx.send(embed=embed)
  """エラーハンドリング"""
  if isinstance(error, commands.CommandNotFound):
    await ctx.send('そのコマンドは存在しません。')
  elif isinstance(error, commands.MissingRequiredArgument):
    await ctx.send('必要な引数が不足しています。')
  else:
    print(f'エラーが発生しました: {error}')

if __name__ == '__main__':
  token = os.getenv('DISCORD_TOKEN')
  if token:
    bot.run(token)
  else:
    print('エラー: DISCORD_TOKENが設定されていません。.envファイルを確認してください。')