# -*- coding: utf-8 -*- 
import threading
from datetime import datetime

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def log_print(message):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    thread_id = threading.get_ident()
    prefijo = f"[{time}] [{thread_id}]"
    print(prefijo, message)