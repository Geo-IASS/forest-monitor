import installation as inst
from IPython.display import display, HTML
# from IPython.html.widgets import interact
from IPython.html import widgets
from IPython import display
import numpy as np
import matplotlib.pyplot as plt
import presentation as pres


class InteractiveTscModel:


    def __init__(self, cow):
        self.cow = cow
        self.itcs = inst.InstalledTCS(cow)


    def initialMastPositions(self, mastCoords):
        self.mastCoords = np.array(mastCoords)


    def initialMastHeights(self, mastHeights):
        self.mastHeights = mastHeights

    def initialPlatformLoc(self, coord, height):
        self.platCoord = coord
        self.platHeight = height


    def interact(self):

        self.itcs.positionMasts(self.mastCoords, self.mastHeights)

        swExtent = self.mastCoords.min(axis=0)
        neExtent = self.mastCoords.max(axis=0)

        w = widgets.interactive(
            self.posPlatform,
            xPlat=widgets.FloatSliderWidget(min=swExtent[0], max=neExtent[0], value=self.platCoord[0], step=1.0),
            yPlat=widgets.FloatSliderWidget(min=swExtent[1], max=neExtent[1], value=self.platCoord[1], step=1.0),
            height=widgets.FloatSliderWidget(min=0, max=200, value=self.platHeight),
            weight=widgets.FloatSliderWidget(min=0, max=1000, value=500)
        )

        display.display(w)


    def posPlatform(self, xPlat, yPlat, height, weight):

        def tableRow(title, form, vals):
            return '<tr><th>' + title + '</th>' + ' '.join([('<td>' + form + '</td>').format(x) for x in vals]) + '</tr>\n'

        okay = self.itcs.positionPlatform([xPlat, yPlat], height, weight)
        if not okay:
            print 'One or more cables would need to be in compression to position the platform {}m above ({},{})'.format(height,xPlat,yPlat)
            return

        d, zt, zg = self.itcs.getTerrainBeneathCables(resolution=10)
        zc, mc = self.itcs.getCableClearance(d, zt)

        if mc < 1.0:
            attr = ' style="color:red;"'
        else:
            attr = ''

        s = '<table>\n'
        s += tableRow('Cable', '{}', range(1, 4))
        s += tableRow('Length [m]', '{:0.0f}', [self.itcs.tcs.c[i].length() for i in range(3)])
        s += tableRow('Tension [N]', '{:0.0f}', self.itcs.tcs.tensionAtMasts())
        s += '</table>\n'
        s += '<p{}>Minimum canopy clearance: {:0.2f}m</p>\n'.format(attr, mc)

        display.display(HTML(s))

        plt.figure(figsize=(12,8))


        ax = plt.subplot(111, aspect='equal')
        pres.showInstallation2d(ax, self.itcs, [0,500], [1500,1500], showPlat=True)

        plt.figure(figsize=(12,8))
        axt = range(3)
        axb = range(3)
        # fig, axes = plt.subplots(ncols=3, nrows=2, sharex=True, sharey=True)
        # plt.setp(axes.flat, aspect=1.0, adjustable='box')


        axt[0] = plt.subplot(231, aspect='equal')
        axt[1] = plt.subplot(232, sharex=axt[0], sharey=axt[0]) #, aspect='equal')
        axt[2] = plt.subplot(233, sharex=axt[0], sharey=axt[0]) #, aspect='equal')

        axb[0] = plt.subplot(234, sharex=axt[0])
        axb[1] = plt.subplot(235, sharex=axt[0], sharey=axb[0])
        axb[2] = plt.subplot(236, sharex=axt[0], sharey=axb[0])

        plt.setp(axt[1].get_yticklabels(), visible=False)
        plt.setp(axt[2].get_yticklabels(), visible=False)
        plt.setp(axb[1].get_yticklabels(), visible=False)
        plt.setp(axb[2].get_yticklabels(), visible=False)


        axt[0].set_ylabel('elevation [m]')
        axb[0].set_ylabel('clearance from canopy [m]')
        for i in range(3):

            plt.setp(axt[i].get_xticklabels(), visible=False)
            axt[i].plot(d[i], zc[i], 'b-')
            axt[i].plot(d[i], zt[i], 'g-')
            axt[i].plot(d[i], zg[i], 'g-')
            axt[i].plot(d[i][-1], zc[i][-1], 'ro')
            axt[i].plot([0, 5], [zc[i][0], zg[i][0]], 'r-')

            axb[i].set_xlabel('distance from mast {} [m]'.format(i+1))

            axb[i].plot(d[i], zc[i] - zt[i], 'b')



