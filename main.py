import discord
from discord import permissions
from discord.ext import commands
import re
import requests
import pymongo
import ssl
import time
import requests
from discord import Webhook, RequestsWebhookAdapter, AsyncWebhookAdapter
import aiohttp
import asyncio
import tweepy
import os

#Twitter Client
twitter_consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
twitter_consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
tweet_auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)

twitter_access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
twitter_access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
tweet_auth.set_access_token(twitter_access_token, twitter_access_token_secret)
tweet_api = tweepy.API(tweet_auth)


# Mongo DB
mongo_key = os.environ.get("MONGO")
db_client = pymongo.MongoClient(
    mongo_key,
    ssl_cert_reqs=ssl.CERT_NONE
)
db = db_client["tezosGuild"]


# Discord Client
bot = commands.Bot(command_prefix='--')
# discord_client = discord.Client()

channel = None   # set default value at start
guild = None    # set default value at start

# Roles Permissions
admin_ = discord.Permissions(
    add_reactions=True,
    administrator=True,
    attach_files=True,
    ban_members=True,
    change_nickname=True,
    connect=True,
    create_instant_invite=True,
    deafen_members=True,
    embed_links=True,
    external_emojis=True,
    kick_members=True,
    manage_channels=True,
    manage_emojis=True,
    manage_guild=True,
    manage_messages=True,
    manage_nicknames=True,
    manage_permissions=True,
    manage_roles=True,
    manage_webhooks=True,
    mention_everyone=True,
    move_members=True,
    mute_members=True,
    priority_speaker=True,
    read_message_history=True,
    read_messages=True,
    request_to_speak=True,
    send_messages=True,
    send_tts_messages=True,
    speak=True,
    stream=True,
    use_external_emojis=True,
    use_slash_commands=False,
    use_voice_activation=True,
    view_audit_log=True,
    view_channel=True,
    view_guild_insights=False
)
tezos_team_ = discord.Permissions(
    add_reactions=True,
    administrator=False,
    attach_files=True,
    ban_members=True,
    change_nickname=True,
    connect=True,
    create_instant_invite=True,
    deafen_members=True,
    embed_links=True,
    external_emojis=True,
    kick_members=True,
    manage_channels=True,
    manage_emojis=True,
    manage_guild=False,
    manage_messages=True,
    manage_nicknames=True,
    manage_permissions=True,
    manage_roles=True,
    manage_webhooks=False,
    mention_everyone=True,
    move_members=True,
    mute_members=True,
    priority_speaker=True,
    read_message_history=True,
    read_messages=True,
    request_to_speak=True,
    send_messages=True,
    send_tts_messages=True,
    speak=True,
    stream=True,
    use_external_emojis=True,
    use_slash_commands=False,
    use_voice_activation=True,
    view_audit_log=False,
    view_channel=True,
    view_guild_insights=False
)
moderator_ = discord.Permissions(
    add_reactions=True,
    administrator=False,
    attach_files=True,
    ban_members=True,
    change_nickname=True,
    connect=True,
    create_instant_invite=True,
    deafen_members=True,
    embed_links=True,
    external_emojis=True,
    kick_members=True,
    manage_channels=False,
    manage_emojis=False,
    manage_guild=False,
    manage_messages=True,
    manage_nicknames=True,
    manage_permissions=False,
    manage_roles=False,
    manage_webhooks=False,
    mention_everyone=False,
    move_members=True,
    mute_members=True,
    priority_speaker=True,
    read_message_history=True,
    read_messages=True,
    request_to_speak=True,
    send_messages=True,
    send_tts_messages=True,
    speak=True,
    stream=True,
    use_external_emojis=True,
    use_slash_commands=False,
    use_voice_activation=True,
    view_audit_log=False,
    view_channel=True,
    view_guild_insights=False
)
mentor_ = discord.Permissions(
    add_reactions=True,
    administrator=False,
    attach_files=True,
    ban_members=False,
    change_nickname=True,
    connect=True,
    create_instant_invite=True,
    deafen_members=False,
    embed_links=True,
    external_emojis=True,
    kick_members=False,
    manage_channels=False,
    manage_emojis=False,
    manage_guild=False,
    manage_messages=False,
    manage_nicknames=False,
    manage_permissions=False,
    manage_roles=False,
    manage_webhooks=False,
    mention_everyone=True,
    move_members=False,
    mute_members=False,
    priority_speaker=True,
    read_message_history=True,
    read_messages=True,
    request_to_speak=True,
    send_messages=True,
    send_tts_messages=True,
    speak=True,
    stream=True,
    use_external_emojis=True,
    use_slash_commands=False,
    use_voice_activation=True,
    view_audit_log=False,
    view_channel=True,
    view_guild_insights=False
)
clg_lead_ = discord.Permissions(
    add_reactions=True,
    administrator=False,
    attach_files=True,
    ban_members=False,
    change_nickname=True,
    connect=True,
    create_instant_invite=True,
    deafen_members=False,
    embed_links=True,
    external_emojis=True,
    kick_members=False,
    manage_channels=False,
    manage_emojis=False,
    manage_guild=False,
    manage_messages=False,
    manage_nicknames=False,
    manage_permissions=False,
    manage_roles=False,
    manage_webhooks=False,
    mention_everyone=True,
    move_members=False,
    mute_members=False,
    priority_speaker=True,
    read_message_history=True,
    read_messages=True,
    request_to_speak=True,
    send_messages=True,
    send_tts_messages=True,
    speak=True,
    stream=True,
    use_external_emojis=True,
    use_slash_commands=False,
    use_voice_activation=True,
    view_audit_log=False,
    view_channel=True,
    view_guild_insights=False
)
community_lead_ = discord.Permissions(
    add_reactions=True,
    administrator=False,
    attach_files=True,
    ban_members=False,
    change_nickname=True,
    connect=True,
    create_instant_invite=True,
    deafen_members=False,
    embed_links=True,
    external_emojis=True,
    kick_members=False,
    manage_channels=False,
    manage_emojis=False,
    manage_guild=False,
    manage_messages=False,
    manage_nicknames=False,
    manage_permissions=False,
    manage_roles=False,
    manage_webhooks=False,
    mention_everyone=True,
    move_members=False,
    mute_members=False,
    priority_speaker=True,
    read_message_history=True,
    read_messages=True,
    request_to_speak=True,
    send_messages=True,
    send_tts_messages=True,
    speak=True,
    stream=True,
    use_external_emojis=True,
    use_slash_commands=False,
    use_voice_activation=True,
    view_audit_log=False,
    view_channel=True,
    view_guild_insights=False
)
senior_dev_ = discord.Permissions(
    add_reactions=True,
    administrator=False,
    attach_files=True,
    ban_members=False,
    change_nickname=True,
    connect=True,
    create_instant_invite=True,
    deafen_members=False,
    embed_links=True,
    external_emojis=True,
    kick_members=False,
    manage_channels=False,
    manage_emojis=False,
    manage_guild=False,
    manage_messages=False,
    manage_nicknames=False,
    manage_permissions=False,
    manage_roles=False,
    manage_webhooks=False,
    mention_everyone=False,
    move_members=False,
    mute_members=False,
    priority_speaker=True,
    read_message_history=True,
    read_messages=True,
    request_to_speak=True,
    send_messages=True,
    send_tts_messages=True,
    speak=True,
    stream=True,
    use_external_emojis=True,
    use_slash_commands=False,
    use_voice_activation=True,
    view_audit_log=False,
    view_channel=True,
    view_guild_insights=False
)
junior_dev_ = discord.Permissions(
    add_reactions=True,
    administrator=False,
    attach_files=True,
    ban_members=False,
    change_nickname=True,
    connect=True,
    create_instant_invite=True,
    deafen_members=False,
    embed_links=True,
    external_emojis=True,
    kick_members=False,
    manage_channels=False,
    manage_emojis=False,
    manage_guild=False,
    manage_messages=False,
    manage_nicknames=False,
    manage_permissions=False,
    manage_roles=False,
    manage_webhooks=False,
    mention_everyone=False,
    move_members=False,
    mute_members=False,
    priority_speaker=False,
    read_message_history=True,
    read_messages=True,
    request_to_speak=True,
    send_messages=True,
    send_tts_messages=True,
    speak=True,
    stream=True,
    use_external_emojis=True,
    use_slash_commands=False,
    use_voice_activation=True,
    view_audit_log=False,
    view_channel=True,
    view_guild_insights=False
)
clgStd_ = discord.Permissions(
    add_reactions=True,
    administrator=False,
    attach_files=True,
    ban_members=False,
    change_nickname=True,
    connect=True,
    create_instant_invite=True,
    deafen_members=False,
    embed_links=True,
    external_emojis=True,
    kick_members=False,
    manage_channels=False,
    manage_emojis=False,
    manage_guild=False,
    manage_messages=False,
    manage_nicknames=False,
    manage_permissions=False,
    manage_roles=False,
    manage_webhooks=False,
    mention_everyone=False,
    move_members=False,
    mute_members=False,
    priority_speaker=False,
    read_message_history=True,
    read_messages=True,
    request_to_speak=True,
    send_messages=True,
    send_tts_messages=True,
    speak=True,
    stream=True,
    use_external_emojis=True,
    use_slash_commands=False,
    use_voice_activation=True,
    view_audit_log=False,
    view_channel=True,
    view_guild_insights=False
)

