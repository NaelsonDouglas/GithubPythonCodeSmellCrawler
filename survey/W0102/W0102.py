def set_actions(self, actions = []):
    self.actions = actions


def set_actions(self, actions = None):
    if actions:
        self.actions = actions
    else:
        self.actions = []



def append(value, arg = []):
    arg.append(value)
    return arg