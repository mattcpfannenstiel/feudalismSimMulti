import random as r
from Army import Army
from Logger import Logger


class Lord:
    """
    Lords are the main players in the simulation and make all the decisions such as attacking, buying knights, waiting
    or placing a serf.
    """
    log = Logger("Lord", "High")
    turn = 0
    view = False

    def __init__(self, name, Fief, v, num):
        """
        Makes a new lord
        :param name: the name of the lord
        :param Fief: the fief that he rules over
        """
        self.view = v
        if self.view:
            from Gollyhandler import Gollyhandler
            self.g = Gollyhandler()
        self.name = name
        self.combatants = Army()
        self.ready = False
        self.land = Fief
        self.dead = False
        self.number = num

    def getname(self):
        """
        Returns the name
        """
        return self.name

    def prepared(self):
        """
        Returns the boolean ready
        """
        return self.ready

    def decision(self):
        """
        33% Chance to attack, buy, or wait
        Governs the decision mechanism of the Lords (Decision Rule)
        Lords attack the most productive land unit nearby
        """
        self.log.tracktext("Begin scouting and weighted decision")
        scoutReport = self.scouting(self.land)
        self.log.tracktext("Scout report shows a " + str(scoutReport[0]) + "% chance of buying a knight")
        self.log.tracktext("Scout report shows a " + str(scoutReport[1] - scoutReport[0]) +
                                  "% chance of attacking")
        j = r.randint(0, 98)
        if j < scoutReport[0] or scoutReport[2] == True:
            self.log.tracknum(self.name + " is buying knights", self.combatants.getknightcount())
            if self.land.stores.getwealth() > 100:
                self.log.tracktext("In buy phase for " + str(self.name))
                while self.land.stores.getwealth() > 100:
                    self.buyknight()
            self.log.tracktext(str(self.name) + " now has " + str(self.combatants.getknightcount()) + " and " + str(
                self.land.stores.getwealth()))
        if j >= scoutReport[1]:
            self.log.tracktext("In combat phase")
            if self.combatants.getknightcount() > 0:
                target = self.lookforwealthyland()
                if target is not None and \
                                target.owner.ruler.combatants.getknightcount() < self.combatants.getknightcount():
                    while len(target.owner.containedLand) == 0 or (target.owner.ruler.number == self.number):
                        self.land.removeattackoption(target.GRID_LOCATION.xloc, target.GRID_LOCATION.yloc)
                        target = self.lookforwealthyland()
                    if self.view:
                        target.color_change_flash(target.owner.color_number, 5)
                    self.land.removeattackoption(target.GRID_LOCATION.xloc, target.GRID_LOCATION.yloc)
                    self.attack(target)
                    if self.view:
                        target.color_change(target, target.owner.color_number)
                    self.log.tracktext(str(self.name) + " is attacking " + str(target.owner.ruler.name)
                          + " over land unit at " + str(target.GRID_LOCATION.xloc) + ", " + str(target.GRID_LOCATION.yloc))
                    self.land.removeattackoption(target.GRID_LOCATION.xloc, target.GRID_LOCATION.yloc)
                    self.attack(target)

                else:
                    self.log.tracktext("No target available")
        else:
            self.log.tracktext("Waiting")

    def attack(self, landUnit):
        """
        Sends troops into combat, determines the winner and either takes land or defends it
        Rule that governs the battles and decides combat by numbers but if they have the same number of knights
        the battle is decided by a coin flip
        :param landUnit: the land unit that is being targeted by the lord
        """
        self.log.tracktext("Attacking lord has " + str(self.combatants.getknightcount()) + " knights")
        self.log.tracktext("Defending lord has " + str(landUnit.owner.ruler.combatants.getknightcount()) +
                                  " knights")
        if self.combatants.getknightcount() == landUnit.owner.ruler.combatants.getknightcount():
            self.log.tracktext("In tied combat")
            i = r.randint(0, 99)
            if i > 49:
                self.calculate_knight_loss_on_win(landUnit.owner.ruler.combatants, self.combatants)
                landUnit.owner.removeland(landUnit.GRID_LOCATION.xloc, landUnit.GRID_LOCATION.yloc)
                landUnit.changeowner(self.land)
                self.land.containedLand.append(landUnit)
                self.log.tracktext(str(self.name) + " wins the battle")

            else:
                self.log.tracktext(str(landUnit.owner.ruler.name) + " wins the battle")
                landUnit.owner.ruler.calculate_knight_loss_on_win(self.combatants, landUnit.owner.ruler.combatants)
        elif self.combatants.getknightcount() > landUnit.owner.ruler.combatants.getknightcount():
            self.log.tracktext("In normal combat")
            self.calculate_knight_loss_on_win(landUnit.owner.ruler.combatants, self.combatants)
            landUnit.owner.removeland(landUnit.GRID_LOCATION.xloc, landUnit.GRID_LOCATION.yloc)
            landUnit.changeowner(self.land)
            self.land.containedLand.append(landUnit)
            self.log.tracktext(str(self.name) + " wins the battle")

        else:
            self.log.tracktext(str(landUnit.owner.ruler.name) + " wins the battle")
            landUnit.owner.ruler.calculate_knight_loss_on_win(self.combatants, landUnit.owner.ruler.combatants)

    def buyknight(self):
        """
        Buys a knight and adds him to the army that the lord has at his disposal
        """
        if self.land.stores.getwealth() < 0:
            self.log.tracknum("stores are less than zero", self.land.stores.getwealth())
        else:
            self.land.stores.subtractwealth(self.combatants.getcost())
            self.combatants.addknight()

    def lookforwealthyland(self):
        """
        Looks for the most productive land unit from the fief's attack options and returns it
        """
        i = 0
        temp = 0
        if len(self.land.attackoptions) != 0:
            target = self.land.attackoptions[0]
            self.log.tracktext("In wealthy lookup")
            while i < len(self.land.attackoptions):
                if temp < self.land.attackoptions[i].getproduction():
                    temp = self.land.attackoptions[i].getproduction()
                    target = self.land.attackoptions[i]
                i += 1
            self.log.tracktext("Target is " + str(target.owner.ruler.name) + " at " + str(target.GRID_LOCATION.xloc) +
                               ", " + str(target.GRID_LOCATION.yloc))
            return target
        else:
            return None

    def checkifdead(self):
        """
        Checks to see if a lord has any land left
        :return: true means he is defeated, false means he gets to fight on
        """
        if len(self.land.containedLand) == 0:
            return True
        else:
            return False

    def calculate_knight_loss_on_win(self, LKnights, WKnights):
        if LKnights.getknightcount() != 0:
            self.log.tracktext(
                "Knights of loser " + str(LKnights.getknightcount()) + ". Knights of winner: " +
                str(WKnights.getknightcount()))
            compare = WKnights.getknightcount() - LKnights.getknightcount()
            if compare > (.5 * LKnights.getknightcount()):
                compare = .5 * LKnights.getknightcount()
            self.log.tracktext("Loss is: " +  str(int(compare)))
            LKnights.knightcount -= int(compare)
            if LKnights.getknightcount() < 0:
                LKnights.knightcount = 0
            self.log.tracktext("Knights of loser after " + str(LKnights.getknightcount()))
        else:
            self.log.tracktext("No defending knights")

    def scouting(self, fief):
        report = [66, 33, False]
        x = 0
        c = 0
        while x < len(fief.attackoptions):
            if fief.attackoptions[x].owner.ruler.combatants.getknightcount() >= self.combatants.getknightcount():
                report[0] -= 1
                report[1] += 1
                c += 1
            else:
                report[0] += 1
                report[1] -= 1
            x += 1
        report[0] = 100 - report[0]
        report[1] = 100 - report[1]
        if report[0] < 0:
            report[0] = 0
        if report[1] > 100:
            report[1] = 99
        if c == len(fief.attackoptions):
            report[2] = True
        return report
