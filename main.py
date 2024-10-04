import discord
import random
from discord.ext import commands

client = discord.Client()
client = commands.Bot(command_prefix = '!')
from discord.utils import get

players = []
bet = 0
deck = ['2H', '2C', '2S', '2D', '3H', '3C', '3S', '3D', '4H', '4C', '4S', '4D', '5H', '5C', '5S', '5D', '6H', '6C', '6S', '6D', '7H', '7C', '7S', '7D', '8H', '8C', '8S', '8D', '9H', '9C', '9S', '9D', '10H', '10C', '10S', '10D', 'JH', 'JC', 'JS', 'JD', 'QH', 'QC', 'QS', 'QD', 'KH', 'KC', 'KS', 'KD', 'AH', 'AC', 'AS', 'AD']

chosenDeck = [[]]
money = []
moneybet = []
stayedplayers = []
dealerhand = []
dealerbust = False


@client.command()
async def join(ctx):
  global players
  global money
  if not str(ctx.author) in players:
    await ctx.send(str(ctx.author) + ', joined!')
    players.append(ctx.author)
    money.append(100)

  else:
    await ctx.send(str(ctx.author) + ', you already joined!')

@client.command()
async def showplayers(ctx):
  global players
  await ctx.send(players)

@client.command()
async def reset(ctx):
  global players
  global bet
  global deck
  global chosenDeck
  global money
  global moneybet
  global stayedplayers
  global dealerhand
  global dealerbust

  players = []
  bet = 0
  deck = ['2H', '2C', '2S', '2D', '3H', '3C', '3S', '3D', '4H', '4C', '4S', '4D', '5H', '5C', '5S', '5D', '6H', '6C', '6S', '6D', '7H', '7C', '7S', '7D', '8H', '8C', '8S', '8D', '9H', '9C', '9S', '9D', '10H', '10C', '10S', '10D', 'JH', 'JC', 'JS', 'JD', 'QH', 'QC', 'QS', 'QD', 'KH', 'KC', 'KS', 'KD', 'AH', 'AC', 'AS', 'AD']

  chosenDeck = [[]]
  money = []
  moneybet = []
  stayedplayers = []
  dealerhand = []
  dealerbust = False

  await ctx.send("Reset")

@client.command()
async def play_round(ctx):
  global bet
  global moneybet
  global i
  global chosenDeck
  global deck
  global players
  global money
  global stayedplayers
  global dealerhand
  global dealerbust
  if not len(players) == 0:
    for x in range(0, len(players)):
      await ctx.send(str(players[x]) + ', how much would you like to bet?')
      msg = await client.wait_for('message', check=lambda message: message.author == players[x])
      bet = int(msg.content)
      if not bet > money[x] and bet > 0:
        moneybet.append(bet)
        await ctx.send('Okay.')
        num1 = random.randint(0, len(deck)-1)
        num2 = num1
        
        while num2 == num1:
          num2 = random.randint(0, len(deck)-1)

        chosenDeck.append([deck[num1], deck[num2]])
        deck.pop(max(num1, num2))
        deck.pop(min(num1, num2))
        await ctx.send(str(players[x]) + ', you were drawn ' + str(chosenDeck[x+1]))
        await ctx.send(str(players[x]) + ', your hand is worth ' + str(calcHand(chosenDeck[x+1])))
      else:
        await ctx.send('This exceeds your total')

    num1 = random.randint(0, len(deck)-1)
    num2 = num1
        
    while num2 == num1:
      num2 = random.randint(0, len(deck)-1)

    dealerhand.append(deck[num1])
    dealerhand.append(deck[num2])
    deck.pop(max(num1, num2))
    deck.pop(min(num1, num2))
    await ctx.send('The dealer\'s first card is ' + str(dealerhand[0]))
        
    for x in range(0, len(players)):
      await decision(ctx, x)

    while calcHand(dealerhand) < 16:
      await ctx.send('The dealer hits.')
      num1 = random.randint(0, len(deck)-1)

      dealerhand.append(deck[num1])
      deck.pop(num1)
      await ctx.send('The dealer\'s hand is ' + str(dealerhand))
      await ctx.send('The dealer\'s total is ' + str(calcHand(dealerhand)))

      if calcHand(dealerhand) > 21:
        await ctx.send('The dealer busts.')
        dealerbust = True

        
    for x in stayedplayers:
      if dealerbust:
        money[x] = money[x] + moneybet[x]
      else:
        if calcHand(chosenDeck[x+1]) > calcHand(dealerhand):
          await ctx.send(str(players[x]) + ', you won!')
          money[x] = money[x] + moneybet[x]
        else:
          await ctx.send(str(players[x]) + ', you lost!')
          money[x] = money[x] - moneybet[x]

    await ctx.send(str(dealerhand))
    
    for x in range(0, len(players)):
      await ctx.send(str(players[x]) + '\'s balance is ' + str(money[x]))
    bet = 0
    deck = ['2H', '2C', '2S', '2D', '3H', '3C', '3S', '3D', '4H', '4C', '4S', '4D', '5H', '5C', '5S', '5D', '6H', '6C', '6S', '6D', '7H', '7C', '7S', '7D', '8H', '8C', '8S', '8D', '9H', '9C', '9S', '9D', '10H', '10C', '10S', '10D', 'JH', 'JC', 'JS', 'JD', 'QH', 'QC', 'QS', 'QD', 'KH', 'KC', 'KS', 'KD', 'AH', 'AC', 'AS', 'AD']

    chosenDeck = [[]]
    moneybet = []
    stayedplayers = []
    dealerhand = []
    dealerbust = False
  else:
    await ctx.send('No players!')

