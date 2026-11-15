import base64,sys,json
o=sys.argv[1]
c=json.load(open(sys.argv[2]))["colors"]
K=c["canvas"]; C=" ".join(str(int(K[i:i+2],16)) for i in (1,3,5))  # canvas as hex and as "r g b"
w=base64.b64encode(open(f"{o}/dith.webp","rb").read()).decode()
svg=("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='256' height='144' viewBox='0 0 256 144' preserveAspectRatio='none'%3E"
 "%3Cdefs%3E%3Cpattern id='p' width='1' height='1' patternUnits='userSpaceOnUse'%3E%3Ccircle cx='.5' cy='.5' r='.36' fill='%23fff'/%3E%3C/pattern%3E%3C/defs%3E"
 "%3Crect width='256' height='144' fill='%23000'/%3E%3Crect width='256' height='144' fill='url(%23p)'/%3E%3C/svg%3E")
ROOT=f':root{{--im-dots:url("{svg}");--im-pic:url("data:image/webp;base64,{w}");}}\n'
IMG='var(--im-dots) center/cover no-repeat fixed,var(--im-pic) center/cover no-repeat fixed,'+K
LANE=f'linear-gradient(90deg,transparent,rgb({C}/var(--im-lane,.8)) 16% 84%,transparent)'
FLOOR=f'linear-gradient(to top,rgb({C}/.97) 0,rgb({C}/.9) 22%,rgb({C}/0) 58%) fixed'
SPOT=f'radial-gradient(ellipse 30% 46% at 50% 38%,rgb({C}/.04) 0,rgb({C}/.4) 55%,rgb({C}/.88) 100%) fixed'
def sel(p,parts): return ",".join(p+x for x in parts)
COLS=['[data-chat-column]','[data-workspace-area="home"]','[data-settings-page-scroll]']
SB=['[data-slot="sidebar-inner"]']
def bg(p,parts,layers,n):
    bm=",".join(["normal"]*n+["multiply","normal"])
    return f'{sel(p,parts)}{{background:{",".join(layers+[IMG])}!important;background-blend-mode:{bm}!important;image-rendering:pixelated;}}\n'
D='.dark '; L=':root:not(.dark) '
css=ROOT
css+=bg(D,COLS,[LANE,SPOT],2)+bg(D,SB,[SPOT],1)
css+=bg(L,COLS,[LANE,FLOOR],2)+bg(L,SB,[FLOOR,f'linear-gradient(rgb({C}/.55),rgb({C}/.55)) fixed'],2)
css+=('[data-chat-column]:not(:has([data-timeline-row-kind])),[data-workspace-area="home"]{--im-lane:0;}\n'
 '[data-chat-column] *,[data-workspace-area="home"] *,[data-settings-page-scroll] *,[data-slot="sidebar-inner"] *{image-rendering:auto;}\n'
 '[data-chat-header],[data-chat-column] [data-workspace-area="conversation"],[data-chat-column] [data-workspace-area="home"]{background:transparent!important;}\n'
 '[data-workspace-area="conversation"] [data-timeline-loading]{background:transparent!important;}\n'
 '[data-workspace-area="conversation"],[data-workspace-area="home"],[data-slot="sidebar-inner"]{text-shadow:0 1px 3px rgb(0 0 0/.9),0 0 2px rgb(0 0 0/.8);}\n'
 '[data-chat-column] [class*="absolute inset-0 z-20 flex items-center"]{align-items:flex-end!important;padding-bottom:28px;}\n'
 '[class~="group/draft-hero"] h1>span:first-child{font-size:0!important;}\n'
 '[class~="group/draft-hero"] h1>span:first-child::before{content:"What should we blast";font-size:1.875rem;}\n'
 '[class~="group/draft-hero"] h1>span:first-child>span{font-size:1.875rem;}\n'
 '[data-slot="composer-context-strip"]{background:transparent!important;-webkit-backdrop-filter:none!important;backdrop-filter:none!important;}\n'
 '[data-chat-composer-form]{background:transparent!important;box-shadow:none!important;}\n'
 '[data-user-message-bubble]{border:1px solid rgb(242 184 75/.18)!important;}\n'
 '::selection{background:rgba(229,72,77,.35);}\n')
open(f"{o}/combo.css","w").write(css); print(len(css))
