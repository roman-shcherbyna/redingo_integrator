from helpers._reports.logging_config import logger
import requests
import os
from dotenv import load_dotenv

load_dotenv()


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
