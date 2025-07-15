import asyncio
import os
import xml.etree.ElementTree as ET
from pathlib import Path
from helpers._reports.logging_config import logger
from helpers.requests_api import requests_main_for_products, requests_main_for_quantities
from helpers.utils import create_confirmation_file


var_dir = Path(os.environ.get("FILES_PATH"))

#####################################################################################################################

def processing_artykuly(artykuly_xml_files_sorted, sku_set):

    for artykuly_xml_path in artykuly_xml_files_sorted:
            errors = False

            try:
                tree = ET.parse(artykuly_xml_path)
                root = tree.getroot()

                product_data_map = {}

                for art in root.findall("art"):
                    magento_sku = art.findtext("kat")

                    if magento_sku not in sku_set:

                        product_data_map[magento_sku] = {
                            "name_first": art.findtext("nazwa"),
                            "name_second": art.findtext("nazwa2"),
                            "name": art.findtext("nazwa_oryg"),
                            "vat_rate": art.findtext("vat"),
                            "qty": int(art.findtext("stan")),
                            "price_brutto": art.findtext("cena_b"),
                            "id_kat_tree": art.findtext("id_kat_tree"),
                            "id_kat": art.findtext("id_kat"),
                            "season": art.findtext("p3"),
                            "season_year": art.findtext("p4"),
                            "promotional_price_n": art.findtext("cena_prom_n"),
                            "promotional_price_b": art.findtext("cena_prom_b"),
                            "barcode": art.findtext("kod_kres"),
                            "attribute_set_id": 4,
                            "visibility": 1,
                            "status": 2,
                        }
                        logger.info(f"New product {magento_sku}")
                        logger.info(f"Data for {magento_sku}: {product_data_map[magento_sku]}")

                results = asyncio.run(requests_main_for_products(product_data_map))
                if any(res is None for res in results):
                    errors = True
                    logger.error(f"Error in requests results for {artykuly_xml_path.name}: {results}")

            except Exception as e:
                logger.error(f"Error with parsing {artykuly_xml_path.name}: {e}")
                errors = True

            finally:
                create_confirmation_file(artykuly_xml_path.name)

            if errors:
                dest = var_dir / "errors_archive" / artykuly_xml_path.name
                artykuly_xml_path.replace(dest)
                logger.info(f"File {artykuly_xml_path.name} has been moved to the error_archive")

            else:
                artykuly_xml_path.replace(
                    var_dir / "artykuly_archive" / artykuly_xml_path.name
                )
                logger.debug(f"File {artykuly_xml_path.name} has been moved to the artykuly_archive")

#####################################################################################################################

def processing_ceny_stany(ceny_stany_xml_files_sorted, sku_set):

    for ceny_stany_xml_path in ceny_stany_xml_files_sorted:
            errors = False

            try:
                tree = ET.parse(ceny_stany_xml_path)
                root = tree.getroot()

                stock_and_price_data_map = {}

                for art in root.findall("art"):
                    magento_sku = art.get("idx")

                    s_elem = art.find("s")
                    qty = int(s_elem.text) if s_elem is not None else None

                    c_elem = art.find("ca/c")
                    price_brutto = (
                        float(c_elem.get("b"))
                        if c_elem is not None and c_elem.get("b")
                        else None
                    )

                    if magento_sku in sku_set:
                        stock_and_price_data_map[magento_sku] = {
                            "qty": qty,
                            "price_brutto": price_brutto,
                        }
                    else:
                        logger.error(f"The SKU {magento_sku} does not exist in Magento, so the source quantity cannot be updated {ceny_stany_xml_path.name}")
                        errors = True


                results = asyncio.run(requests_main_for_quantities(stock_and_price_data_map))
                if any(res is None for res in results):
                    errors = True
                    logger.error(f"Error in requests results for {ceny_stany_xml_path.name}: {results}")


            except Exception as e:
                print(f"Error with parsing {ceny_stany_xml_path.name}: {e}")
                errors = True
            
            finally:
                create_confirmation_file(ceny_stany_xml_path.name)

            if errors:
                    dest = var_dir / "errors_archive" / ceny_stany_xml_path.name
                    ceny_stany_xml_path.replace(dest)
                    logger.info(f"File {ceny_stany_xml_path.name} has been moved to the error_archive")

            else:
                ceny_stany_xml_path.replace(
                    var_dir / 'ceny_stany_archive' / ceny_stany_xml_path.name
                    )
                logger.info(f"File {ceny_stany_xml_path.name} has been moved to the ceny_stany_archive")