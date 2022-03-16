from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line, Quad, Triangle    
    
def init_ship(self):
    with self.canvas:
        Color(0,0,0)
        self.ship = Triangle()

def update_ship(self):
    center_x = self.width / 2
    base_y = self.ship_base_y*self.height
    ship_half_width = self.ship_width*self.width / 2
    self.ship_coordinates[0] = (center_x - ship_half_width, base_y)
    self.ship_coordinates[1] = (center_x, base_y + self.ship_height*self.height)
    self.ship_coordinates[2] = (center_x + ship_half_width, base_y)
    x1, y1 = self.transform(*self.ship_coordinates[0])
    x2, y2 = self.transform(*self.ship_coordinates[1])
    x3, y3 = self.transform(*self.ship_coordinates[2])
    self.ship.points = [x1, y1, x2, y2, x3, y3]
    
def ship_collision(self):
    for i in range(0, len(self.tiles_coordinate)):
        ti_x, ti_y = self.tiles_coordinate[i]
        if ti_y > self.current_loop_y+1:
            return False
        if self.ship_collision_tiles(ti_x, ti_y):
            return True
    return False

def ship_collision_tiles(self, ti_x, ti_y):
    xmin, ymin = self.get_tiles_coordinates(ti_x, ti_y)
    xmax, ymax = self.get_tiles_coordinates(ti_x+1, ti_y+1)
    for i in range(0,3):
        p_x, p_y = self.ship_coordinates[i]
        if xmin <= p_x <= xmax and ymin <= p_y <= ymax:
            return True
    return False