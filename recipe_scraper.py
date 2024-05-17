import requests
from bs4 import BeautifulSoup
#
URL = "https://www.recipetineats.com/spaghetti-bolognese/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(id="wprm-recipe-container-25094")

recipe_name = results.find("h2", class_="wprm-recipe-name wprm-block-text-bold")
ingredient_elements = results.find_all("li", class_="wprm-recipe-ingredient")
instruction_elements = results.find_all("li", class_="wprm-recipe-instruction")
# ingredient_elements = results.find_all("span", class_="wprm-recipe-ingredient-name")


print(f"\n               {recipe_name.text}               ")
print("\n**Ingredients:**\n")
for ingredient_element in ingredient_elements:
    amount_element = ingredient_element.find("span", class_="wprm-recipe-ingredient-amount")
    unit_element = ingredient_element.find("span", class_="wprm-recipe-ingredient-unit")
    name_element = ingredient_element.find("span", class_="wprm-recipe-ingredient-name")
    if amount_element != None:
        print(f"{amount_element.text} ", end="")
    if unit_element != None:
        print(f"{unit_element.text} ", end="")
    if name_element != None:
        print(name_element.text)
print()

print("\n**Instructions:**\n")
index = 1
for instruction_element in instruction_elements:
    text_element = instruction_element.find("div", class_="wprm-recipe-instruction-text")
    if text_element != None:
        print(f"{index}: {text_element.text}")
        index += 1
    
print()


