
import napari
from dask_image.imread import imread
import tifffile

import dask.array as da
import numpy as np
from dask.diagnostics import ProgressBar
from tqdm.dask import TqdmCallback







# # path = r"C:\Users\turnerp\Desktop\GapSeq2 Presentation\Sequencing\GAPSeqCompetitveDegen7nt_Degen7ntSeal80nMcompseal500nML532L638Exp200.tif"
# # path = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Rasched-Hafez\KK NIM\240104 rpoDPAM richM9 CCNIM\rpoDPAM rich M9_rpoDPAM richM9 FOV2-1.tif"
path = r"G:\rpoDPAM rich M9_rpoDPAM richM9 FOV2-1.tif"

# Create a Dask array from your file
# dask_array = da.from_array(path)

# viewer = napari.Viewer()
# viewer = napari.view_image(dask_array)


stack = imread(path)
cropped = stack[:10,:,:stack.shape[1] // 2]

# image = np.array(cropped)

# with TqdmCallback(desc="Computing"):
#     image = cropped.compute()



viewer = napari.view_image(cropped)


# stack = tifffile.imread(path)

# napari.view_image(stack, contrast_limits=[0,2000], multiscale=False)