member_ = discord.Permissions(
    add_reactions=True,
    administrator=False,
    attach_files=True,
    ban_members=False,
    change_nickname=True,
    connect=True,
    create_instant_invite=True,
    deafen_members=False,
    embed_links=True,
    external_emojis=True,
    kick_members=False,
    manage_channels=False,
    manage_emojis=False,
    manage_guild=False,
    manage_messages=False,
    manage_nicknames=False,
    manage_permissions=False,
    manage_roles=False,
    manage_webhooks=False,
    mention_everyone=False,
    move_members=False,
    mute_members=False,
    priority_speaker=False,
    read_message_history=True,
    read_messages=True,
    request_to_speak=True,
    send_messages=True,
    send_tts_messages=False,
    speak=True,
    stream=True,
    use_external_emojis=True,
    use_slash_commands=False,
    use_voice_activation=True,
    view_audit_log=False,
    view_channel=True,
    view_guild_insights=False
)

# **********************************************************************************************
# College Categry Permission
admin_clg_ctg = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=True,
    manage_permissions=True,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=True,
    embed_links=True,
    attach_files=True,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=True,
    manage_messages=True,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
    connect=True,
    speak=True,
    stream=True,
    use_voice_activation=True,
    priority_speaker=True,
    mute_members=True,
    deafen_members=True,
    move_members=True,
    request_to_speak=True,
)
tezos_team_clg_ctg = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=True,
    manage_permissions=True,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=True,
    embed_links=True,
    attach_files=True,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=True,
    manage_messages=True,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
    connect=True,
    speak=True,
    stream=True,
    use_voice_activation=True,
    priority_speaker=True,
    mute_members=True,
    deafen_members=True,
    move_members=True,
    request_to_speak=True,
)
moderator_clg_ctg = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=True,
    manage_permissions=False,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=True,
    embed_links=True,
    attach_files=True,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=False,
    manage_messages=True,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
    connect=True,
    speak=True,
    stream=True,
    use_voice_activation=True,
    priority_speaker=True,
    mute_members=True,
    deafen_members=True,
    move_members=True,
    request_to_speak=True,
)
mentor_clg_ctg = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=True,
    manage_permissions=False,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=True,
    embed_links=True,
    attach_files=True,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=True,
    manage_messages=False,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
    connect=True,
    speak=True,
    stream=True,
    use_voice_activation=True,
    priority_speaker=True,
    mute_members=False,
    deafen_members=False,
    move_members=False,
    request_to_speak=True,
)
lead_clg_ctg = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=True,
    manage_permissions=False,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=True,
    embed_links=True,
    attach_files=True,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=True,
    manage_messages=True,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
    connect=True,
    speak=True,
    stream=True,
    use_voice_activation=True,
    priority_speaker=True,
    mute_members=True,
    deafen_members=True,
    move_members=True,
    request_to_speak=True,
)
community_lead_clg_ctg = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=True,
    manage_permissions=False,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=True,
    embed_links=True,
    attach_files=True,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=True,
    manage_messages=True,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
    connect=True,
    speak=True,
    stream=True,
    use_voice_activation=True,
    priority_speaker=True,
    mute_members=True,
    deafen_members=True,
    move_members=True,
    request_to_speak=True,
)
senior_dev_clg_ctg = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=False,
    manage_permissions=False,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=True,
    embed_links=True,
    attach_files=True,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=True,
    manage_messages=False,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
    connect=True,
    speak=True,
    stream=True,
    use_voice_activation=True,
    priority_speaker=True,
    mute_members=False,
    deafen_members=False,
    move_members=False,
    request_to_speak=True,
)
junior_dev_clg_ctg = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=False,
    manage_permissions=False,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=True,
    embed_links=True,
    attach_files=True,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=False,
    manage_messages=False,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
    connect=True,
    speak=True,
    stream=True,
    use_voice_activation=True,
    priority_speaker=False,
    mute_members=False,
    deafen_members=False,
    move_members=False,
    request_to_speak=True,
)
clgStd_clg_ctg = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=False,
    manage_permissions=False,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=True,
    embed_links=True,
    attach_files=True,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=False,
    manage_messages=False,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
    connect=True,
    speak=True,
    stream=True,
    use_voice_activation=True,
    priority_speaker=False,
    mute_members=False,
    deafen_members=False,
    move_members=False,
    request_to_speak=True,
)
member_clg_ctg = discord.PermissionOverwrite(
    view_channel=False,
    manage_channels=False,
    manage_permissions=False,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=True,
    embed_links=True,
    attach_files=True,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=False,
    manage_messages=False,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
    connect=False,
    speak=False,
    stream=False,
    use_voice_activation=False,
    priority_speaker=False,
    mute_members=False,
    deafen_members=False,
    move_members=False,
    request_to_speak=False,
)

