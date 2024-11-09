import os

class Lock:
    locked = False
    folder = None
    lock = None

    def __init__(self, folder: str):
        self.folder = folder
        if not os.path.exists(folder):
            os.makedirs(folder)

    def lock(self):
        self.locked = True
        self.lock = open(os.path.join(self.folder, '.lock'), 'w')

    def unlock(self):
        if self.locked:
            self.locked = False
            self.lock.close()
            os.remove(os.path.join(self.folder, '.lock'))

    def is_locked(self):
        return self.locked