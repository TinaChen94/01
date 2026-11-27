# usage: radial2.py src.png N k out.png [band_inner_radius]
import sys, numpy as np
from PIL import Image
src=np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float)
N=int(sys.argv[2]); k=int(sys.argv[3]); out=sys.argv[4]; W=360/N
H,Wd=src.shape[:2]
bg=np.median(np.concatenate([src[:8].reshape(-1,3),src[-8:].reshape(-1,3)]),0)
m=np.abs(src-bg).sum(2)>40; m[:3]=m[-3:]=False; m[:,:3]=m[:,-3:]=False
ys,xs=np.nonzero(m); cx,cy=(xs.min()+xs.max())/2,(ys.min()+ys.max())/2
ang=np.arange(0,360,0.5); R=[]
for t in np.radians(ang):
    r=np.arange(250,min(H,Wd)//2+20)
    x=(cx+r*np.cos(t)).astype(int); y=(cy+r*np.sin(t)).astype(int)
    ok=(x>=0)&(x<Wd)&(y>=0)&(y<H); idx=np.nonzero(m[y[ok],x[ok]])[0]
    R.append(r[ok][idx.max()] if len(idx) else 0)
R=np.array(R); thr=(R.max()+R.min())/2
mins=[i for i in range(len(R)) if R[i]==R[np.arange(i-12,i+13)%len(R)].min() and R[i]<thr]
g=[]
for i in mins:
    if not g or ang[i]-ang[g[-1]]>8: g.append(i)
print('center',cx,cy,'Rmax',R.max(),'Rmin',R.min(),'gullets',len(g))
th0=ang[g[k%len(g)]]; th1=ang[g[(k+1)%len(g)]]; Ws=(th1-th0)%360; print('src tooth width',Ws)
yy,xx=np.mgrid[0:H,0:Wd]; r=np.hypot(xx-cx,yy-cy); t=np.degrees(np.arctan2(yy-cy,xx-cx))%360
rel=(t-th0)%W
def samp(theta):
    th=np.radians(theta)
    sx=np.clip(cx+r*np.cos(th),0,Wd-1); sy=np.clip(cy+r*np.sin(th),0,H-1)
    x0=np.floor(sx).astype(int); y0=np.floor(sy).astype(int)
    x1=np.minimum(x0+1,Wd-1); y1=np.minimum(y0+1,H-1); fx=(sx-x0)[...,None]; fy=(sy-y0)[...,None]
    return src[y0,x0]*(1-fx)*(1-fy)+src[y0,x1]*fx*(1-fy)+src[y1,x0]*(1-fx)*fy+src[y1,x1]*fx*fy
A=samp(th0+rel*Ws/W); B=samp(th0+Ws+(rel-W)*Ws/W)
d=1.5; w=np.clip((rel-(W-d))/d,0,1)[...,None]; rep=A*(1-w)+B*w
rr=float(sys.argv[5]) if len(sys.argv)>5 else R.min()-30
rad=np.clip((r-(rr-4))/8,0,1)[...,None]
Image.fromarray((src*(1-rad)+rep*rad).clip(0,255).astype(np.uint8)).save(out)
print('band from r',rr)
