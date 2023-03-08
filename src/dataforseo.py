import os
import uuid
import requests
from dotenv import load_dotenv
import urllib.parse
from typing import Union, Optional
import base64
import json
import time
from db_wrapper import MongoManager
from datetime import datetime
from loguru import logger
import sys

#urllib.parse.quote(query)

load_dotenv()

mondb = MongoManager(db_name="Dataforseo")

SCRAPER_API_KEY = os.getenv("SCRAPER_API_KEY")
DATAFORSEO_API_KEY  = os.getenv("DATAFORSEO_API_KEY")
SCRAPEDO_API_KEY = os.getenv("SCRAPEDO_API_KEY")

# https://www.scraperapi.com/
SERVICE_SCRAPER_ASYNC = "http://async.scraperapi.com/jobs"
ENDPOINT_SCRAPER = "http://api.scraperapi.com?"
PROXY_SCRAPER = "http://scraperapi:APIKEY@proxy-server.scraperapi.com:8001"
SERVICE_SCRAPER_STRUCTERED_DATA = "https://api.scraperapi.com/structured/"

# https://scrape.do/
SERVICE_SCRAPEDO = "http://api.scrape.do?" + "token=" + SCRAPEDO_API_KEY + "&url="
COMMAND_PROXY_SCRAPEDO = "curl --proxy http://{0}@proxy.scrape.do:8080 --insecure {1}"
#cmd = COMMAND_PROXY_SCRAPEDO.format(SCRAPEDO_API_KEY,target_url)

PRODUCTS = ["https://www.trendyol.com/alfais/4939-usb-3-0-to-ethernet-cevirici-donusturucu-adaptor-gigabit-destekli-p-133387267?boutiqueId=61&merchantId=327407",
            "https://www.trendyol.com/alfais/4939-usb-3-0-to-ethernet-cevirici-donusturucu-adaptor-gigabit-destekli-p-133387267/yorumlar?boutiqueId=61&merchantId=327407"]


def create_fname(prefix):
    random_file_name = ''.join([prefix, "-", str(uuid.uuid4().hex[:6])])
    return random_file_name

def fetch_from_scrapedo(target_url: Optional[list | str], proxy_on: bool=False):
    if proxy_on:
        pass
    else:
        if isinstance(target_url, list):
            for uri in target_url:
                res = requests.get(url=SERVICE_SCRAPEDO + urllib.parse.quote(uri))
                print(res.status_code)
                print(res.content)
        elif isinstance(target_url, str):
            res = requests.get(url=SERVICE_SCRAPEDO+urllib.parse.quote(target_url))
            with open(create_fname("response"), "w", encoding="UTF-8") as f:
                f.write(res.content.decode("utf-8"))
            print(res.status_code)
            try:
                print(res.json())  # hata veriyor.

            except Exception as e:
                print(e)
        else:
            print("wrong data type!")


