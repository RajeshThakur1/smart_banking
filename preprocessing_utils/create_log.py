from application_logging import logger

class Create_preprocessing_logs:
    def __init__(self):
        self.logger = logger.App_Logger()

    def insert_log(self,file,log_msg):
        log_file = open(file, 'a+')
        self.logger.log(log_file,log_msg)
        log_file.close()