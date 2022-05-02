from location import get_location
from openweather import get_current_weather
from PIL import Image, ImageFont, ImageDraw
from inky import InkyWHAT
from datetime import datetime

icon_dir = '/home/pi/Documents/projects/python/E-Paper/E-Paper-Notification-Center/E-Paper-Notification-Center/icons/'

if __name__ == '__main__':
	display = InkyWHAT("red")
	display.set_border(display.WHITE)

	img = Image.new('RGBA', (400, 300), (255, 255, 255))
	icon = Image.open('./icons/thunderstorm.png').convert('RGBA')

	pixels = icon.load()

	if icon.mode == 'RGBA':
		for y in range(icon.size[1]):
			for x in range(icon.size[0]):
				if pixels[x, y][3] < 255:
					pixels[x, y] = (255, 255, 255, 255)

	img.paste(icon, (0, 0))

	pal_img = Image.new('P', (1, 1))
	pal_img.putpalette((255, 255, 255, 0, 0, 0, 255, 0, 0) + (0, 0, 0) * 252)

	img = img.convert('RGB').quantize(palette=pal_img)

	display.set_image(img)
	display.show()
'''
	# Load test icon
	icon = Image.open(icon_dir+'thunderstorm.png')
	#img = Image.open(icon_dir+'background.png')
	img = Image.new('RGBA', (400, 300), (255, 255, 255))

	draw = ImageDraw.Draw(img)

	Image.Image.paste(img, icon, (0, 50))

	font = ImageFont.truetype("DejaVuSans.ttf", 16)

	loc = get_location()

#	weather_data = get_current_weather(loc[1])
#	print(weather_data)
	weather_data = []
	# Extract current temp
	if 'main' in weather_data:
		if 'temp' in weather_data['main']:
			temp = str(weather_data['main']['temp']) + ' °F'
		else:
			temp = 'ERR'
	else:
			temp = 'ERR'

#	img.save('test.png')
	font = ImageFont.truetype("DejaVuSans.ttf", 24)
	draw.text((130, 75), temp, display.BLACK, font)

	message = loc[0]

	cur_time = (datetime.now()).strftime("%I:%M %p")

	w, h = font.getsize(cur_time)

	draw.line([(0, 22), (display.WIDTH, 22)], fill=(0, 0, 0))
	x = (display.WIDTH - w)

	font = ImageFont.truetype("DejaVuSans.ttf", 16)

	draw.text((22, 2), message, display.RED, font)
	draw.text((x, 2), cur_time, display.RED, font)

	# Location Icon
	icon = Image.open('/home/pi/Documents/projects/python/E-Paper/E-Paper-Notification-Center/E-Paper-Notification-Center/icons/location.png', mode='r').convert('P')
	icon = icon.resize((20, 20))
	Image.Image.paste(img, icon, (0, 0))

#	img.show()

	pal_img = Image.new('P', (1, 1))
	pal_img.putpalette((255, 255, 255, 0, 0, 0, 255, 0, 0) + (0, 0, 0)*252)

	img.convert('RGB').quantize(palette=pal_img)
	display.set_image(img)
	display.show()


'''
