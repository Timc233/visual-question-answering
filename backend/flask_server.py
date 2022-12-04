#!/user/bin/env python3
# encoding: utf-8
import json
import os
from flask import Flask, request, jsonify, render_template, send_file
from werkzeug.utils import secure_filename
from voice_to_text import voice_to_text, text_to_voice
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# data_file_address = 'C:/Users/zyte4/OneDrive/Documents/个人资料/BU_2022_FALL/EC601/Code/tmp/data.txt'
# question_file_address = 'C:/Users/zyte4/OneDrive/Documents/个人资料/BU_2022_FALL/EC601/Code/tmp/question.wav'
# answer_file_address = 'C:/Users/zyte4/OneDrive/Documents/个人资料/BU_2022_FALL/EC601/Code/answer.mp3'


upload_folder = 'uploads/'
app.config['UPLOAD_FOLDER'] = upload_folder
image_addr = None
question_addr = None
answer_addr = ".\\answer.mp3"

if not os.path.exists(upload_folder):
    os.mkdir(upload_folder)

app.config['UPLOAD_FOLDER'] = upload_folder
allowed_extentions = ['jpg']

def check_file_extention(filename):
    return filename.split('.')[-1] in allowed_extentions

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/wait_photo')
def wait_photo():
    return render_template('wait_photo.html')


@app.route('/upload_photo', methods=['GET', 'POST'])
def uploader_photo():
    if 'file' not in request.files:
        print("No files")
        return "GG"
    f = request.files['file']
    # f.save(secure_filename(f.filename))
    image_addr = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)+ '.jpg')
    f.save(image_addr)
    return jsonify({'response': 'success'})


@app.route('/upload_question', methods=['GET', 'POST'])
def uploader_question():
    if request.method == 'POST':
        f = request.files['file']
        question_addr = f.filename
        question_addr = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
        f.save(question_addr)

        # convert question .mav file into text
        question_text = voice_to_text(question_addr)
        # return render_template('wait_processing.html')

        # run VQA module and get answer in text
        # answer_text = VQA(image_addr, question_text)
        answer_text = "This is EC601, team 2, VQA project."

        # convert text in mp3 voice file
        text_to_voice(answer_text)

        return send_file(answer_addr)

@app.route('/test', methods=['POST'])
def str_test():
    if 'file' not in request.files:
        print("No files")
        return "GG"
    file = request.files['file']
    file.save('./test_file.jpg')
    print("OK")

    return "OK"


app.run(debug=False)

