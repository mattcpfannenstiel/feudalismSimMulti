class Grain:
    """
    This class tracks the grain stores, surplus status and wealth of a fief
    """
    def __init__(self, fief):
        """
        This creates a new instance of the grain class
        :param fief: represents the fief that owns the grain
        """
        self.surplus = False
        self.wealth = 0
        self.upkeep = 0
        self.store = fief

    def addwealth(self, w):
        """
        Adds a value to wealth
        """
        self.wealth += w

    def subtractwealth(self, s):
        """
        Subtracts value from wealth
        """
        self.wealth = self.wealth - s

    def getwealth(self):
        """
        Returns the wealth
        """
        return self.wealth

    def setwealth(self, w):
        """
        Sets the value of wealth
        """
        self.wealth = w

    def atsurplus(self):
        """
        Returns the boolean surplus
        """
        return self.surplus

    def getupkeep(self):
        """
        Returns upkeep
        """
        return self.upkeep

    def setupkeep(self):
        """
        Sets the total upkeep of the Lord each turn
        """
        self.upkeep = self.store.ruler.army.calculateupkeep() + self.store.calculateupkeep()
