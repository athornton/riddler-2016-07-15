#!/usr/bin/env python3
import CoinFlipper
import statistics

class IteratedFlipper:
    def __init__(self,x=1,y=1,trials=1,debug=False):
        self.numflips=[]
        self.x=x
        self.y=y
        if x > 0:
            x = -x
        if y < 0:
            y = -y
        self.trials=trials
        self.debug=debug
        self.mean=0.0
        self.stddev=0.0
        self.variance=0.0
        self.winners=[]
        self.winner="?"
        self.winfrac=-1.0

    def runtrials(self):
        """Run trials and get statistics"""
        hmap={ "H": "X",
               "T": "Y"}
        for i in range(self.trials):
            self._dbgstr("Trial %d of %d:" % ( (i+1),self.trials))
            c=CoinFlipper.CoinFlipper(debug=self.debug)
            tot=0
            while True:
                tot=c.getcurrent()
                if tot >= self.y or tot <= self.x:
                    break
                c.flip()
            count=c.getcount()
            winner=hmap[(c.getseq())[-1]]
            self._dbgstr("Trial %d: Flips: %d ; Winner %s" %
                         ((i+1),count,winner))
            self.numflips.append(count)
            self.winners.append(winner)
        if self.trials == 1:
            self.mean=tot + 0.0
            self.stddev=-1.0
            self.variance=-1.0
        else:
            self.mean=statistics.mean(self.numflips)
            self.stddev=statistics.pstdev(self.numflips)
            self.variance=statistics.variance(self.numflips)
        xwin = [ x for x in self.winners if x=="X" ]
        xwinf = (0.0 + len(xwin)) / self.trials
        if xwinf == 0.5:
            self.winner="tie"
            self.winfrac=xwinf
        elif xwinf > 0.5:
            self.winner="X"
            self.winfrac=xwinf
        else:
            self.winner="Y"
            self.winfrac=1 - xwinf
        self._dbgstr("Mean: %f ; Std.Dev: %f ; Variance %f" %
                     (self.mean,self.stddev,self.variance) )
        self._dbgstr("Winner: %s (%f)" % (self.winner,self.winfrac))

    def _dbgstr(self,str):
        if self.debug:
            print(str)
