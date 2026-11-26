# heal horizontal seam (theta 0/180) in disc + force groove ring to a perfect circle
import sys, numpy as np
from PIL import Image
src=np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float); out=sys.argv[2]
H,W=src.shape[:2]
bg=np.median(src[:8].reshape(-1,3),0); m=np.abs(src-bg).sum(2)>40
ys,xs=np.nonzero(m); cx,cy=(xs.min()+xs.max())/2,(ys.min()+ys.max())/2
g=src.mean(2)
def bil(img,sx,sy):
    sx=np.clip(sx,0,W-1.001); sy=np.clip(sy,0,H-1.001); x0=sx.astype(int); y0=sy.astype(int); fx=(sx-x0)[...,None]; fy=(sy-y0)[...,None]
    return img[y0,x0]*(1-fx)*(1-fy)+img[y0,x0+1]*fx*(1-fy)+img[y0+1,x0]*(1-fx)*fy+img[y0+1,x0+1]*fx*fy
yy,xx=np.mgrid[0:H,0:W]; dx=xx-cx; dy=yy-cy; r=np.hypot(dx,dy); t=np.degrees(np.arctan2(dy,dx))%360
# 1) seam heal: within +-4deg of 0/180, for hub-edge..groove, replace with rotated samples (concentric texture)
def rot(deg):
    th=np.radians(t+deg); return bil(src,cx+r*np.cos(th),cy+r*np.sin(th))
dist=np.minimum.reduce([np.abs((t-a+180)%360-180) for a in (0,180)])
win=np.clip(1-dist/4,0,1)**0.7
side=np.where(((t+90)%360)<180,1,-1)  # pick sample side consistently
rep=0.5*rot(9)+0.5*rot(-9)
rmask=np.clip((r-190)/4,0,1)*np.clip((408-r)/4,0,1)
w=(win*rmask)[...,None]
img=src*(1-w)+rep*w
# 2) groove radius per angle -> warp to mean radius (affects r in 200..430 smoothly)
angs=np.arange(0,360,2.0); rg=[]
for a in np.radians(angs):
    rr=np.arange(370,425); x=cx+rr*np.cos(a); y=cy+rr*np.sin(a)
    v=bil(img,x,y).mean(1); rg.append(rr[v.argmin()])
rg=np.array(rg,float)
# smooth (circular)
k=np.ones(7)/7; rg=np.convolve(np.r_[rg[-3:],rg,rg[:3]],k,'valid')
R0=rg.mean(); print('groove radius before: min',rg.min(),'max',rg.max(),'-> target',round(R0,1))
rgt=np.interp(t,angs,rg,period=360)
# piecewise-linear radial map: output radius R0 samples source radius rgt; fixed at 200 and 440
r1,r2=200.0,440.0
sr=np.where(r<=R0, r1+(r-r1)*(rgt-r1)/(R0-r1), rgt+(r-R0)*(r2-rgt)/(r2-R0))
sr=np.where((r<r1)|(r>r2), r, sr)
th=np.radians(t); warped=bil(img,cx+sr*np.cos(th),cy+sr*np.sin(th))
Image.fromarray(warped.clip(0,255).astype(np.uint8)).save(out)
