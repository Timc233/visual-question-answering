import speech_recognition as sr
from gtts import gTTS


def text_to_voice(text, language='en'):
    voice_obj = gTTS(text=text, lang=language, slow=False)

    # Saving the converted audio in a mp3 file named
    # welcome
    voice_obj.save("answer.mp3")


def voice_to_text(filename):
    # initialize the recognizer
    r = sr.Recognizer()

    # open the file
    with sr.AudioFile(filename) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)
        return(text)


if __name__ == "__main__":
    voice_filename = "machine-learning_speech-recognition_16-122828-0002.wav"
    voice_to_text(voice_filename)

    text = 'This is VQA team'
    text_to_voice(text)