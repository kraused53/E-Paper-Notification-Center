import geocoder

def get_location():
	g = geocoder.ip('me')
	data = []
	data.append(str(g.city+', '+g.state))
	data.append(g.latlng)
	return data


if __name__ == '__main__':
	print(get_location())
