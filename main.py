import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="$", intents = intents)
bot.remove_command("help")

webrole = ["webrole", "webrolê", "web role", "web rolê"]
starter_sentences = ["Webrolê? Aoba!"]
welcome_messages = ["Olá {0}! Seja muito bem-vinde ao **{1}**! Aqui temos bastante depressão, álcool, sexo, drogas e suco de laranja!", "Opa minhe jovem {0}, tranquilo? Seja muito bem-vinde ao **{1}**! O cardápio de hoje é de torradas com creme de ansiedade para a entrada, tartare de peixe ao molho de depressão e, para fechar, uma barra de diamante negro na sobremesa! Nada melhor que chocolate com cacos de vidro!", "Salve salve {0}! Bem-vinde ao **{1}**! Sinta-se em casa, afinal, é pra você estar mesmo CACETE NOIS TAMO NO MEIO DE UMA PANDEMIA.", "Carai não guento mais escrever \"Bem-vinde ao **{1}**! Cacos de vidro depressão e Pererê pão doce\"\n{0} Só cola aí caralho\nCuidado com os membros do proletariado. Eles não mordem mas latem que é uma beleza!"]

if "responding" not in db.keys():
  db["responding"] = True
if "sending_welcome" not in db.keys():
  db["sending_welcome"] = True

board = {"one": "1️⃣", "two": "2️⃣", "three": "3️⃣", "four": "4️⃣", "five": "5️⃣", "six": "6️⃣", "seven": "7️⃣", "eight": "8️⃣", "nine": "9️⃣"}
playerOne = None
playerTwo = None
startGame = False
endGame = False
winner = None
loser = None
shift = 0

@bot.group(invoke_without_command=True)
async def ajuda(ctx):
  em = discord.Embed(title="Ajuda", description="Use $ajuda <comando> para mais informações sobre o comando.", color=discord.Colour.magenta())
  em.add_field(name = "Diversão", value="chucknorris, falar, frase, rick, rolagem", inline=False)
  em.add_field(name = "Miscelânea", value="oi", inline=False)
  em.add_field(name = "Mensagens", value="boasvindas, mensagem", inline=False)
  await ctx.send(embed = em)

@ajuda.command()
async def boasvindas(ctx, *args):
  if len(args) == 0:
    em = discord.Embed(title="Boas-Vindas", description="Comandos relacionados à funcionalidade do bot de enviar mensagens de boas-vindas aos novos membros do servidor.", color=discord.Colour.blurple())
    em.add_field(name="**Comandos**", value="adicionar, enviando, lista, remover", inline=False)
    await ctx.send(embed = em)
  else:
    action = args[0].lower()
    if action == "adicionar":
      em = discord.Embed(title="Adicionar (boasvindas)", description="Adiciona uma mensagem de boas-vindas ao banco de dados.", color=discord.Colour.purple())
      em.add_field(name="**Mensagens**", value="Para mencionar o usuário na mensagem de boas-vindas, insira \"{0}\" no local da menção. Para inserir o nome do servidor, escreva \"{1}\".", inline=False)
      em.add_field(name="**Sintaxe**", value="$boasvindas adicionar <mensagem>", inline=False)
      await ctx.send(embed = em)
    elif action == "enviando":
      em = discord.Embed(title="Enviando (boasvindas)", description="Define se o bot está enviando mensagens de boas-vindas aos novos membros do servidor. Escreva \"verdadeiro\" após o comando para ativar a funcionalidade, caso contrário, escreva \"falso\".", color=discord.Colour.purple())
      em.add_field(name="**Sintaxe**", value="$boasvindas enviando <booleano>", inline=False)
      await ctx.send(embed = em)
    elif action == "lista":
      em = discord.Embed(title="Lista (boasvindas)", description="Lista as mensagens de boas-vindas adicionadas pelos membros do servidor ao banco de dados.", color=discord.Colour.purple())
      em.add_field(name="**Sintaxe**", value="$boasvindas lista", inline=False)
      await ctx.send(embed = em)
    elif action == "remover":
      em = discord.Embed(title="Remover (boasvindas)", description="Remove uma mensagem de boas-vindas do banco de dados.", color=discord.Colour.purple())
      em.add_field(name="**Sintaxe**", value="$boasvindas remover <índice da mensagem>", inline=False)
      await ctx.send(embed = em)

