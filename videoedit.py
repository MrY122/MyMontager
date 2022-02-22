import wave
import json
import ffmpeg
from tkinter import *
from vosk import Model, KaldiRecognizer

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

	if save_text == True:
		text = open(path + "/text.txt", "w")
		text.write(final)
		text.close()

def main_process():

	audio_settings = True
	video_settings = False

	main_file = input("Адрес видео/аудио файла")
	path = ""

	tmp_path = path.split("\\")
	for i in range(len(tmp_path) - 1):
		path += tmp_path[i]

	#main_file = ffmpeg.input(path)

	if audio_settings == True:
		text = audio_recognition(main_file, save_text, path)
		print(audio)

	"""
	if video_settings == True:
		video = main_file.video

	final = ffmpeg.output(audio, path[:-4] + "_processed.mp3").run()
	"""

#Окно
window = Tk()
window.title("My Montager")

save_text = BooleanVar()
save_text.set(False)

chk_audio = Checkbutton(window, text='Сохранить текст', var=save_text)  
chk_audio.grid(column=0, row=0)

main_btn = Button(window, text="Запуск", command=main_process)
main_btn.grid(column=0, row=1)

window.mainloop()