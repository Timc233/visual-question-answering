from flask import Flask, request

app = Flask(__name__)


@app.post("/picture")
def start_new_process():
    return 0


@app.put("/picture")
def receive_picture():
    return 0


@app.put("/voice")
def receive_voice():
    return 0


@app.delete("/stop")
def delete_process():
    return 0



app.run(debug=True)

