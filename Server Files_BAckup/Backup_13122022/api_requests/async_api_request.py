import aiohttp
import asyncio
import time
import api_config as apic
import api_methods as apim
import logging
import urllib.parse
import datetime
import pytz
import sys
sys.path.insert(0, '/home/apliatsios/dlyberis/Neo4j')
import Neo4j_transactions as neo4j

start_time = time.time()

async def get_data(session, url, headers, name, api_name, lat, lon):
    async with session.get(url, headers=headers) as resp:
        logging.info("GET request to {}, URL: {}.".format(api_name,url))
        json_data = await resp.json()
        ts = datetime.datetime.now(pytz.timezone('Europe/Athens')).strftime("%Y-%m-%dT%H:%M:%S")
        logging.info("RESPONSE: {}, STATUS: {}, URL: {}.".format(urllib.parse.urlsplit(url).hostname,resp.status,url))
        data = await apim.parse_api(json_data,name,api_name,lat,lon,ts)
        logging.info("Parsing data from {}, for  URL: {} is completed.".format(api_name,url))
        return data

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        # for val in apic.Loc.values():
        #     [url, headers] = apim.create_req_url(val['lat'], val['lon'], val['api_name'])
        #     tasks.append(asyncio.ensure_future(get_data(session, url, headers, val['api_name'], val['lat'], val['lon'])))
        for val in apic.Loc.items():
            [url, headers] = apim.create_req_url(val[1]['lat'], val[1]['lon'], val[1]['api_name'])
            tasks.append(asyncio.ensure_future(get_data(session, url, headers, val[0], val[1]['api_name'], val[1]['lat'], val[1]['lon'])))
        original_data = await asyncio.gather(*tasks)
        
    for data in original_data:
        logging.info("Ready to write API Request Data")
        neo4j.write_api_data(data)
        logging.info("API Request Data was written")

if __name__ == '__main__':

    logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
    rootLogger = logging.getLogger()
    fileHandler = logging.FileHandler('apis_req.log')
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
    rootLogger.setLevel(logging.INFO)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print("--- %s seconds ---" % (time.time() - start_time))
