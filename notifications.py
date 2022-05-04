\from location import get_location
from openweather import get_current_weather
from PIL import Image, ImageFont, ImageDraw
from inky import InkyWHAT
from datetime import datetime

icon_dir = '/home/pi/Documents/projects/python/E-Paper/E-Paper-Notification-Center/E-Paper-Notification-Center/icons/'


'''
	Takes a .PNG PIL object and returns the image with all transparent pixels filled in
'''
def convert_icon_background(icon):
	# Break image into individual pixels
	pix = icon.load()

	# If given object is a .PNG file
	if icon.mode == 'RGBA':
		# Check every pixel in the image
		for y in range(icon.size[1]):
			for x in range(icon.size[0]):
				# If pixel has a transparency value that is anything other that solid
				if pix[x, y][3] < 255:
					# Convert the pixel to a solid white one
					pix[x, y] = (255, 255, 255, 255)
	# Return the adjusted image pixels
	return pix


'''
	Takes a current weather dataset and returns a file name for the correct icon
'''
def select_icon(weather_data):
	# If function cannot select the proper file name, function will return None
	file_name = None

	'''
		Make sure that ALL data is present BEFORE trying to access it
		If any data is missing, do not display icon
	'''
	# Check for current time
	if 'dt' in weather_data:
		# Check for sys data entry, contains sunrise/sunset data
		if 'sys' in weather_data:
			# Check for weather id data entry
			if ('weather' in weather_data):
				# Extract time stamps
				dt = int(weather_data['dt'])
				sr = int(weather_data['sys']['sunrise'])
				ss = int(weather_data['sys']['sunset'])
				id = int(weather_data['weather'][0]['id'])

			'''
				First, check for icons that do not change depending on the time of day
			'''
			# Thunderstorm (id=2xx)
			if (id >= 200) and (id < 300):
				file_name = '11d@2x.png'
			# Drizzle (id=3xx)
			elif (id >= 300) and (id < 400):
				file_name = '09d@2x.png'
			# Freezing rain (id == 511)
			elif id == 511:
				file_name = '13d@2x.png'
			# Rain Showers
			elif (id > 511) and (id < 600):
				file_name = '09d@2x.png'
			# Snow (id=6xx)
			elif (id >= 600) and (id < 700):
				file_name = '13n@2x.png'
			# Fog (id=7xx)
			elif (id >= 700) and (id < 800):
				file_name = '50d@2x.png'
			# Scattered Clouds
			elif id == 802:
				file_name = '03d@2x.png'
			# Mostly Clouds
			elif (id == 803) or (id == 804):
				file_name = '04n@2x.png'
			#check for time-dependant icons
			# Daytime
			elif (dt > sr) and (dt < ss):
				# Clear (id=800)
				if id == 800:
					file_name = '01d@2x.png'
				# Few Clouds
				elif id == 801:
					file_name = '02d@2x.png'
				# Rain
				else:
					file_name = '10d@2x.png'
			# Nighttime
			else:
				# Clear (id=800)
				if id == 800:
					file_name = '01n@2x.png'
				# Few Clouds
				elif id == 801:
					file_name = '02n@2x.png'
				# Rain
				else:
					file_name = '10n@2x.png'

	# Return file name
	return file_name


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
	# Check that current weather is available
	if 'main' in weather_data:
		# Extract temperature data
		if 'temp' in weather_data['main']:
			cur_temp = str(weather_data['main']['temp'])
		else:
			cur_temp = 'N/A'

		# Extract air pressure data
		if 'pressure' in weather_data['main']:
			cur_press = str(weather_data['main']['pressure'])
		else:
			cur_press = 'N/A'

		# Extract humidity data
		if 'humidity' in weather_data['main']:
			cur_hum = str(weather_data['main']['humidity'])
		else:
			cur_hum = 'N/A'
	else:
		cur_temp = 'ERR'
		cur_press = 'ERR'
		cur_hum = 'ERR'

	# Extract Cloud Cover
	if 'clouds' in weather_data:
		cur_clouds = str(weather_data['clouds']['all'])
	else:
		cur_clouds = 'N/A'
	# Extract Visibility
	if 'visibility' in weather_data:
		cur_vis = str(weather_data['visibility'])
	else:
		cur_vis = 'N/A'
	# Extract Wind Speed
	if 'wind' in weather_data:
		cur_ws = str(weather_data['wind']['speed'])
	else:
		cur_ws = 'N/A'

	# Create and format weather information block
	data_block = '''{0} °F air temperature
{1}% humidity
{2} hPa air pressure
{3}% cloud cover
{4}m visibility
{5}mph winds'''.format(cur_temp, cur_hum, cur_press, cur_clouds, cur_vis, cur_ws)

	# Select icon to display
	icon_name = select_icon(weather_data)

	'''
		Set up background and image manipulation classes
	'''
	# Create Empty Image to display to E-Paper
	img = Image.new('RGBA', (400, 300), (255, 255, 255))
	# Create ImageDraw Class to draw / write on img
	draw = ImageDraw.Draw(img)
	# Create font for future text objects
	font = ImageFont.truetype("LiberationMono-Regular.ttf", 16)

	'''
		Open, process and paste a weather icon
	'''
	# If an icon was selected earlier
	if icon_name is not None:
		# Open Random Weather Icon
		icon = Image.open(icon_dir+icon_name).convert('RGBA')
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
		Place current weather
	'''
	# Change font size
#	font = ImageFont.truetype("DejaVuSans.ttf", 24)
	# Place current temp
#	draw.text((130, 50), cur_temp, display.BLACK, font)
#	w, h = font.getsize(cur_temp)
	# Place current humidity
#	draw.text((130, (50+h+2)), cur_hum, display.BLACK, font)
	# Place current pressure
#	draw.text((130, (50+h+h+2+2)), cur_press, display.BLACK, font)
	# Place data block
	draw.text((130, 50), data_block, display.BLACK, font)


	'''
		Check to see if it is Friday or Saturday
	'''
	# Get day of week
	weekday = datetime.today().weekday()
	# Check for Friday or Saturday
	if (weekday == 4) or (weekday == 5):
		# Check for current time
		if 'dt' in weather_data:
			# Check for sys data entry, contains sunrise/sunset data
			if 'sys' in weather_data:
				# Check for weather id data entry
				if ('weather' in weather_data):
					# Extract time stamps
					dt = int(weather_data['dt'])
					sr = int(weather_data['sys']['sunrise'])
					ss = int(weather_data['sys']['sunset'])

					icon = None

					# If Friday and after sunset
					if (weekday == 4) and (dt >= ss):
						# Open Shabbat Icon
						icon = Image.open(icon_dir+'Shabbat.png').convert('RGBA')
						# Remove transparent background from icon
						pixels = convert_icon_background(icon)
					# If Saturday and before sunset
					elif (weekday == 5) and (dt < ss):
						# Open Shabbat Icon
						icon = Image.open(icon_dir+'Shabbat.png').convert('RGBA')
						# Remove transparent background from icon
						pixels = convert_icon_background(icon)
					# If Saturday and less than 2 hours after sunset
					elif (weekday == 5) and ((dt - ss) <= 3600):
						# Open Havdalah Icon
						icon = Image.open(icon_dir+'Havdalah.png').convert('RGBA')
						# Remove transparent background from icon
						pixels = convert_icon_background(icon)

					if icon is not None:
						# Paste Candle Icon
						Image.Image.paste(img, icon, (display.HEIGHT - 50, 0))


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
