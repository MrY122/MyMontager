from vosk import Model, KaldiRecognizer
import wave
import json
import ffmpeg

def audio_recognition(main_file, save_text, path):
	model = Model("Models/vosk-model-small-ru-0.22") #или "Models/vosk-model-small-ru-0.22" - более быстрая, но менее точная

	wf = wave.open(main_file, "rb")
	rec = KaldiRecognizer(model, wf.getframerate())

	final = ''

	while True:

		data = wf.readframes(4000)

		if len(data) == 0:
			break

		if rec.AcceptWaveform(data):
			res = json.loads(rec.Result())

			if len(res) != 0:
				final += f" {res['text']}"

#	if save_text.get() == True:
	fullname = path + "text.txt"
	print(fullname)
	text = open(fullname, "w", encoding="utf-8")
	text.write(final)
	text.close()