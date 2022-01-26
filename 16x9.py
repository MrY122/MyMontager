import ffmpeg
import os
import cv2
from PIL import Image, ImageFilter, ImageEnhance
import math


def Margin(param1, param2):
	return round((param2 - ((param1 * 9) / 16)) / 2)

def Padding(param):
	return round((1920 - param) / 2)


path = input("Путь к папке") + "/"
files = os.listdir(path)

try:
	os.mkdir(path + "processed")
except:
	print("Папка уже существует")


for file in files:

	fullname = path + file
	#Изображение
	if file[-3:] == "png" or file[-3:] == "jpg" or file[-4:] == "jpeg" or file[-4:] == "webp":

		im = Image.open(fullname)
		(width, height) = im.size
		if im.size != (1920, 1080):
		#Задний фон
			final = im.copy()

			#Обрезка
			orientation = 0

			if width / height < 16 / 9: #вертикальное изображение
				margin = Margin(width, height)
				orientation = 1 #вертикальное

				final = final.crop((0, margin, width, height - margin))

			else: #широкое изображение (или im.size[0] / im.size[1] > 16 / 9)
				margin = Margin(height, width)
				orientation = 0

				final = final.crop((margin, 0, width - margin, height))

			final = final.resize((1920, 1080))

			#Блюр
			final = final.filter(ImageFilter.BLUR)
			for i in range(10):
				final = final.filter(ImageFilter.BLUR)

			#Затемнение
			enhancer = ImageEnhance.Brightness(final)
			final = enhancer.enhance(0.5)

			if orientation == 1:
				im = im.resize((round((1080 * width) / height), 1080))
				padding = Padding(im.size[0]) #Даже не спрашивай, почему оно называется так, просто нужно было назвать как-то, чтобы передавался примерный смысл

				bg = final.copy()
				final = bg.paste(im, (padding, 0)) #Вертикальное

			else:
				im = im.resize((1920, round((1920 * height) / width)))
				padding = Padding(im.size[1])

				bg = final.copy()
				final = bg.paste(im, (0, padding)) #Горизонтальное
			
			bg.save(path + "processed/" + file)

#Видео
"""
	elif file[-3:] == "mp4":
		vid = cv2.VideoCapture(fullname)
		height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
		width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)

		if height != 1080 or width != 1920:
			video = ffmpeg.input(fullname)
"""