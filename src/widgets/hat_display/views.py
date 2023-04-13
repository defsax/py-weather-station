import math
import weatherhat
from PIL import Image, ImageDraw, ImageFont
from fonts.ttf import ManropeBold as UserFont

COLOR_WHITE = (255, 255, 255)
COLOR_BLUE = (31, 137, 251)
COLOR_GREEN = (99, 255, 124)
COLOR_YELLOW = (254, 219, 82)
COLOR_RED = (247, 0, 63)
COLOR_BLACK = (0, 0, 0)
COLOR_GREY = (100, 100, 100)


class View:
    def __init__(self, image):
        self._image = image
        self._draw = ImageDraw.Draw(image)

        self.font_large = ImageFont.truetype(UserFont, 80)
        self.font = ImageFont.truetype(UserFont, 50)
        self.font_medium = ImageFont.truetype(UserFont, 44)
        self.font_small = ImageFont.truetype(UserFont, 28)

    @property
    def canvas_width(self):
        return self._image.size[0]

    @property
    def canvas_height(self):
        return self._image.size[1]

    def button_a(self):
        return False

    def button_b(self):
        return False

    def button_x(self):
        return False

    def button_y(self):
        return False

    def update(self):
        pass

    def render(self):
        self.clear()

    def clear(self):
        self._draw.rectangle((0, 0, self.canvas_width, self.canvas_height), (0, 0, 0))


class SensorView(View):
    title = ""
    GRAPH_BAR_WIDTH = 20

    def __init__(self, image, sensordata, settings=None):
        View.__init__(self, image)
        self._data = sensordata
        self._settings = settings

    def blend(self, a, b, factor):
        blend_b = factor
        blend_a = 1.0 - factor
        return tuple([int((a[i] * blend_a) + (b[i] * blend_b)) for i in range(3)])

    def heading(self, data, units):
        if data < 100:
            data = "{:0.1f}".format(data)
        else:
            data = "{:0.0f}".format(data)

        tw, th = self._draw.textsize(data, self.font_large)

        self._draw.text(
            (0, 32), data, font=self.font_large, fill=COLOR_WHITE, anchor="lm"
        )

        self._draw.text(
            (tw, 64), units, font=self.font_medium, fill=COLOR_WHITE, anchor="lb"
        )

    def footer(self, label):
        self._draw.text(
            (int(self.canvas_width / 2), self.canvas_height - 30),
            label,
            font=self.font_medium,
            fill=COLOR_GREY,
            anchor="mm",
        )

    def graph(
        self,
        values,
        graph_x=0,
        graph_y=0,
        width=None,
        height=None,
        vmin=0,
        vmax=1.0,
        bar_width=2,
        colors=None,
    ):
        if not len(values):
            return

        if width is None:
            width = self.canvas_width

        if height is None:
            height = self.canvas_height

        if colors is None:
            #         Blue          Teal           Green        Yellow         Red
            colors = [
                (0, 0, 255),
                (0, 255, 255),
                (0, 255, 0),
                (255, 255, 0),
                (255, 0, 0),
            ]

        vrange = vmax - vmin
        vstep = float(height) / vrange

        if vmin >= 0:
            midpoint_y = height
        else:
            midpoint_y = vmax * vstep
            self._draw.line(
                (graph_x, graph_y + midpoint_y, graph_x + width, graph_y + midpoint_y),
                fill=COLOR_GREY,
            )

        max_values = int(width / bar_width)

        values = [entry.value for entry in values[-max_values:]]

        for i, v in enumerate(values):
            v = min(vmax, max(vmin, v))

            offset_y = graph_y

            if vmin < 0:
                bar_height = midpoint_y * float(v) / float(vmax)
            else:
                bar_height = midpoint_y * float(v - vmin) / float(vmax - vmin)

            if v < 0:
                offset_y += midpoint_y
                bar_height = (height - midpoint_y) * float(abs(v)) / abs(vmin)

            color = float(v - vmin) / float(vmax - vmin) * (len(colors) - 1)
            color_idx = int(
                color
            )  # The integer part of color becomes our index into the colors array
            blend = (
                color - color_idx
            )  # The fractional part forms the blend amount between the two colours
            bar_color = colors[color_idx]
            if color_idx < len(colors) - 1:
                bar_color = self.blend(colors[color_idx], colors[color_idx + 1], blend)
                bar_color = bar_color

            x = i * bar_width

            if v < 0:
                self._draw.rectangle(
                    (
                        graph_x + x,
                        offset_y,
                        graph_x + x + int(bar_width / 2),
                        offset_y + bar_height,
                    ),
                    fill=bar_color,
                )
            else:
                self._draw.rectangle(
                    (
                        graph_x + x,
                        offset_y + midpoint_y - bar_height,
                        graph_x + x + int(bar_width / 2),
                        offset_y + midpoint_y,
                    ),
                    fill=bar_color,
                )


