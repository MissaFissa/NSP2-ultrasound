import matplotlib.pyplot as plt
import numpy as np
import click
import matplotlib
import pandas as pd
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import matplotlib.tri as mtri
from mpl_toolkits.mplot3d import Axes3D
from nsp2_ultrasound.model import UltrasonicExperiment

@click.command()
@click.argument("start")
@click.argument("stop")
@click.argument("name")
def initiate(start, stop, name):

    experiment = UltrasonicExperiment(start, stop)
    experiment.scan(name)
    experiment.envelope()
    experiment.scan_water()

    times = experiment.all_times
    ranges = experiment.ranges
    envelopes = experiment.amplitude_envelope_all
    envelopes_water = experiment.amplitude_envelope_all_water

    array_times = np.array(times)
    array_ranges = np.array(ranges)
    array_envelopes = np.array(envelopes)

    fig1 = plt.figure(figsize = (10, 8))

    for i in range(6, 11):

        plt.plot(times[i], envelopes[i], color = 'red')
        plt.plot(times[i], envelopes_water[i], color = 'green')

    plt.xlabel('time (ms)')
    plt.ylabel('amplitude')
    plt.grid()
    plt.tight_layout()

    fig2 = plt.figure(figsize = (10, 8))

    c = plt.pcolormesh(ranges, times[0], np.array(envelopes).T, shading = 'gouraud')
    plt.colorbar(c)
    plt.xlabel('position of transducer (mm)')
    plt.ylabel('time (ms)')
    plt.tight_layout()

    fig3 = plt.figure(figsize = (10, 8))

    df = pd.DataFrame(array_envelopes.T, index = times[0], columns = ranges)
    c = plt.pcolormesh(df, shading = 'gouraud')
    plt.colorbar(c)

    fig4, ax4 = plt.subplots(subplot_kw = {"projection": "3d"}, figsize = (10, 8))

    X = np.array(ranges)
    Y = np.array(times[0])
    X, Y = np.meshgrid(X, Y)
    Z = np.array(envelopes).T

    surf4 = ax4.plot_surface(X, Y, Z, cmap = cm.coolwarm, linewidth = 0, antialiased = False)

    ax4.zaxis.set_major_locator(LinearLocator(10))
    ax4.zaxis.set_major_formatter("{x:.02f}")
    ax4.set_xlabel("position of transducer (mm)")
    ax4.set_ylabel("time (ms)")
    ax4.set_zlabel("amplitude")

    fig4.colorbar(surf4, shrink = 0.5, aspect = 5)
 
    plt.close(fig1)
    plt.close(fig2)
    plt.close(fig3)
    plt.close(fig4)

    plt.show()