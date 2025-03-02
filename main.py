import discord
import requests
import json
import os
import subprocess
import re

from random import randrange

ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents = intents)

calHeader = """
    include "cores/select.cal"
    include "std/io.cal"
    include "std/array.cal"
    include "std/nullterm.cal"
    include "std/ops.cal"
    include "std/random.cal"
"""

languages = [
    "C", "C++", "D", "V", "Fortran", "Verilog", "Prolog", "Forth", "Go", "Rust", "Zig",
    "Porth", "Callisto", "YSL", "YSL-R", "YSL-C", "Bash", "Batch", "Haskell", "OCaml",
    "Python", "JavaScript", "Ruby", "HTML", "CSS", "Markdown", "PowerShell", "Brainfuck",
    "Malbolge", "Jupyter Notebook", "Vue", "Vala", "uxntal", "Concata", "APL", "WPL",
    "Modal", "Carbon", "Nim"
]
libraries = [
    "ncurses", "SDL2", "asyncio", "vibe.d", "discord.js", "discord.py", "Unity",
    "Unreal Engine", "Rails", "stb", "Godot", "YSL-M"
]
people = [
    "Bill Gates", "Linus Torvalds", "Brendan Eich", "Richard Stallman",
    "Bjarne Stroustrup", "Ada Lovelace", "Alan Turing", "John von Neumann", "Elon Musk"
]
companies = ["Microsoft", "Google", "Meta", "Shopify", "YouTube", "Discord", "NASA"]
issues = ["memory safety", "race condition", "goto statement", "segmentation fault"]
takes = [
    "Did you know that $L is the worst programming language in the world?",
    "Did you know that $L is the best programming language in the world?",
    "Why are schools not teaching $A? We're setting our kids up to fail.",
    "$L users couldn't even print Hello World in $L.",
    "$A is toxic for humanity. This is not an opinion, it's an absolute truth.",
    "$A users should be sent to prison for life.",
    "$A users don't understand programming.",
    "I have been coding in $L for $N years and I still do not understand why people use $A.",
    "$A fans are smarter than the average programmers.",
    "I'm sick of these pseudo-intellectual $A users, sitting in their ivory towers, looking down on the rest of us.",
    "The $A community is toxic.",
    "The fact that we're still using $A in 2024 is a problem.",
    "Average $A user vs average $A enjoyer.",
    "Every tech stack should include $A.",
    "People may disagree with the things I say, but I'd like to remind the haters that I have worked on a one-billion line $L codebase.",
    "$A is a $I disaster waiting to happen.",
    "I have been working with $A for over $N years, AMA.",
    "Well written $L is what heaven looks like.",
    "$P was the first true computer scientist.",
    "$P, inventor of $A is who we should all aspire to be like.",
    "$A was pioneered by $P",
    "Coding in $L is mental torture.",
    "I have a PhD in Computer Science and I'm still not sure how $A works.",
    "Honestly, $A fans are insufferable",
    "Everyone should learn $L as their first language.",
    "$L is not a programming language. Change my mind.",
    "AITA from banning my GF from using $L?",
    "I just started a new job at $C. My boss, $P just told me to refactor 58235 lines of $L. Kill me.",
    "$P debunked $A a long time ago.",
    "$A fans are quickly taking over the tech world and that's good.",
    "I'm genuinely surprised to hear that there are programmers who use $A",
    "I'm genuinely surprised to hear that there are programmers who don't use $A",
    "IMO, $P needs to start looking at $A.",
    "Oh, your code is written in $L? Sorry, I don't speak stupid.",
    "I think I'm addicted to working with $A. Does anyone else feel the same?",
    "$A is just $A mixed with $A.",
    "I had an interviewer laugh in my face when I said I use $A.",
    "I have an irrational hatred for $A.",
    "I just purchased the domain name $A.net. I'm going to make a fortune.",
    "$A fans don't deserve to be in tech.",
    "If Jesus was alive today, he would be using $A.",
    "I love $P so much!",
    "We should really stop listening to $P. They told us to use $A, after all.",
    "I'm not an $A fan, but I'm a $A fan.",
    "Coding in $L is like walking over hot coals.",
    "After just a few hours, I've optimised my $L codebase $Nx. Writing up a blog post as we speak.",
    "Where are all the $A jobs? Are people really looking for $A?",
    "I just donated $$2348 to $P's Patreon. They deserve it.",
    "Did you know $L is one of the oldest programming languages in the world?",
    "$C uses $A so it must be good.",
    "$A doesn't need $A, it's perfect already.",
    "Gen Z kids don't understand $A.",
    "The perfect programming language is $L mixed with $L.",
    "One of my greatest achievements is becoming a moderator of r/$A.",
    "I'm looking for a new job. I'm not sure if I should apply to $C. I've heard they're $A haters.",
    "Started learning $L yesterday. Already built an AI that can solve $I. Should I drop out of school?"
]

