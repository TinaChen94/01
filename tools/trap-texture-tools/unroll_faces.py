# mode guide : draw 4 faces (1..4 left->right) side by side, each face-on
# mode bake  : bake painted strips into the model UV
import sys, math, numpy as np
from PIL import Image, ImageDraw, ImageFont
mode=sys.argv[1]
V=[];T=[];F=[];FP=[]
for ln in open('in/TrapB.obj'):
    p=ln.split()
    if not p: continue
    if p[0]=='v': V.append([float(x) for x in p[1:4]])
    elif p[0]=='vt': T.append([float(x) for x in p[1:3]])
    elif p[0]=='f':
        idx=[(int(q.split('/')[0])-1,int(q.split('/')[1])-1) for q in p[1:]]; FP.append(idx)
        for k in range(1,len(idx)-1): F.append((idx[0],idx[k],idx[k+1]))
V=np.array(V);T=np.array(T)
W,H=1024,1536; top,bot=60,1500; y0=V[:,1].min(); sc=(bot-top)/(V[:,1].max()-y0)
SXK=2.0
CX=[W*(i+0.5)/4 for i in range(4)]            # strip centers for faces 1..4
FA=[157.5,112.5,67.5,22.5]                     # face normal azimuths, left->right as seen from front
def face_of(n):
    az=math.degrees(math.atan2(n[2],n[0]))%360
    return int(np.argmin([abs((az-f+180)%360-180) for f in FA]))
def to_strip(Q,k):
    r=math.radians(90-FA[k]); R=np.array([[math.cos(r),0,-math.sin(r)],[0,1,0],[math.sin(r),0,math.cos(r)]])
    Qr=Q@R.T; return CX[k]+Qr[...,0]*sc*SXK, bot-(Qr[...,1]-y0)*sc
if mode=='guide':
    im=Image.new('RGB',(W,H),(128,128,128)); d=ImageDraw.Draw(im)
    fnt=ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',48)
    for f in FP:
        P=V[[a for a,_ in f]]; n=np.cross(P[1]-P[0],P[2]-P[0]); n/=np.linalg.norm(n)+1e-9
        if abs(n[1])>0.9: continue
        k=face_of(n); x,y=to_strip(P,k); pts=list(zip(x,y))
        b=int(150+40*n[1]); d.polygon(pts,fill=(b,b-15,b-35))
        for i in range(len(pts)): d.line([pts[i],pts[(i+1)%len(pts)]],fill=(235,195,110),width=3)
    im.save('spike_unroll_guide.png')
    lab=im.copy(); dl=ImageDraw.Draw(lab)
    for i in range(4): dl.text((CX[i],20),str(i+1),fill=(255,40,40),font=fnt,anchor='mt')
    lab.save('spike_unroll_guide_labeled.png'); print('ok')
else:
    from scipy import ndimage as nd
    src=np.asarray(Image.open(sys.argv[2]).convert('RGB')).astype(float); Hs,Ws=src.shape[:2]
    sx_,sy_=Ws/W,Hs/H; N=1024; out=sys.argv[3]
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
            x,y=to_strip(Q,face_of(n)); x=np.clip(x*sx_,0,Ws-1.001); y=np.clip(y*sy_,0,Hs-1.001)
            ix=x.astype(int); iy=y.astype(int); fx=(x-ix)[...,None]; fy=(y-iy)[...,None]
            col=src[iy,ix]*(1-fx)*(1-fy)+src[iy,ix+1]*fx*(1-fy)+src[iy+1,ix]*(1-fx)*fy+src[iy+1,ix+1]*fx*fy
        yy,xx=np.nonzero(ins); img[yy+ya,xx+xa]=col[yy,xx]; filled[yy+ya,xx+xa]=True
    for _ in range(8):
        g=nd.binary_dilation(filled)&~filled
        if not g.any(): break
        acc=np.zeros_like(img); cnt=np.zeros((N,N))
        for dy,dx in [(-1,0),(1,0),(0,-1),(0,1)]:
            sh=np.roll(np.roll(filled,dy,0),dx,1); acc+=np.roll(np.roll(img,dy,0),dx,1)*sh[...,None]; cnt+=sh
        nv=g&(cnt>0); img[nv]=acc[nv]/cnt[nv][:,None]; filled|=nv
    img[~filled]=dark; Image.fromarray(img.clip(0,255).astype(np.uint8)).save(out); print('saved',out)