class MainView(SensorView):
    """Main Overview.

    Displays weather summary and navigation hints.

    """

    title = "Overview"

    def draw_info(
        self,
        x,
        y,
        color,
        label,
        data,
        desc,
        right=False,
        vmin=0,
        vmax=20,
        graph_mode=False,
    ):
        w = 200
        o_x = 0 if right else 40

        if graph_mode:
            vmax = max(vmax, max([h.value for h in data]))  # auto ranging?
            self.graph(
                data,
                x + o_x + 30,
                y + 20,
                180,
                64,
                vmin=vmin,
                vmax=vmax,
                bar_width=20,
                colors=[color],
            )
        else:
            if type(data) is list:
                if len(data) > 0:
                    data = data[-1].value
                else:
                    data = 0

            if data < 100:
                data = "{:0.1f}".format(data)
            else:
                data = "{:0.0f}".format(data)

            self._draw.text(
                (x + w + o_x, y + 20 + 32),  # Position is the right, center of the text
                data,
                font=self.font_large,
                fill=color,
                anchor="rm",  # Using "rm" stops text jumping vertically
            )

        self._draw.text(
            (x + w + o_x, y + 90 + 40),
            desc,
            font=self.font,
            fill=COLOR_WHITE,
            anchor="rb",
        )
        label_img = Image.new("RGB", (130, 40))
        label_draw = ImageDraw.Draw(label_img)
        label_draw.text(
            (0, 40) if right else (0, 0),
            label,
            font=self.font_medium,
            fill=COLOR_GREY,
            anchor="lb" if right else "lt",
        )
        label_img = label_img.rotate(90, expand=True)
        if right:
            self._image.paste(label_img, (x + w, y))
        else:
            self._image.paste(label_img, (x, y))

    def render(self):
        SensorView.render(self)
        self.render_graphs()

    def render_graphs(self, graph_mode=False):
        # ~ self.draw_info(0, 0, (20, 20, 220), "RAIN", self._data.rain_mm_sec.history(), "mm/s", vmax=self._settings.maximum_rain_mm, graph_mode=graph_mode)
        # ~ self.draw_info(0, 150, (20, 20, 220), "PRES", self._data.pressure.history(), "hPa", graph_mode=graph_mode)
        self.draw_info(
            0,
            300,
            (20, 100, 220),
            "TEMP",
            self._data.temperature.history(),
            "°C",
            graph_mode=graph_mode,
            vmin=self._settings.minimum_temperature,
            vmax=self._settings.maximum_temperature,
        )

        x = int(self.canvas_width / 2)
        self.draw_info(
            x,
            0,
            (220, 20, 220),
            "WIND",
            self._data.wind_speed.history(),
            "m/s",
            right=True,
            graph_mode=graph_mode,
        )
        self.draw_info(
            x,
            150,
            (220, 100, 20),
            "LIGHT",
            self._data.lux.history(),
            "Wm2",
            right=True,
            graph_mode=graph_mode,
        )
        self.draw_info(
            x,
            300,
            (10, 10, 220),
            "HUM",
            self._data.relative_humidity.history(),
            "%rh",
            right=True,
            graph_mode=graph_mode,
        )


class MainViewGraph(MainView):
    title = "Overview: Graphs"

    def render(self):
        SensorView.render(self)
        self.render_graphs(graph_mode=True)


class WindDirectionView(SensorView):
    """Wind Direction."""

    title = "Wind"
    metric = "m/sec"

    def __init__(self, image, sensordata, settings=None):
        SensorView.__init__(self, image, sensordata, settings)

    def render(self):
        SensorView.render(self)
        ox = self.canvas_width / 2
        oy = 40 + ((self.canvas_height - 60) / 2)
        needle = self._data.needle
        speed_ms = self._data.wind_speed.average(60)
        # gust_ms = self._data.wind_speed.gust()
        compass_direction = self._data.wind_direction.average_compass()

        radius = 80
        speed_max = 4.4  # m/s
        speed = min(speed_ms, speed_max)
        speed /= float(speed_max)

        arrow_radius_min = 20
        arrow_radius_max = 60
        arrow_radius = (
            speed * (arrow_radius_max - arrow_radius_min)
        ) + arrow_radius_min
        arrow_angle = math.radians(130)

        tx, ty = ox + math.sin(needle) * (radius - arrow_radius), oy - math.cos(
            needle
        ) * (radius - arrow_radius)
        ax, ay = ox + math.sin(needle) * (radius - arrow_radius), oy - math.cos(
            needle
        ) * (radius - arrow_radius)

        arrow_xy_a = (
            ax + math.sin(needle - arrow_angle) * arrow_radius,
            ay - math.cos(needle - arrow_angle) * arrow_radius,
        )
        arrow_xy_b = (
            ax + math.sin(needle) * arrow_radius,
            ay - math.cos(needle) * arrow_radius,
        )
        arrow_xy_c = (
            ax + math.sin(needle + arrow_angle) * arrow_radius,
            ay - math.cos(needle + arrow_angle) * arrow_radius,
        )

        # Compass red end
        self._draw.line((ox, oy, tx, ty), (255, 0, 0), 5)

        # Compass white end
        """
        self._draw.line((
            ox,
            oy,
            ox + math.sin(needle - math.pi) * radius,
            oy - math.cos(needle - math.pi) * radius
        ), (255, 255, 255), 5)
        """

        self._draw.polygon([arrow_xy_a, arrow_xy_b, arrow_xy_c], fill=(255, 0, 0))

        if self._settings.wind_trails:
            trails = 40
            trail_length = len(self._data.needle_trail)
            for i, p in enumerate(self._data.needle_trail):
                # r = radius
                r = radius + trails - (float(i) / trail_length * trails)
                x = ox + math.sin(p) * r
                y = oy - math.cos(p) * r

                self._draw.ellipse(
                    (x - 2, y - 2, x + 2, y + 2), (int(255 / trail_length * i), 0, 0)
                )

        radius += 60
        for direction, name in weatherhat.wind_degrees_to_cardinal.items():
            p = math.radians(direction)
            x = ox + math.sin(p) * radius
            y = oy - math.cos(p) * radius

            name = "".join([word[0] for word in name.split(" ")])
            tw, th = self._draw.textsize(name, font=self.font_small)
            x -= tw / 2
            y -= th / 2
            self._draw.text((x, y), name, font=self.font_small, fill=COLOR_GREY)

        self.heading(speed_ms, self.metric)
        self.footer(self.title.upper())

        direction_text = "".join([word[0] for word in compass_direction.split(" ")])

        self._draw.text(
            (self.canvas_width, 32),
            direction_text,
            font=self.font_large,
            fill=COLOR_WHITE,
            anchor="rm",
        )


