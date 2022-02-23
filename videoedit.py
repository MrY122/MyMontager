import preparer

import wave
import json
import ffmpeg
from tkinter import *
from vosk import Model, KaldiRecognizer

def audio_recognition(main_file, path):
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

	if save_text.get() == True:
		text = open(path + "/text.txt", "w")
		text.write(final)
		text.close()

def main_process():
	save_convert.get()
	save_to16x9.get()

	audio_settings = True
	video_settings = False

	preparer.main(save_convert.get(), save_to16x9.get())

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

save_to16x9 = BooleanVar()
save_to16x9.set(False)

save_convert = BooleanVar()
save_convert.set(False)

preparer_text = Label(window, text="Подготовка файлов в папке:")
preparer_text.grid(column=0, row=0)

chk_to16x9 = Checkbutton(window, text="Подстроить под разрешение 16х9", var=save_to16x9)  
chk_to16x9.grid(column=0, row=1)

chk_convert = Checkbutton(window, text="Конвертировать исходники в распространённые форматы", var=save_convert)  
chk_convert.grid(column=1, row=1)

chk_audio = Checkbutton(window, text="Сохранить текст", var=save_text)  
chk_audio.grid(column=0, row=2)

main_btn = Button(window, text="Запуск", command=main_process)
main_btn.grid(column=0, row=3)

window.mainloop()