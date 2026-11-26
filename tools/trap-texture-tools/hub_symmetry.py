import sys, numpy as np
from PIL import Image
src=np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float); out=sys.argv[2]
N=int(sys.argv[3]); th0=float(sys.argv[4]); rmax=float(sys.argv[5])
H,W=src.shape[:2]; bg=np.median(src[:8].reshape(-1,3),0); m=np.abs(src-bg).sum(2)>40
ys,xs=np.nonzero(m); cx,cy=(xs.min()+xs.max())/2,(ys.min()+ys.max())/2
yy,xx=np.mgrid[0:H,0:W]; r=np.hypot(xx-cx,yy-cy); t=np.degrees(np.arctan2(yy-cy,xx-cx))%360
Wd=360/N; rel=(t-th0)%Wd
def samp(theta):
    th=np.radians(theta); sx=np.clip(cx+r*np.cos(th),0,W-1.001); sy=np.clip(cy+r*np.sin(th),0,H-1.001)
    x0=sx.astype(int); y0=sy.astype(int); fx=(sx-x0)[...,None]; fy=(sy-y0)[...,None]
    return src[y0,x0]*(1-fx)*(1-fy)+src[y0,x0+1]*fx*(1-fy)+src[y0+1,x0]*(1-fx)*fy+src[y0+1,x0+1]*fx*fy
A=samp(th0+rel); B=samp(th0+rel-Wd); d=3; w=np.clip((rel-(Wd-d))/d,0,1)[...,None]
rep=A*(1-w)+B*w
k=np.clip((rmax-r)/4,0,1)[...,None]
Image.fromarray((src*(1-k)+rep*k).clip(0,255).astype(np.uint8)).save(out)
print('center',cx,cy)