# **********************************************************************************************

# College Announcement Permission
admin_clg_anc = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=True,
    manage_permissions=True,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=True,
    embed_links=True,
    attach_files=True,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=True,
    manage_messages=True,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
)
tezos_team_clg_anc = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=True,
    manage_permissions=True,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=True,
    embed_links=True,
    attach_files=True,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=True,
    manage_messages=True,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
)
moderator_clg_anc = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=True,
    manage_permissions=False,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=True,
    embed_links=True,
    attach_files=True,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=False,
    manage_messages=True,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
)
mentor_clg_anc = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=True,
    manage_permissions=False,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=True,
    embed_links=True,
    attach_files=True,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=True,
    manage_messages=False,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
)
lead_clg_anc = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=True,
    manage_permissions=False,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=True,
    embed_links=True,
    attach_files=True,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=True,
    manage_messages=True,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
)
community_lead_clg_anc = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=True,
    manage_permissions=False,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=True,
    embed_links=True,
    attach_files=True,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=True,
    manage_messages=True,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
)
senior_dev_clg_anc = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=False,
    manage_permissions=False,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=False,
    embed_links=False,
    attach_files=False,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=False,
    manage_messages=False,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
)
junior_dev_clg_anc = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=False,
    manage_permissions=False,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=False,
    embed_links=False,
    attach_files=False,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=False,
    manage_messages=False,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
)
clgStd_clg_anc = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=False,
    manage_permissions=False,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=False,
    embed_links=False,
    attach_files=False,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=False,
    manage_messages=False,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
)
member_clg_anc = discord.PermissionOverwrite(
    view_channel=False,
    manage_channels=False,
    manage_permissions=False,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=True,
    embed_links=True,
    attach_files=True,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=False,
    manage_messages=False,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
)

