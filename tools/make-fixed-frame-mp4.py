# coding: utf-8

import argparse

# Plot
import matplotlib.pyplot as plt
from matplotlib import animation
import seaborn as sns
import numpy as np

from scipy.ndimage.interpolation import zoom

from maxwellbloch import mb_solve

# Parse filename
parser = argparse.ArgumentParser(description="Takes an MBSolve problem \
    defined in a JSON file and outputs an MP4 video showing the propagation.")
parser.add_argument('-f', '--file', help='Path of input file.', required=True)
parser.add_argument('-c', '--speed-of-light',
    help='Speed of Light in the system units.', default=0.1, required=False)
parser.add_argument('-m', '--y-min', help='Minimum of the y-axis.',
    default=0.0, required=False)
parser.add_argument('-y', '--y-max', help='Maximum of the y-axis maximum',
    default=1.0, required=False)
parser.add_argument('-z', '--zoom', help="To use interpolation on the output \
    data, select the order of interpolation. (e.g. 2, 4). Note this may \
    introduce numerical artefacts.", default=1,
    required=False)

opts = parser.parse_args()
print(opts)

json_file = opts.file
speed_of_light = float(opts.speed_of_light)
y_min = float(opts.y_min)
y_max = float(opts.y_max)

mb_solve_00 = mb_solve.MBSolve().\
                from_json(json_file)

Omegas_zt, states_zt = mb_solve_00.mbsolve(recalc=False)

### ANIMATION

Omegas_fixed = mb_solve_00.Omegas_fixed_frame(0, speed_of_light)

tlist = mb_solve_00.tlist
zlist = mb_solve_00.zlist

# Zoom
z = 4
Omegas_fixed = zoom(Omegas_fixed, z)
tlist = zoom(tlist, z)
zlist = zoom(zlist, z)

fig = plt.figure(2, figsize=(12, 5))
ax = fig.add_subplot(111)

line, = ax.plot([], [], lw=2, clip_on=False)
t_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)

for y in [0.0, 1.0]:
    ax.axvline(y, c='black', lw=1.0, ls='dashed')

ax.set_xlim((-0.2, 1.2))
ax.set_ylim((y_min, y_max))

ax.set_xlabel('Distance ($L$)')
ax.set_ylabel('Rabi Frequency ($\Gamma / 2\pi $)')

def init():
    line.set_data([], [])
    t_text.set_text('')
    return (line, t_text)

def animate(i):
    x = zlist
    y = np.abs(Omegas_fixed[:, i])/(2.0*np.pi)
    line.set_data(x, y)

    for coll in (ax.collections):
        ax.collections.remove(coll)

    ax.fill_between(x, 0., y, alpha=0.5, clip_on=False, interpolate=True)


    t_text.set_text('t = {:.1f} $/\Gamma$'.format(tlist[i]))
    return (line, t_text)

# call the animator. blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=len(tlist), interval=25,
                               blit=False)

# Set up formatting for the movie files
Writer = animation.writers['ffmpeg']
writer = Writer(fps=30, metadata=dict(artist='Me'), bitrate=1800)

anim.save(json_file + '.mp4', writer=writer)

plt.show()