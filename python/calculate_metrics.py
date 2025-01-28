import numpy as np
import pydicom
from utils import get_roi_circles, calculate_geom_dist, plot_circles, get_snr_cnr, plot_rects

# T1 flat
filename = "../data/T1_flat.dcm"
slc = 18
threshold = 0.3*0.4
circle_circumference_threshold = 0.4
min_pixel_x = 50
min_pixel_y = 40
max_pixel_x = 60
max_pixel_y = 115
mm_pixel = 1.6
noise_rects = [[(5, 10), (5, 10)], [(5, 10), (112 - 15, 10)]]
signal_rect = [(58, 5), (53, 5)]

# T2 domed
filename = "../data/T2_domed.dcm"
slc = 15
threshold = 0.25
circle_circumference_threshold = 0.5
min_pixel_x = 55
min_pixel_y = 40
max_pixel_x = 60
max_pixel_y = 115
mm_pixel = 1.5
noise_rects = [[(5, 10), (5, 10)], [(5, 10), (120 - 15, 10)]]
signal_rect = [(59, 5), (38, 5)]

# T2 flat
filename = "../data/T2_flat.dcm"
slc = 17
threshold = 0.3
circle_circumference_threshold = 0.4
min_pixel_x = 55
min_pixel_y = 40
max_pixel_x = 60
max_pixel_y = 115
mm_pixel = 1.5
noise_rects = [[(5, 10), (5, 10)], [(5, 10), (120 - 15, 10)]]
signal_rect = [(63, 5), (40, 5)]

# T1 domed
filename = "../data/T1_domed.dcm"
slc = 17
threshold= 0.35*0.4
circle_circumference_threshold = 0.5
min_pixel_x = 50
min_pixel_y = 40
max_pixel_x = 60
max_pixel_y = 115
mm_pixel = 1.6
noise_rects = [[(5, 10), (5, 10)], [(5, 10), (112 - 15, 10)]]
signal_rect = [(56, 5), (50, 5)]


ds = pydicom.dcmread(filename)
im = ds.pixel_array[slc, :, :]

circles = get_roi_circles(im, threshold, circle_circumference_threshold, min_pixel_x, min_pixel_y, max_pixel_x, max_pixel_y)
print("Circles:", circles)
f, ax = plot_circles(im, circles)
distances = calculate_geom_dist(circles, mm_pixel)
print("Distances:", distances, "mean", np.mean(distances))

snr, cnr = get_snr_cnr(im, noise_rects, signal_rect)
print("SNR:", snr, "CNR:", cnr)
f, ax = plot_rects(im, noise_rects, signal_rect, ax=ax)

