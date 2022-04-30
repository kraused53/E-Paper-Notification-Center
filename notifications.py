from location import get_location
from PIL import Image, ImageFont, ImageDraw
from inky import InkyWHAT

if __name__ == '__main__':
	display = InkyWHAT("red")
	display.set_border(display.WHITE)

	icon = Image.open('./icons/test.png', mode='r').convert('P')
	img = Image.new('P', (display.WIDTH, display.HEIGHT), (255, 255, 255))
	draw = ImageDraw.Draw(img)

	font = ImageFont.truetype("DejaVuSans.ttf", 12)

	loc = get_location()

	message = loc[0]
	print(loc[1])
	latlong = '[' + str(loc[1][0]) + ', ' + str(loc[1][1]) + ']'

	w, h = font.getsize(latlong)

	draw.line([(0, 22), (display.WIDTH, 22)], fill=(0, 0, 0))
	x = (display.WIDTH - w)

	draw.text((22, 2), message, display.RED, font)
	draw.text((x, 2), latlong, display.RED, font)

	Image.Image.paste(img, icon, (0, 30))

	# Location Icon
	icon = Image.open('./icons/location.png', mode='r').convert('P')
	icon = icon.resize((20, 20))
	Image.Image.paste(img, icon, (0, 0))

	draw.text((130, 30), "Temperature:\n    Min:\n    Max:\nPressure:\nHumidity:\nVisibility:\nWind:\n    Speed:\n    Direction:\n    Gust:", display.BLACK, font)

	img.show()
	display.set_image(img)
	display.show()


"""

	# Day 1
	icon = Image.open('./icons/clouds.png', mode='r').convert('P')
	icon = icon.resize((50, 50))
	Image.Image.paste(img, icon, (25, display.HEIGHT-50))

	# Day 2
	icon = Image.open('./icons/fog.png', mode='r').convert('P')
	icon = icon.resize((50, 50))
	Image.Image.paste(img, icon, (25+50*1, display.HEIGHT-50))

	# Day 3
	icon = Image.open('./icons/rain.png', mode='r').convert('P')
	icon = icon.resize((50, 50))
	Image.Image.paste(img, icon, (25+50*2, display.HEIGHT-50))

	# Day 4
	icon = Image.open('./icons/light_rain.png', mode='r').convert('P')
	icon = icon.resize((50, 50))
	Image.Image.paste(img, icon, (25+50*3, display.HEIGHT-50))

	# Day 5
	icon = Image.open('./icons/thunder.png', mode='r').convert('P')
	icon = icon.resize((50, 50))
	Image.Image.paste(img, icon, (25+50*4, display.HEIGHT-50))

	# Day 6
	icon = Image.open('./icons/thunderstorm.png', mode='r').convert('P')
	icon = icon.resize((50, 50))
	Image.Image.paste(img, icon, (25+50*5, display.HEIGHT-50))

	# Day 7
	icon = Image.open('./icons/moon.png', mode='r').convert('P')
	icon = icon.resize((50, 50))
	Image.Image.paste(img, icon, (25+50*6, display.HEIGHT-50))

	img.show()
	display.set_image(img)
	display.show()
"""
