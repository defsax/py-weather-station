import weatherhat

class WeatherHat():
  def __init__(self):
    super(WeatherHat, self).__init__()
    self.sensors = weatherhat.WeatherHAT()