@ajuda.command()
async def chucknorris(ctx):
  em = discord.Embed(title="Chuck Norris", description="Responde com uma piada sobre o Chuck Norris.", color=discord.Colour.purple())
  em.add_field(name="**Sintaxe**", value="$chucknorris", inline=False)
  await ctx.send(embed = em)

@ajuda.command()
async def falar(ctx):
  em = discord.Embed(title="Falar", description="Faz com que o bot escreva algo.", color=discord.Colour.purple())
  em.add_field(name="**Sintaxe**", value="$falar <mensagem>", inline=False)
  await ctx.send(embed = em)

@ajuda.command()
async def frase(ctx):
  em = discord.Embed(title="Frase", description="Responde com uma frase inspiradora aleatória a partir da API Zen Quotes.", color=discord.Colour.purple())
  em.add_field(name="**Sintaxe**", value="$frase", inline=False)
  await ctx.send(embed = em)

@ajuda.command()
async def mensagem(ctx, *args):
  if len(args) == 0:
    em = discord.Embed(title="Mensagem", description="Comandos relacionados à funcionalidade do bot de responder a mensagens contendos o termo \"Webrole\" e variações.", color=discord.Colour.blurple())
    em.add_field(name="**Comandos**", value="adicionar, lista, remover, respondendo", inline=False)
    await ctx.send(embed = em)
  else:
    action = args[0].lower()
    if action == "adicionar":
      em = discord.Embed(title="Adicionar (mensagem)", description="Adiciona uma mensagem ao banco de dados.", color=discord.Colour.purple())
      em.add_field(name="**Sintaxe**", value="$mensagem adicionar <mensagem>", inline=False)
      await ctx.send(embed = em)
    elif action == "lista":
      em = discord.Embed(title="Lista (mensagem)", description="Lista as mensagens adicionadas pelos membros do servidor ao banco de dados.", color=discord.Colour.purple())
      em.add_field(name="**Sintaxe**", value="$mensagem lista", inline=False)
      await ctx.send(embed = em)
    elif action == "remover":
      em = discord.Embed(title="Remover (mensagem)", description="Remove uma mensagem do banco de dados.", color=discord.Colour.purple())
      em.add_field(name="**Sintaxe**", value="$mensagem remover <índice da mensagem>", inline=False)
      await ctx.send(embed = em)
    elif action == "respondendo":
      em = discord.Embed(title="Respondendo", description="Define se o bot está interagindo com todas as mensagens contendo o termo 'webrole' e variantes. Escreva \"verdadeiro\" após o comando para ativar a funcionalidade, caso contrário, escreva \"falso\".", color=discord.Colour.purple())
      em.add_field(name="**Sintaxe**", value="$mensagem respondendo <booleano>", inline=False)
      await ctx.send(embed = em)

@ajuda.command()
async def oi(ctx):
  em = discord.Embed(title="Oi", description="O bot responde com um \"Olá\".", color=discord.Colour.purple())
  em.add_field(name="**Sintaxe**", value="$oi", inline=False)
  await ctx.send(embed = em)

@ajuda.command()
async def rick(ctx):
  em = discord.Embed(title="Rick", description="Never Gonna Give You Up", color=discord.Colour.purple())
  em.add_field(name="**Sintaxe**", value="$rick", inline=False)
  await ctx.send(embed = em)

@ajuda.command()
async def rolagem(ctx):
  em = discord.Embed(title="Rolagem", description="Faz a rolagem de dados.", color=discord.Colour.purple())
  em.add_field(name="**Sintaxe**", value="$rolagem <dados>", inline=False)
  em.add_field(name="**Dados**", value="Os dados podem ser escritos com letra maiúscula ou minuscúla, com ou sem espaços. Também é possível fazer a rolagem de diferentes quantidade e tipos de dados, ou valores inteiros, incluindo um símbolo de soma (+) entre os membros da adição.", inline=False)
  await ctx.send(embed = em)

