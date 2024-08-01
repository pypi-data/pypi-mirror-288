import logging

def setup_logging():
    #  ��������־��¼��
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # ������־д��error.log �ļ�
    error_handler = logging.FileHandler('logs/error.log')
    error_handler.setLevel(logging.ERROR)
    error_formatter = logging.Formatter('%(asctime)s %(levelname)s:%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    error_handler.setFormatter(error_formatter)

    # ������־ д��operation.log �ļ�
    operation_handler = logging.FileHandler('logs/operation.log')
    operation_handler.setLevel(logging.INFO)
    operation_formatter = logging.Formatter('%(asctime)s %(levelname)s:%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    operation_handler.setFormatter(operation_formatter)

    root_logger.addHandler(error_handler)
    root_logger.addHandler(operation_handler)

# ��ʼ����־����
setup_logging()

logger = logging.getLogger(__name__)