class DataForSeo:
    DATAFORSEO_API_KEY  = os.getenv("DATAFORSEO_API_KEY")
    def __init__(self):
        self.username = "mehmetzahidisik@gmail.com"
        self.password = DataForSeo.DATAFORSEO_API_KEY
        self.credentials = f"{self.username}:{self.password}"
        self.encoded_cred = base64.b64encode(self.credentials.encode("utf-8")).decode("utf-8")
        self.PRODUCT_ASIN = []
        self.PRODUCT_ID = []
        self.LOCATIONS = []
        self.URL_GET_TASK_RESULT = "https://api.dataforseo.com/v3/merchant/amazon/reviews/task_get/advanced/{}"
        self.URL_GET_PRODUCT_ID = "https://api.dataforseo.com/v3/merchant/amazon/reviews/task_post"
        self.URL_GET_LOCATIONS = "https://api.dataforseo.com/v3/merchant/amazon/locations"
        # cred="$(printf ${login}:${password} | base64)"

    def init_db(self):
        db = mondb.get_database()
        collection_name = "test"

        query = {key: {'$exists': True}}
        collection = db[collection_name]
        #query = {key: {'$eq': None, '$type': 'null'}}
        existing_doc = collection.find_one(query)
        if existing_doc is None:
            collection.insert_one(self.get_location_info())
            logger.info("Inserted locations into collection")

            
        


    def get_task_result_by_id(self, id):
        headers = {
            "Authorization": f"Basic {self.encoded_cred}",
            "Content-Type": "application/json"
            }
        url = self.URL_GET_TASK_RESULT.format(id)
        print(url)
        return requests.get(url, headers=headers).json()   
    
    def get_product_info(self, asin):
        c = 0     
        try:
            id = self.get_id_by_asin(asin=asin)
            if id:
                while True:
                    if c == 5:
                        logger.info("loop executed 5 times. exiting...")
                        break                                    
                    response = self.get_task_result_by_id(id)
                    logger.info(response['tasks'][0]['status_code'])
                    print(type(response['tasks'][0]['status_code']))
                    
                    if response['status_code'] == 20000 and response['tasks'][0]['status_code'] == 20000:
                        result = response['tasks'][0]['result'][0]
                        data = {"task_id": id,
                                "date": datetime.now(),
                                "title": result['title'],
                                "rating": result['rating'],
                                "items_count": result['items_count'],
                                "items": result['items']
                                }
                         
                        doc = mondb.add_document(data, "test")
                        logger.info(doc)
                        logger.info("Success DONE .")
                        break
                    time.sleep(5)
                    c +=1
            else:
                logger.info("id is None")
        except Exception as e:
            logger.error(e)
            raise "Failed !"

                

    def get_id_by_asin(self, asin: str, location_code: int=2840):
        headers = {
            "Authorization": f"Basic {self.encoded_cred}",
            "Content-Type": "application/json"
            }
        payload = [
            {
        "language_code": "en_US",
        "location_code": location_code,
        "asin": asin
        }
        ]
        try:
            response = requests.post(self.URL_GET_PRODUCT_ID, headers=headers,
                                     data=json.dumps(payload)).json()
            logger.info(type(response))
            logger.info(response)

            
            if response["status_code"] == 20000 and response["tasks"][0]["status_code"] == 20100:
                logger.info("Task successfully created.")
                id = response['tasks'][0]['id']
                logger.info(f"Task id: {id}")
                return id
            return None
        except Exception as e:
            logger.error(e)
            return None
        

    def get_location_info(self):
        try:
            response = requests.get(self.URL_GET_LOCATIONS).json()
            return {"locations": response}
        except Exception as e:
            print(e)
            return {}

    

        #for i in response['result']:
        #    self.LOCATIONS.append({
        #        'location_code': i['location_code'],
        #        'location_name': i['location_name'],
        #        'country_iso_code': i["country_iso_code"]
        #        }
        #        )
        return self.LOCATIONS
        

class Reinforest:
    def __init__(self):
        self.api_key = os.getenv("REINFOREST_API_KEY")

    def get_result(self):
        # set up the request parameters
        params = {
        'api_key': self.api_key,
          'amazon_domain': 'amazon.com.tr',
          'asin': 'B0BTDTX1GL',
          'type': 'reviews',
          'language': 'tr_TR',
          'include_html': 'false',
          'output': 'json'
        }

        # make the http GET request to Rainforest API
        api_result = requests.get('https://api.rainforestapi.com/request', params, timeout=120).json()

        # print the JSON response from Rainforest API
        return api_result
        #print(json.dumps(api_result))

        
if __name__ == "__main__":
    seo = DataForSeo()
    #seo.get_product_info(asin="B085G5CDY7")
    #print(seo.get_task_result_by_id("03071839-5501-0415-0000-a2a913a98375"))
    



    #rein = Reinforest()
    #response = rein.get_result()
    #print(response)
    #with open('reinforest.json', 'w') as f:
    #    json.dump(response, f)
    
    
    
    

    
    

    

                
        




