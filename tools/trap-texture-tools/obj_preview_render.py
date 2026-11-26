import sys, numpy as np, math
from PIL import Image
obj,tex,out=sys.argv[1:4]; yaw=math.radians(float(sys.argv[4])); pitch=math.radians(float(sys.argv[5]))
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
V=np.vstack([V,V*[1,1,-1]]); F=F+[((a+90 if False else a+len(V)//2,ta),(c+len(V)//2,tc),(b+len(V)//2,tb)) for (a,ta),(b,tb),(c,tc) in F]  # mirror back half
tx=np.asarray(Image.open(tex).convert('RGB')).astype(float); TN=tx.shape[0]
c,s=math.cos(yaw),math.sin(yaw); R1=np.array([[c,0,s],[0,1,0],[-s,0,c]])
cp,sp=math.cos(pitch),math.sin(pitch); R2=np.array([[1,0,0],[0,cp,-sp],[0,sp,cp]])
P=(V-[0,300,0])@R1.T@R2.T
S=600; N=int(sys.argv[6]) if len(sys.argv)>6 else 700; sc=N*0.9/650
img=np.full((N,N,3),70.); zb=np.full((N,N),-1e9)
for (a,ta),(b,tb),(cc,tc) in F:
    q=P[[a,b,cc]]; uv=T[[ta,tb,tc]]
    X=N/2+q[:,0]*sc; Y=N/2-q[:,1]*sc; Z=q[:,2]
    x0,x1=int(max(0,X.min())),int(min(N-1,X.max())); y0,y1=int(max(0,Y.min())),int(min(N-1,Y.max()))
    if x1<x0 or y1<y0: continue
    gx,gy=np.meshgrid(np.arange(x0,x1+1)+.5,np.arange(y0,y1+1)+.5)
    den=(Y[1]-Y[2])*(X[0]-X[2])+(X[2]-X[1])*(Y[0]-Y[2])
    if abs(den)<1e-9: continue
    l1=((Y[1]-Y[2])*(gx-X[2])+(X[2]-X[1])*(gy-Y[2]))/den; l2=((Y[2]-Y[0])*(gx-X[2])+(X[0]-X[2])*(gy-Y[2]))/den; l3=1-l1-l2
    ins=(l1>=0)&(l2>=0)&(l3>=0)
    z=l1*Z[0]+l2*Z[1]+l3*Z[2]
    yy,xx=np.nonzero(ins); zz=z[yy,xx]; ok=zz>zb[yy+y0,xx+x0]
    yy,xx,zz=yy[ok],xx[ok],zz[ok]
    u=l1[yy,xx]*uv[0,0]+l2[yy,xx]*uv[1,0]+l3[yy,xx]*uv[2,0]; v=l1[yy,xx]*uv[0,1]+l2[yy,xx]*uv[1,1]+l3[yy,xx]*uv[2,1]
    px=np.clip((u*TN).astype(int),0,TN-1); py=np.clip(((1-v)*TN).astype(int),0,TN-1)
    img[yy+y0,xx+x0]=tx[py,px]; zb[yy+y0,xx+x0]=zz
Image.fromarray(img.clip(0,255).astype(np.uint8)).save(out)
