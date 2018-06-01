import aiohttp
from box import Box
import urllib.parse


class LolError(Exception):
    '''
    Raised when the Riot API returns a status code other than 200 (success).
    This error does nothing by itself, you will have to check for the exception and handle it yourself.
    '''
    pass



class Client:
    '''
    This class is the main client of the Talon wrapper.
    It represents the object that is used to connect to the client.
    Through this object, you can request any endpoints that are listed below.
    '''

    def __init__(self, token, session=None):
        '''
        Constructs the Client used for requests.

        ---Arguments---
        token (Required, str): The API key that you have from the Riot API website. An invalid/blank key will return 403 (Forbidden).
        session (Optional, ClientSession): This can be a ClientSession for the client to use. Defaults to an aiohttp.ClientSession(),
        '''
        self.token = token
        self.base_url = ".api.riotgames.com/lol/"
        self.session = aiohttp.ClientSession() if session is None else session
        



    async def _get(self, endpoint, query, region='na1'):
        query = urllib.parse.quote(str(query))
        async with self.session.get("https://{}{}{}{}api_key={}".format(region, self.base_url, endpoint, query, self.token), params=self.query_string) as resp:
            if resp.status != 200:
                raise LolError("Riot API returned a non-200 code. Error code: {}".format(resp.status))
            resp = await resp.json()
            try:
                return Box(resp)
            except:
                raise LolError("Error occurred while decoding data.")
            # In an older version, I let the Box return the normal JSON response
            # if Box'ing it failed. This time, it will only raise an error. 


    '''
    Champions

    These requests involve the requests from the endpoint: CHAMPION-V3
    To find specifics about the data returned from the requests, please check the Riot API documentation at:
    https://developer.riotgames.com
    '''

    async def get_all_champions(self, region='na1'):
        '''
        Gets information for ALL champion information.

        ---Arguments---
        region (Optional, str): The region to execute this request on.
        All possible regions for this argument include: ru, kr, br1, oc1, jp1, na1, eun1, euw1, tr1, la1, la2.
        Defaults to North America (na1) if region is None.
        '''
        return await self._get(endpoint="static-data/v3/champions/", query="{}".format("?locale=en_US&champData=all&tags=all&"), region=region)

    async def get_champion(self, query, region='na1'):
        '''
        Request that gets LoL champion information for a specific champion, by the Champion ID.

        ---Arguments---
        region (Optional, str): The region to execute this request on. 
        All possible regions for this argument include: ru, kr, br1, oc1, jp1, na1, eun1, euw1, tr1, la1, la2.
        Defaults to North America (na1) if region is None.
        
        query (str): The ID of the champion that is being requested. Mandatory for this request.
        '''
        return await self._get(endpoint="static-data/v3/champions/", query="{}{}".format(query, "?locale=en_US&champData=all&tags=all&"), region=region)


    async def get_item(self, query, region='na1'):
        '''
        Request that gets LoL item information for a specific item, by the item's ID.

        ---Arguments---
        region (Optional, str): The region to execute this request on.
        All possible regions for this argument include: ru, kr, br1, oc1, jp1, na1, eun1, euw1, tr1, la1, la2.
        Defaults to North America (na1) if region is None.

        query (str): The ID of the item that is being requested. Mandatory for this request.
        '''
        return await self._get(endpoint="/lol/static-data/v3/items/", query="{}{}".format(query, "?"))

    '''
    Champion Masteries

    These requests involve the requests from the endpoint: CHAMPION-MASTERY-V3
    To find specifics about the data returned from the requests, please check the Riot API documentation at:
    https://developer.riotgames.com
    '''


    async def get_champion_mastery(self, query, region=None):
        '''
        Request that gets LoL champion mastery information for a summoner.

        Note that this makes 2 requests: 
        1 to SUMMONER-V3 to retrieve the Summoner ID associated with the username.
        1 to CHAMPION-MASTERY-V3 to retrieve the summoner's champion masteries.

        ---Arguments---
        region (Optional, str): The region to execute this request on. 
        All possible regions for this argument include: ru, kr, br1, oc1, jp1, na1, eun1, euw1, tr1, la1, la2.
        Defaults to North America (na1) if region is None.
        
        query (str): The summoner's username from which to get the champion masteries from. Mandatory for this request.
        '''
        if region is None:
            region = 'na1'
        lol = await self._get(endpoint="summoner/v3/summoners/by-name/", query="{}{}".format(query, "?"), region=region)
        summonerid = lol.id
        return await self._get(endpoint="champion-mastery/v3/champion-masteries/by-summoner/", query="{}{}".format(str(summonerid), "?"), region=region)
        #Returning champion masteries may cause some errors with Box. Luckily I handled it. 
        #Instead of lol.thing, you might want to try lol['thing'], in case Box broke somehow.



    '''
    Summoner

    These requests involve the requests from the endpoint: SUMMONER-V3
    To find specifics about the data returned from the requests, please check the Riot API documentation at:
    https://developer.riotgames.com
    '''


    async def get_summoner(self, query, region=None):
        '''
        Request that gets an LoL summoner's profile, by their name.

        ---Arguments---
        region (Optional, str): The region to execute this request on. 
        All possible regions for this argument include: ru, kr, br1, oc1, jp1, na1, eun1, euw1, tr1, la1, la2.
        Defaults to North America (na1) if region is None.

        query (str): The Summoner's username. Mandatory for this request.
        '''
        if region is None:
            region = 'na1'
        return await self._get(endpoint="summoner/v3/summoners/by-name/", query="{}{}".format(query, "?"), region=region)


    '''
    Leagues

    These requests involve the requests from the endpoint: LEAGUE-V3
    To find specifics about the data returned from the requests, please check the Riot API documentation at:
    https://developer.riotgames.com
    '''

    async def get_summoner_league(self, query, region=None):
        '''
        Request that gets an LoL summoner's League information, by their name.
        
        region (Optional, str): The region to execute this request on. 
        All possible regions for this argument include: ru, kr, br1, oc1, jp1, na1, eun1, euw1, tr1, la1, la2.
        Defaults to North America (na1) if region is None.

        query (str): The Summoner's username. Mandatory for this request.
        '''
        if region is None:
            region = 'na1'
        lol = await self._get(endpoint="summoner/v3/summoners/by-name/", query=query, region=region)
        summonerid = lol.id
        return await self._get(endpoint="/lol/league/v3/positions/by-summoner/", query="{}{}".format(summonerid, "?"), region=region)










