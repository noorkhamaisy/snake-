class Snake:
    def __init__(self, length, location):
        self.length = length
        self.location = location
        self.coordinates = []
        self.coordinates.append(location)

    def move(self, movekey):
        snakehead = self.coordinates[-1]
        snake_moved = 0
        if movekey == "Up":
            self.coordinates.append((snakehead[0], snakehead[1] + 1))
            snake_moved = 1
        if movekey == "Down":
            self.coordinates.append((snakehead[0], snakehead[1] - 1))
            snake_moved = 1
        if movekey == "Right":
            self.coordinates.append((snakehead[0] + 1, snakehead[1]))
            snake_moved = 1
        if movekey == "Left":
            self.coordinates.append((snakehead[0] - 1, snakehead[1]))
            snake_moved = 1
        if len(self.coordinates) > self.length:
            self.coordinates.pop(0)
        if snake_moved == 1:
            return True
        return False

    def add_length(self, to_add):
        self.length += to_add

    def get_head(self):
        return self.coordinates[-1]

    def get_coordinates(self):
        return self.coordinates

