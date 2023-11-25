import keyboard
import flask
import whisper
import sounddevice as sd
from scipy.io.wavfile import write
import requests
from flask import Flask, jsonify
import threading
import logging
from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS from flask_cors module

app = Flask(__name__)
CORS(app)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

json_cmd = {}
record_button = "r"
quit_button = "q"


@app.route('/get_text', methods=['GET'])
def get_text():
    return json_cmd

@app.route('/reset', methods=['GET'])
def reset():
    print("------ Reset ------")
    global json_cmd
    json_cmd = {}
    resp = jsonify(success=True)
    return resp


def record():
    print("Recording...")
    freq = 44100
    duration = 10
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)
    #sd.wait()

    while (keyboard.is_pressed(record_button)):
        continue

    write("temp/recording.wav", freq, recording)
    print("Sound captured")

def translate(model):

    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio("temp/recording.wav")
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")

    # decode the audio
    options = whisper.DecodingOptions(fp16 = False)
    result = whisper.decode(model, mel, options)
    translation = result.text.lower()
    print("Translation: " + translation)

    action_words = [["click", "press", "select"], ["scroll"]]

    global json_cmd

    for group in action_words:
        for word in group:

            if word in translation:
                json_cmd = {
                    "action": "",
                    "element": "",
                }
                # get the index of the word
                index = translation.index(word)
                print("Action word detected at index: " + str(index))

                json_cmd["action"] = group[0]
                json_cmd["element"] = translation[index + len(word) + 1 : len(translation) - 1]
                print(json_cmd)
                break


def run_flask():
    print("Run flask")
    app.run(port=5000)

def main():
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    model = whisper.load_model("base")

    while True:
        if keyboard.is_pressed('r'):
            record()
            translate(model)
        if keyboard.is_pressed('q'):
            break


if __name__ == "__main__":
    main()