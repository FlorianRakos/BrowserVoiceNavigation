import whisper
import sounddevice as sd
from scipy.io.wavfile import write



freq = 44100
duration = 5

recording = sd.rec(int(duration * freq),
                   samplerate=freq, channels=2)
sd.wait()


write("temp/recording.wav", freq, recording)
print("Sound captured")

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
print(result.text)

