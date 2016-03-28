import golly as g



class Gollyhandler:
    """
    Handles all the Golly calls so that it wont have to be imported into the files that need it
    """

    def __init__(self):
        """
        Makes a new Golly command handler
        """
        self.name = "FeudalSim"

    def topopup(self, text):
        """
        Outputs text to a popup in Golly
        :param text: text to be output
        """
        g.note(text)

    def select_rectangle_for_borders(self, startx, starty, width, height):
        """
        Selects the grid to have a border set around it
        :param startx: Starting x position of the grid
        :param starty: Starting y position of the grid
        :param width: Width of the grid
        :param height: Height of the grid
        """
        g.select([startx, starty, width, height])

    def set_border_color(self, fief):
        """
        Sets the selected grid to the color assisgned to the fief
        :param fief: The fief that has already been assigned a color
        """
        g.setcolors([fief.color_number, fief.red, fief.green, fief.blue])

    def toconsole(self, text):
        """
        Outputs text to the console in Golly
        :param text: text to be output
        """
        g.show(text)

    def cellchange(self, x, y, state):
        """
        Sets the color of the specific cell
        :param x: the x location of the cell
        :param y: the y location of the cell
        :param state: the color state that the cell is in
        """
        g.setcell(x, y, state)

    def setstatecolors(self, state, r, gr, b):
        """
        Sets the color of the specified state
        :param state: the color state to be changed
        :param r: the red value
        :param gr: the green value
        :param b: the blue value
        """
        g.setcolors([state, r, gr, b])

    def setrule(self, text):
        """
        Sets the rule in Golly to the specified rule
        :param text: the name of the rule to be changed to
        """
        g.setrule(text)

    def getuserinputint(self, text, default):
        """
        Gets user input from a popup window in Golly
        :param text: the text to be displayed
        :param default: the default value to show up in the entry field
        :return: the value that was inputted by the user
        """
        temp = int(g.getstring(text, default))
        return temp

    def setsimname(self, text):
        """
        Names the simulation that is being displayed
        :param text: the name to be displayed
        """
        g.new(text)

    def update(self):
        """
        Updates the display in Golly to reflect the changes made
        """
        g.update()

    def setpos(self, x, y):
        """
        Sets the position of the screen in golly to center in on the location
        :param x: x position to zoom to
        :param y: y position to zoom to
        """
        g.setpos(x, y)
