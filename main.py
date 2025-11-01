from helpers._reports.logging_config import logger
from helpers.processing import processing_artykuly, processing_ceny_stany
from helpers.requests_api import get_all_products_from_magento
from helpers.utils import check_lock_file, create_lock_file, delete_lock_file, check_artykuly_files, check_ceny_stany_files, create_basic_dirs, check_all_files



def main():

    check_lock_file()

    try:
        create_lock_file() 

        create_basic_dirs()

        artykuly_xml_files_sorted = check_artykuly_files()

        ceny_stany_xml_files_sorted = check_ceny_stany_files()

        if check_all_files(artykuly_xml_files_sorted, ceny_stany_xml_files_sorted): return

        sku_set = get_all_products_from_magento()

        processing_artykuly(artykuly_xml_files_sorted, sku_set)

        processing_ceny_stany(ceny_stany_xml_files_sorted, sku_set)
                

    except Exception as e:
        logger.error(f"Error in main: {e}")

    finally:
        delete_lock_file()



if __name__ == "__main__":
    main()
    print('text')
    print('text')
    print('text3')

