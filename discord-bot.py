import discord
from discord.ext import commands
from discord.utils import get 

import asyncio
import json
import time
import random

import authkey
#import opencv

#global parameters
numgame_start = False
numgame_answer = 0
guesses = 0
timealive = 0

#initialize bot information
client = commands.Bot(command_prefix = '!')
token = authkey.authkey


#state that we have connected to discord on first contact
@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

#this even happens every single time a user writes a message!
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(f"{message.author.name}: {message.content}")
    await client.process_commands(message)

# [COMMAND] simple hello to the user command
@client.command(pass_context=True)
async def hi(ctx):
    await ctx.channel.send(f"Hello {ctx.author.name}!")

# [COMMAND] guess number 
@client.command(pass_context=True)
async def numgame(ctx, num):
    global numgame_start
    global numgame_answer
    global guesses

    if not numgame_start:
        await ctx.channel.send("No number game started yet, generating random number...")
        numgame_answer = random.randrange(0,100,1)
        print(numgame_answer)
        time.sleep(3)
        await ctx.channel.send("Number between 0-100 generated, use !numgame [arg] again to begin playing!")
        numgame_start = True
    else:
        try:
            num = int(num)
            if num > numgame_answer:
                guesses += 1
                await ctx.channel.send(f"Your number is {num}. Too high, try again! You have guessed {guesses} times.")
            elif num < numgame_answer:
                guesses += 1 
                await ctx.channel.send(f"Your number is {num}. Too low, try again! You have guesses {guesses} times.")
            else:
                await ctx.channel.send(f"Your number is {num}. My number was {numgame_answer}. You win! Your guesses: {guesses}.")
                #reset parameters
                guesses = 0
                numgame_start = False
                numgame_answer = 0
        except:
            await ctx.channel.send(f"Invalid character! Please try again.")
            
# [COMMAND] rock paper scissors                  
@client.command(pass_context=True)
async def rps(ctx, user:str):
    global rps_choices
    global computer_choice
    global user_score
    global comp_score

    rps_choices = ["rock","paper","scissors"]
    computer_choice = random.choice(rps_choices)
    val = user.lower()
    
    #await ctx.channel.send(f"val:{val} comp:{computer_choice}")
    
    if val not in rps_choices:            
        if val == "reset":
            await ctx.channel.send("Resetting scoreboard...")
            time.sleep(2)
            user_score = 0
            comp_score = 0
            await ctx.channel.send("Scoreboard reset!")
        elif val == "score":
            await ctx.channel.send(f"Your score is {user_score} ---- My score is {comp_score}")
        else:
            await ctx.channel.send("not a valid option")
    else:
        if computer_choice == val:
            await ctx.channel.send(f"Tie! both players picked {val}")
        if computer_choice == "rock":
            if val == "paper":
                await ctx.channel.send(f"You win! you picked {val} and I picked {computer_choice}")
                user_score += 1
            elif val == "scissors":
                await ctx.channel.send(f"I win! you picked {val} and I picked {computer_choice}")
                comp_score += 1
        if computer_choice == "paper":
            if val == "rock":
                await ctx.channel.send(f"I win! you picked {val} and I picked {computer_choice}")
                comp_score += 1
            elif val == "scissors":
                await ctx.channel.send(f"You win! you picked {val} and I picked {computer_choice}") 
                user_score += 1   
        if computer_choice == "scissors":
            if val == "paper":
                await ctx.channel.send(f"I win! you picked {val} and I picked {computer_choice}")
                comp_score += 1    
            elif val == "rock":   
                await ctx.channel.send(f"You win! you picked {val} and I picked {computer_choice}") 
                user_score += 1
        
client.run(token)

