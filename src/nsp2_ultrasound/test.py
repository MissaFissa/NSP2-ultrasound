import matplotlib.pyplot as plt
import numpy as np
import click
import matplotlib
import pandas as pd
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import matplotlib.tri as mtri
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
from scipy.spatial import Delaunay
from matplotlib.ticker import MultipleLocator
from mpl_toolkits.mplot3d.axes3d import get_test_data
from scipy.interpolate import griddata

from nsp2_ultrasound.model import UltrasonicExperiment

experiment = UltrasonicExperiment(60, 170)
experiment.scan("aluminium")

times = experiment.all_times
amps = experiment.all_amps
adjusted_signals = experiment.adjusted_signals_all
times_water = experiment.all_times_water
time = times[0]
time_water = times_water[0]
positions = experiment.positions
positions_cm = experiment.positions_cm
envelopes = experiment.amplitude_envelope_all
envelopes_water = experiment.amplitude_envelope_all_water

positions_cm = [i / 10 for i in positions]

positions_cm_500 = []

for i in positions_cm:

    positions_cm_500.append(500 * [i])

depths = [i * experiment.constant_water for i in time] 
depths_water = [i * experiment.constant_water for i in time_water]

depths_12 = []

for j in range(len(times)):

    depth = [i * experiment.constant_water for i in time] 
    depths_12.append(depth)

positions_cm_500 = []

for i in positions:

    positions_cm_500.append(500 * [i])

array_positions_cm_500 = np.array(positions_cm_500)

positions_cm_all = []
depths_all = []
envelopes_all = []

for i in range(len(times)):

    positions_cm_all.extend(positions_cm_500[i])
    depths_all.extend(depths_12[i])
    envelopes_all.extend(envelopes[i])

fig1 = plt.figure(figsize = (10, 8))

gs = fig1.add_gridspec(2, 2, hspace = 0, wspace = .3)
(ax1, ax2), (ax3, ax4) = gs.subplots(sharex = 'row')

c = ax1.pcolormesh(positions_cm, time, np.array(envelopes).T, shading = 'gouraud')
cbar = plt.colorbar(c)
ax1.set_title("With object")
ax1.set(ylabel = 'Time (ms)')
ax1.set_xticks([])

c = ax2.pcolormesh(positions_cm, time_water, np.array(envelopes_water).T, shading = 'gouraud')
cbar = plt.colorbar(c)
ax2.set_title("Without object")
ax2.set(ylabel = 'Time (ms)')
ax2.set_xticks([])

c = ax3.pcolormesh(positions_cm, depths, np.array(envelopes).T, shading = 'gouraud')
cbar = plt.colorbar(c)
ax3.set(xlabel = 'Lateral direction (cm)', ylabel = 'Axial direction (cm)')

c = ax4.pcolormesh(positions_cm, depths_water, np.array(envelopes_water).T, shading = 'gouraud')
cbar = plt.colorbar(c)
ax4.set(xlabel = 'Lateral direction (cm)', ylabel = 'Axial direction (cm)')

fig2, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize = (10, 8))

c = ax1.pcolormesh(positions_cm, time, np.array(envelopes).T, shading = 'gouraud')
cbar = plt.colorbar(c)
ax1.set_title("With object")
ax1.set(xlabel = 'Lateral direction (cm)', ylabel = 'Time (ms)')

c = ax2.pcolormesh(positions_cm, time_water, np.array(envelopes_water).T, shading = 'gouraud')
cbar = plt.colorbar(c)
ax2.set_title("Without object")
ax2.set(xlabel = 'Lateral direction (cm)', ylabel = 'Time (ms)')

c = ax3.pcolormesh(positions_cm, depths, np.array(envelopes).T, shading = 'gouraud')
cbar = plt.colorbar(c)
ax3.set(xlabel = 'Lateral direction (cm)', ylabel = 'Axial direction (cm)')

c = ax4.pcolormesh(positions_cm, depths_water, np.array(envelopes_water).T, shading = 'gouraud')
cbar = plt.colorbar(c)
ax4.set(xlabel = 'Lateral direction (cm)', ylabel = 'Axial direction (cm)')

plt.rcParams['font.family'] = "sans-serif"

fig3 = plt.figure(figsize = (10, 8))

gs = fig3.add_gridspec(2, 1, hspace = 0, wspace = .3)
(ax1, ax2) = gs.subplots(sharex = 'row')

