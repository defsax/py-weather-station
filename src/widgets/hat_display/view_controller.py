import RPi.GPIO as GPIO

class ViewController:
  def __init__(self, views):
    self.BUTTONS = [5, 6, 16, 24]
    
    self.views = views
    self._current_view = 0
    self._current_subview = 0

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(self.BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    for pin in self.BUTTONS:
      GPIO.add_event_detect(pin, GPIO.FALLING, self.handle_button, bouncetime=200)

  def handle_button(self, pin):
    index = self.BUTTONS.index(pin)
    label = LABELS[index]

    if label == "A":  # Select View
      self.button_a()

    if label == "B":
      self.button_b()

    if label == "X":
      self.button_x()

    if label == "Y":
      self.button_y()

  @property
  def home(self):
    return self._current_view == 0 and self._current_subview == 0

  def next_subview(self):
    view = self.views[self._current_view]
    if isinstance(view, tuple):
      self._current_subview += 1
      self._current_subview %= len(view)

  def next_view(self):
    self._current_subview = 0
    self._current_view += 1
    self._current_view %= len(self.views)

  def prev_view(self):
    self._current_subview = 0
    self._current_view -= 1
    self._current_view %= len(self.views)

  def get_current_view(self):
    view = self.views[self._current_view]
    if isinstance(view, tuple):
      view = view[self._current_subview]

    return view

  @property
  def view(self):
    return self.get_current_view()

  def update(self):
    self.view.update()

  def render(self):
    self.view.render()

  def button_a(self):
    if not self.view.button_a():
          self.next_view()

  def button_b(self):
    self.view.button_b()

  def button_x(self):
    if not self.view.button_x():
      self.next_subview()
      return True
    return True

  def button_y(self):
    return self.view.button_y()
