import discord
from discord.ext import commands
import re
import json
import sys
import requests
import urllib.request
import os
import time
from threading import Thread
import pymongo
import asyncio
import websockets
import tweepy


mongo_key = os.environ.get("MONGO")
db_client = pymongo.MongoClient(
    mongo_key
)

bot = commands.Bot(command_prefix='>')
discord_client = discord.Client()
db = db_client["tezosGuild"]

# Bot Commands


@bot.command()
async def check_bot(ctx):
    await ctx.send('Bot is alive!')


@bot.command(pass_context=True)
async def add_college(ctx, *, text: str):
    try:
        guild = ctx.guild
        member = ctx.author
        channel = ctx.channel
        clg = text.replace(" ", "").replace(",", "_").lower()
        regex = re.compile('[@!#$%^&*()<>?/\|}{~:]')
        roles = [str(i) for i in member.roles]

        if "admin" in roles:
            if not(regex.search(clg) == None):
                await ctx.send("Wrong College Name!! \nContact **Admin**, or read guidelines again.")
                return

            clg_role = discord.utils.get(guild.roles, name=clg)
            if not clg_role:
                await guild.create_role(name=clg, permissions=discord.Permissions(read_messages=True), colour=discord.Colour.blue(), mentionable=True, reason="Add college "+clg)
                clg_role = discord.utils.get(guild.roles, name=clg)
                await ctx.send("Created Role "+str(clg_role))
            else:
                await ctx.send("Role Already Exists "+str(clg_role))
            return
        else:
            await ctx.send("You are not admin.")
            return
    except:
        await ctx.send("Check command format or contact **Admin**")


@bot.command(pass_context=True)
async def set_college(ctx, user: discord.User, *, text: str):
    try:
        guild = ctx.guild
        member = ctx.author
        channel = ctx.channel

        clg = text.replace(" ", "").replace(",", "_").lower()
        regex = re.compile('[@!#$%^&*()<>?/\|}{~:]')
        new_mem_id = user.id
        new_mem = await guild.fetch_member(new_mem_id)
        roles = [str(i) for i in member.roles]

        if "Community Lead" in roles:
            all_role = [str(i) for i in guild.roles]
            if clg in all_role:
                clg_role = discord.utils.get(guild.roles, name=clg)
                await new_mem.add_roles(clg_role, atomic=True, reason="Add college "+clg)
                await ctx.send(str(new_mem) + " granted role of " + str(clg_role))
                return
            else:
                await ctx.send("Contact **Admin** to get your college name.")
                return

        else:
            if member == new_mem:
                if not(regex.search(clg) == None):
                    await ctx.send("Wrong College Name!! \nContact **Admin**, or read guidelines again.")
                    return
                clg_role = discord.utils.get(guild.roles, name=clg)
                if not clg_role:
                    await ctx.send("College not found!! Contact your Community Lead or @admin.")
                else:
                    await new_mem.add_roles(clg_role, atomic=True, reason="Add college "+clg)
                    await ctx.send(str(new_mem) + " granted role of " + str(clg_role))
                return
            else:
                await ctx.send("Tag yourself to give role!!\n Or Contact your Community Lead.")
                return
    except:
        await ctx.send("Check command format or contact **Admin**")


@bot.command(pass_context=True)
async def set_college_lead(ctx, user: discord.User, *, text: str):
    try:
        guild = ctx.guild
        member_id = user.id
        member = await guild.fetch_member(member_id)

        channel = ctx.channel
        clg = text.replace(" ", "").replace(",", "_").lower()
        regex = re.compile('[@!#$%^&*()<>?/\|}{~:]')
        roles = [str(i) for i in member.roles]
        if "admin" in roles:
            if not(regex.search(clg) == None):
                await ctx.send("Wrong College Name!! \nContact **Admin**, or read guidelines again.")
                return

            role_name = clg + " | " + "Lead"
            clg_lead_role = discord.utils.get(guild.roles, name=role_name)
            lead_role = discord.utils.get(guild.roles, name="Community Lead")
            clg_role = discord.utils.get(guild.roles, name=clg)

            if not clg_lead_role:
                await guild.create_role(name=role_name, permissions=discord.Permissions(read_messages=True), colour=discord.Colour.gold(), mentionable=True, reason="Add college lead"+role_name)
                clg_lead_role = discord.utils.get(guild.roles, name=role_name)
                await ctx.send("Created Role "+str(clg_lead_role))

            if not clg_role:
                await guild.create_role(name=clg, permissions=discord.Permissions(read_messages=True), colour=discord.Colour.blue(), mentionable=True, reason="Add college name"+clg)
                clg_role = discord.utils.get(guild.roles, name=clg)
                await ctx.send("Created Role "+str(clg_role))

            if not lead_role:
                await guild.create_role(name="Community Lead", permissions=discord.Permissions(read_messages=True), colour=discord.Colour.red(), mentionable=True, reason="Add community lead")
                lead_role = discord.utils.get(
                    guild.roles, name="Community Lead")
                await ctx.send("Created Role "+str(lead_role))

            clg_lead_role = discord.utils.get(guild.roles, name=role_name)
            lead_role = discord.utils.get(guild.roles, name="Community Lead")
            clg_role = discord.utils.get(guild.roles, name=clg)

            await member.add_roles(clg_lead_role, atomic=True, reason="Add college Lead"+clg)
            await member.add_roles(clg_role, atomic=True, reason="Add college "+clg)
            await member.add_roles(lead_role, atomic=True, reason="Add Community Lead")

            await ctx.send(str(member) + " granted role of " + str(clg_lead_role))
            await ctx.send(str(member) + " granted role of " + str(lead_role))
            await ctx.send(str(member) + " granted role of " + str(clg_role))
            return
        else:
            await ctx.send("You are not admin.")
            return
    except Exception as e:
        print(e)
        await ctx.send("Check command format or contact **Admin**")


