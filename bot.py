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
import validators
import tldextract
import requests
from bs4 import BeautifulSoup

load_dotenv(override=True)

BOT_TOKEN: Final[str] = os.getenv("BOT_TOKEN")
CHANNEL_ID: Final[int] = int(os.getenv("CHANNEL_ID"))
MAX_TIMEOUT: Final[int] = 60

intents: Intents = Intents.default()
intents.message_content = True

# print(BOT_TOKEN)
# print(CHANNEL_ID)
# print(type(CHANNEL_ID))

bot = commands.Bot(command_prefix="!", intents=intents)

accepted_websites = ["recipetineats"]


# Initialise meal class
class Meal:
    def __init__(self, name, category, ingredients, instructions):
        self.name = name
        self.category = category
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


@bot.command(name='survey')
async def survey(ctx):
    # Prompt the user with questions here
    await ctx.send('What is your username?')




# !addmeal: Allows user to provide a URL for a meal to be added to the database
@bot.command(brief='Provide a URL for a meal to add to the database')
async def addmeal(ctx):
    await ctx.send("Send the link of the recipe you would like to add to the database")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    
    try:
        user_link_choice = await bot.wait_for('message', check=check, timeout=MAX_TIMEOUT)
    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond.")
        return
    
    link_choice = user_link_choice.content.lower()

    valid = validators.url(link_choice)

    website_domain = tldextract.extract(link_choice).domain

    # Check if website is supported
    if website_domain not in accepted_websites:
        await ctx.send("This website is not currently supported. Use !websites to see a supported list.")
        return

    # Check if website is valid
    # if valid:
    #     await ctx.send("That URL is valid, thank-you.")
    # else:
    #     await ctx.send("Invalid URL. Try again.")

    if not valid:
        await ctx.send("Invalid URL. Try again.")
        
    await ctx.send("What category do you wish to place this recipe into?"
                "\n1. Vegetarian\n2. Low-Carb\n3. High-Protein\n")
    # Define check function to filter messages from the original author and the same channel
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    
    try:
        user_meal_choice = await bot.wait_for('message', check=check, timeout=60)
    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond.")
        return
    
    meal_choice = user_meal_choice.content.lower()

    if meal_choice in ['1', 'vegetarian']:
        category = "Vegetarian"
    elif meal_choice in ['2', 'low-carb', 'low', 'carb']:
        category = "Low-Carb"
    elif meal_choice in ['3', 'high-protein', 'high', 'protein']:
        category = "High-Protein"

    # Need to loop to allow multiple choices
    else:
        await ctx.send("Invalid choice. Please select a valid option.")
        return
    


    recipe = recipe_scraper(ctx, link_choice, category) 

    if recipe == 0:
        await ctx.send("Invalid URL. Make sure the URL directs toward a recipe with ingredients and instructions.")
    elif recipe == 1:
        await ctx.send("Recipe has been added.")
    elif recipe == 2:
        await ctx.send("This recipe already exists in the database.")


        

    # if recipe_scraper(ctx, link_choice):
    #     await ctx.send("Recipe has been added.")
    # else:
    #     await ctx.send("Invalid URL. Make sure the URL directs toward a recipe with ingredients and instructions.")

    