# **********************************************************************************************

# College Voice Channel Permission
admin_clg_voice = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=True,
    manage_permissions=True,
    connect=True,
    speak=True,
    stream=True,
    use_voice_activation=True,
    priority_speaker=True,
    mute_members=True,
    deafen_members=True,
    move_members=True,
)
tezos_team_clg_voice = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=True,
    manage_permissions=True,
    connect=True,
    speak=True,
    stream=True,
    use_voice_activation=True,
    priority_speaker=True,
    mute_members=True,
    deafen_members=True,
    move_members=True,
)
moderator_clg_voice = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=True,
    manage_permissions=False,
    connect=True,
    speak=True,
    stream=True,
    use_voice_activation=True,
    priority_speaker=True,
    mute_members=True,
    deafen_members=True,
    move_members=True,
)
mentor_clg_voice = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=True,
    manage_permissions=False,
    connect=True,
    speak=True,
    stream=True,
    use_voice_activation=True,
    priority_speaker=True,
    mute_members=False,
    deafen_members=False,
    move_members=False,
)
lead_clg_voice = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=True,
    manage_permissions=False,
    connect=True,
    speak=True,
    stream=True,
    use_voice_activation=True,
    priority_speaker=True,
    mute_members=True,
    deafen_members=True,
    move_members=True,
)
community_lead_clg_voice = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=True,
    manage_permissions=False,
    connect=True,
    speak=True,
    stream=True,
    use_voice_activation=True,
    priority_speaker=True,
    mute_members=True,
    deafen_members=True,
    move_members=True,
)
senior_dev_clg_voice = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=False,
    manage_permissions=False,
    connect=True,
    speak=True,
    stream=True,
    use_voice_activation=True,
    priority_speaker=True,
    mute_members=False,
    deafen_members=False,
    move_members=False,
)
junior_dev_clg_voice = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=False,
    manage_permissions=False,
    connect=True,
    speak=True,
    stream=True,
    use_voice_activation=True,
    priority_speaker=False,
    mute_members=False,
    deafen_members=False,
    move_members=False,
)
clgStd_clg_voice = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=False,
    manage_permissions=False,
    connect=True,
    speak=True,
    stream=True,
    use_voice_activation=True,
    priority_speaker=False,
    mute_members=False,
    deafen_members=False,
    move_members=False,
)
member_clg_voice = discord.PermissionOverwrite(
    view_channel=False,
    manage_channels=False,
    manage_permissions=False,
    connect=False,
    speak=False,
    stream=False,
    use_voice_activation=False,
    priority_speaker=False,
    mute_members=False,
    deafen_members=False,
    move_members=False,
)

# **********************************************************************************************