class WindSpeedView(SensorView):
    """Wind Speed."""

    title = "WIND"
    metric = "m/s"

    def render(self):
        SensorView.render(self)
        self.heading(self._data.wind_speed.latest().value, self.metric)
        self.footer(self.title.upper())

        self.graph(
            self._data.wind_speed.history(),
            graph_x=4,
            graph_y=70,
            width=self.canvas_width,
            height=self.canvas_height - 130,
            vmin=self._settings.minimum_wind_ms,
            vmax=self._settings.maximum_wind_ms,
            bar_width=self.GRAPH_BAR_WIDTH,
        )


class RainView(SensorView):
    """Rain."""

    title = "Rain"
    metric = "mm/s"

    def render(self):
        SensorView.render(self)
        self.heading(self._data.rain_mm_sec.latest().value, self.metric)
        self.footer(self.title.upper())

        self.graph(
            self._data.rain_mm_sec.history(),
            graph_x=4,
            graph_y=70,
            width=self.canvas_width,
            height=self.canvas_height - 130,
            vmin=self._settings.minimum_rain_mm,
            vmax=self._settings.maximum_rain_mm,
            bar_width=self.GRAPH_BAR_WIDTH,
        )


class TemperatureView(SensorView):
    """Temperature."""

    title = "TEMP"
    metric = "°C"

    def render(self):
        SensorView.render(self)
        self.heading(self._data.temperature.latest().value, self.metric)
        self.footer(self.title.upper())

        self.graph(
            self._data.temperature.history(),
            graph_x=4,
            graph_y=70,
            width=self.canvas_width,
            height=self.canvas_height - 130,
            vmin=self._settings.minimum_temperature,
            vmax=self._settings.maximum_temperature,
            bar_width=self.GRAPH_BAR_WIDTH,
        )


class LightView(SensorView):
    """Light."""

    title = "Light"
    metric = "lux"

    def render(self):
        SensorView.render(self)
        self.heading(self._data.lux.latest().value, self.metric)
        self.footer(self.title.upper())

        self.graph(
            self._data.lux.history(int(self.canvas_width / self.GRAPH_BAR_WIDTH)),
            graph_x=4,
            graph_y=70,
            width=self.canvas_width,
            height=self.canvas_height - 130,
            vmin=self._settings.minimum_lux,
            vmax=self._settings.maximum_lux,
            bar_width=self.GRAPH_BAR_WIDTH,
        )


class PressureView(SensorView):
    """Pressure."""

    title = "PRESSURE"
    metric = "hPa"

    def render(self):
        SensorView.render(self)
        self.heading(self._data.pressure.latest().value, self.metric)
        self.footer(self.title.upper())

        self.graph(
            self._data.pressure.history(int(self.canvas_width / self.GRAPH_BAR_WIDTH)),
            graph_x=4,
            graph_y=70,
            width=self.canvas_width,
            height=self.canvas_height - 130,
            vmin=self._settings.minimum_pressure,
            vmax=self._settings.maximum_pressure,
            bar_width=self.GRAPH_BAR_WIDTH,
        )


class HumidityView(SensorView):
    """Pressure."""

    title = "Humidity"
    metric = "%rh"

    def render(self):
        SensorView.render(self)
        self.heading(self._data.relative_humidity.latest().value, self.metric)
        self.footer(self.title.upper())

        self.graph(
            self._data.relative_humidity.history(
                int(self.canvas_width / self.GRAPH_BAR_WIDTH)
            ),
            graph_x=4,
            graph_y=70,
            width=self.canvas_width,
            height=self.canvas_height - 130,
            vmin=0,
            vmax=100,
            bar_width=self.GRAPH_BAR_WIDTH,
        )
