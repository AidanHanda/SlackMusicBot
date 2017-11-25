from core import poll
from settings import init


def run(data):
    '''
    Runs the rest of the app 
    :param data: The data from config
    :return: 
    '''
    init(data)
    poll()
