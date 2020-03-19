"""
Copyright (c) 2020, creatable

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


import aiohttp
import asyncio
import discord
import html
from discord.ext import commands

bot = commands.Bot(command_prefix='b!', description="""A utility bot for Reddit verification.
Copyright (c) 2020, creatable (https://creatable.cafe)""")

@bot.event
async def on_ready():
    print("""
 _          _      _      
| |        (_)    | |     
| |__  _ __ _  ___| | __  
| '_ \| '__| |/ __| |/ /  
| |_) | |  | | (__|   < _ 
|_.__/|_|  |_|\___|_|\_(_)

by creatable""")

@bot.command()
async def verify(ctx, *args):
    if len(args) != 0:
        verifiedrole = discord.utils.get(ctx.guild.roles, name="Verified")
        verifystring = f"""-----BEGIN BRICK VERIFICATION STRING-----
{ctx.author.id}
-----END BRICK VERIFICATION STRING-----"""
        if verifiedrole in ctx.author.roles:
            await ctx.send("ERROR: You're already verified!")
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://www.reddit.com/user/{args[0]}/about.json', allow_redirects = False) as response:
                    if response.status != 404:
                        desc = html.unescape((await response.json())["data"]["subreddit"]["public_description"])
                        if (verifystring) in desc:
                            await ctx.author.add_roles(verifiedrole)
                            await ctx.author.edit(nick = f"u/{args[0]}")
                            await ctx.send("""Successfully verified!
You can now remove the verification string from your profile at <https://new.reddit.com/settings/profile> if you want.""")
                        else:
                            await ctx.send(f"""Go to <https://new.reddit.com/settings/profile> and add the following block to your "About" section: 
```{verifystring}```
Then do `b!verify {discord.utils.escape_mentions(args[0])}` again to verify your Reddit account.""")

                    else:
                        await ctx.send("ERROR: I can't find that user.")
    else:
        ctx.send("ERROR: No arguments were provided.")


bot.run('')