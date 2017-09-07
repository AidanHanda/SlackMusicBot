from core import poll
from settings import init


def run(data):
    init(data)
    poll()
