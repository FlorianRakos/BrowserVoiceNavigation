import keyboard
import whisper
import sounddevice as sd
from scipy.io.wavfile import write

def record():
    freq = 44100
    duration = 5
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)
    sd.wait()


    write("temp/recording.wav", freq, recording)
    print("Sound captured")

def translate():

    model = whisper.load_model("base")

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
    print(translation)

    action_words = [["click", "press", "select"], ["scroll"]]

    json_cmd = {
        "action": "",
        "element": "",
    }

    for group in action_words:
        for word in group:

            if word in translation:
                # get the index of the word
                index = translation.index(word)
                print("Action word detected at index: " + str(index))

                json_cmd["action"] = group[0]
                json_cmd["element"] = translation[index + len(word) + 1 : len(translation) - 1]
                print(json_cmd)
                break

def main():
    while True:
        if keyboard.is_pressed('r'):
            record()
            translate()
        if keyboard.is_pressed('q'):
            break


if __name__ == "__main__":
    main()