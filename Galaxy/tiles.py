import random
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line, Quad, Triangle

def get_tiles_coordinates(self, ti_x, ti_y):
    ti_y = ti_y - self.current_loop_y
    x = self.get_line_x_from_index(ti_x)
    y = self.get_line_y_from_index(ti_y)
    return x, y

def update_tiles(self):
    for i in range(0, self.NB_tiles):
        tile = self.tiles_coordinate[i]
        xmin, ymin = self.get_tiles_coordinates(tile[0], tile[1])
        xmax, ymax = self.get_tiles_coordinates(tile[0]+1, tile[1]+1)
        x1, y1 = self.transform(xmin, ymin)
        x2, y2 = self.transform(xmin, ymax)
        x3, y3 = self.transform(xmax, ymax)
        x4, y4 = self.transform(xmax, ymin)
        self.tiles[i].points = [x1, y1, x2, y2, x3, y3, x4, y4]
    
def generate_tile_coordinate(self):
    last_x = 0
    last_y = 0
    for i in range(len(self.tiles_coordinate)-1, -1, -1):
         if self.tiles_coordinate[i][1] < self.current_loop_y:
            del self.tiles_coordinate[i]
    if len(self.tiles_coordinate) > 0:
        last_x = self.tiles_coordinate[-1][0]
        last_y = self.tiles_coordinate[-1][1] + 1
    for i in range(len(self.tiles_coordinate), self.NB_tiles):
        r = random.randint(0, 2)
        self.tiles_coordinate.append((last_x, last_y))
        if last_x == self.end_index-1:
            r = 2
        if last_x == self.start_index:
            r = 1
        if r == 1:
            last_x += 1
            self.tiles_coordinate.append((last_x, last_y))
            last_y += 1
            self.tiles_coordinate.append((last_x,last_y))
        if r == 2:
            last_x -= 1
            self.tiles_coordinate.append((last_x, last_y))
            last_y += 1
            self.tiles_coordinate.append((last_x,last_y))
        last_y += 1
    
