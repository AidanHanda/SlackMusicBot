from core import poll
from settings import init
import commands #Imported so all of the commands register!

def run(data):
    init(data)
    poll()