#!/user/bin/env python3
# encoding: utf-8
import json
import os
from flask import Flask, request, jsonify, render_template, send_file
from werkzeug.utils import secure_filename
from voice_to_text import voice_to_text, text_to_voice

app = Flask(__name__)
data_file_address = 'C:/Users/zyte4/OneDrive/Documents/个人资料/BU_2022_FALL/EC601/Code/tmp/data.txt'
# question_file_address = 'C:/Users/zyte4/OneDrive/Documents/个人资料/BU_2022_FALL/EC601/Code/tmp/question.wav'
# answer_file_address = 'C:/Users/zyte4/OneDrive/Documents/个人资料/BU_2022_FALL/EC601/Code/answer.mp3'
# upload_folder = "uploads/"


# if not os.path.exists(upload_folder):
#     os.mkdir(upload_folder)
#
# app.config['UPLOAD_FOLDER'] = upload_folder
# allowed_extentions = ['jpg']
#
# def check_file_extention(filename):
#     return filename.split('.')[-1] in allowed_extentions
#
# custmor = {'visual': None, 'question': None, 'answer': None}
# @app.route('/')
# def app_main():
#     t = request.args.get('type')
#     c = request.args.get('content')
#     # GET IMAGE UPLOAD
#     if t == 'visual':
#         # initialize
#         custmor = {}
#         f = request.files['file']
#         if not check_file_extention(f.filename):
#             return "image file extention is not allowed"
#         custmor['visual'] = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
#         f.save(custmor['visual'])
#         return "visual upload success"
#
#     # GET QUESTION VOICE UPLOAD
#     if t == 'question':
#         f = request.files['file']
#         if not check_file_extention(f.filename):
#             return "question file extention is not allowed"
#         question_file = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
#         custmor['question'] = voice_to_text(question_file)
#
#         custmor['answer'] = VQA_module(custmor['visual'], custmor['question'])
#         text_to_voice(custmor['answer'])
#
#         return send_file(answer_file_address)





# @app.route('/upload', methods = ['GET', 'POST'])
# def uploadfile():
#     print('here')
#     if request.method == 'POST':
#         print('here2')
#         f = request.files['file']
#         print(f)
#         if check_file_extention(f.filename):
#             f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
#             return 'file uploaded successfully'
#         else:
#             return 'file extension is not allowed'


@app.route('/', methods=['GET'])
def query_records():
    name = request.args.get('name')
    print(name)
    with open(data_file_address, 'r') as f:
        data = f.read()
        records = json.loads(data)
        print(records)
        for record in records:
            print(record)
            if record['name'] == name:
                return jsonify(record)
        return jsonify({'error': 'data not found'})


@app.route('/', methods=['PUT'])
def create_record():
    print("PUT:")
    record = json.loads(request.data)

    print(record)
    with open(data_file_address, 'r') as f:
        data = f.read()
    if not data:
        records = [record]
    else:
        records = json.loads(data)
        records.append(record)
    with open(data_file_address, 'w') as f:
        f.write(json.dumps(records, indent=2))
    return jsonify(record)


@app.route('/', methods=['POST'])
def update_record():
    record = json.loads(request.data)
    new_records = []
    with open(data_file_address, 'r') as f:
        data = f.read()
        records = json.loads(data)
    for r in records:
        if r['name'] == record['name']:
            r['email'] = record['email']
        new_records.append(r)
    with open(data_file_address, 'w') as f:
        f.write(json.dumps(new_records, indent=2))
    return jsonify(record)


@app.route('/', methods=['DELETE'])
def delte_record():
    record = json.loads(request.data)
    new_records = []
    with open(data_file_address, 'r') as f:
        data = f.read()
        records = json.loads(data)
        for r in records:
            if r['name'] == record['name']:
                continue
            new_records.append(r)
    with open(data_file_address, 'w') as f:
        f.write(json.dumps(new_records, indent=2))
    return jsonify(record)


app.run(debug=False)

