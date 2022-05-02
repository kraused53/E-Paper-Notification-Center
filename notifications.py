from location import get_location
from openweather import get_current_weather
from PIL import Image, ImageFont, ImageDraw
from inky import InkyWHAT
from datetime import datetime

icon_dir = '/home/pi/Documents/projects/python/E-Paper/E-Paper-Notification-Center/E-Paper-Notification-Center/icons/'


def convert_icon_background(icon):
	pix = icon.load()

	if icon.mode == 'RGBA':
		for y in range(icon.size[1]):
			for x in range(icon.size[0]):
				if pix[x, y][3] < 255:
					pix[x, y] = (255, 255, 255, 255)

	return pix


# Runs when notifications.py is run as main
if __name__ == '__main__':
	display = InkyWHAT("red")
	display.set_border(display.WHITE)

	'''
		Gather location and weather data
	'''
	# Use current IP address to get rough location
	loc = get_location()
	# OpenWeatherAPI to get weather forecast for found location
	weather_data = get_current_weather(loc[1])

	'''
		Process Weather Data
	'''
	# Extract current temp
	if 'main' in weather_data:
		if 'temp' in weather_data['main']:
			cur_temp = str(weather_data['main']['temp']) + ' °F'
		else:
			cur_temp = 'ERR'
	else:
		cur_temp = 'ERR'

	'''
		Set up background and image manipulation classes
	'''
	# Create Empty Image to display to E-Paper
	img = Image.new('RGBA', (400, 300), (255, 255, 255))
	# Create ImageDraw Class to draw / write on img
	draw = ImageDraw.Draw(img)
	# Create font for future text objects
	font = ImageFont.truetype("DejaVuSans.ttf", 16)

	'''
		Open, process and paste a weather icon
	'''
	# Open Random Weather Icon
	icon = Image.open(icon_dir+'thunderstorm.png').convert('RGBA')
	# Remove transparent background from icon
	pixels = convert_icon_background(icon)
	# Paste Weather Icon onto image
	img.paste(icon, (0, 50))

	'''
		Open, process and paste location icon
	'''
	# Open location icon
	icon = Image.open(icon_dir+'location.png').convert('RGBA')
	# Scale icon to fit
	icon = icon.resize((20, 20))
	# Remove transparent background from icon
	pixels = convert_icon_background(icon)
	# Paste location icon
	Image.Image.paste(img, icon, (0, 0))

	'''
		Create and place title (Location and time)
	'''
	# Extract city name
	city_name = loc[0]
	# Generate time
	cur_time = (datetime.now()).strftime("%I:%M %p")
	# Get time string width
	w, h = font.getsize(cur_time)
	# Calculate Time starting x-position
	x = (display.WIDTH - w)
	# Place city Name
	draw.text((22, 2), city_name, display.RED, font)
	# Place Time
	draw.text((x, 2), cur_time, display.RED, font)

	'''
		Place current temperature
	'''
	# Change font size
	font = ImageFont.truetype("DejaVuSans.ttf", 24)
	# Place current temp
	draw.text((120, 75), cur_temp, display.BLACK, font)

	'''
		Aesthetic lines for clarity
	'''
	# Draw line to isolate title line
	draw.line([(0, 22), (display.WIDTH, 22)], fill=(0, 0, 0))

	pal_img = Image.new('P', (1, 1))
	pal_img.putpalette((255, 255, 255, 0, 0, 0, 255, 0, 0) + (0, 0, 0) * 252)

	img = img.convert('RGB').quantize(palette=pal_img)

	display.set_image(img)
	display.show()
