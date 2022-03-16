from kivy import platform
from kivy.uix.relativelayout import RelativeLayout

def _keyboard_closed(self):
    self._keyboard.unbind(on_key_down=self._on_keyboard_down)
    self._keyboard.unbind(on_key_up=self._on_keyboard_up)
    self._keyboard = None
def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[1] == 'left':
        self.current_speed_x = self.speed_x
    elif keycode[1] == 'right':
        self.current_speed_x = -self.speed_x
    return True
def _on_keyboard_up(self, keyboard, keycode):
    self.current_speed_x = 0
    return True
def in_desktop(self):
    if platform in ('linux', 'win', 'macosx'):
        return True
    else:
        return False
def on_touch_down(self, touch):
    if not self.state_game_over and self.state_game_started:
        if touch.x < int(self.width/2):
            self.current_speed_x = self.speed_x
        else:
            self.current_speed_x = -self.speed_x
    return super(RelativeLayout, self).on_touch_down(touch)
    
def on_touch_up(self, touch):
    self.current_speed_x = 0