c = ax1.pcolormesh(positions_cm, depths, np.array(envelopes).T, shading = 'gouraud', cmap = 'inferno', antialiased = False)
cbar = plt.colorbar(c)
ax1.set_ylabel('Axial direction (cm)', fontsize = 13)
ax1.set_xticks([])

c = ax2.pcolormesh(positions_cm, depths_water, np.array(envelopes_water).T, shading = 'gouraud', cmap = 'inferno', antialiased = False)
cbar = plt.colorbar(c)
ax2.set_xlabel('Lateral direction (cm)', fontsize = 13)
ax2.set_ylabel('Axial direction (cm)', fontsize = 13)

fig4, ax = plt.subplots(subplot_kw = {'projection': '3d'}, figsize = (10, 8))

X = np.array(positions_cm_500)
Y = np.array(depths)
Z = np.array(envelopes)

scamap = plt.cm.ScalarMappable(cmap = 'inferno')
fcolors = scamap.to_rgba(Z)

ax.plot_surface(X, Y, Z, facecolors = fcolors, cmap = 'inferno', linewidth = 0, antialiased = True)
ax.set_xlabel("Lateral direction (cm)")
ax.set_ylabel("'Axial direction (cm)")
ax.set_zlabel("Amplitude")
fig4.colorbar(scamap, ax = plt.gca())

fig5, ax5 = plt.subplots(nrows = 1, ncols = 1, figsize = (10, 8))

for i in range(5, 6):

    ax5.plot(times[i], amps[i], color = 'white')
    ax5.plot(times[i], envelopes[i], color = 'red')
    ax5.plot([min(times[0]), min(times[0])], [min(amps[i]), max(amps[i])], color = 'yellow', lw = 2)
    ax5.plot([max(times[0]), max(times[0])], [min(amps[i]), max(amps[i])], color = 'yellow', lw = 2)

    # plt.plot(times[i], adjusted_signals[i], color = 'red')
    # plt.plot(times[i], envelopes[i], color = 'green')

major_ticks_x = np.linspace(0.208, 0.218, 6)
minor_ticks_x = np.linspace(0.208, 0.218, 36)
major_ticks_y = np.linspace(0, 250, 6)
minor_ticks_y = np.linspace(0, 250, 36)

ax5.set_facecolor('black')
ax5.set_xlabel('Time (ms)', fontsize = 13)
ax5.set_ylabel('Amplitude', fontsize = 13)

ax5.set_xticks(major_ticks_x)
ax5.set_xticks(minor_ticks_x, minor = True)
ax5.set_yticks(major_ticks_y)
ax5.set_yticks(minor_ticks_y, minor = True)

ax5.grid(True, which = 'major', color = 'lime', alpha = .4)
ax5.grid(True, which = 'minor', lw = .5, color = 'lime', alpha = .2)

plt.close(fig1)
plt.close(fig2)
plt.close(fig3)
plt.close(fig4)
# plt.close(fig5)

plt.show()


points2D = np.vstack([positions_cm_all, depths_all]).T

tri = Delaunay(points2D) 
I, J, K = (tri.simplices).T

fig = go.Figure(go.Mesh3d(x = positions_cm_all, y = depths_all, z = envelopes_all,
                        i = I, j = J, k = K, colorscale = "ice" )) 

# fig.show()

# experiment = UltrasonicExperiment(60, 170)
# experiment.scan("aluminium")
# experiment.scan_water()
# experiment.envelope()
# experiment.depth()

# times = experiment.all_times
# time = times[0]
# ranges = experiment.ranges
# positions = experiment.ranges
# envelopes = experiment.amplitude_envelope_all
# heights = [i for i in np.arange(0, 12, 1)]

# heights_500 = []

# for i in heights:

#     heights_500.append(500 * [i])

# array_heights_500 = np.array(heights_500)

# ranges_500 = []

# for i in ranges:

#     ranges_500.append(500 * [i])

# array_ranges_500 = np.array(ranges_500)

# intervals = []

# for i in range(len(ranges) - 1):

#     intervals.append([ranges[i], ranges[i + 1]])

# array_intervals = np.array(intervals)
# array_times = np.array(times)
# array_ranges = np.array(ranges)
# array_envelopes = np.array(envelopes)

# ranges_all = []
# times_all = []
# heights_all = []
# envelopes_all = []

# for i in range(len(times)):

