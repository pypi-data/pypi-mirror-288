import cv2
import numpy as np
import tifffile
from napari.utils.notifications import show_info
from roifile import ImagejRoi, roiread
import matplotlib.pyplot as plt
import traceback



def read_imagej_file(path, image, widget_notifications=True):
    
    contours = []
    mask = np.zeros(image.shape[-2:])
    
    # reads overlays sequentially and then converts them to openCV contours
    try:
        for roi in roiread(path):
            coordinates = roi.integer_coordinates

            top = roi.top
            left = roi.left

            coordinates[:, 1] = coordinates[:, 1] + top
            coordinates[:, 0] = coordinates[:, 0] + left

            cnt = np.array(coordinates).reshape((-1, 1, 2)).astype(np.int32)
            contours.append(cnt)

        for i in range(len(contours)):
            cnt = contours[i]
            cv2.drawContours(
                mask,
                [cnt],
                contourIdx=-1,
                color=(i + 1, i + 1, i + 1),
                thickness=-1,
            )
    except:
        print(traceback.format_exc())
        if widget_notifications:
            show_info("Image does not contain ImageJ Overlays")

    return mask


def export_imagej(image, contours, metadata, file_path):
    overlays = []

    for i in range(len(contours) - 1):
        try:
            cnt = contours[i]
            cnt = np.vstack(cnt).squeeze()
            roi = ImagejRoi.frompoints(cnt)
            roi = roi.tobytes()

            overlays.append(roi)

        except:
            pass

    tifffile.imwrite(
        file_path,
        image,
        imagej=True,
        metadata={"Overlays": overlays, "metadata": metadata},
    )




path = r"C:\Users\turnerp\Desktop\220610_JR-NIM_Chitosan_WT_AQ1_posXY0_channels_t0_posZ0_colour0.tif"

image = tifffile.imread(path)


mask = read_imagej_file(path, image)


plt.imshow(mask)
plt.show()





