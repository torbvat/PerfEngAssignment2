class Player:
    def __init__(self, name, rating):
        self.name = name
        self.rating = rating

    def get_name(self):
        return self.name

    def __repr__(self):
        return f"[{self.name}, Rating: {self.rating}]"
