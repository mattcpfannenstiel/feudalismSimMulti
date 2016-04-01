from Load import Load
from Logger import Logger
import threading
import time

class Run:
    """
    Handles the running of the simulation through its yearly cycles
    """
    log = Logger("Run", "Low")

    def __init__(self):
        """
        Makes a new instance of the run class
        """
        self.new = Load("Feudalism Simulation", True)
        self.log.tracktext("Now Loading")
        self.board = self.new.initialize()
        self.log.tracktext("Loading done")
        cont = 1
        while cont == 1:
            cont = self.cycle()
        self.log.track_popup_only("Simulation complete")

    def thread_work(self, lord):
        lord.log.tracktext(lord.name + " is running at: " + time.ctime(time.time()))
        lord.land.calculatewealth()
        lord.land.placeserf()
        lord.land.findborders(self.board[0], self.board[3], self.board[4])
        lord.decision()
        lord.log.tracktext(lord.name + " is done at: " + time.ctime(time.time()))

    def cycle(self):
        """
        Goes through the turn for each lord for every year
        :return: a zero when the number of runs is complete
        """
        i = 0
        while i < self.board[2]:
            self.log.trackconsoleonly("Yearly cycle", i)
            lordturn = 0
            wincondition = self.how_many_are_left()
            if wincondition != 1:
                while lordturn < len(self.board[1]):
                    self.board[1][lordturn].dead = self.board[1][lordturn].checkifdead()
                    if not self.board[1][lordturn].dead:
                        # threadwork here
                        self.log.tracktext("Turn")
                        threading.Thread(target=self.thread_work(self.board[1][lordturn]))
                        self.log.tracktext("Past thread")
                        lordturn += 1
                    else:
                        self.log.tracktext(str(self.board[1][lordturn].name) + " is defeated")
                        lordturn += 1
            i += 1
            if wincondition == 1:
                self.log.track_popup_only("Simulation ended in year " + str(i))
                i = self.board[2]
        return 0

    def how_many_are_left(self):
        i = 0
        c = len(self.board[1])
        while i < len(self.board[1]):
            if self.board[1][i].dead:
                c -= 1
            i += 1
        return c

