# Fine dark dither: dots on a near-black grid, grey "off" dots, colour only in the art's bright areas.
# Usage: dither.py original.png outdir cols ncol spread dark
import sys, subprocess, os
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance
src,o=sys.argv[1],sys.argv[2]; cols,ncol=int(sys.argv[3]),int(sys.argv[4]); spread,dark=float(sys.argv[5]),float(sys.argv[6])
im=Image.open(src).convert("RGB"); W,H=im.size; rows=round(cols*H/W)
# background mask: the flat purple field -> Whirl canvas, no dots
A=np.asarray(im,dtype=int); r,g,b=A[...,0],A[...,1],A[...,2]
purple=(r>60)&(r<125)&(g<30)&(b>60)&(b<110)
mk=Image.fromarray((purple*255).astype(np.uint8))
bg=np.asarray(mk.resize((cols,rows),Image.BOX))>127
im=ImageEnhance.Color(im).enhance(0.85).resize((cols,rows),Image.LANCZOS)
a=255*(np.asarray(im,dtype=float)/255)**1.25*dark
pal=np.array(Image.fromarray(a.astype(np.uint8)).quantize(ncol-1,method=Image.Quantize.MAXCOVERAGE).getpalette()[:(ncol-1)*3],dtype=float).reshape(-1,3)
pal=np.vstack([pal,[[38,38,38]],[[19,19,19]]])  # grey "off" dot, Whirl canvas background
B=np.array([[0,8,2,10],[12,4,14,6],[3,11,1,9],[15,7,13,5]])/16-0.47
t=np.tile(B,(rows//4+1,cols//4+1))[:rows,:cols,None]
a2=np.clip(a+t*spread,0,255)
idx=((a2[:,:,None,:]-pal[None,None])**2).sum(-1).argmin(-1)
idx[bg]=len(pal)-1
out=Image.fromarray(idx.astype(np.uint8),"P"); out.putpalette([int(v) for v in pal.flatten()])
out.save(f"{o}/dith.png",optimize=True)
subprocess.run(["cwebp","-quiet","-lossless","-z","9",f"{o}/dith.png","-o",f"{o}/dith.webp"])
cell=4; rgb=out.convert("RGB").resize((cols*cell,rows*cell),Image.NEAREST)
m=Image.new("L",rgb.size,0); dr=ImageDraw.Draw(m)
for y in range(rows):
  for x in range(cols): dr.rectangle([x*cell+.6,y*cell+.6,x*cell+cell-1.4,y*cell+cell-1.4],fill=255)
Image.composite(rgb,Image.new("RGB",rgb.size,(8,7,10)),m).save(f"{o}/dith_preview.png")
print(cols,rows,"webp",os.path.getsize(f"{o}/dith.webp"))