# College Discussion Permission
admin_clg_disc = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=True,
    manage_permissions=True,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=True,
    embed_links=True,
    attach_files=True,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=True,
    manage_messages=True,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
)
tezos_team_clg_disc = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=True,
    manage_permissions=True,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=True,
    embed_links=True,
    attach_files=True,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=True,
    manage_messages=True,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
)
moderator_clg_disc = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=True,
    manage_permissions=False,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=True,
    embed_links=True,
    attach_files=True,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=False,
    manage_messages=True,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
)
mentor_clg_disc = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=True,
    manage_permissions=False,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=True,
    embed_links=True,
    attach_files=True,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=True,
    manage_messages=False,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
)
lead_clg_disc = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=True,
    manage_permissions=False,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=True,
    embed_links=True,
    attach_files=True,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=True,
    manage_messages=True,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
)
community_lead_clg_disc = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=True,
    manage_permissions=False,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=True,
    embed_links=True,
    attach_files=True,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=True,
    manage_messages=True,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
)
senior_dev_clg_disc = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=False,
    manage_permissions=False,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=False,
    embed_links=False,
    attach_files=False,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=False,
    manage_messages=False,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
)
junior_dev_clg_disc = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=False,
    manage_permissions=False,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=False,
    embed_links=False,
    attach_files=False,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=False,
    manage_messages=False,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
)
clgStd_clg_disc = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=False,
    manage_permissions=False,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=False,
    embed_links=False,
    attach_files=False,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=False,
    manage_messages=False,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
)
member_clg_disc = discord.PermissionOverwrite(
    view_channel=False,
    manage_channels=False,
    manage_permissions=False,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=True,
    embed_links=True,
    attach_files=True,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=False,
    manage_messages=False,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
)

# **********************************************************************************************

# College Developer Permission
admin_clg_dev = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=True,
    manage_permissions=True,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=True,
    embed_links=True,
    attach_files=True,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=True,
    manage_messages=True,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
)
tezos_team_clg_dev = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=True,
    manage_permissions=True,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=True,
    embed_links=True,
    attach_files=True,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=True,
    manage_messages=True,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
)
moderator_clg_dev = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=True,
    manage_permissions=False,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=True,
    embed_links=True,
    attach_files=True,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=False,
    manage_messages=True,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
)
mentor_clg_dev = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=True,
    manage_permissions=False,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=True,
    embed_links=True,
    attach_files=True,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=True,
    manage_messages=False,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
)
lead_clg_dev = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=True,
    manage_permissions=False,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=True,
    embed_links=True,
    attach_files=True,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=True,
    manage_messages=True,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
)
community_lead_clg_dev = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=True,
    manage_permissions=False,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=True,
    embed_links=True,
    attach_files=True,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=True,
    manage_messages=True,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
)
senior_dev_clg_dev = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=False,
    manage_permissions=False,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=False,
    embed_links=False,
    attach_files=False,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=False,
    manage_messages=False,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
)
junior_dev_clg_dev = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=False,
    manage_permissions=False,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=False,
    embed_links=False,
    attach_files=False,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=False,
    manage_messages=False,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
)
clgStd_clg_dev = discord.PermissionOverwrite(
    view_channel=True,
    manage_channels=False,
    manage_permissions=False,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=False,
    embed_links=False,
    attach_files=False,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=False,
    manage_messages=False,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
)
member_clg_dev = discord.PermissionOverwrite(
    view_channel=False,
    manage_channels=False,
    manage_permissions=False,
    manage_webhooks=False,
    create_instant_invite=True,
    send_messages=True,
    embed_links=True,
    attach_files=True,
    add_reactions=True,
    use_external_emojis=True,
    mention_everyone=False,
    manage_messages=False,
    read_message_history=True,
    send_tts_messages=True,
    use_slash_commands=False,
)


print("********** BOT ACTIVATED **********")

# Bot Commands


@bot.command()
async def check_bot(ctx):
    await ctx.send('Bot is Alive!')