# Returns {0: ,1: , 2: }
def recipe_scraper(ctx, URL, category):
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find(class_="wprm-recipe-container")


    try:
        recipe_name = results.find("h2", class_="wprm-recipe-name wprm-block-text-bold")
        ingredient_elements = results.find_all("li", class_="wprm-recipe-ingredient")
        instruction_elements = results.find_all("li", class_="wprm-recipe-instruction")
    except AttributeError as e:
        # print(e)
        # print("Invalid URL")
        return 0
    
    # ingredient_elements = results.find_all("span", class_="wprm-recipe-ingredient-name")


    # print(f"\n               {recipe_name.text}               ")
    # print("\n**Ingredients:**\n")

    ingredients = []
    instructions = []

    for ingredient_element in ingredient_elements:
        ingredient = {}
        amount_element = ingredient_element.find("span", class_="wprm-recipe-ingredient-amount")
        unit_element = ingredient_element.find("span", class_="wprm-recipe-ingredient-unit")
        name_element = ingredient_element.find("span", class_="wprm-recipe-ingredient-name")
        if amount_element != None:
            ingredient["amount"] = amount_element.text
            # print(f"{amount_element.text} ", end="")
        else:
            ingredient["amount"] = ""
        if unit_element != None:
            ingredient["unit"] = unit_element.text
            # print(f"{unit_element.text} ", end="")
        else:
            ingredient["unit"] = ""
        if name_element != None:
            ingredient["name"] = name_element.text
        else:
            ingredient["name"] = ""
            # print(name_element.text)

        # ingredient = {
        #     "amount": amount_element,
        #     "unit": unit_element,
        #     "name": name_element
        # }

        ingredients.append(ingredient)
    
    # print(ingredients)


    # print("\n**Instructions:**\n")
    index = 1
    for instruction_element in instruction_elements:
        text_element = instruction_element.find("div", class_="wprm-recipe-instruction-text")
        if text_element != None:
            instruction = {
                "step": index,
                "description": text_element.text
            }

            # print(f"{index}: {text_element.text}")
            index += 1
        instructions.append(instruction)
    
    # print(instructions)
        


    recipe = {
        "name": recipe_name.text,
        "category": category,
        "ingredients": ingredients,
        "instructions": instructions
    }

    # print(recipe)


    # Check if the recipe already exists in the database
    db_session = get_db_session()

    # print(db_session.find_one({"name": recipe_name.text}))
    # print(db_session.count_documents({"name": recipe_name.text}))

    if db_session.count_documents({"name": recipe_name.text}) < 1:
        # print("\n** TESTING **")
        db_session.insert_one(recipe)
        return 1
    # else:
        # ctx.send("This recipe is already in the database.")

    return 2



@bot.command(brief='See accepted websites to use for a recipe submission')
async def websites(ctx):
    embed = discord.Embed(title='RecipeTin Eats', url='https://www.recipetineats.com/', color=0xf4796c)
    await ctx.send("The following websites will work with the URL submission:\n")
    await ctx.send(embed=embed)
    # await ctx.send("The following websites will work with the URL submission:\n\nRecipeTinEats (www.recipetineats.com)")

    
@bot.command(brief='See all available meals in database')
async def seemeals(ctx):
    db_session = get_db_session()
    meal_list = db_session.find({}, {"name": 1})
    for meal in meal_list:
        await ctx.send(meal['name'])



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
    

    meal_choice = user_meal_choice.content.lower()

    if meal_choice in ['1', 'vegetarian']:
        meals = db_session.find({'category': 'Vegetarian'})
    elif meal_choice in ['2', 'low-carb', 'low', 'carb']:
        meals = db_session.find({'category': 'Low-Carb'})
    elif meal_choice in ['3', 'high-protein', 'high', 'protein']:
        meals = db_session.find({'category': 'High-Protein'})
    else:
        await ctx.send("Invalid choice. Please select a valid option.")
        return
    

    meals_list = [meal for meal in meals]
    
    if meals_list:
        selected_meal = random.choice(meals_list)
        await ctx.send(f"Here's your meal suggestion based on your choice:\n\n                          **{selected_meal['name']}**")
        await ctx.send("**INGREDIENTS**")
        for ingredient in selected_meal['ingredients']:
            await ctx.send(f"{ingredient['amount']} {ingredient['unit']} {ingredient['name']}")
        await ctx.send("\n**INSTRUCTIONS**\n")
        for instruction in selected_meal['instructions']:
            await ctx.send(f"**{instruction['step']}.** {instruction['description']}")

    else:
        await ctx.send("No meals found for the selected category.")

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

