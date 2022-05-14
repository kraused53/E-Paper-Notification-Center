from location import get_location
from openweather import get_current_weather
from PIL import Image, ImageFont, ImageDraw
from inky import InkyWHAT
from datetime import datetime

icon_dir = '/home/pi/Documents/projects/python/E-Paper/E-Paper-Notification-Center/E-Paper-Notification-Center/icons/'


'''
    Class to store weather information
'''
class WeatherData:
    def __init__(self, weather_json):
        # Create variables for current weather data
        self.air_temperature = None
        self.humidity = None
        self.cloud_cover = None
        self.image = None
        self.time = None
        self.sunrise = None
        self.sunset = None
        # Create Variables for weekly forecast
        self.week_min_temps = None
        self.week_max_temps = None
        self.week_icons = None
        
        # Fill variables
        if 'current' in weather_json:
            if 'dt' in weather_json['current']:
                self.time = int(weather_json['current']['dt'])
            if 'sunrise' in weather_json['current']:
                self.sunrise = int(weather_json['current']['sunrise'])
            if 'sunset' in weather_json['current']:
                self.sunset = int(weather_json['current']['sunset'])
            if 'temp' in weather_json['current']:
                self.air_temperature = str(weather_json['current']['temp'])
            if 'humidity' in weather_json['current']:
                self.humidity = int(weather_json['current']['humidity'])
            if 'clouds' in weather_json['current']:
                self.cloud_cover = int(weather_json['current']['clouds'])
            if 'weather' in weather_json['current']:
                if 'icon' in weather_json['current']['weather'][0]:
                    self.image = str(weather_json['current']['weather'][0]['icon']) + '@2x.png'
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


'''
    Lay out Weekly forecast
'''
def weekly_forecast(data, screen):
    return screen


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
	weather_data = WeatherData(get_current_weather(loc[1]))

	'''
		Process Weather Data
	'''
	# Extract current temp
	if weather_data.air_temperature is None:
		cur_temp = 'N/A'
	else:
		cur_temp = str(weather_data.air_temperature)

	# Extract humidity data
	if weather_data.humidity is None:
		cur_hum = 'N/A'
	else:
		cur_hum = str(weather_data.humidity)

	# Extract Cloud Cover
	if weather_data.cloud_cover is None:
		cur_clouds = 'N/A'
	else:
		cur_clouds = str(weather_data.cloud_cover)
	
	# Create and format weather information block
	data_block = '''{0} °F
{1}% humidity
{2}% cloud cover'''.format(cur_temp, cur_hum, cur_clouds)

	# Select icon to display
	icon_name = weather_data.image

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
	# Place data block
	font = ImageFont.truetype("LiberationMono-Regular.ttf", 24)
	draw.text((130, 55), data_block, display.BLACK, font)
	font = ImageFont.truetype("LiberationMono-Regular.ttf", 16)


	'''
		Check to see if it is Friday or Saturday
	'''
	# Get day of week
	weekday = datetime.today().weekday()
	# Check for Friday or Saturday
	if (weekday == 4) or (weekday == 5):
		# Make sure that all necessary info is available
		if weather_data.time is not None:
			if weather_data.sunset is not None:
				if weather_data.sunrise is not None:
					icon = None

					# If Friday and after sunset
					if (weekday == 4) and (weather_data.time >= weather_data.sunset):
						# Open Shabbat Icon
						icon = Image.open(icon_dir+'Shabbat.png').convert('RGBA')
						# Remove transparent background from icon
						pixels = convert_icon_background(icon)
					# If Saturday and before sunset
					elif (weekday == 5) and (weather_data.time < weather_data.sunset):
						# Open Shabbat Icon
						icon = Image.open(icon_dir+'Shabbat.png').convert('RGBA')
						# Remove transparent background from icon
						pixels = convert_icon_background(icon)
					# If Saturday and less than 2 hours after sunset
					elif (weekday == 5) and ((weather_data.time - weather_data.sunset) <= 3600):
						# Open Havdalah Icon
						icon = Image.open(icon_dir+'Havdalah.png').convert('RGBA')
						# Remove transparent background from icon
						pixels = convert_icon_background(icon)

					if icon is not None:
						# Paste Candle Icon
						Image.Image.paste(img, icon, (display.WIDTH-50, 50))


    # Add Weekly forecast to screen
	draw = weekly_forecast(weather_data, draw)

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
