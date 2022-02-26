import preparer
import SpeechRecognizing

from tkinter import *

def main_process():
	save_convert.get()
	save_to16x9.get()

	audio_settings = True

	preparer.main(save_convert.get(), save_to16x9.get())

	main_file = input("Адрес видео/аудио файла")
	path = ""

	tmp_path = path.split("\\")
	for i in range(len(tmp_path) - 1):
		path += tmp_path[i]

	if audio_settings == True:
		text = SpeechRecognizing.audio_recognition(main_file, save_text, path)

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

chk_save_text = Checkbutton(window, text="Сохранить текст", var=save_text)  
chk_save_text.grid(column=0, row=2)

main_btn = Button(window, text="Запуск", command=main_process)
main_btn.grid(column=0, row=3)

window.mainloop()