class ResortMasterList(object):
    resorts: list = None
    cur_index: int = 0
    num_resorts: int = 0

    def __init__(self):
        self.resorts = ['killington', 'hood', 'steamboat']
        self.num_resorts = len(self.resorts)

    def get_next_resort(self):
        if self.cur_index == self.num_resorts - 1:
            self.cur_index = 0
        else:
            self.cur_index += 1
        return self.resorts[self.cur_index]

    def get_previous_resort(self):
        if self.cur_index == 0:
            self.cur_index = self.num_resorts - 1
        else:
            self.cur_index -= 1
        return self.resorts[self.cur_index]

    def get_resort_at_index(self, index: int):
        self.cur_index = index
        return self.resorts[index]