@bot.command(pass_context=True)
async def set_db(ctx, user: discord.User, clg: discord.Role, *, text: str):
    try:
        guild = ctx.guild
        lead_id = user.id
        lead = await guild.fetch_member(lead_id)

        clg_role_id = clg.id
        clg_role = guild.get_role(clg_role_id)
        channel = ctx.channel
        auth = ctx.author
        roles = [str(i) for i in auth.roles]
        if "admin" in roles:
            text = text.split(" ")
            insta_link = ""
            twitter_link = ""
            linkedin_link = ""
            youtube_link = ""
            medium_link = ""
            discord_link = ""
            for i in text:
                if "instagram" in i:
                    insta_link = i
                elif "twitter" in i:
                    twitter_link = i
                elif "linkedin" in i:
                    linkedin_link = i
                elif "youtube" in i:
                    youtube_link = i
                elif "discord" in i:
                    discord_link = i
                elif "medium" in i:
                    medium_link = i
                # await ctx.send(i)
            clg_list_db = db["colleges"]
            if not clg_list_db.find_one({"college_name": str(clg_role)}):
                clg_name_id = db.colleges.insert_one(
                    {"college_name": str(clg_role)}).inserted_id
                await ctx.send(str(clg_role) + " Added at " + str(clg_name_id))

            lead_db = db["lead"]
            if not lead_db.find_one({"college_name": str(clg_role), "lead_name": str(lead)}):

                lead_data = {
                    "college_name": str(clg_role),
                    "college_id": str(clg_role_id),
                    "lead_name": str(lead),
                    "lead_id": str(lead_id),
                }
                lead_data_id = lead_db.insert_one(lead_data).inserted_id

                await ctx.send(str(lead)+" Added to MongoDB at " + str(lead_data_id))
            else:
                await ctx.send(str(lead)+" Already Exists in MongoDB")

            social_ = db["social_"]
            if not social_.find_one({"college_name": str(clg_role)}):

                social_data = {
                    "college_name": str(clg_role),
                    "college_id": str(clg_role_id),
                    "instagram_": insta_link,
                    "discord_": discord_link,
                    "medium_": medium_link,
                    "youtube_": youtube_link,
                    "linkedin_": linkedin_link,
                    "twitter_": twitter_link
                }
                social_id = social_.insert_one(social_data).inserted_id

                await ctx.send("Social Data added to MongoDB at " + str(social_id))
            else:
                await ctx.send("Social Media Already Exists")
        else:
            await ctx.send("You are not admin.")
            return

    except Exception as e:
        print(e)
        await ctx.send("Check command format or contact **Admin**")


# Instagram

def get_user_fullname(html):
    return html.json()["graphql"]["user"]["full_name"]


def get_total_photos(html):
    return int(html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["count"])


def get_last_publication_url(html):
    return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["shortcode"]


def get_last_photo_url(html):
    return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["display_url"]


def get_last_thumb_url(html):
    return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["thumbnail_src"]


def get_description_photo(html):
    return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"]


def get_instagram_html(INSTAGRAM_USERNAME):
    headers = {
        "Host": "www.instagram.com",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }
    html = requests.get("https://www.instagram.com/" +
                        INSTAGRAM_USERNAME + "/feed/?__a=1", headers=headers)
    return html


MY_CHANNEL_ID = 859902674596921364


@bot.event
async def on_ready():
    global channel
    while True:
        if not channel:
            channel = bot.get_channel(MY_CHANNEL_ID)  # access to channel

        if not channel:
            print("[on_ready] can't access channel:", MY_CHANNEL_ID)
        else:
            clg_db = db.colleges.find()
            social_db = db.social_.find()
            visited_ = db["visited_"]
            brk = await bot.fetch_channel(MY_CHANNEL_ID)
            for _name in list(clg_db):

                clg_name = _name["college_name"]
                brk = await bot.fetch_channel(MY_CHANNEL_ID)
                for _social in list(social_db):
                    brk = await bot.fetch_channel(MY_CHANNEL_ID)
                    if _social["college_name"] == clg_name:

                        social_insta = _social["instagram_"]
                        insta_id = str(social_insta).replace(
                            "https://www.instagram.com", "").replace("/", "")
                        html = get_instagram_html(insta_id)
                        visited_db = db.visited_.find()
                        visit_link = [_link["link"] for _link in visited_db]
                        brk = await bot.fetch_channel(MY_CHANNEL_ID)
                        if(get_last_publication_url(html) in visit_link):
                            brk = await bot.fetch_channel(MY_CHANNEL_ID)

                        else:
                            id_ = visited_.insert_one(
                                {"link": get_last_publication_url(html)})
                            em = discord.Embed(color=15467852,
                                               title="Post by @"+insta_id+"",
                                               url="https://www.instagram.com/p/" +
                                               get_last_publication_url(
                                                   html)+"/",
                                               description=get_description_photo(
                                                   html),
                                               image=get_last_photo_url(html),
                                               thumbnail=get_last_thumb_url(
                                                   html),
                                               )

                            await channel.send(embed=em)


channel = None   # set default value at start


if __name__ == "__main__":
    bot_key = os.environ.get("KEY")
    bot.run(bot_key)