@bot.command(pass_context = True)
async def bot_help(ctx):
    embed=discord.Embed(title="Tezos Bot Commands", url="https://github.com/bhavyagoel/tezos_bot", description="This is an utility bot to server Tezos Developer Hub Discord Server.", color=0x4400ff)
    embed.set_author(name="Bhavya Goel", url="https://github.com/bhavyagoel", icon_url="https://avatars.githubusercontent.com/u/12731278?v=4")
    embed.set_thumbnail(url="https://raw.githubusercontent.com/bhavyagoel/tezos_bot/main/619.png")
    embed.add_field(name="--check_bot", value="Checks if the bot is working.", inline=False)
    embed.add_field(name="--add_college clg_name", value="Used to insert a new college to the server, can only be executed by **Admins**. Special Characters are not allowed in college name. *Eg - --add_college vit, vellore*", inline=False)
    embed.add_field(name="--set_college @user clg_name", value="Used to access college specific channels in the server. *Eg - --set_college @bhavya vit, vellore*", inline=False)
    embed.add_field(name="--set_lead @user clg_name", value="Used to update college lead in the server, can only be executed by **Admins**. Special Characters are not allowed in college name. *Eg - --set_lead @bhavya vit, vellore*", inline=False)
    embed.add_field(name="--set_db @lead @clg_role links", value="Used to update college social links in the server, can only be executed by **Admins**. *Eg - --set_db @bhavya @vit_vellore https://www.instagram.com/tdc_vellore/*", inline=False)
    embed.set_footer(text="If you face any difficulties with the commands feel free to open an issue in the GitHub Repository.")
    await ctx.send(embed=embed)

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

                await guild.create_role(name=clg, permissions=clgStd_, colour=discord.Colour.blue(), mentionable=True, reason="Add college "+clg)
                clg_std_role = discord.utils.get(guild.roles, name=clg)
                await ctx.send("Created Role "+str(clg_std_role))

                lead_name = str(clg)+" | Lead"
                await guild.create_role(name=lead_name, permissions=clg_lead_, colour=discord.Colour.dark_gold(), mentionable=True, reason="Add college lead"+clg)
                clg_lead_role = discord.utils.get(guild.roles, name=lead_name)
                await ctx.send("Created Role "+str(clg_lead_role))

                admin_role = discord.utils.find(
                    lambda m: m.name == "admin", guild.roles)
                tezos_team_role = discord.utils.find(
                    lambda m: m.name == "Tezos Team", guild.roles)
                moderator_role = discord.utils.find(
                    lambda m: m.name == "Moderator", guild.roles)
                mentor_role = discord.utils.find(
                    lambda m: m.name == "Mentor", guild.roles)
                community_lead_role = discord.utils.find(
                    lambda m: m.name == "Community Lead", guild.roles)
                senior_dev_role = discord.utils.find(
                    lambda m: m.name == "Senior Dev", guild.roles)
                junior_dev_role = discord.utils.find(
                    lambda m: m.name == "Junior Dev", guild.roles)
                member_role = discord.utils.find(
                    lambda m: m.name == "Member", guild.roles)
                clg_lead_role = discord.utils.find(
                    lambda m: m.name == lead_name, guild.roles)
                clg_std_role = discord.utils.find(
                    lambda m: m.name == clg, guild.roles)

                overwrite_ctg = {
                    admin_role: admin_clg_ctg,
                    tezos_team_role: tezos_team_clg_ctg,
                    moderator_role: moderator_clg_ctg,
                    mentor_role: mentor_clg_ctg,
                    community_lead_role: community_lead_clg_ctg,
                    senior_dev_role: senior_dev_clg_ctg,
                    junior_dev_role: junior_dev_clg_ctg,
                    member_role: member_clg_ctg,
                    clg_std_role: clgStd_clg_ctg,
                    clg_lead_role: lead_clg_ctg,
                    guild.default_role: discord.PermissionOverwrite(
                        view_channel=False,
                        connect=False,
                    )
                }
                ctg = await guild.create_category_channel(name=clg, overwrites=overwrite_ctg)
                await ctx.send("Created Category "+str(ctg))

                anc_ovwrt = {
                    admin_role: admin_clg_anc,
                    tezos_team_role: tezos_team_clg_anc,
                    moderator_role: moderator_clg_anc,
                    mentor_role: mentor_clg_anc,
                    community_lead_role: community_lead_clg_anc,
                    senior_dev_role: senior_dev_clg_anc,
                    junior_dev_role: junior_dev_clg_anc,
                    member_role: member_clg_anc,
                    clg_std_role: clgStd_clg_anc,
                    clg_lead_role: lead_clg_anc,
                    guild.default_role: discord.PermissionOverwrite(
                        view_channel=False,
                        connect=False,
                    )
                }
                chnl_anc = await guild.create_text_channel(name="Announcements", overwrites=anc_ovwrt, category=ctg)
                await ctx.send("Created Announcement Channel "+str(chnl_anc))

                dev_ovwrt = {
                    admin_role: admin_clg_dev,
                    tezos_team_role: tezos_team_clg_dev,
                    moderator_role: moderator_clg_dev,
                    mentor_role: mentor_clg_dev,
                    community_lead_role: community_lead_clg_dev,
                    senior_dev_role: senior_dev_clg_dev,
                    junior_dev_role: junior_dev_clg_dev,
                    member_role: member_clg_dev,
                    clg_std_role: clgStd_clg_dev,
                    clg_lead_role: lead_clg_dev,
                    guild.default_role: discord.PermissionOverwrite(
                        view_channel=False,
                        connect=False,
                    )
                }
                chnl_dev = await guild.create_text_channel(name="Developers", overwrites=dev_ovwrt, category=ctg)
                await ctx.send("Created Developer Channel "+str(chnl_dev))

                disc_ovwrt = {
                    admin_role: admin_clg_disc,
                    tezos_team_role: tezos_team_clg_disc,
                    moderator_role: moderator_clg_disc,
                    mentor_role: mentor_clg_disc,
                    community_lead_role: community_lead_clg_disc,
                    senior_dev_role: senior_dev_clg_disc,
                    junior_dev_role: junior_dev_clg_disc,
                    member_role: member_clg_disc,
                    clg_std_role: clgStd_clg_disc,
                    clg_lead_role: lead_clg_disc,
                    guild.default_role: discord.PermissionOverwrite(
                        view_channel=False,
                        connect=False,
                    )
                }
                chnl_disc = await guild.create_text_channel(name="Discussion", overwrites=disc_ovwrt, category=ctg)
                await ctx.send("Created Discussion Channel "+str(chnl_disc))

                voice_ovwrt = {
                    admin_role: admin_clg_voice,
                    tezos_team_role: tezos_team_clg_voice,
                    moderator_role: moderator_clg_voice,
                    mentor_role: mentor_clg_voice,
                    community_lead_role: community_lead_clg_voice,
                    senior_dev_role: senior_dev_clg_voice,
                    junior_dev_role: junior_dev_clg_voice,
                    member_role: member_clg_voice,
                    clg_std_role: clgStd_clg_voice,
                    clg_lead_role: lead_clg_voice,
                    guild.default_role: discord.PermissionOverwrite(
                        view_channel=False,
                        connect=False,
                    )
                }
                chnl_voice = await guild.create_voice_channel(name="Voice", overwrites=voice_ovwrt, category=ctg)
                await ctx.send("Created Discussion Channel "+str(chnl_voice))

                await ctx.send("**MAKE SURE TO SET ROLE POSITION.**")
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
async def set_lead(ctx, user: discord.User, *, text: str):
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