@ajuda.command()
async def velha(ctx):
  em = discord.Embed(title="Velha", description="Inicia um jogo da velha. O usuário que digitar o comando é o primeiro a jogar (controla o X). Para outra pessoa entrar no jogo, basta enviar adicionar um \"entrar\" ao comando, esse usuário será o segundo a jogar (controla o O).", color=discord.Colour.purple())
  em.add_field(name="**Sintaxe**", value="$velha [argumento]", inline=False)
  await ctx.send(embed = em)

@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Game("Tetris | $ajuda"))
  print("{} has connected to Discord!".format(bot.user))

@bot.event
async def on_member_join(member):
  guild = member.guild
  if guild.system_channel is not None:
    if db["sending_welcome"]:
      options = welcome_messages
      if "welcome" in db.keys():
        options = options + db["welcome"].value
    welcome_message = random.choice(options).format(member.mention, member.guild.name)
    await guild.system_channel.send(welcome_message)

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  msg = message.content
  if db["responding"] and message.channel != message.guild.system_channel:
    options = starter_sentences
    if "sentences" in db.keys():
      options = options + db["sentences"].value
    if any(word in msg.lower() for word in webrole):
      await message.channel.send(random.choice(options))
  await bot.process_commands(message)

@bot.command(name="boasvindas")
async def welcome(ctx, *args):
  def update_welcome(welcome_message):
    if "welcome" in db.keys():
      welcome = db["welcome"]
      welcome.append(welcome_message)
      db["welcome"] = welcome
    else:
      db["welcome"] = [welcome_message]
    
  def delete_welcome(index):
    index = index - 1
    welcome = db["welcome"]
    if len(welcome) > index:
      del welcome[index]
    db["welcome"] = welcome
  
  action = args[0]
  args = args[1:]
  if action.lower() == "adicionar":
    message = ""
    count = 0
    for arg in args:
      if count == 0:
        message += arg
      else:
        message += " " + arg
      count += 1
    if message == "":
      return
    update_welcome(message)
    await ctx.channel.send("Mensagem de boas-vindas adicionada.")
  elif action.lower() == "remover":
    if len(args) != 1:
      return
    else:
      index = int(args[0])
      delete_welcome(index)
      await ctx.channel.send("Mensagem de boas-vindas de índice {} apagada.".format(index))
  elif action.lower() == "lista":
    welcome = []
    if "welcome" in db.keys():
      welcome = db["welcome"]
    if len(welcome.value) == 0:
      await ctx.channel.send("A lista está vazia.")
    else:
      listWelcome = ">>> "
      index = 0
      for msg in welcome.value:
        index += 1
        listWelcome += str(index) + ". " + msg + "\n"
      await ctx.channel.send(listWelcome)
  elif action.lower() == "enviando":
    value = args[0]
    if value.lower() == "verdadeiro":
      db["sending_welcome"] = True
      await ctx.channel.send("O bot está enviando mensagem de boas-vindas ao membros novos.")
    elif value.lower() == "falso":
      db["sending_welcome"] = False
      await ctx.channel.send("O bot não está enviando mensagens de boas-vindas aos membros novos.")

@bot.command(name="chucknorris")
async def get_fact(ctx):
  response = requests.get("https://api.chucknorris.io/jokes/random")
  json_data = json.loads(response.text)
  fact = json_data["value"]
  await ctx.channel.send(fact)

@bot.command(name="falar")
async def speak(ctx, *args):
  message = ""
  count = 0
  for arg in args:
    if count == 0:
      message += arg
    else:
      message += " " + arg
    count += 1
  if message == "":
    return
  await ctx.channel.send(message)

@bot.command(name="frase")
async def get_quotes(ctx):
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]["q"]
  author = json_data[0]["a"]
  em = discord.Embed(title=author, description=quote, color=discord.Colour.gold())
  await ctx.send(embed = em)