chatServers = []
chatChannels = []

def GetTakeWord(takeType):
    array = []
    if takeType == "A":
        randomType = randrange(0, 2)
        if randomType == 0:
            array = languages
        elif randomType == 1:
            array = libraries
    elif takeType == "P":
        array = people
    elif takeType == "L":
        array = languages
    elif takeType == "C":
        array = companies
    elif takeType == "N":
        return str(randrange(5, 26))
    elif takeType == "I":
        array = issues
    elif takeType == "$":
        return "$"
    else:
        return f"(UNIMPLEMENTED {takeType})"

    return array[randrange(0, len(array))]

def MakeHotTake():
    takeSrc = takes[randrange(0, len(takes))]
    takeRes = ""
    i       = 0

    while i < len(takeSrc):
        if takeSrc[i] == '$':
            i       += 1
            takeRes += GetTakeWord(takeSrc[i])
        else:
            takeRes += takeSrc[i]
        i += 1

    return takeRes

async def subreddit(message, sr):
    sent = False

    while not sent:
        subreddit = requests.get(f"https://www.reddit.com/r/{sr}.json?limit=100")
        res = subreddit.json()
        which = randrange(0, len(res["data"]["children"]))
        print(len(res["data"]["children"]))

        print(res["data"]["children"][which]["data"]["url"])
        if not "i.redd.it" in res["data"]["children"][which]["data"]["url"]:
            continue

        await message.reply(res["data"]["children"][which]["data"]["url"])
        sent = True

async def SendMessage(contents, avoid):
    for channel in chatChannels:
        if channel == avoid:
            continue
        try:
            await client.get_channel(channel).send(contents)
        except:
            pass

