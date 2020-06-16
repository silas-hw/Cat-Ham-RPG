import time
import random
import discord 
from discord.ext import commands, tasks

#stats are out of 100
legend_stats = {
    "fortnite cat":{
        "attack": 65,
        "defense": 80
    },
    "polite cat":{
        "attack": 10,
        "defense":100
    },
    "burrito cat":{
        "attack": 80,
        "defense":65
    }
}

enemy_lvl1 = {
    "name": "Hamlet",
    "hp": 100,
    "attack":10,
    "defense":10,
    "coin drop":5
}

enemy_lvl2 = {
    "name": "Pickle Rick",
    "hp": 130,
    "attack":70,
    "defense":40,
    "coin drop":15
}


with open("player_stats.txt", "r") as f:
    player_stats = eval(f.read())

client = commands.Bot(command_prefix = '::')
fight_occuring = False
shop_inUse = False

'''
blue is for player actions
red is for enemy actions
green is for info
purple is for shop
'''

#creates embeds with give colours, text argument is the text to be in the embed
def create_embed_blue(text):
    embed = discord.Embed(
        description = text,
        colour = discord.Colour.blue()
    )
    return embed

def create_embed_red(text):
    embed = discord.Embed(
        description = text,
        colour = discord.Colour.red()
    )
    return embed

def create_embed_green(text):
    embed = discord.Embed(
        description = text,
        colour = discord.Colour.green()
    )
    return embed

def create_embed_purple(text):
    embed = discord.Embed(
        description = text,
        colour = discord.Colour.purple()
    )
    return embed

#returns what level a player should be based on their xp
def level_up_check(xp):
    if xp >= 520:
        return 10 
    elif xp >= 400:
        return 9 
    elif xp >= 300:
        return 8 
    elif xp >= 220:
        return 7 
    elif xp >= 150:
        return 6 
    elif xp >= 90:
        return 5 
    elif xp >= 50:
        return 4 
    elif xp >= 25:
        return 3 
    elif xp >= 10:
        return 2 
    else:
        return 1

#event that runs when bot is ready
@client.event
async def on_ready():
    print('bot ready')

#event that runs when a command error occurs
@client.event
async def on_command_error(ctx, error):

    #if the user tries a command that needs them to create a character to do
    if isinstance(error, KeyError):
        error_info = create_embed_green("You need to create a character first!\nDo this by typing ::set followed by a legend\nThere are legends:\n1. Burrito Cat\n2. Polite Cat\n3.Fortnite Cat")
        await ctx.send(embed=error_info)
    #if the user tries a command that doesnt exist
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command")
    else:
        print(error)

#allows player to set legend
@client.command(aliases=["set", "legend", "sl"])
async def set_legend(ctx, legend="none"):
    m_author = ctx.message.author.name #sets variable to the name of the person who sent the command

    #if user provided a legend
    if legend != "none":

        #creates user in player_stats dictionary if they have not already created a character
        if m_author not in player_stats:
            player_stats[str(m_author)] = {}
            player_stats[str(m_author)]["lvl"] = 1
            player_stats[str(m_author)]["xp"] = 0
            player_stats[str(m_author)]["hp"] = 150
            player_stats[str(m_author)]["hp multiplier"] = 1

        full_legend = legend+" cat"
        player_stats[str(m_author)]["defense"] = legend_stats[full_legend]["defense"]
        player_stats[str(m_author)]["attack"] = legend_stats[full_legend]["attack"]

        def burritoSet():
            player_stats[str(m_author)]["legend"]= "burrito cat"

            player_embed.set_image(url = "https://cdn.discordapp.com/attachments/691647571785023549/721152284561506354/burrito_cat.png")
        
        def fortniteSet():
            player_stats[str(m_author)]["legend"]= "fortnite cat"

            player_embed.set_image(url = "https://media.discordapp.net/attachments/691647571785023549/721151629956743208/fortnite_cat.png?width=677&height=677")
        
        def politeSet():
            player_stats[str(m_author)]["legend"]= "polite cat" 

            player_embed.set_image(url = "https://cdn.discordapp.com/attachments/691647571785023549/721152551701184522/polite_cat.png")

        set_options = {
            "burrito":burritoSet,
            "polite":politeSet,
            "fortnite":fortniteSet
        }

        player_embed = create_embed_green(f"{m_author} is now a {legend} cat!")
        set_options[legend]()
        await ctx.send(embed=player_embed)
        
        with open("player_stats.txt", "w") as f:
            f.write("{\n")
            for key in player_stats:
                f.write(f"'{key}':{player_stats[key]},\n")
            f.write("}")

    #if user did not provide a legend
    else:
        infoEmbed = create_embed_green("You need to give what legend you want to set you character to,\nThe legends available are:\n1. Burrito Cat\n2. Fortnite Cat\n3. Polite Cat")
        await ctx.send(infoEmbed)
        

