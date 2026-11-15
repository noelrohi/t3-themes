import sys, io, base64
import numpy as np
from PIL import Image, ImageOps, ImageEnhance, ImageFilter, ImageDraw
src,o,cols,ncol,spread=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),float(sys.argv[5])
im=Image.open(src).convert("RGB"); W,H=im.size; rows=round(cols*H/W)
im=ImageOps.autocontrast(im.filter(ImageFilter.UnsharpMask(4,120,2)),cutoff=1)
im=ImageEnhance.Color(im).enhance(1.35).resize((cols,rows),Image.LANCZOS)
a=255*(np.asarray(im,dtype=float)/255)**1.6; im=Image.fromarray(a.astype(np.uint8))
pal=np.array(im.quantize(ncol,method=Image.Quantize.MEDIANCUT).getpalette()[:ncol*3],dtype=float).reshape(-1,3)
# darkest palette entry -> dim grey "off" dot
d=pal.sum(1).argmin(); pal[d]=[40,37,48]
B=np.array([[0,8,2,10],[12,4,14,6],[3,11,1,9],[15,7,13,5]])/16-0.47
t=np.tile(B,(rows//4+1,cols//4+1))[:rows,:cols,None]
a2=np.clip(a+t*spread,0,255)
idx=((a2[:,:,None,:]-pal[None,None])**2).sum(-1).argmin(-1)
out=Image.fromarray(idx.astype(np.uint8),"P"); out.putpalette([int(v) for v in pal.flatten()])
out.save(f"{o}/dith.png",optimize=True)
import subprocess; subprocess.run(["cwebp","-quiet","-lossless","-z","9",f"{o}/dith.png","-o",f"{o}/dith.webp"])
rgb=out.convert("RGB"); cell=6
big=rgb.resize((cols*cell,rows*cell),Image.NEAREST)
m=Image.new("L",big.size,0); dr=ImageDraw.Draw(m)
for y in range(rows):
  for x in range(cols):
    cx,cy=(x+.5)*cell,(y+.5)*cell; r=cell*.36; dr.ellipse([cx-r,cy-r,cx+r,cy+r],fill=255)
Image.composite(big,Image.new("RGB",big.size,0),m).save(f"{o}/dith_preview.png")
import os
print(cols,rows,"png",os.path.getsize(f"{o}/dith.png"),"webp",os.path.getsize(f"{o}/dith.webp"))
