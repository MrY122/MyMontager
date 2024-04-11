import ffmpeg
import os
from videoprops import get_video_properties
from PIL import Image, ImageFilter, ImageEnhance
import math
import shutil
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

def convert(fullname, path, file, final_format):

	if fullname[-3:] == "svg":
		drawing = svg2rlg(fullname)
		renderPM.drawToFile(drawing, fullname[:-3] + "png", fmt='PNG')
		shutil.move(fullname, path + "old/" + file)

	elif fullname[-3:] == "gif" or fullname[-3:] == "avi" or fullname[-3:] == "mov":
		conv = ffmpeg.input(fullname)
		conv = ffmpeg.output(conv, fullname[:-3] + "mp4")
		ffmpeg.run(conv)
		shutil.move(fullname, path + "old/" + file)

	elif fullname[-3:] == "png" or fullname[-3:] == "jpg":
		im = Image.open(fullname)
		im.save(fullname[:-3] + final_format)
		shutil.move(fullname, path + "old/" + file)

	elif fullname[-4:] == "jpeg" or fullname[-4:] == "webp":
		im = Image.open(fullname)
		im.save(fullname[:-4] + final_format)
		shutil.move(fullname, path + "old/" + file)


def to_16x9(fullname, path, file):

	#Изображение
	if fullname[-3:] == "png" or fullname[-3:] == "jpg" or fullname[-4:] == "jpeg" or fullname[-4:] == "webp":

		im = Image.open(fullname)
		(width, height) = im.size
		if im.size != (1920, 1080):
		#Задний фон
			final = im.copy()

			#Обрезка
			orientation = 0

			if width / height < 16 / 9: #вертикальное изображение
				margin = round((height - ((width * 9) / 16)) / 2)
				orientation = 1 #вертикальное

				final = final.crop((0, margin, width, height - margin))

			else: #широкое изображение (или im.size[0] / im.size[1] > 16 / 9)
				margin = round((width - ((height * 16) / 9)) / 2)
				orientation = 0

				final = final.crop((margin, 0, width - margin, height))

			final = final.resize((1920, 1080))

			#Блюр
			for i in range(15):
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
				padding = padding = round((1080 - im.size[1]) / 2)

				bg = final.copy()
				final = bg.paste(im, (0, padding)) #Горизонтальное
			
			bg.save(path + "processed/" + file)
		else:
			shutil.move(fullname, path + "processed/" + file)

	#Видео
	elif fullname[-3:] == "mp4":
		props = get_video_properties(fullname)
		width = props['width']
		height = props['height']

		if height != 1080 or width != 1920:
			bg = ffmpeg.input(fullname)
			orientation = 0

			if width / height < 16 / 9: #вертикальное видео
				margin = round((height - ((width * 9) / 16)) / 2)
				orientation = 1

			else: #широкое видео
				margin = round((width - ((height * 16) / 9)) / 2)
				orientation = 0

			#Задний фон
			if orientation == 1:
				margin = round((height - ((width * 9) / 16)) / 2)
				bg = bg.video.filter("crop", x="0", y=str(margin), w=str(width), h=str(height - (margin * 2)))

			else:
				margin = round((width - ((height * 16) / 9)) / 2)
				bg = bg.filter("crop", x=str(margin), y="0", w=str(width - (margin * 2)), h=str(height))
			bg = bg.filter("scale", 1920, 1080)
			bg = bg.filter("boxblur", lp="1", lr="50", cr="25").filter("eq", brightness=-0.1)
			bgo = ffmpeg.output(bg, path + "processed/bg" + file)
			ffmpeg.run(bgo)

			#Передний план
			fg = ffmpeg.input(fullname)
			if orientation == 1:
				fg = fg.filter("scale", -1, 1080)
				fg = ffmpeg.output(fg, path + "processed/fg" + file)
				ffmpeg.run(fg)

				props = get_video_properties(path + "processed/fg" + file)
				width = props['width']

				padding = round((1920 - width) / 2)

				final = ffmpeg.filter([ffmpeg.input(path + "processed/bg" + file), ffmpeg.input(path + "processed/fg" + file)],"overlay", x=str(padding))

			else:
				fg = fg.filter("scale", 1920, -1)
				fg = ffmpeg.output(fg, path + "processed/fg" + file)
				ffmpeg.run(fg)

				props = get_video_properties(path + "processed/fg" + file)
				height = props['height']

				padding = round((1080 - height) / 2)

				final = ffmpeg.filter([ffmpeg.input(path + "processed/bg" + file), ffmpeg.input(path + "processed/fg" + file)],"overlay", y=str(padding))
			
			final = ffmpeg.output(final, path + "processed/" + file)
			ffmpeg.run(final)

			os.remove(path + "processed/fg" + file)
			os.remove(path + "processed/bg" + file)
		else:
			shutil.move(fullname, path + "processed/" + file)
	print(file + " обработан")



def main(to16x9, convert_, path, convert_format):
	final_format = convert_format

	path = path + "/"

	files = os.listdir(path)
	try:
		os.mkdir(path + "processed")
	except:
		pass

	try:
		os.mkdir(path + "old")
	except:
		pass

	for file in files:
		fullname = path + file
		if convert_ == True:
			convert(fullname, path, file, final_format)

	files = os.listdir(path)
	for file in files:
		fullname = path + file
		if to16x9 == True:
			try:
				to_16x9(fullname, path, file)
			except:
				pass

	files = os.listdir(path + "processed")
	for file in files:
		shutil.move(path + "processed/" + file, path + file)
	os.rmdir(path + "processed")