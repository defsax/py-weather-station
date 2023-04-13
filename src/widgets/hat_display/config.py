import pathlib
import yaml

class Config:
  """Class to hold weather UI settings."""
  def __init__(self, settings_file="settings.yml"):
    self._file = pathlib.Path(settings_file)

    self._last_save = None

    # Wind Settings
    self.wind_trails = True

    # BME280 Settings
    self.minimum_temperature = -10
    self.maximum_temperature = 40

    self.minimum_pressure = 1000
    self.maximum_pressure = 1100

    self.minimum_lux = 100
    self.maximum_lux = 1000

    self.minimum_rain_mm = 0
    self.maximum_rain_mm = 10

    self.minimum_wind_ms = 0
    self.maximum_wind_ms = 40

    self.load()

  def load(self):
    if not self._file.is_file():
      return False

    try:
      self._config = yaml.safe_load(open(self._file))
    except yaml.parser.ParserError as e:
      raise yaml.parser.ParserError(
          "Error parsing settings file: {} ({})".format(self._file, e)
      )

  @property
  def _config(self):
    options = {}
    for k, v in self.__dict__.items():
      if not k.startswith("_"):
        options[k] = v
    return options

  @_config.setter
  def _config(self, config):
    for k, v in self.__dict__.items():
      if k in config:
        setattr(self, k, config[k])