@bot.command(name="mensagem")
async def message(ctx, *args):
  def update_sentences(message):
    if "sentences" in db.keys():
      sentences = db["sentences"]
      sentences.append(message)
      db["sentences"] = sentences
    else:
      db["sentences"] = [message]
    
  def delete_message(index):
    index = index - 1
    sentences = db["sentences"]
    if len(sentences) > index:
      del sentences[index]
    db["sentences"] = sentences
  
  action = args[0]
  args = args[1:]
  if action.lower() == "adicionar":
    message = ""
    count = 0
    for arg in args:
      if count == 0:
        message += arg
      else:
        message += " " + arg
      count += 1
    if message == "":
      return
    update_sentences(message)
    await ctx.channel.send("Mensagem adicionada.")
  elif action.lower() == "remover":
    if len(args) != 1:
      return
    else:
      index = int(args[0])
      delete_message(index)
      await ctx.channel.send("Mensagem de índice {} apagada.".format(index))
  elif action.lower() == "lista":
    sentences = []
    if "sentences" in db.keys():
      sentences = db["sentences"]
    if len(sentences.value) == 0:
      await ctx.channel.send("A lista está vazia.")
    else:
      listMessages = ">>> "
      index = 0
      for msg in sentences.value:
        index += 1
        listMessages += str(index) + ". " + msg + "\n"
      await ctx.channel.send(listMessages)
  elif action.lower() == "respondendo":
    value = args[0]
    if value.lower() == "verdadeiro":
      db["responding"] = True
      await ctx.channel.send("O bot está respondendo.")
    elif value.lower() == "falso":
      db["responding"] = False
      await ctx.channel.send("O bot não está respondendo.")
  
@bot.command(name="oi")
async def hi(ctx):
  await ctx.message.reply("Olá!", mention_author=True)

