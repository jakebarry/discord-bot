import asyncio
import random
from discord.ext import commands, tasks
from typing import Final
import os
from dotenv import load_dotenv
import discord
from discord import Intents
import pymongo
from pymongo import MongoClient



load_dotenv(override=True)

BOT_TOKEN: Final[str] = os.getenv("BOT_TOKEN")
CHANNEL_ID: Final[int] = int(os.getenv("CHANNEL_ID"))

intents: Intents = Intents.default()
intents.message_content = True

# print(BOT_TOKEN)
# print(CHANNEL_ID)
# print(type(CHANNEL_ID))

bot = commands.Bot(command_prefix="!", intents=intents)

# Initialise meal class
class Meal:
    def __init__(self, name, type, ingredients, instructions):
        self.name = name
        self.type = type
        self.ingredients = ingredients
        self.instructions = instructions

# Set up database
def get_db_session():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['MealPlanner']
    collection = db['Meals']
    return collection


# Initial bot message
@bot.event
async def on_ready():
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Hello! RecipeBot is ready!")
    await channel.send("Type !help to see available commands.")


# !hello: Bot sends a hello message to the user.
@bot.command(brief='Bot sends a hello message to the user')
async def hello(ctx):
    user_id = ctx.author.name
    await ctx.send(f"Hello, {user_id}!")

# @bot.command()
# async def add(ctx, *arr):
#     result = 0
#     for i in arr:
#         result += int(i)

#     await ctx.send(f"Result = {result}")

@bot.command(brief='Provide a URL for a meal to add to the database')
async def addmeal(ctx):
    await ctx.send("Send the link of the recipe you would like to add to the database")

    try:
        user_link = await bot.wait_for('message', check=check, timeout=60)
    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond.")
    return

    # await ctx.send("Sorry! Function not implemented yet.")


@bot.command(brief='See accepted websites to use for a recipe submission')
async def websites(ctx):
    embed = discord.Embed(title='RecipeTin Eats', url='https://www.recipetineats.com/', color=0xf4796c)
    await ctx.send("The following websites will work with the URL submission:\n")
    await ctx.send(embed=embed)
    # await ctx.send("The following websites will work with the URL submission:\n\nRecipeTinEats (www.recipetineats.com)")

    
@bot.command(brief='See all available meals in database')
async def seemeals(ctx):
    db_session = get_db_session()
    meal_list = db_session.find({}, {"Meal": 1})
    for meal in meal_list:
        await ctx.send(meal['Meal'])



@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("There is such command.\nType !help to see available commands.")
    else:
        raise error

@bot.command(brief='Receive a recipe idea with ingredients and instructions')
async def planmeal(ctx):
    db_session = get_db_session()
    await ctx.send("Please select an option:\n1. Vegetarian\n2. Low-Carb\n3. High-Protein\n")

    # Define check function to filter messages from the original author and the same channel
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    
    try:
        user_meal_choice = await bot.wait_for('message', check=check, timeout=60)
    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond.")
        return

    # meal = None
    # if user_meal_choice.content.lower() in ['1', 'vegetarian']:
    #     await ctx.send("You chose Vegetarian.")
    #     meal = 1
    # elif user_meal_choice.content.lower() in ['2', 'low-carb', 'low', 'carb']:
    #     await ctx.send("You chose Low-Carb.")
    #     meal = 2
    # elif user_meal_choice.content.lower() in ['3', 'high-protein', 'high', 'protein']:
    #     await ctx.send("You chose High-Protein.")
    #     meal = 3
    # else:
    #     await ctx.send("Invalid choice. Please select a valid option.")
    
    # if meal:
    #     await ctx.send(f"Here's your meal suggestion based on your choice:\n{meal}")


    meal_choice = user_meal_choice.content.lower()

    if meal_choice in ['1', 'vegetarian']:
        meals = db_session.find({'Type': 'Vegetarian'})
    elif meal_choice in ['2', 'low-carb', 'low', 'carb']:
        meals = db_session.find({'Type': 'Low-Carb'})
    elif meal_choice in ['3', 'high-protein', 'high', 'protein']:
        meals = db_session.find({'Type': 'High-Protein'})
    else:
        await ctx.send("Invalid choice. Please select a valid option.")
        return
    

    meals_list = [meal for meal in meals]
    
    if meals_list:
        selected_meal = random.choice(meals_list)
        await ctx.send(f"Here's your meal suggestion based on your choice:\n{selected_meal['Meal']}")
    else:
        await ctx.send("No meals found for the selected type.")






# Set up database
# client = pymongo.MongoClient('mongodb://lcalhost:27017/')
# db = client['meal_database']
# collection = db['meal_collection']

# @bot.command(name='savemealplan')
# async def save_meal_plan(ctx, plan_name):
#     user_id = ctx.author.id  # This line retrieves the user_id of the message author
#     user_data = collection.find_one({'user_id': user_id})
#     if user_data:
#         # Update existing data
#         collection.update_one({'user_id': user_id}, {'$set': {'meal_plan': plan_name}})
#     else:
#         # Insert new user data
#         new_data = {'user_id': user_id, 'meal_plan': plan_name}
#         collection.insert_one(new_data)

#     await ctx.send(f'{plan_name} meal plan saved for user {user_id}')



bot.run(BOT_TOKEN)

