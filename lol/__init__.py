import aiohttp


class LolError(Exception):
	'''
	Raised when the Riot API returns a status code other than 200 (success).
	This error does nothing by itself, you will have to check for the exception and handle it yourself.
	'''
	pass


class Client:
	def __init__(self, token, session=None):
        self.token = token
        self.query_string = {"api_key": token}
        self.base_url = ".api.riotgames.com/lol/"
        self.session = aiohttp.ClientSession() if session is None else session


    async def _get(self, endpoint, query, region):
    	async with self.session.get(f"https://{region}{self.base_url}{endpoint}{query}", params=self.query_string) as resp:
    		if resp.status != 200:
    			raise LolError(f"Riot API returned a non-200 code. Details: {resp.status}")
    		resp = await resp.json()
    		return resp['data']


    async def get_summoner(self, region=None, query):
    	'''
    	Request that gets an LoL summoner's profile, by their name.

    	---Arguments---
    	region (Optional, str): The region to execute this request on. 
    	All possible regions for this argument include: ru, kr, br1, oc1, jp1, na1, eun1, euw1, tr1, la1, la2.
    	Defaults to North America if region is None.

    	query (str): The Summoner's username. Mandatory for this request.
    	'''
    	if region is None:
    		region = 'na1'
    	return await self._get(f"summoner/v3/summoners/by-name/{query}", region)


    async def get_champion(self, region=None, query):
    	'''Request that gets LoL champion information for a specific champion, by the Champion ID.
    	---Arguments---
    	region (Optional, str): The region to execute this request on. 
    	All possible regions for this argument include: ru, kr, br1, oc1, jp1, na1, eun1, euw1, tr1, la1, la2.
    	Defaults to North America if region is None.
		
		query (str): The ID of the champion that is being requested. Mandatory for this request.
    	'''
    	if region is None:
    		region = 'na1'
    	return await self._get(f"/lol/static-data/v3/champions/{query}", region)






