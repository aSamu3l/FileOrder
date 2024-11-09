import os

class Lock:
    """
    A class to handle file-based locking mechanism for a specified folder.

    Attributes:
        locked (bool): A flag indicating whether the lock is currently active.
        folder (str): The path to the folder where the lock file will be created.
        lock (file object): The file object representing the lock file.
    """

    locked = False
    folder = None
    lock = None

    def __init__(self, folder: str):
        """
        Initializes the Lock object with a specified folder.
        Creates the folder if it does not exist.

        Args:
            folder (str): The path to the folder where the lock file will be created.
        """
        self.folder = folder
        if not os.path.exists(folder):
            os.makedirs(folder)

    def lock(self):
        """
        Activates the lock by creating a lock file in the specified folder.
        Sets the locked attribute to True.
        """
        self.locked = True
        self.lock = open(os.path.join(self.folder, '.lock'), 'w')

    def unlock(self):
        """
        Deactivates the lock by closing and removing the lock file.
        Sets the locked attribute to False.
        """
        if self.locked:
            self.locked = False
            self.lock.close()
            os.remove(os.path.join(self.folder, '.lock'))

    def is_locked(self):
        """
        Checks if the lock is currently active.

        Returns:
            bool: True if the lock is active, False otherwise.
        """
        return self.locked