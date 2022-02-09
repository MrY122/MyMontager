import wave
import json
import ffmpeg
from vosk import Model, KaldiRecognizer

def Test(main_file):
	model = Model("Models/vosk-model-small-ru-0.22")

	wf = wave.open(main_file, "rb")
	rec = KaldiRecognizer(model, wf.getframerate())

	while True:

		result = ''
		last_n = False

		data = wf.readframes(4000)

		if len(data) == 0:
			break

		if rec.AcceptWaveform(data):
			res = json.loads(rec.Result())
			return res

main_file = "C:/Users/Александр/Desktop/projects python/Test/тест.wav"
print(Test(main_file))