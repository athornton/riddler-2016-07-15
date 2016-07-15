#!/usr/bin/env python3
import IteratedFlipper
import argparse

def _parse_args():
    parser=argparse.ArgumentParser(description='Flip a coin and keep score.')
    parser.add_argument("-d","--debug",action="store_true",
                        help="Enable debugging")
    parser.add_argument("-x","--x","-X","--X",type=int,default=1,
                        help="Absolute value of max X score")
    parser.add_argument("-y","--y","-Y","--Y",type=int,default=1,
                        help="Absolute value of max Y score")
    parser.add_argument("-t","--trials",type=int,default=100,
                        help="Number of trials")
    args=parser.parse_args()
    return args

def main():
    args=_parse_args()
    x=args.x
    y=args.y
    t = args.trials
    if x > 0:
        x=-x
    if y < 0:
        y=-y
    if t < 1:
        raise ValueError("Number of trials must be at least 1")
    dbg=args.debug
    pred=[]
    ppr=[]
    for xx in range(-1,(x-1),-1):
        for yy in range(1,(y+1)):
            r=IteratedFlipper.IteratedFlipper(x=xx,y=yy,trials=t,
                                              debug=args.debug)
            r.runtrials()
            posx=-xx
            print("x=%d, y=%d, t=%d:" % (posx, yy, t))
            print("    Actual: mean flips %f, winner %s(%f)" %
                (r.mean, r.winner, r.winfrac))
            pwin="X"
            pfrac=1.0 - ((0.0 + posx) / (posx + yy))
            pflips = posx * yy
            if posx == yy:
                pwin="tie"
            elif posx > yy:
                pwin="Y"
                pfrac=1.0 - (( 0.0 + yy) / (posx + yy))
            print("    Predicted: mean flips %d, winner %s(%f)" %
                  (pflips,pwin,pfrac))
            em = r.mean - pflips
            pred.append(em/(0.0 + pflips))
            er = r.winfrac - pfrac
            ppr.append(er)
            if pwin != r.winner:
                er = r.winfrac - ( 1.0 - pfrac)
            if dbg:
                import statistics
                print("    Error: Mean flips %f, probability %f" %
                      (em,er))
                print("Average flip error (expected 0): %f" %
                      statistics.mean(pred))
                print("Average prob. error (expected 0): %f" %
                      statistics.mean(ppr))
                print("Flip error stddev: %f" % statistics.pstdev(pred))
                print("Prob error stddev: %f" % statistics.pstdev(ppr))
    
    
if __name__ == "__main__":
    main()

