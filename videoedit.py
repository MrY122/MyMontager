#Не обращайте внимание. Это всё в основном для теста. По нормальному сделаю в следующем коммите

import ffmpeg

class Audio:
	def silence_remove(main_file):
		file = main_file.audio.filter("silenceremove", start_periods="0")
		return file

class Video:
	pass

audio_settings = True
video_settings = True

path = input("Адрес видео/аудио файла")
main_file = ffmpeg.input(path)

if audio_settings == True:
	audio = Audio.silence_remove(main_file)

if video_settings == True:
	video = main_file.video

final = ffmpeg.output(audio, video, path[:-4] + "_processed.mp4").run()