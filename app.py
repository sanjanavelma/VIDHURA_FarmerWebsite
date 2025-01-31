from flask import Flask, request, jsonify, render_template
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os

app = Flask(__name__)

# Language Dictionary
dic = {
    'english': 'en', 'hindi': 'hi', 'french': 'fr', 'spanish': 'es',
    'german': 'de', 'chinese': 'zh-cn', 'japanese': 'ja'
}

# Function to recognize speech
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        return query
    except:
        return "None"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    to_lang = data['language'].lower()

    if to_lang not in dic:
        return jsonify({'error': 'Language not supported'})

    to_lang_code = dic[to_lang]

    # Recognize speech
    query = recognize_speech()
    if query == "None":
        return jsonify({'error': 'Speech not recognized'})

    # Translate text
    translator = Translator()
    translated_text = translator.translate(query, dest=to_lang_code).text

    # Convert to speech
    tts = gTTS(text=translated_text, lang=to_lang_code, slow=False)
    audio_file = "static/captured_voice.mp3"
    tts.save(audio_file)

    return jsonify({'translated_text': translated_text, 'audio_url': audio_file})

if __name__ == '__main__':
    app.run(debug=True)