async def initialise_(channel):
    guild = channel.guild
    admin_role = discord.utils.find(lambda m: m.name == "admin", guild.roles)
    if not admin_role:
        await guild.create_role(name="admin", permissions=admin_, colour=discord.Colour.dark_red(), mentionable=True, reason="Add Admin")
    else:
        await admin_role.edit(permissions=admin_, colour=discord.Colour.dark_red(), mentionable=True, reason="Fix Admin")

    tezos_team_role = discord.utils.find(
        lambda m: m.name == "Tezos Team", guild.roles)
    if not tezos_team_role:
        await guild.create_role(name="Tezos Team", permissions=tezos_team_, colour=discord.Colour.dark_blue(), mentionable=True, reason="Add Tezos Team")
    else:
        await tezos_team_role.edit(permissions=tezos_team_, colour=discord.Colour.dark_blue(), mentionable=True, reason="Fix Tezos Team")

    moderator_role = discord.utils.find(
        lambda m: m.name == "Moderator", guild.roles)
    if not moderator_role:
        await guild.create_role(name="Moderator", permissions=moderator_, colour=discord.Colour.purple(), mentionable=True, reason="Add Moderator")
    else:
        await moderator_role.edit(permissions=moderator_, colour=discord.Colour.purple(), mentionable=True, reason="Fix Moderator")

    mentor_role = discord.utils.find(lambda m: m.name == "Mentor", guild.roles)
    if not mentor_role:
        await guild.create_role(name="Moderator", permissions=mentor_, colour=discord.Colour.purple(), mentionable=True, reason="Add Mentor")
    else:
        await mentor_role.edit(permissions=mentor_, colour=discord.Colour.purple(), mentionable=True, reason="Fix Mentor")

    community_lead_role = discord.utils.find(
        lambda m: m.name == "Community Lead", guild.roles)
    if not community_lead_role:
        await guild.create_role(name="Community Lead", permissions=community_lead_, colour=discord.Colour.dark_orange(), mentionable=True, reason="Add Community Lead")
    else:
        await community_lead_role.edit(permissions=community_lead_, colour=discord.Colour.dark_orange(), mentionable=True, reason="Fix Community Lead")

    senior_dev_role = discord.utils.find(
        lambda m: m.name == "Senior Dev", guild.roles)
    if not senior_dev_role:
        await guild.create_role(name="Senior Dev", permissions=senior_dev_, colour=discord.Colour.dark_teal(), mentionable=True, reason="Add Senior Dev")
    else:
        await senior_dev_role.edit(permissions=senior_dev_, colour=discord.Colour.dark_teal(), mentionable=True, reason="Fix Senior Dev")

    junior_dev_role = discord.utils.find(
        lambda m: m.name == "Junior Dev", guild.roles)
    if not junior_dev_role:
        await guild.create_role(name="Junior Dev", permissions=junior_dev_, colour=discord.Colour.teal(), mentionable=True, reason="Add Junior Dev")
    else:
        await junior_dev_role.edit(permissions=junior_dev_, colour=discord.Colour.teal(), mentionable=True, reason="Fix Junior Dev")

    member_role = discord.utils.find(lambda m: m.name == "Member", guild.roles)
    if not member_role:
        await guild.create_role(name="Member", permissions=member_, colour=discord.Colour.blurple(), mentionable=True, reason="Add Member")
    else:
        await member_role.edit(permissions=member_, colour=discord.Colour.blurple(), mentionable=True, reason="Fix Member")


