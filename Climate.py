import random as r


class Climate:
    """
    This represents the number of growing days for each landunit
    """
    def __init__(self):
        """
        Creates a new instance of climate class for a landunit
        """
        self.growthmax = 300
        self.growthmin = 80
        self.growthdays = r.randint(self.growthmin, self.growthmax)


    def getgrowthdays(self):
        """
        :return: Returns the number of growth days for a land unit
        """
        return self.growthdays