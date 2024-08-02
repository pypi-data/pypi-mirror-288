from loguru import logger
from datetime import datetime
import os

class Singleton:
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)

        return cls._instance

class LogStream(Singleton):
    def __init__(self, logfile_dir):
        self.logfile_dir = logfile_dir

    def __if_path_exists(self, logfile_dir):
        if os.path.exists(logfile_dir):
            return True

        return False

    def __created_at(self):
        now = datetime.now()
        return now.strftime('%d.%m.%Y, %H:%M:%S')

    def __record_ttl(self, level=5):
        if level == 5:
            return 'DEBUG'

        elif level == 4:
            return 'INFO'

        elif level == 3:
            return 'WARNING'

        elif level == 2:
            return 'ERROR'

        elif level == 1:
            return 'FATAL'

        else:
            return 'DEBUG'

    def clear(self):
        logfile_dir = self.logfile_dir
        if not self.__if_path_exists(logfile_dir):
            logger.error('Log file not exists!')
            return

        with open(logfile_dir, 'w') as f:
            f.write('')

        return

    def read(self):
        try:
            logfile_dir = self.logfile_dir
            if not self.__if_path_exists(logfile_dir):
                logger.error('Log file not exists!')
                return []

            with open(logfile_dir, 'r') as f:
                logfile = f.readlines()

            logfile = [record.replace('\n', '').strip() for record in logfile]
            return logfile

        except Exception as e:
            logger.error(str(e))

        return []

    def __call__(self, **kwargs):
        try:
            logfile_dir = self.logfile_dir
            if not self.__if_path_exists(logfile_dir):
                logger.error('Log file not exists!')
                return

            description = kwargs.get('description', 'No description')
            level = kwargs.get('level', 5)
            created_at = self.__created_at()
            record_ttl = self.__record_ttl(level)
            record = f'{record_ttl}: {description} ({created_at})\n'

            with open(logfile_dir, 'a') as f:
                f.write(record) 

        except Exception as e:
            logger.error(str(e))

        return