MY_CHANNEL_ID = 859902674596921364


# Twitter
async def twitter_(channel):
    try:
        while True:
            social_db = db.social_.find()
            visited_ = db["visited_"]
            brk = await bot.fetch_channel(MY_CHANNEL_ID)
            
            for _social in list(social_db):
                clg_name = _social["college_name"]
                social_twitter = _social["twitter_"]
                if social_twitter != "":
                    twitter_id = str(social_twitter).replace(
                        "https://twitter.com", "").replace("/", "")
                    tweets = tweet_api.user_timeline(
                        screen_name=twitter_id,
                        count=1,
                        include_rts=False,
                        tweet_mode='extended'
                    )
                    if tweets:
                        visited_db = db.visited_.find()
                        visit_link = [_link["link"]
                                        for _link in visited_db]
                        brk = await bot.fetch_channel(MY_CHANNEL_ID)
                        for tweet in tweets:
                            alpha = tweet._json
                            tweet_url = "https://twitter.com/twitter/statuses/" + alpha["id_str"]
                            try:
                                if(str(tweet_url) in visit_link):
                                    brk = await bot.fetch_channel(MY_CHANNEL_ID)

                                else:
                                    
                                    id_ = visited_.insert_one(
                                        {
                                            "link": tweet_url
                                        }
                                    )
                                    
                                    em = discord.Embed(color=15467852,
                                                        title="Tweet by @"+twitter_id+"",
                                                        url=tweet_url,
                                                        description=alpha["full_text"],
                                                        image=alpha["entities"]["media"][0]["media_url_https"],
                                                        thumbnail=alpha["entities"]["media"][0]["media_url_https"],
                                                    )
                                    await channel.send(embed=em)

                            except:
                                if(tweet_url) in visit_link:
                                    brk = await bot.fetch_channel(MY_CHANNEL_ID)

                                else:
                                    id_ = visited_.insert_one(
                                        {
                                            "link": tweet_url
                                        }
                                    )
                                    em = discord.Embed(color=15467852,
                                                    title="Tweet by @"+twitter_id+"",
                                                    url=tweet_url,
                                                    description=alpha["full_text"],
                                                    )

                                    await channel.send(embed=em)
                                
            await asyncio.sleep(900)  # Sleep 15 Minutes for each Update
    except Exception as e:
        await channel.send("Inform **Admins** that Bot has crashed. **Tweepy Failed**")
# Medium

# YouTube

# LinkedIN

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


async def instagram_(channel):
    try:
        while True:
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
                        brk = await bot.fetch_channel(MY_CHANNEL_ID)
                        if social_insta != "":
                            insta_id = str(social_insta).replace(
                                "https://www.instagram.com", "").replace("/", "")
                            html = get_instagram_html(insta_id)
                            visited_db = db.visited_.find()
                            visit_link = [_link["link"]
                                          for _link in visited_db]
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
                                                   image=get_last_photo_url(
                                                       html),
                                                   thumbnail=get_last_thumb_url(
                                                       html),
                                                   )

                                await channel.send(embed=em)
            await asyncio.sleep(600)  # Sleep 10 Minutes for each Update
    except Exception as e:
        await channel.send("Inform **Admins** that Bot has crashed. **Insta Scrapper Failed**")


@bot.event
async def on_ready():
    global channel
    global guild
    guild = await bot.fetch_guild(859794440625192970)
    channel = bot.get_channel(MY_CHANNEL_ID)
    if not channel:
        channel = bot.get_channel(MY_CHANNEL_ID)  # access to channel
        brk = await bot.fetch_channel(MY_CHANNEL_ID)
    if not channel:
        print("[on_ready] can't access channel:", MY_CHANNEL_ID)
        brk = await bot.fetch_channel(MY_CHANNEL_ID)
    else:
        bot.loop.create_task(initialise_(channel))
        bot.loop.create_task(twitter_(channel))
        bot.loop.create_task(instagram_(channel))
        
if __name__ == "__main__":
    bot_key = os.environ.get("DISCORD")
    bot.run(bot_key)
