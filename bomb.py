from game_parameters import get_random_bomb_data


class Bomb:
    def __init__(self, location, radius, time):
        self.location = location
        self.radius = radius
        self.time = time

    def change_location(self):
        data = get_random_bomb_data()
        self.location = (data[0], data[1])
        self.radius = data[2]
        self.time = data[3]
        return self

    def change_data(self, x, y, radius, time):
        self.location = (x, y)
        self.radius = radius
        self.time = time

    def explosion(self, R):
        if R < 0:
            R = 0
        x = self.location[0]
        y = self.location[1]
        new_ls = []
        for i in range(x - R, x + R + 1):
            for j in range(y - R, y + R + 1):
                if abs(x - i) + abs(y - j) == R:
                    new_ls.append((i, j))
        return new_ls

    def get_location(self):
        return self.location

    def get_time(self):
        return self.time

    def get_radius(self):
        return self.radius


