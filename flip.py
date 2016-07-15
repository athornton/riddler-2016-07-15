#!/usr/bin/env python3
import IteratedFlipper
import argparse

def _parse_args():
    parser=argparse.ArgumentParser(description='Flip a coin and keep score.')
    parser.add_argument("-d","--debug",action="store_true",
                        help="Enable debugging")
    parser.add_argument("-x","--x","-X","--X",type=int,default=1,
                        help="Absolute value of needed X score")
    parser.add_argument("-y","--y","-Y","--Y",type=int,default=1,
                        help="Absolute value of needed Y score")
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
    r=IteratedFlipper.IteratedFlipper(x=x,y=y,trials=t,debug=args.debug)
    r.runtrials()
    print("x=%d, y=%d, t=%d:" % (x,y,t))
    print("Mean: %f ; Std Dev %f ; Variance %f" % (r.mean,r.stddev,r.variance))
    print("Winner: %s (%f)" % (r.winner,r.winfrac))
    
if __name__ == "__main__":
    main()

