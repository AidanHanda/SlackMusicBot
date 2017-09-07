from core import poll
from settings import init
import commands

def run(data):
    init(data)
    poll()