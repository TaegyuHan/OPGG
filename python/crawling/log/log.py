"""

  log 설정 파일 입니다.

"""

import logging

# log 저장 경로
LOG_PATH = "C:/github/OPGG/python/crawling/log/example.log"




class CustomFormatter(logging.Formatter):
    """Python 로그 색 변경 클래스

    Returns:
        setFormatter() : 함수에 넣어 사용
    """

    grey = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s | %(name)s | %(levelname)s | %(message)s - (%(filename)s:%(lineno)d) "

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)




def make_logger(name="OPGG", log_path=LOG_PATH):
    """로그 객체 생성

    Args:
        name (str, optional): 로그 이름 
                    Defaults to "OPGG".

        log_path ([type], optional): 로그 저장경로. 
                    Defaults to LOG_PATH.

    Returns:
        [class]: <class 'logging.Logger'>
    """

    #1 logger instance를 만든다.
    logger = logging.getLogger(name)

    #2 logger의 level을 가장 낮은 수준인 DEBUG로 설정해둔다.
    logger.setLevel(logging.DEBUG)
    
    #4 handler instance 생성
    console = logging.StreamHandler()
    file_handler = logging.FileHandler(filename=log_path, encoding='utf-8')
    
    #5 handler 별로 다른 level 설정
    console.setLevel(logging.INFO)
    file_handler.setLevel(logging.DEBUG)

    #6 handler 출력 format 지정
    console.setFormatter(CustomFormatter())
    file_handler.setFormatter(CustomFormatter())

    #7 logger에 handler 추가
    logger.addHandler(console)
    logger.addHandler(file_handler)

    return logger

# logger = make_logger()