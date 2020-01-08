from src.backend.config import ConfigFunctions


class ResortMasterList(object):
    conf: ConfigFunctions = None
    resorts: list = None
    cur_index: int = 0
    num_resorts: int = 0

    def __init__(self):
        self.conf = ConfigFunctions()
        self.resorts = self.conf.get_list_of_resorts()
        self.num_resorts = len(self.resorts)

    def get_next_resort(self):
        self.cur_index = (self.cur_index + 1) % self.num_resorts
        return self.resorts[self.cur_index]

    def get_previous_resort(self):
        self.cur_index = (self.cur_index - 1) % self.num_resorts
        return self.resorts[self.cur_index]

    def get_resort_at_index(self, index: int):
        self.cur_index = index
        return self.resorts[index]

    def get_current_index(self):
        return self.cur_index

    def get_resort_amount(self):
        return self.num_resorts

