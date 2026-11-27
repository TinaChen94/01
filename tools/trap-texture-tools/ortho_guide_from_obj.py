import numpy as np, math
from PIL import Image, ImageDraw
V0=np.array([[float(x) for x in l.split()[1:4]] for l in open('in/TrapB.obj') if l.startswith('v ')])
F=[[int(q.split('/')[0])-1 for q in l.split()[1:]] for l in open('in/TrapB.obj') if l.startswith('f ')]
# full model: mirror back half (z -> -z)
n=len(V0); V=np.vstack([V0,V0*[1,1,-1]]); F=F+[[i+n for i in f[::-1]] for f in F]
a=math.radians(22.5); R=np.array([[math.cos(a),0,math.sin(a)],[0,1,0],[-math.sin(a),0,math.cos(a)]])
V=V@R.T                      # rotate so a FACE points at the camera (+z)
W,H=1024,1536; top,bot=60,1500; sc=(bot-top)/(V[:,1].max()-V[:,1].min()); y0=V[:,1].min()
X=lambda p:(W/2+p[0]*sc, bot-(p[1]-y0)*sc)
im=Image.new('RGB',(W,H),(128,128,128)); d=ImageDraw.Draw(im); faces=[]
for f in F:
    P=V[f]; nn=np.cross(P[1]-P[0],P[2]-P[0]); nn/= (np.linalg.norm(nn)+1e-9)
    if nn[2]>0.02: faces.append((P[:,2].mean(),f,nn))
for _,f,nn in sorted(faces,key=lambda t:t[0]):
    b=int(60+70*nn[2]+25*nn[1]); d.polygon([X(V[i]) for i in f],fill=(b+20,b,b-15))
for _,f,nn in faces:
    pts=[X(V[i]) for i in f]
    for i in range(len(pts)): d.line([pts[i],pts[(i+1)%len(pts)]],fill=(235,195,110),width=3)
im.save('spike_ortho_guide_face.png'); print('scale',sc)
