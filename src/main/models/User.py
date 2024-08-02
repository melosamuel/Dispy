class User:
    user_id: int
    name: str

    def __init__(self, id: int, name: str):
        self.user_id = id
        self.name = name

    def get_id(self):
        return self.user_id
    
    def get_name(self):
        return self.name