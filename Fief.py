import random
from Gollyhandler import Gollyhandler
from Logger import Logger

g = Gollyhandler()

class Fief:
    """
    This class is for land management and wealth tracking for a lord
    """
    log = Logger("Fief", "High")
    protected_blue = [90]
    protected_green = [216]
    protected_red = [230]

    def __init__(self, fiefnum, color_state, v):
        """
        Makes a new fief
        :param fiefnum: the number of the fief that should match the lord number
        :param color_state: the state number that the fief has as its color
        :return:
        """
        self.view = v
        self.fiefnumber = fiefnum
        self.serf_number = 0
        self.atWar = False
        self.preparedForWar = False
        self.containedLand = []
        self.borders = []
        self.attackoptions = []
        self.ruler = None
        self.stores = None
        self.color_number = color_state
        self.red = None
        self.green = None
        self.blue = None
        self.color = [self.red, self.green, self.blue]

    def changewarstatus(self):
        """
        Changes at War status to at war or not at war
        """
        self.atWar = not self.atWar

    def changepreparedness(self):
        """
        Changes a fief preparedness to be either prepared for war or unprepared for war
        """
        self.preparedForWar = not self.preparedForWar

    def addland(self, LandUnit):
        """
        Adds land to the end of the contained land list
        :param LandUnit: the landunit to be added
        """
        self.containedLand.append(LandUnit)

    def removeland(self, x, y):
        """
        Removes land from fiefs list
        :param x: the x location of the target landunit
        :param y: the y location of the target landunit
        """
        if len(self.containedLand) != 0:
            i = 0
            t = True
            while t:
                while i < len(self.containedLand):
                    if self.containedLand[i].GRID_LOCATION.xloc == x and self.containedLand[i].GRID_LOCATION.yloc == y:
                        self.containedLand.pop(i)
                        t = False
                    i += 1

    def findborders(self, fmap, width, height):
        """
        Looks through landunits and finds the ones that border other fiefdoms it then adds it to the bordering units list
        """
        self.log.tracktext("Finding Borders")
        self.attackoptions = []
        self.borders = []
        i = 0
        while i < len(self.containedLand):
            c = self.containedLand[i].getvonneumann(fmap, width, height)
            self.log.tracktext("Found Von Neumann Neighborhood. Length is " + str(len(c)))
            j = 0
            d = 0
            tempAttackOptions = []
            while j < len(c):
                if c[j].owner.fiefnumber != self.fiefnumber:
                    self.log.tracktext("Found non member")
                    if -self.borders.__contains__(self.containedLand[i]):
                        self.borders.append(self.containedLand[i])
                        self.log.tracktext("Added to borders")
                    d += 1
                    tempAttackOptions.append(c[j])
                    self.log.tracktext("Added to attack options")
                j += 1
                if d == len(c):
                    self.log.tracktext("Starting Land Loss")
                    self.land_loss(i, c, self)
                    self.removeland(self.containedLand[i].GRID_LOCATION.xloc, self.containedLand[i].GRID_LOCATION.yloc)
                else:
                    self.add_attack_options(tempAttackOptions)
            i += 1

    def getfiefsize(self):
        return len(self.containedLand)

    def getattackoptions(self):
        return self.attackoptions

    def removeattackoption(self, x, y):
        """
        Removes attack option from the list after it has been used
        :param x: the x location of the target landunit
        :param y: the y location of the target landunit
        """
        i = 0
        t = False
        while i < len(self.attackoptions):
            if self.attackoptions[i].GRID_LOCATION.xloc == x and self.attackoptions[i].GRID_LOCATION.yloc == y:
                self.attackoptions.pop(i)
            i += 1
            if t:
                break

    def findupkeep(self):
        """
        Finds the upkeep for all the serfs on a fief (serfs multiplied by upkeep cost)
        """
        i = 0
        cost = 0
        while i < len(self.containedLand):
            cost += self.containedLand[i].getupkeep()
            i += 1
        return cost

    def placeserf(self):
        """
        Places serf on a random land unit in the fief that isn't full (10 serfs is full)
        """
        x = True
        while x:
            self.log.tracktext("Placing serf")
            r = random.randint(0, (len(self.containedLand) - 1))
            if not self.containedLand[r].full:
                self.containedLand[r].addserf()
                if self.view:
                    self.containedLand[r].color_change_flash(self.color_number, 2)
                self.log.tracktext("Serf placed in " + str(self.containedLand[r].GRID_LOCATION.xloc) +
                                   ", " + str(self.containedLand[r].GRID_LOCATION.yloc) + " by " + self.ruler.name)
                self.serf_number += 1
                x = False
            if self.alllandfull():
                x = False
            else:
                self.log.tracktext("Land unit " + str(r) + " is full")

    def calculatewealth(self):
        """
        Calculates wealth on entire fief
        Rule that governs wealth calculation based on land unit production
        """
        i = 0
        final = 0
        while i < len(self.containedLand):
            temp = self.containedLand[i].getproduction()
            temp = (temp - self.containedLand[i].getupkeep())
            final += temp
            i += 1
        final = final - self.ruler.combatants.calculateupkeep()
        self.stores.wealth += final
        self.log.tracktext(str(self.ruler.name) + " has " + str(self.stores.wealth) + " grain at his disposal")

    def alllandfull(self):
        """
        Checks to see if all land in a fief is full of serfs
        :return: true for all landunits full and false for room to be utilized
        """
        self.log.tracktext("Got into all land full?")
        self.log.tracktext("Contained land has " + str(len(self.containedLand)) + " land units in it")
        if len(self.containedLand) != 0:
            i = 0
            while i < len(self.containedLand):
                if not self.containedLand[i].full:
                    self.log.tracktext("Free land unit for serf placement")
                    return False
                else:
                    self.log.tracktext("No room for a serf")
                    return True
        else:
            self.log.tracktext("No land free for serf placement")
            return True

    def land_loss(self, num, cellList, fief):
        tempPotentialOwners = []
        i = 0
        j = 0
        a = 0
        while i < len(cellList):
            self.log.tracktext("Checking surrounding rulers")
            if not tempPotentialOwners.__contains__(cellList[i].owner.ruler.number):
                tempPotentialOwners.append(cellList[i].owner.ruler.number)
            i += 1
        tempPotententialOwnersNumber = [0 for x in range(len(tempPotentialOwners))]
        self.log.tracktext("Checking number of surrounding land units")
        while j < len(tempPotentialOwners):
            x = 0
            while x < len(cellList):
                # self.log.track_popup_only("Cell list check")
                if cellList[x].owner.ruler.number == tempPotentialOwners[j]:
                    self.log.tracktext("Incrimenting")
                    tempPotententialOwnersNumber[j] += 1
                x += 1
            j += 1
        nOwner = fief.ruler.number
        while nOwner is fief.ruler.number:
            nOwner = self.find_new_owner(tempPotententialOwnersNumber)
        self.log.tracktext("Setting new owner to fief " + str(tempPotentialOwners[nOwner]) + ". Old owner is fief " + str(fief.ruler.number))
        if nOwner is not None:
            while a < len(cellList):
                if tempPotentialOwners[nOwner] == cellList[a].owner.ruler.number:
                    cellList[a].owner.containedLand.append(fief.containedLand[num])
                    fief.containedLand[num].changeowner(cellList[a].owner)
                    cellList[a].owner.containedLand[len(cellList[a].owner.containedLand)-1].delay()
                    self.log.tracktext("Finished delay")
                    break
                a += 1

    def add_attack_options(self, landUnitList):
        self.log.tracktext("Got into add attack options")
        i = 0
        while i < len(landUnitList):
            self.attackoptions.append(landUnitList[i])
            i += 1

    @staticmethod
    def find_new_owner(list):
        i = 0
        temp = 0
        rtemp = 0
        if len(list) == 0:
            return None
        while i < len(list):
            if temp > list[i]:
                temp = list[i]
                rtemp = i
            i += 1
        return rtemp