import preparer
import SpeechRecognizing

from tkinter import *

def main_process():
	save_convert.get()
	save_to16x9.get()

	audio_settings = True

	preparer.main(save_to16x9.get(), save_convert.get())

	main_file = input("Адрес видео/аудио файла")

	path = ""

	tmp_path = main_file.split("\\")
	for i in range(len(tmp_path) - 1):
		path += tmp_path[i] + "\\"

	if audio_settings == True:
		text = SpeechRecognizing.audio_recognition(main_file, save_text, path)

def select_dir():
	path_dir = filedialog.askopenfilename(title="выберите папку")

def select_file():
	pass

#Окно
window = Tk()
window.title("My Montager")

save_text = BooleanVar()
save_text.set(False)

save_to16x9 = BooleanVar()
save_to16x9.set(False)

save_convert = BooleanVar()
save_convert.set(False)

selected_dir = Label(window, text="Путь")
selected_dir.grid(column=1, row=0)

select_dir = Button(window, text="Выбрать папку", command=select_dir)
select_dir.grid(column=0, row=0)

selected_file = Label(window, text="Путь")
selected_file.grid(column=1, row=1)

select_file = Button(window, text="Выбрать файл", command=select_file)
select_file.grid(column=0, row=1)

preparer_text = Label(window, text="Подготовка файлов в папке:")
preparer_text.grid(column=0, row=2)

chk_to16x9 = Checkbutton(window, text="Подстроить под разрешение 16х9", var=save_to16x9)  
chk_to16x9.grid(column=0, row=3)

chk_convert = Checkbutton(window, text="Конвертировать исходники в распространённые форматы", var=save_convert)  
chk_convert.grid(column=1, row=3)

speech_recognition_text = Label(window, text="Функции распознавания речи:")
speech_recognition_text.grid(column=0, row=4)

chk_save_text = Checkbutton(window, text="Сохранить текст", var=save_text)  
chk_save_text.grid(column=0, row=5)

main_btn = Button(window, text="Запуск", command=main_process)
main_btn.grid(column=0, row=6)

window.mainloop()