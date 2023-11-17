import datetime
import os
import async_api_request as apireq
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import sys
sys.path.insert(0, r'/home/apliatsios/dlyberis/Neo4j/Neo4j')
import Neo4j_transactions as neo4j

if __name__ == '__main__':

    logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
    rootLogger = logging.getLogger('apscheduler')
    fileHandler = logging.FileHandler('/home/apliatsios/dlyberis/scheduler.log')
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
    rootLogger.setLevel(logging.DEBUG)

    

    scheduler = AsyncIOScheduler()
    scheduler.add_job(apireq.main, 'interval', minutes=15)
    scheduler.start()

    try:
        neo4j.neo4j_init(logging)
        asyncio.get_event_loop().run_forever()

    except (KeyboardInterrupt, SystemExit) as err:
        logging.exception(err)
        scheduler.shutdown()
        neo4j.neo4j_destroy()
    finally:
        neo4j.neo4j_destroy()
