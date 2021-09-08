import os
import sys
import time
import json
import random
import bcrypt
import sqlite3
import discord
import requests
from api import userdata
from api import configfile
from urllib.parse import quote
from discord.ext import commands
from pydactyl import PterodactylClient
from requests.exceptions import HTTPError
from flask import Flask, session, render_template, redirect, url_for, request
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized


app = Flask(__name__)

app.secret_key = configfile.discordsettings["secret_key"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"
app.config["DISCORD_CLIENT_ID"] = configfile.discordsettings["application_id"]
app.config["DISCORD_CLIENT_SECRET"] = configfile.discordsettings["secret_key"]
app.config["DISCORD_REDIRECT_URI"] = configfile.discordsettings["redirect_uri"]
pteroapplication = PterodactylClient(configfile.pteroURL, configfile.pteroAppKey)

discord = DiscordOAuth2Session(app)


@app.route('/callback/')
def callback():
    discord.callback()
    return redirect(url_for('index'))


@app.route('/login/')
def login():
    return discord.create_session()


@app.route('/')
def index():
    if discord.authorized:

        user = discord.fetch_user()

        try:
            userdata.checkIfUserExists(user.email)
            return f"you have an account! Here is your user data: {userdata.checkIfUserExists(user.email)}"
            
        except IndexError:
            return redirect(url_for('createuser'))
        

    elif not discord.authorized:
        return "u havent logged in <a href=\"/login/\">click here to login</a>"


@app.route('/logout/')
def logout():

    discord.revoke()

    return redirect(url_for('index'))


@app.route('/earn')
def earn():
    """Earn using Arc"""
    return render_template('afk.html')


@app.route('/create/')
@requires_authorization
def createuser():

    user = discord.fetch_user()

    try:
        userdata.checkIfUserExists(user.email)
        return redirect(url_for('index'))

    except IndexError:
        userdata.create_user(user.username, user.email, user.id)
        return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
