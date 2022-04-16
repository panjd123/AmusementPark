import json
import os


class Settings:
    def __init__(self):
        self.screen_width = 400
        self.screen_height = 400
        self.col = 15
        self.row = 15
        self.bg_color = (200, 200, 200)
        self.snake_color = (100, 100, 100)
        self.head_color = (0, 0, 0)
        self.food_color = (255, 245, 225)
        self.cell_color = (0, 180, 100)
        self.snake_speed = 1.5
        self.cell_width = self.screen_width / self.col
        self.cell_height = self.screen_height / self.row
        self.screen_size = (self.screen_width, self.screen_height)
        self.search_area = 1000000

    def load(self, entries: dict = {}):
        self.__dict__.update(entries)


def load_settings():
    settings = Settings()
    settings_file_path = './settings.json'
    if os.path.exists(settings_file_path):
        with open(settings_file_path) as f_obj:
            settings_dict = json.load(f_obj)
        settings.load(settings_dict)
    else:
        with open(settings_file_path, "x") as f_obj:
            json.dump(settings.__dict__, f_obj)
    return settings


if __name__ == '__main__':
    load_settings()
