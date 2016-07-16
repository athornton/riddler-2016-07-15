#!/usr/bin/env python3
import IteratedFlipper
import argparse
import math

def _parse_args():
    parser=argparse.ArgumentParser(description='Flip a coin and keep score.')
    parser.add_argument("-d","--debug",action="store_true",
                        help="Enable debugging")
    parser.add_argument("-s","--statistics",action="store_true",
                        help="Enable statistics")
    parser.add_argument("-x","--x","-X","--X",type=int,default=1,
                        help="Absolute value of max X score")
    parser.add_argument("-y","--y","-Y","--Y",type=int,default=1,
                        help="Absolute value of max Y score")
    parser.add_argument("-t","--trials",type=int,default=100,
                        help="Number of trials")
    args=parser.parse_args()
    return args

# https://hflog.wordpress.com/2014/04/01/how-to-perform-a-chi-squared-goodness-of-fit-test-in-python/

def chisquare(obsv,expc):
    t=0
    for o, e in zip(obsv,expc):
        d = float(o) - float(e)
        t = t + (( d ** 2 ) / float(e))
    df=len(obsv) - 1
    return t,chisquarecdf(t,df)

def ilgf(s,z):
    val=0
    for k in range(0,100):
        val+=(((-1)**k)*z**(s+k))/(math.factorial(k)*(s+k))
     
    return val

def gf(x):
    upper_bound=100.0
    resolution=1000000.0
    step=upper_bound/resolution
    val=0
    rolling_sum=0
    while val<=upper_bound:
        rolling_sum+=step*(val**(x-1)*(math.exp(-val)))
        val+=step
    return rolling_sum

def chisquarecdf(x,k):
    return 1-ilgf(k/2,x/2)/gf(k/2)

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
    stat=args.statistics
    pred=[]
    ppr=[]
    obsv=[]
    opr=[]
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
            if stat:
                pred.append(pflips)
                obsv.append(r.mean)
                ppr.append(pfrac)
                kfrac=r.winfrac
                if r.winner != pwin:
                    kfrac = 1 - kfrac
                opr.append(kfrac)
    if stat:
        cs,p=chisquare(obsv,pred)
        csp,pp=chisquare(opr,ppr)
        print("Chi-squared values:")
        print("  mean flips %f (pval=%f) ; win prob. %f (pval=%f)" %
              (cs,p,csp,pp))
    
    
if __name__ == "__main__":
    main()

