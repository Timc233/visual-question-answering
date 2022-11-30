# visual-question-answering

## package
- conda

## environment
### backend

- Enter backend directory \
`cd /backend`

- Use first cmd to create new conda environment for vqa project or active an existed environment \
`conda create env vqa python=3.10`\
`conda activate vqa`

- Use pip to install all liberaries \
`pip install -r requirements.txt`

- Run backend server and the port is 5000 \
`python flask_server.py`

#### API
- /upload_photo\
  method: POST \
  form-data: {'KEY': 'file', 'VALUE': \<photo file\>} \
  response: {'response': 'success'}
- /upload_question \
  method: POST \
  form-data: {'KEY': 'file', 'VALUE': \<question file\>} \
  response: <answer.mp3>
  

