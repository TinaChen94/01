# make the steel hub perfectly round & concentric (RGBA safe)
import sys, numpy as np
from PIL import Image
im=Image.open(sys.argv[1]).convert('RGBA'); A=np.asarray(im).astype(float); out=sys.argv[2]
rgb=A[...,:3]; H,W=rgb.shape[:2]
sat=rgb.max(2)-rgb.min(2)
cx0,cy0=(W-1)/2,(H-1)/2
# 1) fit circle to steel outer edge
pts=[]
for t in np.radians(np.arange(0,360,2)):
    r=np.arange(H*0.12,H*0.26,0.25); x=cx0+r*np.cos(t); y=cy0+r*np.sin(t)
    s=sat[y.astype(int),x.astype(int)]; i=np.nonzero(s>35)[0]
    if len(i): pts.append((x[i[0]],y[i[0]]))
P=np.array(pts); M=np.c_[2*P,np.ones(len(P))]; b=(P**2).sum(1)
hx,hy,c=np.linalg.lstsq(M,b,rcond=None)[0]; R=np.sqrt(c+hx*hx+hy*hy)
print('hub fit center',round(hx,2),round(hy,2),'R',round(R,2),'(blade center',cx0,cy0,')')
# use blade center for final (hub concentric with blade), sample from fitted hub center
yy,xx=np.mgrid[0:H,0:W]; r=np.hypot(xx-cx0,yy-cy0); t=np.degrees(np.arctan2(yy-cy0,xx-cx0))%360
def samp(theta,rad):
    th=np.radians(theta); sx=np.clip(hx+rad*np.cos(th),0,W-1.001); sy=np.clip(hy+rad*np.sin(th),0,H-1.001)
    x0=sx.astype(int); y0=sy.astype(int); fx=(sx-x0)[...,None]; fy=(sy-y0)[...,None]
    return A[y0,x0]*(1-fx)*(1-fy)+A[y0,x0+1]*fx*(1-fy)+A[y0+1,x0]*(1-fx)*fy+A[y0+1,x0+1]*fx*fy
# 2) ring band: averaged radial profile from one clean 12deg wedge
th0v=float(sys.argv[4]); ri=float(sys.argv[3])*R
rs=np.arange(0,R+6,0.25); angs=np.arange(th0v,th0v+12,0.5)
prof=np.zeros((len(rs),4))
for a in angs:
    th=np.radians(a); sx=hx+rs*np.cos(th); sy=hy+rs*np.sin(th)
    x0=sx.astype(int); y0=sy.astype(int); fx=(sx-x0)[:,None]; fy=(sy-y0)[:,None]
    prof+=A[y0,x0]*(1-fx)*(1-fy)+A[y0,x0+1]*fx*(1-fy)+A[y0+1,x0]*(1-fx)*fy+A[y0+1,x0+1]*fx*fy
prof/=len(angs)
ring=np.stack([np.interp(r,rs,prof[:,c]) for c in range(4)],-1)
# restore low-frequency angular sheen from original (sampled around fitted center)
orig=samp(t,r)
def angprof(img):
    L=img[...,:3].mean(2); band=(r>ri)&(r<R-2); bins=(t[band]/2).astype(int)%180
    s=np.bincount(bins,L[band],180)/np.maximum(np.bincount(bins,None,180),1)
    k=np.ones(9)/9; s=np.convolve(np.r_[s[-4:],s,s[:4]],k,'valid'); return s
ratio=angprof(orig)/np.maximum(angprof(ring),1)
rt=np.interp(t,np.arange(0,360,2)+1,ratio,period=360)[...,None]
ring[...,:3]*=rt
# 3) inner bolt area: 6-fold symmetry
N6=6; W6=60; th6=float(sys.argv[5]); rel6=(t-th6)%W6
inA=samp(th6+rel6,r); inB=samp(th6+rel6-W6,r); w6=np.clip((rel6-(W6-3))/3,0,1)[...,None]
inner=inA*(1-w6)+inB*w6
# compose: inner (r<ri) | ring (ri..R+1.5) | original outside (feathered)
kin=np.clip((ri+1.5-r)/3,0,1)[...,None]
new=inner*kin+ring*(1-kin)
kout=np.clip((R+2.5-r)/2,0,1)[...,None]
res=A*(1-kout)+new*kout
Image.fromarray(res.clip(0,255).astype(np.uint8),'RGBA').save(out)
