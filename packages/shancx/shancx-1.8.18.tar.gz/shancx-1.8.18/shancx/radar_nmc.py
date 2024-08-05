
import matplotlib.pyplot as plt
import datetime
from hjnwtx.colormap import cmp_hjnwtx
import os

def mkDir(path):
    if "." in path:
        os.makedirs(os.path.dirname(path),exist_ok=True)
    else:
        os.makedirs(path, exist_ok=True)

def drawpic(array_dt,temp = "temp"):
    now_str = datetime.datetime.now().strftime("%Y%m%d%H%M")
    if len(array_dt.shape)==3:
        for i , img_ch_nel in enumerate(array_dt): 
            plt.imshow(img_ch_nel,vmin=0,vmax=100,cmap=cmp_hjnwtx["radar_nmc"])
            plt.colorbar()
            outpath = f"./radar_nmc/{temp}_{now_str}.png"
            mkDir(outpath)
            plt.savefig(outpath)
            plt.close()
    if len(array_dt.shape)==2:
            plt.imshow(array_dt,vmin=0,vmax=100,cmap=cmp_hjnwtx["radar_nmc"])
            plt.colorbar()
            outpath = f"./radar_nmc/{temp}_{now_str}.png"
            mkDir(outpath)
            plt.savefig(outpath)
            plt.close() 
 
print("done")