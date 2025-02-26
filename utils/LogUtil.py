from datetime import datetime


class LogUtil:

    @staticmethod
    def log_with_datetime(message: str):
        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {message}')

    @staticmethod
    def log(message: str):
        print(message)