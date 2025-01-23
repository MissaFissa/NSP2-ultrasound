import matplotlib.pyplot as plt
import numpy as np

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

#plot 4 heatmaps of empty fish tank and with aluminium block inside, with different labels for the axes.
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

#plot 4 heatmaps of empty fish tank and with aluminium block inside, with different labels for the axes and matching x-axes.
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

#plot both heatmaps with matching x-axes.
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

#plot for the waveform used in the analysis.
fig4, ax4 = plt.subplots(nrows = 1, ncols = 1, figsize = (10, 8))

for i in range(5, 6):

    ax4.plot(times[i], amps[i], color = 'white')
    ax4.plot([min(times[0]), min(times[0])], [min(amps[i]), max(amps[i])], color = 'yellow', lw = 2)
    ax4.plot([max(times[0]), max(times[0])], [min(amps[i]), max(amps[i])], color = 'yellow', lw = 2)

major_ticks_x = np.linspace(0.208, 0.218, 6)
minor_ticks_x = np.linspace(0.208, 0.218, 36)
major_ticks_y = np.linspace(0, 250, 6)
minor_ticks_y = np.linspace(0, 250, 36)

ax4.set_facecolor('black')
ax4.set_xlabel('Time (ms)', fontsize = 13)
ax4.set_ylabel('Amplitude', fontsize = 13)

ax4.set_xticks(major_ticks_x)
ax4.set_xticks(minor_ticks_x, minor = True)
ax4.set_yticks(major_ticks_y)
ax4.set_yticks(minor_ticks_y, minor = True)

ax4.grid(True, which = 'major', color = 'lime', alpha = .4)
ax4.grid(True, which = 'minor', lw = .5, color = 'lime', alpha = .2)

#plot the heatmaps in two seperate rows.
fig5, (ax1, ax2) = plt.subplots(2, 1, figsize = (10, 8))

c1 = ax1.pcolormesh(positions_cm, depths, np.array(envelopes).T, shading = 'gouraud', cmap = "inferno", antialiased = False)
c2 = ax2.pcolormesh(positions_cm, depths_water, np.array(envelopes_water).T, shading = 'gouraud', cmap = "inferno", antialiased = False)
plt.colorbar(c1)
plt.colorbar(c2)
ax1.set_title("Aluminium block in fish tank", fontsize = 13)
ax1.set_xlabel('Lateral direction (cm)', fontsize = 13)
ax1.set_ylabel('Axial direction (cm)', fontsize = 13)
ax2.set_title("Empty fish tank", fontsize = 13)
ax2.set_xlabel('Lateral direction (cm)', fontsize = 13)
ax2.set_ylabel('Axial direction (cm)', fontsize = 13)
plt.tight_layout()

# plt.close(fig1)
# plt.close(fig2)
plt.close(fig3)
plt.close(fig4)
plt.close(fig5)

plt.show()