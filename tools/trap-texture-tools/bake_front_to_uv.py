# Bake a corner-front orthographic elevation onto the model, taking every face
# from the nearest CENTER face (faces 2/3) -> no side-face stretching.
import sys, math, numpy as np
from PIL import Image
from scipy import ndimage as nd
obj,imgp,hwp,out=sys.argv[1:5]; N=int(sys.argv[5])
V=[];T=[];F=[]
for ln in open(obj):
    p=ln.split()
    if not p: continue
    if p[0]=='v': V.append([float(x) for x in p[1:4]])
    elif p[0]=='vt': T.append([float(x) for x in p[1:3]])
    elif p[0]=='f':
        idx=[(int(q.split('/')[0])-1,int(q.split('/')[1])-1) for q in p[1:]]
        for k in range(1,len(idx)-1): F.append((idx[0],idx[k],idx[k+1]))
V=np.array(V);T=np.array(T)
src=np.asarray(Image.open(imgp).convert('RGB')).astype(float); Hs,Ws=src.shape[:2]; HW=np.load(hwp)
top,bot,cx=16,994,511.5
mlo,mhi=V[:,1].min(),V[:,1].max()
HM=np.array([[0,.006],[.057,.035],[.067,.041],[.183,.163],[.191,.169],[.324,.299],[.333,.309],[.486,.450],[.494,.460],
             [.587,.583],[.627,.604],[.830,.827],[.867,.854],[1,1]])
hs=np.round(V[:,1],3); rh=np.unique(hs); rr=np.array([np.hypot(V[hs==h][:,0],V[hs==h][:,2]).max() for h in rh])
def to_img(Q):
    f=(Q[...,1]-mlo)/(mhi-mlo); fi=np.interp(f,HM[:,0],HM[:,1]); y=bot-fi*(bot-top)
    row=np.clip(y.astype(int),0,Hs-1); r=np.maximum(np.interp(Q[...,1],rh,rr),1e-3)
    return cx+Q[...,0]/r*np.maximum(HW[row]-1.5,0), y
dark=np.array([20,18,26.]); img=np.zeros((N,N,3)); filled=np.zeros((N,N),bool)
for tri in F:
    vi=[a for a,_ in tri]; ti=[b for _,b in tri]; P=V[vi]
    n=np.cross(P[1]-P[0],P[2]-P[0]); nn=np.linalg.norm(n)
    if nn==0: continue
    n/=nn; UV=T[ti]*N; UV[:,1]=N-UV[:,1]
    xa,ya=np.floor(UV.min(0)).astype(int); xb,yb=np.ceil(UV.max(0)).astype(int)
    xa,ya=max(xa,0),max(ya,0); xb,yb=min(xb,N-1),min(yb,N-1)
    if xb<xa or yb<ya: continue
    gx,gy=np.meshgrid(np.arange(xa,xb+1)+.5,np.arange(ya,yb+1)+.5)
    a,b,c=UV; den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
    if abs(den)<1e-9: continue
    l1=((b[1]-c[1])*(gx-c[0])+(c[0]-b[0])*(gy-c[1]))/den; l2=((c[1]-a[1])*(gx-c[0])+(a[0]-c[0])*(gy-c[1]))/den; l3=1-l1-l2
    ins=(l1>=-1e-4)&(l2>=-1e-4)&(l3>=-1e-4)
    if not ins.any(): continue
    Q=l1[...,None]*P[0]+l2[...,None]*P[1]+l3[...,None]*P[2]
    if n[1]<-0.9: col=np.broadcast_to(dark,Q.shape)
    else:
        az=math.degrees(math.atan2(n[2],n[0]))%360
        fa=22.5+45*round((az-22.5)/45); tgt=67.5 if fa<90 else 112.5
        r=math.radians(tgt-fa)                      # rotate about Y by +r (azimuth increases)
        R=np.array([[math.cos(r),0,-math.sin(r)],[0,1,0],[math.sin(r),0,math.cos(r)]])
        x,y=to_img(Q@R.T)
        if fa in (22.5,157.5):           # side faces: skip the painted V-chevron at each tier bottom
            for J in (951,830,697,550):
                vh=0.42*HW[J-8]; z=(y>J-vh)&(y<J-4); y=np.where(z,J-vh-2,y)
        x=np.clip(x,0,Ws-1.001); y=np.clip(y,0,Hs-1.001)
        ix=x.astype(int); iy=y.astype(int); fx=(x-ix)[...,None]; fy=(y-iy)[...,None]
        col=src[iy,ix]*(1-fx)*(1-fy)+src[iy,ix+1]*fx*(1-fy)+src[iy+1,ix]*(1-fx)*fy+src[iy+1,ix+1]*fx*fy
        if fa in (22.5,157.5): col=col*np.array([0.69,0.73,0.88])
    yy,xx=np.nonzero(ins); img[yy+ya,xx+xa]=col[yy,xx]; filled[yy+ya,xx+xa]=True
for _ in range(int(8*N/1024)):
    g=nd.binary_dilation(filled)&~filled
    if not g.any(): break
    acc=np.zeros_like(img); cnt=np.zeros((N,N))
    for dy,dx in [(-1,0),(1,0),(0,-1),(0,1)]:
        sh=np.roll(np.roll(filled,dy,0),dx,1); acc+=np.roll(np.roll(img,dy,0),dx,1)*sh[...,None]; cnt+=sh
    nv=g&(cnt>0); img[nv]=acc[nv]/cnt[nv][:,None]; filled|=nv
img[~filled]=dark; Image.fromarray(img.clip(0,255).astype(np.uint8)).save(out); print('saved',out)