#     ranges_all.extend(ranges_500[i])
#     times_all.extend(times[i])
#     heights_all.extend(heights_500[i])
#     envelopes_all.extend(envelopes[i])

# v_water = experiment.v_water
# v_al = experiment.v_al
# constant_water = experiment.constant_water
# constant_al = experiment.constant_al


# depth_object =  (7.5 / 100) 
# test_time = depth_object / v_al

# print('t_start: ', experiment.t_start, 't_end: ', experiment.t_end)
# print('t_min:', min(time), 't_max: ', max(time))
# print('t_end - t_start: ', experiment.t_end - experiment.t_start)
# print('measured t_max - t_min: ', 0.212080 - 0.202100)
# print('calulated time (ms)', test_time * 1000)

# depths = []

# for i in range(len(times)):

#     d = []

#     for j in times[i]:

#         d.append(j * constant_water)

#     depths.append(d)

# print(depths)
# print(len(depths))

# fig1 = plt.figure(figsize = (10, 8))

# for i in range(6, 11):

#     plt.plot(depths[i], envelopes[i])

# plt.xlabel('Lateral direction (mm)')
# plt.ylabel('amplitude')
# plt.grid()
# plt.tight_layout()
# plt.show()


# print(depths)
# print(len(depths))
   




# df = pd.DataFrame(array_envelopes.T, index = time, columns = positions)

# x, y = np.meshgrid(df.columns,df.index)

# fig = plt.figure(figsize = (10, 8))

# c = plt.pcolormesh(x, y, np.array(df.loc[-1::]), shading = 'gouraud')
# plt.colorbar(c)
# plt.xlabel('Lateral direction (mm)')
# plt.ylabel('Axial direction (mm)')

# plt.show()

# fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
# X, Y, Z = get_test_data(0.05)
# C = np.linspace(-5, 5, Z.size).reshape(Z.shape)
# scamap = plt.cm.ScalarMappable(cmap='inferno')
# fcolors = scamap.to_rgba(C)
# ax.plot_surface(X, Y, Z, facecolors=fcolors, cmap='inferno')
# fig.colorbar(scamap)


# fig3, ax = plt.subplots(subplot_kw = {"projection": "3d"}, figsize = (10, 8))

# X = np.array(positions_cm)
# Y = np.array(depths)
# X, Y = np.meshgrid(X, Y)
# Z = np.array(envelopes).T

# surf = ax.plot_surface(X, Y, Z, cmap = cm.inferno, linewidth = 0, antialiased = True)

# ax.zaxis.set_major_locator(LinearLocator(10))
# ax.zaxis.set_major_formatter("{x:.02f}")
# ax.set_xlabel("Lateral direction (cm)")
# ax.set_ylabel("'Axial direction (cm)")
# ax.set_zlabel("Amplitude")
# fig3.colorbar(surf, shrink = 0.5, aspect = 5)
 

# fig, ax = plt.subplots(subplot_kw = {'projection': '3d'})
# X = array_ranges_500
# Y = array_times
# Z = array_heights_500
# C = array_envelopes

# print(X.shape, Y.shape, C.shape)

# scamap = plt.cm.ScalarMappable(cmap='inferno')
# fcolors = scamap.to_rgba(C)
# ax.plot_surface(X, Y, C, facecolors=fcolors, cmap='inferno')
# fig.colorbar(scamap, ax=plt.gca())
# plt.show()

# points2D = np.vstack([ranges_all, times_all]).T
# tri = Delaunay(points2D) 
# I, J, K = (tri.simplices).T
# print("simplices:", "\n", tri.simplices)

# fig = go.Figure(go.Mesh3d(x = ranges_all, y = times_all, z = heights_all,
#                         i = I, j = J, k = K, 
#                        intensity = envelopes_all, colorscale = "ice" )) 

# fig = go.Figure(go.Mesh3d(x = ranges_all, y = times_all, z = envelopes_all,
#                         i = I, j = J, k = K, 
#                        intensity = heights_all, colorscale = "ice" )) 

# fig = go.Figure(go.Mesh3d(x = ranges_all, y = times_all, z = heights_all,
#                         i = I, j = J, k = K, colorscale = "ice" )) 

# print(np.array(ranges_all).shape, np.array(ranges_all).ndim)
# print(np.array(times_all).shape, np.array(times_all).ndim)
# print(np.array(heights_all).shape, np.array(heights_all).ndim)
# print(np.array(envelopes_all).shape, np.array(envelopes_all).ndim)

# fig.show()