@client.event
async def on_ready():
    print("Bot online")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.id in chatChannels:
        attachments = "\n"
        for attachment in message.attachments:
            attachments += attachment.url + "\n"
        await SendMessage(f"**{message.author.name}**: {message.content.replace('@', '<at>')} {attachments}", message.channel.id)

    #if message.author.id == 584056779793760266:
    #    await message.add_reaction("💉")

    if message.content.startswith("cal!help"):
        await message.reply("""```
Callisto help
=============
Note: remove any backslashes in command syntax

- cal!run \\`\\`\\`
    (code here)
\\`\\`\\`
- This runs the given callisto code (asm blocks are not allowed)

- cal!ping
- This replies with "pong"

- cal!version
- Replies with the compiler version

- cal!take
- Replies with a hot take

- cal!manul
- Sends an image from r/pallascats

- cal!orange
- Sends an image from r/oneorangebraincell

- cal!cat
- Sends a random cat image
        ```""")

    if message.content.startswith("cal!chat"):
        if message.guild.id in chatServers:
            await message.reply("Server is already in chat")
            return

        chatChannels.append(message.channel.id)
        chatServers.append(message.guild.id)
        if isinstance(message.channel, discord.channel.DMChannel):
            await SendMessage(f"**{message.author.name}** joined the chat", 69)
        else:
            await SendMessage(f"**{message.guild.name}:{message.channel.name}** joined the chat", 69)

    if message.content.startswith("cal!leave"):
        if isinstance(message.channel, discord.channel.DMChannel):
            await SendMessage(f"**{message.author.name}** left the chat", 69)
        else:
            await SendMessage(f"**{message.guild.name}:{message.channel.name}** left the chat", 69)
        chatChannels.remove(message.channel.id)

    if message.content.startswith("cal!update_docs") and message.author.id == 739032871087374408:
        msg = await message.reply("Updating...")
        result = subprocess.run(
            "cd ~/docs/docs && git pull && git submodule update --remote --init --recursive && make && cd ../callisto && ./build.sh",
            shell = True, capture_output = True, text = True
        )

        if result.returncode != 0:
            await msg.edit(content = "Fail: " + result.stdout + result.stderr)
        else:
            await msg.edit(content = "Docs updated")

    if message.content.startswith("cal!update_std") and message.author.id == 739032871087374408:
        msg = await message.reply("Updating...")
        result = subprocess.run(
            "cd std && git pull",
            shell = True, capture_output = True, text = True
        )

        if result.returncode != 0:
            await msg.edit(content = "Fail: " + result.stdout + result.stderr)
        else:
            await msg.edit(content = "Std updated")

    if message.content.startswith("cal!update_compiler")  and message.author.id == 739032871087374408:
        msg = await message.reply("Updating...")
        result = subprocess.run(
            "cd ~/app/compiler && git pull && dub build && cp cac ~/calbot/cac",
            shell = True, capture_output = True, text = True
        )

        if result.returncode != 0:
            await msg.edit(content = "Fail: " + result.stdout + result.stderr)
            print(result.stdout)
            print(result.stderr)
        else:
            await msg.edit(content = "Compiler updated")

    if message.content.startswith("cal!goodbye") and message.author.id == 739032871087374408:
        await message.reply("goodbye")
        exit()

    if message.content.startswith("cal!ping"):
        await message.reply("pong")

    if message.content.startswith("cal!manul"):
        await subreddit(message, "pallascats")

    if message.content.startswith("cal!orange"):
        await subreddit(message, "oneorangebraincell")

    if message.content.startswith("cal!cat"):
        req = requests.get("https://api.thecatapi.com/v1/images/search")
        res = json.loads(req.text)
        await message.reply(res[0]["url"])

    if message.content.startswith("cal!version"):
        await message.reply(
            subprocess.run(
                "./cac --version", shell = True, capture_output = True, text = True
            ).stdout
        )

    if message.content.startswith("cal!run ```") or message.content.startswith("cal!run\n```"):
        code = message.content[len("cal!run ```") : -3]
        runCount = randrange(0, 65536)

        with open(f"temp{runCount}.cal", "w") as file:
            file.write(calHeader + code + "\n")

        if ("asm" in code) or ("call" in code) or ("include" in code):
            await message.reply("Asm blocks are not allowed")
            return

        result = subprocess.run(
            f"./cac temp{runCount}.cal -i std -o temp{runCount} -dv File", shell = True, capture_output = True, text = True
        )

        if result.returncode != 0:
            await message.reply(
                "Returned " + str(result.returncode) + "\nOutput:\n" + result.stdout
                + ansi_escape.sub("", result.stderr)
            )
            return

        try:
            result = subprocess.run(
                f"./temp{runCount}", shell = True, capture_output = True, text = True,
                timeout = 5
            )
        except subprocess.TimeoutExpired:
            await message.reply("Program timeouted")
            return
        except UnicodeDecodeError:
            await message.reply("Your program printed invalid unicode")
            return

        await message.reply(
            "```\n" + result.stdout.replace("\r\n", "\n") + result.stderr + "\n```"
        )

        os.system("rm temp*")

    if message.content.startswith("cal!take"):
        await message.reply(MakeHotTake())

    if message.content.startswith("cal!mtake"):
        res = ""
        for i in range(0, 5):
            res += MakeHotTake() + "\n\n"
        await message.reply(res)

client.run("TOKEN")
