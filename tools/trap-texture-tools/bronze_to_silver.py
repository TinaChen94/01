import sys, numpy as np
from PIL import Image
from skimage import color
src,out=sys.argv[1:3]
a=np.asarray(Image.open(src).convert('RGB')).astype(float)/255
lab=color.rgb2lab(a); L,A,B=lab[...,0],lab[...,1],lab[...,2]
# bronze chroma axis from the warm pixels
warm=(B>15)&(L>25)
ax=np.array([A[warm].mean(),B[warm].mean()]); ax/=np.linalg.norm(ax)
pr=A*ax[0]+B*ax[1]                       # bronze component
ox,oy=A-pr*ax[0],B-pr*ax[1]              # orthogonal component (blue-violet ambient etc.) -> kept
keep=0.12                                # a hint of warm reflected light
k=np.where(pr>0,keep,1.0)                # only strip the bronze (positive) side
sh=np.clip((70-L)/50,0,1); hl=np.clip((L-60)/25,0,1); S=1.8*(1-hl)+0.3*hl; ox=np.where(ox<0,ox*(1-hl),ox)
A2=ox*S+pr*k*ax[0]+5*sh; B2=oy*S+pr*k*ax[1]-12*sh
# silver tone: lift mids, keep darks, stronger specular-looking highlights
Ln=L/100; L2=100*np.clip(Ln**0.85*1.08,0,1)
hi=np.clip((Ln-0.55)/0.35,0,1); L2=L2+(100-L2)*hi*0.35
res=color.lab2rgb(np.stack([L2,A2,B2],-1))
Image.fromarray((np.clip(res,0,1)*255).astype(np.uint8)).save(out); print('axis',ax)
