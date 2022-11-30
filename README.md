# visual-question-answering

## environment
### backend
`cd /backend`
`conda create env vqa python=3.10`
`pip install -r requirements.txt`
`python flask_server.py`

#### API
- /upload_photo
  method: POST
  e.g. ./templates/wait_photo.html
  response: {'response': 'success'}
- /upload_question
  method: POST
  e.g. ./templates/wait_question.html
  response: 'answer.mp3'
