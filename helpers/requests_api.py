import os
import asyncio
import httpx
import requests
from helpers._reports.logging_config import logger

from dotenv import load_dotenv
load_dotenv()

#####################################################################################################################


async def send_product(client, sku, data, semaphore):
    API_URL = os.getenv("BASE_URL") + os.getenv("END_POINT_UPDATE")
    token = f"Bearer {os.getenv('TOKEN')}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": token
    }
    
    async with semaphore:
        try:
            payload = {
                "product": {
                    "sku": sku,
                    "name": data["name_first"],
                    "price": float(data["price_brutto"]),
                    "attribute_set_id": data["attribute_set_id"],
                    "visibility": data["visibility"],
                    "status": data["status"],
                }
            }
            resp = await client.post(API_URL, json=payload, headers=headers)
            resp.raise_for_status()
            result = resp.json()
            logger.debug(f"[NEW PRODUCT PAYLOAD] {sku} : {payload}")
            logger.debug(f"[OK] {sku} : {result}")
            return result
        except Exception as e:
            logger.error(f"[ERROR] {sku} : {e}")
            return None


async def requests_main_for_products(product_data_map):
    CONCURRENCY = 20
    semaphore = asyncio.Semaphore(CONCURRENCY)

    async with httpx.AsyncClient(http2=True, timeout=30.0) as client:
        tasks = [
            send_product(client, sku, data, semaphore)
            for sku, data in product_data_map.items()
        ]
        results = await asyncio.gather(*tasks)
        return results

#####################################################################################################################


async def send_quantity(client, sku, data, semaphore):
    API_URL = os.getenv("BASE_URL") + os.getenv("END_POINT_ADD_STOCK")
    token = f"Bearer {os.getenv('TOKEN')}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": token
    }

    async with semaphore:
        try:
            payload = {
                "sourceItems": [
                    {
                        "sku": sku,
                        "source_code": "default",
                        "quantity": int(data["qty"]),
                        "status": 1,
                    }
                ]
            }
            resp = await client.post(API_URL, json=payload, headers=headers)
            resp.raise_for_status()
            result = resp.json()
            logger.debug(f"[PAYLOAD] {sku} : {payload}")
            logger.debug(f"[OK] {sku} : {result}")
            return result
        except Exception as e:
            logger.error(f"[ERROR] {sku} : {e}")
            return None


async def requests_main_for_quantities(stock_and_price_data_map):
    CONCURRENCY = 20
    semaphore = asyncio.Semaphore(CONCURRENCY)

    async with httpx.AsyncClient(http2=True, timeout=30.0) as client:
        tasks = [
            send_quantity(client, sku, data, semaphore)
            for sku, data in stock_and_price_data_map.items()
        ]
        results = await asyncio.gather(*tasks)
        return results
    
#####################################################################################################################


def get_all_products_from_magento(): # add report
    page_size = 100
    current_page = 1
    url = os.getenv("BASE_URL") + os.getenv("END_POINT_ALL_PRODUCTS")
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.environ.get("TOKEN"),
    }
    

    sku_list = []

    while True:
        params = {
        "fields": "items[sku]",
        "searchCriteria[currentPage]": current_page,
        "searchCriteria[pageSize]": page_size,
    }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            items_list = response.json().get("items")
            if items_list is not None:
                sku_list.extend(item.get("sku") for item in items_list)
                current_page += 1

            else:
                break
        else:
            logger.error(f"Error retrieving product SKUs. Response Status Code: {response.status_code}", exc_info=True)
            logger.error(f"Response Content: {response.text}", exc_info=True)
            break
    
    sku_set = set(sku_list)
    logger.info(f"Loaded: {len(sku_set)} SKU")
    return sku_set