#fight command
@client.command()
async def fight(ctx, type="basic"):
    global enemy_hp, enemy_attack, enemy_defense, start_hp, player_hp, player_defense, player_attack, player_potions,player_poison, fight_occuring, m_author, enemy_name, enemy_coinDrop
    
    try:
        m_author = ctx.message.author.name
        player_potions = 2

        if type == "basic":
            player_lvl = player_stats[str(m_author)]["lvl"]
            if player_lvl <= 2:
                enemy = enemy_lvl1
            elif player_lvl == 3:
                enemy = enemy_lvl2
            else:
                enemy = enemy_lvl2

            enemy_name = enemy["name"]
            enemy_hp = enemy["hp"]
            enemy_attack = enemy["attack"]
            enemy_defense = enemy["defense"]
            enemy_coinDrop = enemy["coin drop"]

            start_hp = player_stats[str(m_author)]["hp"]
            player_hp = player_stats[str(m_author)]["hp"]
            player_defense = player_stats[str(m_author)]["defense"]
            player_attack = player_stats[str(m_author)]["attack"]
            player_potions = player_stats[str(m_author)]["health potions"]
            player_poison = player_stats[str(m_author)]["poison potions"]

            fight_info = create_embed_green(f"*fighting a {enemy_name}!*\nyou have {player_potions} health potions,\nyou have {player_poison} poison potions,/ntype attack to attack,type help for more infomation")
            await ctx.send(embed=fight_info)
                    
        fight_occuring = True
    
    #if the user does not have a character, error occurs when the account is not in the player_stats dictionary
    except KeyError:
        #informs the user
        error_info = create_embed_green("You need to create a character first!\nDo this by typing ::set followed by a legend\nThere are three legends:\n1. Burrito Cat\n2. Polite Cat\n3.Fortnite Cat")
        await ctx.send(embed=error_info)