@bot.command(name="rick")
async def rick(ctx):
  await ctx.message.delete()
  await ctx.channel.send("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

@bot.command(name="rolagem")
async def roll(ctx, *args):
  def Is_A_Dice(possibleDice):
    if possibleDice.find("d") == -1:
      return False
    else:
      return True
        
  def Roll_The_Dice(dice):
    d = dice.find("d")
    quantity = int(dice[:d])
    sides = int(dice[d+1:])
    result = 0
    for x in range(quantity):
      result += random.randrange(1, sides+1)
    return result

  diceInput = ""
  for arg in args:
    diceInput += arg
  if diceInput == "":
    return
  diceInput = diceInput.lower().replace(" ", "")
  details = "["+diceInput+" ("
  summand = ""
  total = 0
  index = 0
  for y in diceInput:
    index += 1
    if y == "+":
      if Is_A_Dice(summand) == True:
        result = Roll_The_Dice(summand)
        total += result
        details += str(result) + " "
        summand = ""
        continue
      else:
        total += int(summand)
        details += summand + " "
        summand = ""
        continue
    summand += y
    if index == len(diceInput):
      if Is_A_Dice(summand) == True:
        result = Roll_The_Dice(summand)
        total += result
        details += str(result) + ")]"
      else:
        total += int(summand)
        details += summand + ")]"
  await ctx.channel.send("```md\n# {}\nDetalhes:{}```".format(str(total), details))

@bot.command(name="velha")
async def tictactoe(ctx, *args):
  global board; global playerOne; global playerTwo; global startGame; global endGame; global winner; global loser; global shift
  action = ""

  def check(reaction, user):
    if (shift % 2) == 1:
      if user == playerOne:
        if str(reaction.emoji) == "1️⃣" and board["one"] == "1️⃣":
          board["one"] = "❌"
          return user == playerOne and str(reaction.emoji) == "1️⃣"
        elif str(reaction.emoji) == "2️⃣" and board["two"] == "2️⃣":
          board["two"] = "❌"
          return user == playerOne and str(reaction.emoji) == "2️⃣"
        elif str(reaction.emoji) == "3️⃣" and board["three"] == "3️⃣":
          board["three"] = "❌"
          return user == playerOne and str(reaction.emoji) == "3️⃣"
        elif str(reaction.emoji) == "4️⃣" and board["four"] == "4️⃣":
          board["four"] = "❌"
          return user == playerOne and str(reaction.emoji) == "4️⃣"
        elif str(reaction.emoji) == "5️⃣" and board["five"] == "5️⃣":
          board["five"] = "❌"
          return user == playerOne and str(reaction.emoji) == "5️⃣"
        elif str(reaction.emoji) == "6️⃣" and board["six"] == "6️⃣":
          board["six"] = "❌"
          return user == playerOne and str(reaction.emoji) == "6️⃣"
        elif str(reaction.emoji) == "7️⃣" and board["seven"] == "7️⃣":
          board["seven"] = "❌"
          return user == playerOne and str(reaction.emoji) == "7️⃣"
        elif str(reaction.emoji) == "8️⃣" and board["eight"] == "8️⃣":
          board["eight"] = "❌"
          return user == playerOne and str(reaction.emoji) == "8️⃣"
        elif str(reaction.emoji) == "9️⃣" and board["nine"] == "9️⃣":
          board["nine"] = "❌"
          return user == playerOne and str(reaction.emoji) == "9️⃣"
    elif (shift % 2) == 0:
      if user == playerTwo:
        if str(reaction.emoji) == "1️⃣" and board["one"] == "1️⃣":
          board["one"] = "⭕"
          return user == playerTwo and str(reaction.emoji) == "1️⃣"
        elif str(reaction.emoji) == "2️⃣" and board["two"] == "2️⃣":
          board["two"] = "⭕"
          return user == playerTwo and str(reaction.emoji) == "2️⃣"
        elif str(reaction.emoji) == "3️⃣" and board["three"] == "3️⃣":
          board["three"] = "⭕"
          return user == playerTwo and str(reaction.emoji) == "3️⃣"
        elif str(reaction.emoji) == "4️⃣" and board["four"] == "4️⃣":
          board["four"] = "⭕"
          return user == playerTwo and str(reaction.emoji) == "4️⃣"
        elif str(reaction.emoji) == "5️⃣" and board["five"] == "5️⃣":
          board["five"] = "⭕"
          return user == playerTwo and str(reaction.emoji) == "5️⃣"
        elif str(reaction.emoji) == "6️⃣" and board["six"] == "6️⃣":
          board["six"] = "⭕"
          return user == playerTwo and str(reaction.emoji) == "6️⃣"
        elif str(reaction.emoji) == "7️⃣" and board["seven"] == "7️⃣":
          board["seven"] = "⭕"
          return user == playerTwo and str(reaction.emoji) == "7️⃣"
        elif str(reaction.emoji) == "8️⃣" and board["eight"] == "8️⃣":
          board["eight"] = "⭕"
          return user == playerTwo and str(reaction.emoji) == "8️⃣"
        elif str(reaction.emoji) == "9️⃣" and board["nine"] == "9️⃣":
          board["nine"] = "⭕"
          return user == playerTwo and str(reaction.emoji) == "9️⃣"
          
  def someone_won():
    if board["one"] == board["two"] and board["one"] == board["three"]:
      if board["one"] == "❌":
        return "playerOne"
      elif board["one"] == "⭕":
        return "playerTwo"
    elif board["four"] == board["five"] and board["four"] == board["six"]:
      if board["four"] == "❌":
        return "playerOne"
      elif board["four"] == "⭕":
        return "playerTwo"
    elif board["seven"] == board["eight"] and board["seven"] == board["nine"]:
      if board["seven"] == "❌":
        return "playerOne"
      elif board["seven"] == "⭕":
        return "playerTwo"
    elif board["one"] == board["four"] and board["one"] == board["seven"]:
      if board["one"] == "❌":
        return "playerOne"
      elif board["one"] == "⭕":
        return "playerTwo"
    elif board["two"] == board["five"] and board["two"] == board["eight"]:
      if board["two"] == "❌":
        return "playerOne"
      elif board["two"] == "⭕":
        return "playerTwo"
    elif board["three"] == board["six"] and board["three"] == board["nine"]:
      if board["three"] == "❌":
        return "playerOne"
      elif board["three"] == "⭕":
        return "playerTwo"
    elif board["one"] == board["five"] and board["one"] == board["nine"]:
      if board["one"] == "❌":
        return "playerOne"
      elif board["one"] == "⭕":
        return "playerTwo"
    elif board["three"] == board["five"] and board["three"] == board["seven"]:
      if board["three"] == "❌":
        return "playerOne"
      elif board["three"] == "⭕":
        return "playerTwo"
    elif board["one"] != "1️⃣" and board["two"] != "2️⃣" and board["three"] != "3️⃣" and board["four"] != "4️⃣" and board["five"] != "5️⃣" and board["six"] != "6️⃣" and board["seven"] != "7️⃣" and board["eight"] != "8️⃣" and board["nine"] != "9️⃣":
      return "velha"
    else:
      return False

  for arg in args:
    action += arg
  if action == "" and playerOne == None:
    playerOne = ctx.author
    await ctx.channel.send("{} iniciou um jogo da velha!".format(playerOne.mention))
  elif action == "entrar":
    if playerOne == None and playerTwo == None:
      await ctx.channel.send("Nenhum jogo está ocorrendo.")
    elif playerOne != None and playerTwo == None:
      if ctx.author == playerOne:
        await ctx.channel.send("Infelizmente não é possível jogar contra si mesmo.")
      elif ctx.author.bot == True:
        await ctx.channel.send("Infelizmente não é possível jogar contra um bot.")
      else:
        playerTwo = ctx.author
        startGame = True
        await ctx.channel.send("{} ingressou no jogo de velha contra {}!".format(playerOne.mention, playerTwo.mention))
    elif startGame == True:
      await ctx.channel.send("Espere o atual jogo da velha terminar.")
  elif action == "encerrar":
    board = {"one": "1️⃣", "two": "2️⃣", "three": "3️⃣", "four": "4️⃣", "five": "5️⃣", "six": "6️⃣", "seven": "7️⃣", "eight": "8️⃣", "nine": "9️⃣"}
    startGame = False
    endGame = False
    playerOne = None
    playerTwo = None
    winner = None
    loser = None
    shift = 0
    await ctx.channel.send("Jogo encerrado.")
  if startGame == True:
    while startGame == True and endGame == False:
      shift += 1
      boardMessage = "{}{}{}\n{}{}{}\n{}{}{}".format(board["one"], board["two"], board["three"], board["four"], board["five"], board["six"], board["seven"], board["eight"], board["nine"])
      msg1 = await ctx.channel.send(boardMessage)
      if (shift % 2) == 1:
        msg2 = await ctx.channel.send("{}, é sua rodada!".format(playerOne.mention))
      elif (shift % 2) == 0:
        msg2 = await ctx.channel.send("{}, é sua rodada!".format(playerTwo.mention))
      for x in board:
        if board[x] != "❌" and board[x] != "⭕":
          await msg1.add_reaction(board[x])
      reaction, user = await bot.wait_for('reaction_add', check=check)
      if someone_won() != False:
        await msg1.delete()
        await msg2.delete()
        boardMessage = "{}{}{}\n{}{}{}\n{}{}{}".format(board["one"], board["two"], board["three"], board["four"], board["five"], board["six"], board["seven"], board["eight"], board["nine"])
        msg1 = await ctx.channel.send(boardMessage)
        endGame = True
        if someone_won() == "playerOne":
          winner = playerOne
          loser = playerTwo
          msg2 = await ctx.channel.send("O jogo terminou.\n{}, parabéns pela vitória!\n{}, boa sorte na próxima vez".format(winner.mention, loser.mention))
        elif someone_won() == "playerTwo":
          winner = playerTwo
          loser = playerOne
          msg2 = await ctx.channel.send("O jogo terminou.\n{}, parabéns pela vitória!\n{}, boa sorte na próxima vez!".format(winner.mention, loser.mention))
        elif someone_won() == "velha":
          msg2 = await ctx.channel.send("Deu velha! {} e {}, foi um bom jogo!".format(playerOne.mention, playerTwo.mention))
        board = {"one": "1️⃣", "two": "2️⃣", "three": "3️⃣", "four": "4️⃣", "five": "5️⃣", "six": "6️⃣", "seven": "7️⃣", "eight": "8️⃣", "nine": "9️⃣"}
        startGame = False
        endGame = False
        playerOne = None
        playerTwo = None
        winner = None
        loser = None
        shift = 0
      elif someone_won() == False:
        await msg1.delete()
        await msg2.delete()

keep_alive()
bot.run(os.environ["TOKEN"])