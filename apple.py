from game_parameters import get_random_apple_data


class Apple:
    def __init__(self, location, score):
        self.location = location
        self.score = score

    def change_location(self):
        data = get_random_apple_data()
        self.location = (data[0], data[1])
        self.score = data[2]
        # return self

    def change_data(self, x, y, score):
        self.location = (x, y)
        self.score = score
        # return self

    def ckeck_avail(self, other):
        if self.location == other.location:
            return False
        return True

    def get_score(self):
        return self.score

    def get_location(self):
        return self.location

