class World:
    def __init__(self, y, hill=False):
        self.is_hill = hill
        if hill:
            self.f = lambda x: y * x
        else:
            self.f = lambda x: y
