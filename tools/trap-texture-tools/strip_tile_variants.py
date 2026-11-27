import numpy as np
from PIL import Image
src=np.asarray(Image.open('../../images/25.jpg').convert('RGB')).astype(float)
top=src[180:248]; slot=src[300:346]; bot=src[513:588]
P=212.5; TW=850; OV=15
def cell(strip,cx,flip):
    xs=np.arange(-(P/2+OV),P/2+OV,1.0)+cx
    x0=np.floor(xs).astype(int); f=(xs-x0)[None,:,None]
    c=strip[:,x0]*(1-f)+strip[:,x0+1]*f
    return c[:,::-1] if flip else c
def samp(strip,xs):
    x0=np.floor(xs).astype(int); f=(xs-x0)[None,:,None]
    return strip[:,x0]*(1-f)+strip[:,x0+1]*f
def assemble(strip,seq):
    X=np.arange(TW)+0.5
    out=np.zeros((strip.shape[0],TW,3)); wsum=np.zeros((1,TW,1))
    for i,(cx,fl) in enumerate(seq):
        lo=i*P-OV; hi=(i+1)*P+OV
        m=(X>=lo)&(X<hi)
        local=X[m]-(i*P+P/2)          # -P/2-OV .. P/2+OV
        if fl: local=-local
        c=samp(strip,cx+local)
        w=np.clip(np.minimum(X[m]-lo,hi-X[m])/(2*OV),0,1)
        out[:,m]+=c*w[None,:,None]; wsum[:,m]+=w[None,:,None]
    return out/np.maximum(wsum,1e-6)
def seam(strip,b=30):  # shared seam patch, centred on boundary between bolts 240 and 452
    return strip[:,346-b:346+b]
def finish(t,strip,b=30):
    S=seam(strip,b); w=np.linspace(1,0,b)[None,:,None]
    t[:,:b]=S[:,b:]*w+t[:,:b]*(1-w)
    t[:,-b:]=S[:,:b]*w[:,::-1]+t[:,-b:]*(1-w[:,::-1])
    return t
cellsT=[240,452,673,925,1138]; cellsB=[240,452,673,925,1137]
rng=np.random.default_rng(7)
plans=[ [(240,0),(452,0),(925,0),(1138,0)] ]  # V1 close to the current tile
for v in range(3):
    plans.append([(cellsT[i],int(rng.integers(2))) for i in rng.permutation(5)[:4]])
tiles=[]
for v,pt in enumerate(plans):
    pb=[(cellsB[cellsT.index(cx)], int(rng.integers(2))) for cx,_ in reversed(pt)]
    T=finish(assemble(top,pt),top); B=finish(assemble(bot,pb),bot)
    sl=np.repeat(slot[:,346:347],TW,1)*0+slot[:,:TW] if slot.shape[1]>=TW else None
    S=finish(slot[:,200:200+TW].copy(),slot)
    t=np.concatenate([T,S,B],0).clip(0,255).astype(np.uint8)
    Image.fromarray(t).save(f'rail_var{v+1}_850.png')
    Image.fromarray(t).resize((512,114),Image.LANCZOS).save(f'rail_var{v+1}_512.png')
    tiles.append(t); print('V',v+1,'top cells',pt,'bottom',pb)
# random-order preview: 8 tiles
order=[0,2,1,3,0,3,2,1]
Image.fromarray(np.concatenate([tiles[i] for i in order],1)).resize((512*8//2,57),Image.LANCZOS).save('variants_preview.png')
Image.fromarray(np.concatenate([tiles[i] for i in order],1)).save('variants_preview_full.png')
