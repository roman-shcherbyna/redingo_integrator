from datetime import datetime
from _reports.logging_config import logger
from _reports.telegram_config import send_message_to_telegram
import os
import asyncio

class ReportR:
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self):
        self.report_dict = {
            "main": {
                "total_time": {
                    "start": "",
                    "stop": "",
                    "duration": "",
                },
                "count_of_products": 0,
                "stat": {
                    "counts": {
                        "new": 0,
                        "update": 0,
                    }
                },
            },
            "data": {
                "new": [],
                "update": [],
            },
        }

        self.set_start_time()
        logger.info("Start")

        
    def set_start_time(self):
        start_time = datetime.now().strftime(self.DATE_FORMAT)
        self.report_dict['main']['total_time']['start'] = start_time
        logger.debug((f"Integrator start: {start_time}"))


    def set_stop_time(self):
        stop_time = datetime.now().strftime(self.DATE_FORMAT)
        self.report_dict['main']['total_time']['stop'] = stop_time
        logger.debug((f"Integrator stop: {stop_time}"))

    def calculate_duration(self):
        start = datetime.strptime(self.report_dict['main']['total_time']['start'], self.DATE_FORMAT)
        stop = datetime.strptime(self.report_dict['main']['total_time']['stop'], self.DATE_FORMAT)
        self.report_dict['main']['total_time']['duration'] = str(stop - start)


    def count_of_all_products(self, count):
        self.report_dict['main']['count_of_products'] = count


    def add_data(self, sku, entry_type):
        if entry_type == 'new':
            self.report_dict['data']['new'].append(sku)
            self.report_dict['main']['stat']['counts']['new'] += 1

        if entry_type == 'update':
            self.report_dict['data']['update'].append(sku)
            self.report_dict['main']['stat']['counts']['update'] += 1
        

    def get_report(self):
        return self.report_dict


    def check_errors(self):
        log_dir = os.path.join(os.getenv("LOGS_DIR"), "errors")
        today_date = datetime.now().strftime('%d_%m')
        log_filename = os.path.join(log_dir, f'log_{today_date}.log')

        return True if os.path.getsize(log_filename) > 0 else False


    def send_report(self):
        report_dict = self.get_report()
        has_errors = True
        if not self.check_errors():
            has_errors = False

        asyncio.run(send_message_to_telegram(report_dict, has_errors))

    def final(self):
        self.set_stop_time()
        self.calculate_duration()
        self.send_report()
        logger.info("Stop")