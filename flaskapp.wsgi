#!/usr/bin/python
import sys
import logging

activate_this = '/home/arenas/Escritorio/tesis/venv/bin/activate'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/home/arenas/Escritorio/tesis/")
from application import init_app
application = init_app()
if __name__ == "__main__":
    application.run(host='0.0.0.0',port=5000)

