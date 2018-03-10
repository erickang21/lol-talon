# Talon 

This is an API wrapper, written in Python. It is for the Riot API, which provides information and statistics from League of Legends.

This wrapper is written in `async` and is compatible with [discord.py](https://github.com/Rapptz/discord.py)


*Let's get to work, bois!*

**To set up:**
Run `pip install git+https://github.com/bananaboy21/lol-talon` on your Command Prompt.
Note: The PC where you run this must be the same PC on which you are hosting your app that uses the Talon wrapper.

**To update:**
Updates will be announced in my [Discord server](https://discord.gg/wvkVknA). 
To update the wrapper, run `pip install -U git+https://github.com/bananaboy21/lol-talon` on the same PC.

**Sample Code**
```python
import talon
client = talon.Client(token='Your token BLAH BLAH BLAH')
summoner = await client.get_summoner(region=None, query='banana boy')
print(summoner.summonerLevel)
```

This will output my Summoner Level given the region as `None` (which defaults it to NA1), and the query, or player name, as "banana boy". My level is `28` (I suck.)


**Requirements**
-Python 3.5 or higher.
-Aiohttp.
-Your brain.


**Contributing**
Wanna help out? Or am I a nub? Just submit a pull request anytime, and *it'll probably get accepted 'cuz I'm that bad.*


**Contact MEEEE**
-My Discord: dat banana boi#1982
-Join my coding server: https://discord.gg/wvkVknA
-I'm lonely so typically I should be online. Unless I'm not.


**License**
-Released under MIT license. The fairest of them all.