async def decision(ctx, x):
      global bet
      global moneybet
      global i
      global chosenDeck
      global deck
      global players
      global money
      global stayedplayers
      await ctx.send(str(players[x]) + ', would you like to hit or stay')
      msg = await client.wait_for('message', check=lambda message: message.author == players[x])
      if 'hit' in msg.content.lower():
        num1 = random.randint(0, len(deck)-1)
        chosenDeck[x+1].append(deck[num1])
        deck.pop(num1)
        await ctx.send(str(players[x]) + ', your updated hand ' + str(chosenDeck[x+1]))
        await ctx.send(str(players[x]) + ', your new hand is worth ' + str(calcHand(chosenDeck[x+1])))
        if calcHand(chosenDeck[x+1]) < 21:
          await decision(ctx, x)
        elif calcHand(chosenDeck[x+1]) == 21:
          await ctx.send(str(players[x]) + ', you received a blackjack!')
          money[x] = money[x] + moneybet[x]
        else:
          await ctx.send(str(players[x]) + ', you busted, bozo!')
          money[x] = money[x] - moneybet[x]
      elif 'stay' in msg.content.lower():
        await ctx.send(str(players[x]) + ', your hand is still ' + str(chosenDeck[x+1]))
        stayedplayers.append(x)
  
def calcHand(poop):
  totalWorth = 0
  
  for pee in poop:
    firstLetter = pee[0:1]

    if firstLetter == 'K' or firstLetter == 'Q' or firstLetter == 'J' or firstLetter == 'A' or pee[0:2] == '10':
      if firstLetter == 'A':
        totalWorth = totalWorth + 1
      else:
        totalWorth = totalWorth + 10
    else:
      totalWorth = totalWorth + int(firstLetter)
      
  return totalWorth

@client.command()
async def rules(ctx):
  await ctx.send('```Basic Blackjack Rules: \n\n- The goal of blackjack is to beat the dealer\'s hand without going over 21. \n- Face cards are worth 10. Aces are worth 1 or 11, whichever makes a better hand. \n- Each player starts with two cards, one of the dealer\'s cards is hidden until the end. \n- To \'Hit\' is to ask for another card. To \'Stand\' is to hold your total and end your turn. \n- If you go over 21 you bust, and the dealer wins regardless of the dealer\'s hand. \n- If you are dealt 21 from the start (Ace & 10), you got a blackjack. \n- Blackjack usually means you win 1.5 the amount of your bet. Depends on the casino. \n- Dealer will hit until his/her cards total 17 or higher. \n- Doubling is like a hit, only the bet is doubled and you only get one more card. \n- Split can be done when you have two of the same card - the pair is split into two hands. \n- Splitting also doubles the bet, because each new hand is worth the original bet. \n- You can only double/split on the first move, or first move of a hand created by a split. \n- You cannot play on two aces after they are split. \n- You can double on a hand resulting from a split, tripling or quadrupling you bet.```')

@client.event
async def on_ready():
  print('Bot is ready')

  
client.run('')