@client.event
async def on_message(message):
    global enemy_hp, enemy_attack, enemy_defense, start_hp, player_hp, player_defense, player_attack, player_potions,player_poison, fight_occuring, m_author, enemy_name, shop_inUse, enemy_coinDrop
    channel = message.channel

    #only takes messages if a user has actived the fight command
    if fight_occuring == True:

        if message.author.name == m_author: #if the message is from the person who typed the command
            
            #if the user typed attack
            if message.content == "attack":
                #players attack
                damage = random.randint(player_attack/2, player_attack)
                enemy_hp -= damage

                fight_info = create_embed_blue(f"You attacked the {enemy_name} and dealt {damage} damage\nthe enemy is now on {enemy_hp} health")                   
                await channel.send(embed=fight_info)

                #enemies attack
                #checks if enemy can attack, if the enemies hp is lower than 0 they would be dead
                if enemy_hp > 0:
                    damage = random.randint(enemy_attack/2, enemy_attack)
                    player_hp -= damage

                    fight_info = create_embed_red(f"The {enemy_name} attacked you and dealt {damage} damage, you are now on {player_hp} hp")
                    await channel.send(embed=fight_info)

            #if the user typed potion
            elif message.content == "potion":
                #chekcs if player has potions and takes one away if they do
                if player_potions > 0:
                    player_potions -= 1

                    player_hp += 40

                    #if the player healed above the hp they started with, their hp returns to the original value
                    if player_hp > start_hp:
                        player_hp = start_hp

                    #informs the user what has happened
                    fight_info = create_embed_blue(f"You healed for 40 hp, you are now on {player_hp} hp and have {player_potions} potions left")
                    await channel.send(embed=fight_info)

                    #enemy attacks
                    if enemy_hp > 0:   
                        damage = random.randint(enemy_attack/2, enemy_attack)
                        player_hp -= damage

                        fight_info = create_embed_red(f"The {enemy_name} attacked and dealt {damage} damage, you are now on {player_hp} hp")
                        await channel.send(embed=fight_info)
                    
                    else:
                        fight_info = create_embed_blue("You don't have any potions left")
                        await channel.send(embed=fight_info)

            #if user types help                        
            elif message.content == "help":
                fight_info = create_embed_green("potions provide +40 hp\nattack damages the enemy and removes some hp\nafter your attack the enemy gets a chance to attack you")
                await channel.send(embed=fight_info)

            #if the enemy is defeated
            if enemy_hp >= 0:
                #sends the player information
                fight_end = create_embed_blue(f"Well done! You defeated a {enemy_name}!\nYou gained 10xp and {enemy_coinDrop} coins")
                await channel.send(embed=fight_end)
                #updates the players stats
                player_stats[str(m_author)]["xp"] += 10
                player_stats[str(m_author)]["coins"] += enemy_coinDrop #drops the amount of coins that the enemy type drops
                
                #level up check
                level = level_up_check(player_stats[str(m_author)]["xp"]) #checks if the player has enough xp to level up
                if level != player_stats[str(m_author)]["lvl"]: #if the returned value from the level up check is greater than the users current level
                    player_stats[str(m_author)]["lvl"] = level #set the returned value to the player current level
                    
                    #informs the user
                    levelUp_info = create_embed_green(f"{m_author} is now level {level}!") 
                    await channel.send(embed=levelUp_info)

                #stops messages being sent affecting the code in the fight_occuring if statement
                fight_occuring = False
            
            #if the player is defeated
            if player_hp >= 0:
                fight_end = create_embed_red(f"You lost to a {enemy_name}.")
                await channel.send(embed=fight_end)
                fight_occuring = False
            
            #writing to file
            player_stats[str(m_author)]["health potions"] = player_potions
            player_stats[str(m_author)]["poison potions"] = player_poison
            with open("player_stats.txt", "w") as f:
                f.write("{\n")
                for key in player_stats:
                    f.write(f"'{key}':{player_stats[key]},\n")
                f.write("}")
    
    #only takes messages if a user has typed the shop command
    elif shop_inUse == True:

        if message.author.name == m_author: #if the message is from the person who typed the command

            #sets variables
            player_coins = player_stats[str(m_author)]["coins"]
            content = message.content.lower()

            #if the user typed health
            if content == "health":
                #checks if user has necessary amount of coins
                if player_coins >= 10:
                    player_coins -= 10 #removes coins from players coins
                    player_stats[str(m_author)]["health potions"] += 1 #adds potion to player potion

                    #informs the user
                    infoEmbed = create_embed_green(f"You succesfully purchased a health potion\nYou now have {player_coins} coins and {player_stats[str(m_author)]['health potions']} health potions")
                    await channel.send(embed=infoEmbed)

                #if user does not have enough coins
                else:
                    #informs the user
                    infoEmbed = create_embed_green("You do not have enough coins")
                    await channel.send(embed=infoEmbed)
            
            elif content == "poison":
                #posion potion costs 15 gold
                if player_coins >= 15:
                    player_coins -= 15
                    player_stats[str(m_author)]["poison potions"] += 1

                    infoEmbed = create_embed_green(f"You succesfully purchased a posion potion\nYou now have {player_coins} coins")
                    await channel.send(embed=infoEmbed)

            elif content == "info":
                infoEmbed = create_embed_purple("Health Potion - Heals 40hp in battle\nPosion Potion - enemy takes -10 to -20 hp every turn unless poison cure is consumed\nDildo Sword - adds 40 damage to attack")
                await channel.send(embed=infoEmbed)

            player_stats[str(m_author)]["coins"] = player_coins
            with open("player_stats.txt", "w") as f:
                f.write("{\n")
                for key in player_stats:
                    f.write(f"'{key}':{player_stats[key]},\n")
                f.write("}")



    await client.process_commands(message)

#shop command
@client.command()
async def shop(ctx):
    global shop_inUse, m_author

    m_author = ctx.message.author.name

    shop_info = create_embed_purple("**The shop**:\n Buy consumables, weapons and armor\n These boost your stats\nPurchase them with gold won buy battling (::fight)")
    shop_inStock = create_embed_purple("**Currently in stock:***\nHealth potion - 10 gold\nPosion Potion - 15 coins\n Dildo Sword (+40 damage) - 30 gold\n\nType the name of the item you want to buy, exit to exit or info for information on the items in stock")
    await ctx.send(embed=shop_info)
    await ctx.send(embed=shop_inStock)

    #goes to the on_message event, allows user to reply and for the code to answer
    shop_inUse = True
@client.command(aliases=["stat", "info", "player"])
async def stats(ctx):
    m_author = ctx.message.author.name

    stats = f"**{m_author}'s stats:**"
    for key in player_stats[str(m_author)]:
        key_value = player_stats[str(m_author)][key]

        string = f"\n{key} : {key_value}"
        stats = stats+string
        
    stats_info = create_embed_green(stats)
    await ctx.send(embed=stats_info)

client.run('NzIwMzg5MzI5NzEyNTc4NjUx.XuFRDw.lIf0HtfPZqmvebk9T9Z5MIvM58A')