import geocoder

def get_location():
	return geocoder.ip('me')


if __name__ == '__main__':
	g = geocoder.ip('me')
	print(g.state)
