#!/usr/bin/env python3
import random

class CoinFlipper:
    """Model for fivethirtyeight.com's July 15 Riddler"""
    def __init__(self,debug=False):
        self._current=0
        self._flip=-1
        self.debug=debug
        self._seq=[]

    def flip(self):
        """Flip a coin and track the totals"""
        flip=random.randint(0,1)
        fstr=[ "Heads", "Tails" ]
        self._flip=flip
        if flip==0:
            self._current=self._current-1
            self._seq.append("H")
        else:
            self._current=self._current+1
            self._seq.append("T")
        self._dbgprt("Flip %d: %s; total %d." % (len(self._seq),fstr[flip],
                                                 self._current))

    def getcount(self):
        """Get number of flips"""
        return len(self._seq)

    def getcurrent(self):
        """Get current score"""
        return self._current

    def getseq(self):
        """Get sequence of flips"""
        return self._seq

    def _dbgprt(self,str):
        if self.debug:
            print(str)
            
