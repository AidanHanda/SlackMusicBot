import subprocess
import time
import logging

import settings
from core import poll




def run(data):
    settings.init(data)
    poll()