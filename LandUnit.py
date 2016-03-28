from Climate import Climate
from Location import Location
from Logger import Logger
import time


class LandUnit:
    """
    The basic unit that produces grain and houses serfs
    """
    SERF_MAX = 10
    PRODUCTION_VALUE = 50
    SERF_UPKEEP_COST = 5

    def __init__(self, x, y, fief, v):
        """
        Makes a new land unit
        :param x: the x location of the land unit on the map
        :param y: the y location of the land unit on the map
        :param fief: the fief that the land unit belongs to
        """
        self.view = v
        if self.view:
            from Gollyhandler import Gollyhandler
            self.g = Gollyhandler()
        self.log = Logger("LandUnit", "Low")
        self.farmable = True
        self.serfs = 0
        self.WEATHER = Climate()
        self.owner = fief
        self.full = False
        self.GRID_LOCATION = Location(x, y)

    def changeowner(self, newowner):
        """
        Changes the current owner of the land unit to the new owner
        """
        self.owner = newowner
        self.color_change(self, self.owner.color_number)

    def getlandunit(self, x, y, fmap):
        """
        Returns the land unit from the x, y location from the map
        :return: sends back the landunit at that location
        """
        return fmap[x][y][2]

    def getproduction(self):
        """
        Return the production of the land unit
        :return: the production of the landunit
        """
        return self.PRODUCTION_VALUE * self.serfs

    def getupkeep(self):
        """
        Returns the upkeep of the landunit
        :return: the upkeep from multiplying number of serfs by their upkeep cost
        """
        return self.serfs * self.SERF_UPKEEP_COST

    def getvonneumann(self, fmap, width, height):
        """
        Looks in the land unit's Von Neumann Neighborhood and returns cells inside the map grid
        :param width: X bounds of the map
        :param height: Y bounds of the map
        :param fmap: the map grid to reference from
        :return: the list of cells around the cell
        """
        c = []
        if (width > self.GRID_LOCATION.xloc + 1 >= 0) and (0 <= self.GRID_LOCATION.yloc < height):
            c.append(self.getlandunit(self.GRID_LOCATION.xloc + 1, self.GRID_LOCATION.yloc, fmap))
        if (width > self.GRID_LOCATION.xloc >= 0) and (0 <= self.GRID_LOCATION.yloc + 1 < height):
            c.append(self.getlandunit(self.GRID_LOCATION.xloc, self.GRID_LOCATION.yloc + 1, fmap))
        if (width > self.GRID_LOCATION.xloc - 1 >= 0) and (0 <= self.GRID_LOCATION.yloc < height):
            c.append(self.getlandunit(self.GRID_LOCATION.xloc - 1, self.GRID_LOCATION.yloc, fmap))
        if (width > self.GRID_LOCATION.xloc >= 0) and (0 <= self.GRID_LOCATION.yloc - 1 < height):
            c.append(self.getlandunit(self.GRID_LOCATION.xloc, self.GRID_LOCATION.yloc - 1, fmap))
        return c

    def addserf(self):
        """
        Adds a serf to the land unit unless the land unit is full
        """
        if self.serfs < self.SERF_MAX:
            self.serfs += 1
        else:
            self.full = True

    def color_change_flash(self, color1, color2):
        self.color_change(self, color2)
        self.delay()
        self.color_change(self, color1)

    def color_change(self, target, color):
        self.g.cellchange(target.GRID_LOCATION.xloc, target.GRID_LOCATION.yloc, color)
        self.g.update()

    def delay(self):
        g = True
        t = time.clock()
        at = time.localtime(t)
        self.log.tracktext("Time is: " + str(at[5]))
        while not g:
            yt = time.clock()
            rt = time.localtime(yt)
            self.log.tracktext("Time is: " + str(rt[5]) + ". Start time is: " + str(at[5]))
            self.log.tracktext(str(at[5]%60 - 57))
            if rt[5] == (at[5] + 1):
                g = True
            if rt[5] == (at[5] + 3):
                g = True
            if rt[5] == (at[5]%60 - 59 + 1 or at[5]%60 - 59 + 2):
                g = True

