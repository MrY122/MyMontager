import ffmpeg
import os
import cv2
from PIL import Image, ImageFilter, ImageEnhance
import math

path = input("Путь к папке") + "/"
files = os.listdir(path)

os.mkdir(path + "processed")

for file in files:

	fullname = path + file
	#Изображение
	if file[-3:] == "png" or file[-3:] == "jpg" or file[-4:] == "jpeg" or file[-4:] == "webp":

		if file[-4:] == "webp":
			convert = Image.open(fullname)
			convert.save(fullname[:-3] + "png")
			fullname = fullname[:-3] + "png"
			file = file[:-3] + "png"

		orientation = ""
		im = Image.open(fullname)
		(width, height) = im.size
		if im.size != (1920, 1080):
		#Задний фон
			final = im.copy()

			#Обрезка
			vertical_margin = (height - ((width * 9) / 16)) / 2 #Даже не спрашивай, почему оно называется так, просто нужно было назвать как-то, чтобы передавался примерный смысл
			horizontal_margin = (width - ((height * 16) / 9)) / 2
			orientation = 0

			if width / height < 16 / 9: #вертикальное изображение
				orientation = 1 #вертикальное

				final = final.crop((0, round(vertical_margin), width, height - round(vertical_margin)))

			else: #широкое изображение (или im.size[0] / im.size[1] > 16 / 9)
				orientation = 0

				final = final.crop((round(horizontal_margin), 0, width - round(horizontal_margin), height))

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
				padding = round((1920 - im.size[0]) / 2) #Даже не спрашивай, почему оно называется так, просто нужно было назвать как-то, чтобы передавался примерный смысл

				bg = final.copy()
				final = bg.paste(im, (padding, 0)) #Вертикальное

			else:
				im = im.resize((1920, round((1920 * height) / width)))
				padding = round((1080 - im.size[1]) / 2)

				bg = final.copy()
				final = bg.paste(im, (0, padding)) #Горизонтальное
			
			bg.save(path + "processed/" + file)
"""
	elif file[-3:] == "mp4":
		vid = cv2.VideoCapture(fullname)
		height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
		width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)

		if height != 1080 or width != 1920:
			input = ffmpeg.input(fullname)
"""