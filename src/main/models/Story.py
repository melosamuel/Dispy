class Story:
    story_id: int
    name: str
    synopsis: str
    progresses: dict
    choices: dict

    def __init__(self, story_id: int, name: str, synopsis: str):
        self.story_id = story_id
        self.name = name
        self.synopsis = synopsis
        self.progresses = {}
        self.choices = {}

    def set_progresses(self, progresses: dict):
        self.progresses = progresses

    def set_choices(self, choices: dict):
        self.choices = choices

    def get_progress(self, progress_id: int):
        if self.progresses:
            return self.progresses[progress_id]
        
        return None
    
    def get_choice(self, choice_id: int):
        if self.choices:
            return self.choices[choice_id]
        
        return None

    def get_id(self):
        return self.id
    