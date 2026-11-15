# Fine dark dither: dots on a near-black grid, grey "off" dots, colour only in the art's bright areas.
# Usage: dither.py original.png outdir cols ncol spread dark
import sys, subprocess, os
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageOps
src,o=sys.argv[1],sys.argv[2]; cols,ncol=int(sys.argv[3]),int(sys.argv[4]); spread,dark=float(sys.argv[5]),float(sys.argv[6])
im=Image.open(src).convert("RGB")
im=ImageOps.mirror(im)  # Doom faces left, on the right side of the window
w0,h0=im.size; pad=round(h0*16/9)-w0
wide=Image.new("RGB",(w0+pad,h0),(0,0,0)); wide.paste(im,(pad,0)); im=wide  # widen to 16:9 with black on the left
W,H=im.size; rows=round(cols*H/W)
# background mask: near-black pixels connected to the image edges -> transparent, no dots
A=np.asarray(im,dtype=int)
mk=Image.fromarray(((A.sum(-1)<40)*255).astype(np.uint8)).copy()
for seed in [(0,0),(W-1,0),(0,H//2),(W-1,H//3)]:
    if mk.getpixel(seed)==255: ImageDraw.floodfill(mk,seed,128)
bg=np.asarray(mk.resize((cols,rows),Image.BOX))
bg=np.abs(bg.astype(int)-128)<24
im=ImageEnhance.Color(im).enhance(0.85).resize((cols,rows),Image.LANCZOS)
a=255*(np.asarray(im,dtype=float)/255)**1.25*dark
pal=np.array(Image.fromarray(a.astype(np.uint8)).quantize(ncol-1,method=Image.Quantize.MAXCOVERAGE).getpalette()[:(ncol-1)*3],dtype=float).reshape(-1,3)
pal=np.vstack([pal,[[38,38,38]],[[19,19,19]]])  # grey "off" dot, background (saved transparent)
B=np.array([[0,8,2,10],[12,4,14,6],[3,11,1,9],[15,7,13,5]])/16-0.47
t=np.tile(B,(rows//4+1,cols//4+1))[:rows,:cols,None]
a2=np.clip(a+t*spread,0,255)
idx=((a2[:,:,None,:]-pal[None,None])**2).sum(-1).argmin(-1)
idx[bg]=len(pal)-1
out=Image.fromarray(idx.astype(np.uint8),"P"); out.putpalette([int(v) for v in pal.flatten()])
out.save(f"{o}/dith.png",optimize=True,transparency=len(pal)-1)  # background shows the theme canvas
subprocess.run(["cwebp","-quiet","-lossless","-z","9",f"{o}/dith.png","-o",f"{o}/dith.webp"])
cell=4; rgb=out.convert("RGB").resize((cols*cell,rows*cell),Image.NEAREST)
m=Image.new("L",rgb.size,0); dr=ImageDraw.Draw(m)
for y in range(rows):
  for x in range(cols): dr.rectangle([x*cell+.6,y*cell+.6,x*cell+cell-1.4,y*cell+cell-1.4],fill=255)
Image.composite(rgb,Image.new("RGB",rgb.size,(8,7,10)),m).save(f"{o}/dith_preview.png")
print(cols,rows,"webp",os.path.getsize(f"{o}/dith.webp"))
