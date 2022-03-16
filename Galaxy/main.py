from kivy.config import Config

from menu import MenuWidget
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')
from kivy.app import App
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line, Quad
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import Clock
from kivy.core.window import Window
from kivy.lang import Builder

Builder.load_file('menu.kv')

class MainWidget(RelativeLayout):
    from transform import transform_perspective, transform_2D, transform
    from key_binds import _keyboard_closed, _on_keyboard_down, _on_keyboard_up, in_desktop, on_touch_down, on_touch_up
    from tiles import generate_tile_coordinate, get_tiles_coordinates, update_tiles
    from ship import init_ship, update_ship, ship_collision, ship_collision_tiles
    menu_widget = ObjectProperty()
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)
    menu_title = StringProperty("G   A   L   A   X   Y")
    menu_button_title = StringProperty("S T A R T")
    score_value = StringProperty()
    V_NB_Lines = 8
    H_NB_Lines = 8
    V_Lines_Spacing = 0.4
    H_Lines_Spacing = 0.2
    vertical_lines = []
    horizontal_lines = []
    speed = 1
    speed_x = 3
    current_speed_x = 0
    current_offset_y = 0
    current_offset_x = 0
    current_loop_y = 0
    NB_tiles = 8
    tiles = []
    ship = None
    ship_coordinates = [(0,0),(0,0),(0,0)]
    ship_width = 0.1
    ship_height = 0.035
    ship_base_y = 0.04
    tiles_coordinate = []
    start_index = -int(V_NB_Lines/2) + 1
    end_index = start_index + V_NB_Lines - 1
    state_game_over = False
    state_game_started = False

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.init_vertical_line()
        self.init_horizontal_line()
        self.init_tiles()
        self.init_ship()
        self.pre_fill_tile()
        self.generate_tile_coordinate()
        if self.in_desktop():
            self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
            self._keyboard.bind(on_key_down=self._on_keyboard_down)
            self._keyboard.bind(on_key_up=self._on_keyboard_up)
        Clock.schedule_interval(self.update, 1/60)
    
    def reset_game(self):
        self.current_speed_x = 0
        self.current_offset_y = 0
        self.current_offset_x = 0
        self.current_loop_y = 0
        self.tiles_coordinate = []
        self.score_value = 'S C O R E : 0'
        self.pre_fill_tile()
        self.generate_tile_coordinate()
        self.state_game_over = False

    def init_vertical_line(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.V_NB_Lines):
                self.vertical_lines.append(Line())

    def init_horizontal_line(self):
        with self.canvas:
            Color(1,1,1)
            for i in range(0, self.H_NB_Lines):
                self.horizontal_lines.append(Line())
    
    def init_tiles(self):
        with self.canvas:
            Color(1,1,1)
            for i in range(0, self.NB_tiles):
                self.tiles.append(Quad())

    def button_on_press(self):
        self.reset_game()
        self.state_game_started = True
        self.menu_widget.opacity = 0

    def pre_fill_tile(self):
        for i in range(0,10):
            self.tiles_coordinate.append((0,i))

    def get_line_x_from_index(self, index):
        central_line_x = int(self.width/2)
        spacing = int(self.V_Lines_Spacing*self.width)
        offset = index - 0.5
        line_x = central_line_x + offset*spacing + self.current_offset_x        
        return line_x

    def get_line_y_from_index(self, index):
        spacing_y = int(self.H_Lines_Spacing*self.height)
        line_y = index*spacing_y - self.current_offset_y
        return line_y

    def update_vertical_line(self):
        start_index = -int(self.V_NB_Lines/2) + 1
        for i in range(start_index, start_index + self.V_NB_Lines):
            line_x = self.get_line_x_from_index(i)
            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)
            self.vertical_lines[i].points = [x1, y1, x2, y2]

    def update_horizontal_line(self):
        xmin = self.get_line_x_from_index(self.start_index)
        xmax = self.get_line_x_from_index(self.end_index)
        for i in range(0, self.H_NB_Lines): 
            line_y = self.get_line_y_from_index(i)
            x1, y1 = self.transform(xmin, line_y)
            x2, y2 = self.transform(xmax, line_y)
            self.horizontal_lines[i].points = [x1, y1, x2, y2]

    def update(self, dt):
        self.update_vertical_line()
        self.update_horizontal_line()
        self.update_tiles()
        self.update_ship()
        time_factor = dt*60
        if not self.state_game_over and self.state_game_started:
            speed_y = self.speed * self.height / 100
            self.current_offset_y += speed_y * time_factor
            spacing = self.H_Lines_Spacing*self.height
            while self.current_offset_y >= spacing:
                self.current_offset_y -= spacing
                self.current_loop_y += 1
                self.score_value = 'S C O R E :' + str(self.current_loop_y)
                self.generate_tile_coordinate()
            speed_x = self.current_speed_x * self.width / 100
            self.current_offset_x += speed_x * time_factor
        if not self.ship_collision() and not self.state_game_over:
            self.state_game_over = True
            self.menu_widget.opacity = 1
            self.menu_button_title = 'R E S T A R T'
            self.menu_title = 'G A M E  O V E R'

class GalaxyApp(App):
    def build(self):
        return

GalaxyApp().run()