class Army:
    """
    This tracks the combat strength and upkeep cost of each combat unit
    """
    def __init__(self):
        """
        Creates a new army for a lord
        """
        self.knightcount = 0
        # Upkeep cost
        self.UCOST = 10
        # Buy cost
        self.BCOST = 100


    def getknightcount(self):
        """
        Returns the number of Knights in the army
        """
        return self.knightcount


    def setknightcount(self, k):
        """
        Sets the number of Knights in the army
        """
        self.knightcount = k


    def getcost(self):
        """
        Returns the buy costs of Knights
        """
        return self.BCOST


    def addknight(self):
        """
        Adds a knight to the army
        """
        self.knightcount += 1


    def killknight(self):
        """
        Takes a knight out of the army
        """
        self.knightcount -= 1


    def calculateupkeep(self):
        """
        Returns the upkeep cost of the army
        """
        return self.UCOST * self.knightcount

