import preparer
import automatic_video_editing

from tkinter import *
from tkinter import filedialog

path_dir = ""
path_file = ""

def main_process():
	lbl_status.configure(text="Работа в процессе")
	if path_dir != "":
		preparer.main(save_to16x9.get(), save_convert.get(), path_dir, convert_format.get())
	if path_file != "":
		automatic_video_editing.main(model_path=model_path, video_path=path_file, result_path=result_path, silence=save_silence.get(), 
			threshold=threshold, offset_silence=offset_silence, start_word=start_word, end_word=end_word, offset_words=offset_words, 
			bitrate=bitrate, path_dir=path_dir)
	lbl_status.configure(text="Всё готово!")

def select_dir():
	global path_dir
	path_dir = filedialog.askdirectory(title="выберите папку")
	lbl_dir.configure(text=path_dir)

def select_file():
	global path_file
	global result_path
	path_file = filedialog.askopenfilename(title="выберите файл")
	result_path = path_file[:-4] + "_processed.mp4"
	lbl_file.configure(text=path_file)


model_path = "models/vosk-model-small-ru-0.22"

silence = True

# Default is None, must be like '2500k', '5000k', '10000k' etc.
bitrate = None 

# Next two parameters are used only if silence==True
# threshold of silence time in seconds
threshold = 1
# offset in seconds
offset_silence = 0.25

# Next three parameters are used only if silence==False
# control word that signals the beginning of the video fragment to be cut
start_word = 'йцывапрол'
# control word that signals the ending of the video fragment to be cut
end_word = 'цувапролдж'
# offset in seconds
offset_words = 0.5


#Окно
window = Tk()
window.title("My Preparer")

#Начальные позиции
save_to16x9 = BooleanVar()
save_to16x9.set(False)

save_convert = BooleanVar()
save_convert.set(False)

save_silence = BooleanVar()
save_silence.set(True)

convert_format = StringVar()
convert_format.set("png")


#Обработка видео из папки
lbl_dir = Label(window, text="Путь")
lbl_dir.grid(column=1, row=0)

select_dir = Button(window, text="Выбрать папку", command=select_dir)
select_dir.grid(column=0, row=0)

preparer_text = Label(window, text="Подготовка файлов в папке:")
preparer_text.grid(column=0, row=1)

chk_to16x9 = Checkbutton(window, text="Подстроить под 16х9", var=save_to16x9)  
chk_to16x9.grid(column=0, row=2)

chk_convert = Checkbutton(window, text="Конвертировать в распространённые форматы", var=save_convert)  
chk_convert.grid(column=1, row=2)

om_convert_format = OptionMenu(window, convert_format, "png", "jpg")  
om_convert_format.grid(column=1, row=3)

#Обработка главного видео
lbl_video_settings = Label(window, text="Настройки обработки главного видео:")
lbl_video_settings.grid(column=0, row=4)

lbl_file = Label(window, text="Путь")
lbl_file.grid(column=1, row=5)

select_file = Button(window, text="Выбрать файл", command=select_file)
select_file.grid(column=0, row=5)

#Тишина
chk_silince = Checkbutton(window, text="вырезать тишину", var=save_silence)
chk_silince.grid(column=0, row=6)

#Слова-маркеры


main_btn = Button(window, text="Запуск", command=main_process)
main_btn.grid(column=0, row=7)

lbl_status = Label(window, text="")
lbl_status.grid(column=0, row=8)

window.mainloop()