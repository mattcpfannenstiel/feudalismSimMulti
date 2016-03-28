import math
import random as r

from Fief import Fief
from Grain import Grain
from LandUnit import LandUnit
from Lord import Lord
from Logger import Logger


class Load:
    """
    Creates the map grid and sets up the lords for the simulation
    """
    log = Logger("Load", "Low")

    def __init__(self, Name, v):
        """
        Makes a new load of the simulation and gets user input for variables
        :param Name: Name of the simulation
        """
        self.view = v
        if self.view:
            from Gollyhandler import Gollyhandler
            self.g = Gollyhandler()
        if not self.view:
            print ("View is set to false")
        self.name = Name

        if self.view:
            self.g.setsimname(self.name)

            # Parameters of the simulation for testing purposes
            self.runs = self.g.getuserinputint("Enter the number of iterations", "5000")
            self.lords = self.g.getuserinputint("Enter the number of lords that can be square rooted(Max 100)", "4")
            self.landcount = self.g.getuserinputint("Enter the number of landunits per lord that can be square rooted"
                                                    "(Max 100)", "4")
            self.height = math.sqrt(self.landcount) * math.sqrt(self.lords)
            self.width = math.sqrt(self.landcount) * math.sqrt(self.lords)

            # Sets Golly into a rule set with 8 states to work with
            self.g.setrule("Perrier")

            self.g.setsimname(self.name)
            # Sets Golly to the position view of the x and y coordinates in the center
            # self.g.setpos(str(self.width / 2), str(self.height / 2))

            # State 5 is fought over land and is red
            self.g.setstatecolors(5, 255, 0, 0)

            # State 4 is occupied and battle scarred land and is blue
            self.g.setstatecolors(4, 0, 0, 255)

            # State 3 is occupied and underproducing land and is yellow
            self.g.setstatecolors(3, 230, 216, 90)

            # State 2 is occupied and normal production land and is green
            self.g.setstatecolors(2, 0, 255, 0)

            # State 1 is farmable land and is white
            self.g.setstatecolors(1, 255, 255, 255)
        else:
            self.width = 4
            self.height = 4
            self.runs = 5000
            self.lords = 4
            self.landcount = 4


    def initialize(self):
        """
        Sets up the entire state of the board to the user's specifications
        :return: the state of the board including the map, lords, number of years to go through,
        and width and height of the map
        """

        # Goes through each land unit to give it an initial state and initializes the board
        # Lords are also created with their given fiefs
        fiefnum = 0
        fief_color_number = 6
        startpointx = 0
        startpointy = 0
        lordslist = []
        sidelength = int(math.sqrt(self.landcount))
        lordside = int(math.sqrt(self.lords))
        sidemod = lordside
        if lordside < 2:
            sidemod = lordside - 1
        if lordside % 2 == 1:
            sidemod += 1

        # Sets up landowner and state tracking map
        fmap = self.makemap(self.width, self.height)

        # Sets landunits into fiefs and fiefs into lords ownership
        x = 0
        while fiefnum < self.lords:
            self.log.tracktext(
                "Fiefnum is " + str(fiefnum) + "\nSidemod is " + str(sidemod) + "\nSidelength is " + str(sidelength))
            if fiefnum == 0:
                self.log.tracktext("Starting fief construction")
            elif fiefnum >= lordside:
                if fiefnum % sidemod == 0:
                    startpointx = 0
                    x = startpointx
                    startpointy += sidelength
                else:
                    startpointx += sidelength
                    x = startpointx
            else:
                startpointx += sidelength
                x = startpointx
            fief = Fief(fiefnum, fief_color_number, self.view)
            self.border_color_generate(fief)
            fief_color_number += 1
            while x < startpointx + sidelength:
                y = 0 + startpointy
                while y < startpointy + sidelength:
                    self.populatemap(fief, fmap, x, y, fiefnum)
                    self.make_borders(fief)
                    y += 1
                x += 1
            grain = Grain(fief)
            fief.stores = grain
            lord = Lord("Lord " + str(fiefnum), fief, self.view, fiefnum)
            lord.land.ruler = lord
            lordslist.append(lord)
            fiefnum += 1
        boardstate = self.makeboardstate(fmap, lordslist, self.runs, self.width, self.height)
        self.log.tracktext("Board Creation done")
        return boardstate

    def makemap(self, width, height):
        """
        Makes the map based on the height and width made by the user input
        :param width: square root of the number of lords multiplied by the
        square root of the number of land units per fief
        :param height: square root of the number of lords multiplied by the
        square root of the number of land units per fief
        :return: the created map of the simulation
        """
        fmap = []
        self.log.tracktext("Start map")
        i = 0
        while i < width:
            j = 0
            fmap.append([])
            while j < height:
                fmap[i].append([])
                j += 1
            i += 1
        self.log.tracktext("Map made")
        return fmap

    def makeboardstate(self, fmap, lordslist, runs, width, height):
        """
        Puts all the parameters created in the initialization into a list to be easily referenced
        :param fmap: map of the land units and their state
        :param lordslist: a list including all the lords in the simulation
        :param runs: number years to simulate
        :param width: x size of the simulation
        :param height: y size of the simulation
        :return: a list including all the given parameters
        """
        # Boardstate set up as [fmap, lordslist, runs, width, height]
        boardstate = []
        boardstate.append(fmap)
        boardstate.append(lordslist)
        boardstate.append(runs)
        boardstate.append(width)
        boardstate.append(height)
        return boardstate

    def populatemap(self, fief, fmap, x, y, fiefnum):
        """
        Takes all the given information and adds it to the map and fiefs, then updates the board in Golly to match
        :param fief: the fief the new land unit is being added to
        :param fmap: the map that is updated with new information
        :param x: x location on the map
        :param y: y location on the map
        :param fiefnum: the number of the fief that is being delt with(also the lord's number)
        """
        self.log.tracktext("Lord " + str(fiefnum) + " landunit at " + str(x) + ", " + str(y))
        land = LandUnit(x, y, fief, True)
        fief.containedLand.append(land)
        fmap[x][y].append(x)
        fmap[x][y].append(y)
        fmap[x][y].append(land)
        fmap[x][y].append(fief.color_number)
        if self.view:
            self.g.cellchange(x, y, fief.color_number)
            self.g.update()



    def border_color_generate(self, fief):
        """
        Creates a Color with an rgb value unlike others on the map. Only one randomly generated color may match another
        color already generated
        :param fief: This is the fief that is having color added to it
        :return:
        """
        c = 0
        done = False
        while not done:
            blue = r.randint(1, 254)
            red = r.randint(1, 254)
            green = r.randint(1, 254)
            self.log.tracktext("Starting Blue")
            if self.protected_color_check(fief, blue, fief.protected_blue):
                self.log.tracktext("Blue is in")
                c += 1
            self.log.tracktext("Starting Green")
            if self.protected_color_check(fief, green, fief.protected_green):
                self.log.tracktext("Green is go")
                c += 1
            self.log.tracktext("Starting Red")
            if self.protected_color_check(fief, red, fief.protected_red):
                self.log.tracktext("Red is out")
                c += 1
            if c > 1:
                self.log.tracktext("Got to end condition")
                fief.red = red
                fief.blue = blue
                fief.green = green
                self.add_to_protected_colors(fief, red, green, blue)
                done = True
            self.log.tracknum("C is:", c)
            if c <= 1:
                self.log.tracktext("Got to reset")
                c = 0

    @staticmethod
    def protected_color_check(fief, color, protected_color_list):
        """
        Checks the Protected color list to make sure the generated color doesn't match any on the list
        :param fief: the fief whose color is being addressed
        :param color: the number value of the color
        :param protected_color_list: the list of already generated color
        :return: true for it isn't a protected color and false for the color being on the list
        """
        i = 0
        f = 0
        fief.log.tracknum("Protected list length is:", len(protected_color_list))
        while i < len(protected_color_list):
            fief.log.tracknum("In protected color check", i)
            m = len(protected_color_list)
            fief.log.tracknum("Color is:", color)
            fief.log.tracknum("Protected color is:", protected_color_list[i])
            if color != protected_color_list[i]:
                f += 1
            if m == f:
                return True
            i += 1
        fief.log.tracktext("Failed the protected color check")
        return False

    @staticmethod
    def add_to_protected_colors(fief, red, green, blue):
        """
        After an acceptable color set is found it is added to the lists of protected colors
        :param fief: fief being addressed
        :param red: red color value
        :param green: green color value
        :param blue: blue color value
        """
        fief.blue = blue
        fief.protected_blue.append(blue)
        fief.green = green
        fief.protected_green.append(green)
        fief.red = red
        fief.protected_red.append(red)

    def make_borders(self, fief):
        """
        This routine is to set up the border color for each fief
        :param fief: The fief being generated for
        :param startx: the x position of the land unit in question
        :param starty: the y position of the land unit in quesiton
        :param width: the width of the grid in question
        :param height: the height of the grid in question
        """
        if self.view:
            self.log.tracktext("Going into set fief color")
            self.g.set_border_color(fief)
            self.log.tracktext("Got through border color")
            self.g.update()



