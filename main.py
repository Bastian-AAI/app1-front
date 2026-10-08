# -*- coding: utf-8 -*- 
import os
import json
from app import app, IA_SERVER, IA_URL
from flask import request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from utils import allowed_file
import hashlib
import requests

@app.route('/ejercicio2/app1-front/')
def index_form():
    return render_template('index.html')


@app.route('/ejercicio2/app1-front/upload', methods=['POST'])
def upload_image():
    try:
        if 'file' not in request.files:
            error = 'No se envió ningún archivo'
            return render_template('index.html', error=error)
        file = request.files['file']
        if not file or file.filename == '':
            error = 'No se seleccionó ningún archivo'
            return render_template('index.html', error=error)
        if not allowed_file(file.filename):
            error = 'Archivo no permitido. Solo se permite JPG, JPEG o PNG.'
            return render_template('index.html', error=error)
        file_bytes = file.read()
        print("recibo {} bytes".format(len(file_bytes)))
        base_dir = app.config['UPLOAD_FOLDER']
        md5sum = hashlib.md5(file_bytes).hexdigest()
        filename = md5sum + '_' + secure_filename(file.filename)
        filepath = os.path.join(base_dir, filename)
        print("guardando archivo " + filepath)
        os.makedirs(base_dir, exist_ok=True)
        with open(filepath, "wb") as f:
            f.write(file_bytes)
        files = {'file': file_bytes}
        print("llamando a " + IA_SERVER + IA_URL)
        apicall = requests.post(IA_SERVER + IA_URL, files=files, timeout=(1, 10))
        if apicall.status_code != 200:
            error = "Error contactando la aplicación IA"
            return render_template('index.html', error=error)
        api_json = json.loads(apicall.content.decode('utf-8'))
        return render_template('index.html', filename=filename, result=api_json)
    except Exception as e:
        error_msg = "Error: {}".format(e)
        print(error_msg)
        return render_template('index.html', error=error_msg)


@app.route('/ejercicio2/app1-front/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == "__main__":
    app.run(port=7001)
