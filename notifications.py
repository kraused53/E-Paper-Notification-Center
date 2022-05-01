from location import get_location
from PIL import Image, ImageFont, ImageDraw
from inky import InkyWHAT
from datetime import datetime

icon_dir = '/home/pi/Documents/projects/python/E-Paper/E-Paper-Notification-Center/E-Paper-Notification-Center/icons/'

if __name__ == '__main__':
	display = InkyWHAT("red")
	display.set_border(display.WHITE)

	icon = Image.open(icon_dir+'thunderstorm.png', mode='r').convert('P')
	img = Image.new('P', (display.WIDTH, display.HEIGHT), (255, 255, 255))
	draw = ImageDraw.Draw(img)

	font = ImageFont.truetype("DejaVuSans.ttf", 12)

	loc = get_location()

	message = loc[0]

	cur_time = (datetime.now()).strftime("%I:%M %p")

	w, h = font.getsize(cur_time)

	draw.line([(0, 22), (display.WIDTH, 22)], fill=(0, 0, 0))
	x = (display.WIDTH - w)

	draw.text((22, 2), message, display.RED, font)
	draw.text((x, 2), cur_time, display.RED, font)

	Image.Image.paste(img, icon, (0, 50))

	# Location Icon
	icon = Image.open('/home/pi/Documents/projects/python/E-Paper/E-Paper-Notification-Center/E-Paper-Notification-Center/icons/location.png', mode='r').convert('P')
	icon = icon.resize((20, 20))
	Image.Image.paste(img, icon, (0, 0))

	draw.text((130, 30), "Temperature:\n    Min:\n    Max:\nPressure:\nHumidity:\nVisibility:\nWind:\n    Speed:\n    Direction:\n    Gust:", display.BLACK, font)

#	img.show()
	display.set_image(img)
	display.show()


