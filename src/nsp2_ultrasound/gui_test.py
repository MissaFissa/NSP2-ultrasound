import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import matplotlib.tri as mtri
from mpl_toolkits.mplot3d import Axes3D
from nsp2_ultrasound.model import UltrasonicExperiment

# start = 60 
# stop = 170
# name = "aluminium"
# experiment = UltrasonicExperiment(start, stop)
# all_amps, all_times = experiment.scan(name)
# adjusted_signals_all, amplitude_envelope_all = experiment.envelope()
# # all_amps_water, all_times_water, adjusted_signals_all_water, amplitude_envelope_all_water = experiment.scan_water()
# # experiment.depth()

# X_4D = np.arange(int(start), int(stop) + 10, 10)
# Y_4D =  np.array(all_times[0])
# Z_4D = np.arange(10, 130, 10)
# # Y = np.arange(10, 130, 0.24)

# X_4D, Y_4D = np.meshgrid(X_4D, Y_4D)
# # print(f"X_4D first mesh shape = {X_4D.shape}")

# X_4D, Y_4D = X_4D.ravel(), Y_4D.ravel()
# # print(f"X_4D ravel shape = {X_4D.shape}")

# X_4D_mesh, Y_4D_mesh = (X_4D, Y_4D)
# # print(f"X_4D second mesh shape = {X_4D_mesh.shape}")

# triangles_1 = mtri.Triangulation(X_4D_mesh, Y_4D_mesh).triangles
# print(f"triangles X_4D/Y_4D shape = {triangles_1.shape}")
# # C_4D = np.array(amplitude_envelope_all).T

# list_amplitude_envelopes = []

# for list in amplitude_envelope_all:

#     list_amplitude_envelopes.extend(list)

# C_4D = np.array(list_amplitude_envelopes).T

# print(C_4D.shape)

# colors_1 = np.mean(C_4D[triangles_1], axis = 1)

# print(colors_1.shape)

# (n, m) = (250, 250)

# theta = np.linspace(0, 2 * np.pi, num=n, endpoint=False)

# phi = np.linspace(np.pi * (-0.5 + 1./(m+1)), np.pi*0.5, num=m, endpoint=False)
# theta, phi = np.meshgrid(theta, phi)
# # print(f"theta first mesh shape = {theta.shape}")

# theta, phi = theta.ravel(), phi.ravel()
# # print(f"theta ravel shape = {theta.shape}")

# theta = np.append(theta, [0.]) 

# phi = np.append(phi, [np.pi*0.5])
# mesh_x, mesh_y = ((np.pi*0.5 - phi)*np.cos(theta), (np.pi*0.5 - phi)*np.sin(theta))
# # print(f"theta second mesh shape = {mesh_x.shape}")

# triangles = mtri.Triangulation(mesh_x, mesh_y).triangles
# print(f"triangles theta/phi shape = {triangles.shape}")
# x, y, z = np.cos(phi)*np.cos(theta), np.cos(phi)*np.sin(theta), np.sin(phi)

# vals = np.sin(6*phi) * np.sin(3*theta)
# colors = np.mean(vals[triangles], axis=1)
# print(vals.shape)
# print(colors.shape)

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# cmap = plt.get_cmap('Blues')
# triang = mtri.Triangulation(x, y, triangles)
# collec = ax.plot_trisurf(triang, z, cmap=cmap, shade=False, linewidth=0.)
# collec.set_array(colors)
# collec.autoscale()

import matplotlib
from scipy.interpolate import griddata

# X-Y are transformed into 2D grids. It's like a form of interpolation
x1 = np.linspace(x.min(), x.max(), len(np.unique(x)))
y1 = np.linspace(y.min(), y.max(), len(np.unique(y)))
x2, y2 = np.meshgrid(x1, y1)

# Interpolation of Z: old X-Y to the new X-Y grid.
# Note: Sometimes values ​​can be < z.min and so it may be better to set 
# the values too low to the true minimum value.
z2 = griddata( (x, y), z, (x2, y2), method='cubic', fill_value = 0)
z2[z2 < z.min()] = z.min()

# Interpolation of C: old X-Y on the new X-Y grid (as we did for Z)
# The only problem is the fact that the interpolation of C does not take
# into account Z and that, consequently, the representation is less 
# valid compared to the previous solutions.
c2 = griddata( (x, y), c, (x2, y2), method='cubic', fill_value = 0)
c2[c2 < c.min()] = c.min()

#--------
color_dimension = c2; # It must be in 2D - as for "X, Y, Z".
minn, maxx = color_dimension.min(), color_dimension.max()
norm = matplotlib.colors.Normalize(minn, maxx)
m = plt.cm.ScalarMappable(norm=norm, cmap = name_color_map)
m.set_array([])
fcolors = m.to_rgba(color_dimension)

# At this time, X-Y-Z-C are all 2D and we can use "plot_surface".
fig = plt.figure(); ax = fig.gca(projection='3d')
surf = ax.plot_surface(x2, y2, z2, facecolors = fcolors, linewidth=0, rstride=1, cstride=1,
                       antialiased=False)
cbar = fig.colorbar(m, shrink=0.5, aspect=5)
cbar.ax.get_yaxis().labelpad = 15; cbar.ax.set_ylabel(list_name_variables[index_c], rotation = 270)
ax.set_xlabel(list_name_variables[index_x]); ax.set_ylabel(list_name_variables[index_y])
ax.set_zlabel(list_name_variables[index_z])
plt.title('%s in fcn of %s, %s and %s' % (list_name_variables[index_c], list_name_variables[index_x], list_name_variables[index_y], list_name_variables[index_z]) )
plt.show()