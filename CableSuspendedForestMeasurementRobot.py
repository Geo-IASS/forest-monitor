# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Investigation into Feasibility of a Permanent Cable Based Canopy Access System at Coweeta

# <markdowncell>

# Dave Hawthorne 2015

# <headingcell level=2>

# Background

# <markdowncell>

# Collecting data from forests at Coweeta is a labour intensive exercise.  The difficulty increases with vertical distance from the forest floor.  Conducting measurement in and above the canopy is particularly problematic.  What methods exist, such as slingshotting ropes into the canopy, are haphazard and potentially dangerous as operators need to be positioned below.  
# 
# This document investigates the feasability of a permanently installed cable-suspended parallel robot that traverses the airspace above the canopy for a selected study site.
# 
# The system consists of three masts that project above the canopy on hill slopes above the study site.  From each mast a cable runs to a suspended platform.  That platform can be positioned at any point in the airspace above the canopy by combinations of winching in/playing out cable from the masts.  The platform houses a fourth winch that positions a bob below it.  This bob would house measurement equipment and would decend to the canopy and below.
# 
# The lack of obstacles above the canopy permits automated positioning of the platform, and therefore routine automated measurement.  

# <markdowncell>

# LiDAR
# http://www.velodynelidar.com/lidar/hdlproducts/hdl32e.aspx

# <headingcell level=2>

# Biblography

# <markdowncell>

# <b>Access to the Upper Forest Canopy with a Large Tower Crane</b>
# Geoffrey G. Parker, Alan P. Smith and Kevin P. Hogan
# BioScience
# Vol. 42, No. 9 (Oct., 1992), pp. 664-670
# Published by: Oxford University Press
# Article Stable URL: http://www.jstor.org/stable/1312172
# 
# Meg Lowman Tree Canopy Access Methods [Videos]
# http://treefoundation.org/resources/canopy-methods/
# 
# Company that did the Coweeta walkway
# http://www.canopyaccess.com/index.html
# 
# Commercial offerings for sports broadcast.
# http://en.wikipedia.org/wiki/Skycam
# http://www.cablecam.com/HowWeDoIt.aspx?id=86
# http://skycam.tv.s28625.gridserver.com/sample-page-2/features/

# <markdowncell>

# Having their own mass, the cables supporting the platform can each be modelled by a catenary curve:
# 
# $$
# y = a \cosh{ \frac{x}{a} } = \frac{a}{2} \lgroup e ^ \frac{x}{a} - e ^ \frac{-x}{a}    \rgroup
# $$

# <codecell>

%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
import cableStatics as cs

# <codecell>

c = cs.Cable(5, 4, 10, 0.035)
c.setHorizForce(1)
cs.showCable(c)

# <markdowncell>

# The horizontal components of each of the three cables' tension must cancel for the platform to be static.
# The ratios between the cables' Th is determined by the horizontal alignment of the system components only.  The three Th values are adjusted up or down by the same amount to control the platform's z value.  Note that the ratios between net tension in the cable will not necessarily remain constant.

# <codecell>

import presentation as pres
reload(pres)
pres.showExampleSystem()

# <markdowncell>

# Considerations
# * wind induced vibrations
# * ice loading, bird loading
# * horizontal shift of the platform as load applied to the bob.
# * equipment used for target practice
# * theft of equipment, particularly cable

# <headingcell level=3>

# Cable

# <markdowncell>

# 1/4" kevlar
# 
# http://www.pelicanrope.com/kevlarropes.html
# 
# 1/4" 	3/4" 	4,000 lbs. 	2.4 lb/100ft

# <codecell>

# imperial to metric conversions
def ft2m(ft):
   return ft * 0.3048
def lb2kg(lb):
    return lb * 0.453592
def lb2n(lb):
    return lb * 4.44822162825

# 1/4" KRYPTON-K 
cw = lb2n(2.4)/ft2m(100.0) # kg/m
ts = lb2n(4000) # N 
"cable weight: {:05f}N/m; tensile strength: {:05f}N".format(cw, ts)

# <headingcell level=2>

# Nomenclature

# <markdowncell>

# bob/plummet/descender
# 
# platform/nexus/

# <headingcell level=2>

# Bob Design

# <markdowncell>

# The design of the cable robot is simplified by the absence of snags.  Tensioning of the cables would keep the platform and all cables at a safe distance above the highest trees to avoid snagging.  If the system is to employ a bob the descends into the canopy and below the care will have to be paid to minimising and managing snags.  
# 
# * Use imaging/lidar to identify clear descent columns
# * Monitor position and tilt of the bob as it descends
# * Have the bob descend on a single line
# * Construct the bob so that its centre of gravity is low
# * Employ a teardrop profile to aid extraction
# * Rate the cables and mast to cater for an extraction force to pull through snags
# * Allow the bob line to be unspooled completely so that if upwards extraction is prevented then the bob might be lowered to the ground for manual retrieval.  Carry enough bob cable to reach the ground.
# 
# If the bob were to be lowered on two, reasonably well spaced lines through uninterupted space then the horizontal orientation of the bob might be fixed by those two lines.  The presence of branches and other vegetation would interfer with this arrangement.  Use of two lines increases the likelihood of snagging so this proposal uses a single line.  For all but simple point measurements (temperature/atmosphere samples) the orientation of the bob matters.  
# 
# * Rotate and stabilise the bob using a coaxial reaction wheel.
# * use fans to blow air to rotate the bob.   
# * allow the bob to rotate freely but record the orientation to allow correction post measurement.
# 
# The design of the bob involves a number of technical risks.

# <headingcell level=2>

# Positioning

# <markdowncell>

# The system is suited to cove locations with steep sides. 
# 
# As an exercise, we shall specify a system to provide coverage of some of watershed 18, which contains 3 high value plots.

# <codecell>

import coweeta
import osgeo.ogr as oo
sws = oo.Open('coweeta_subwatersheds/coweeta_subwatersheds.dbf')
l = sws.GetLayerByIndex(0)
numFeat = l.GetFeatureCount()
# print('numFeat', numFeat)
#f = l.GetFeature(0)
#gr = f.GetGeometryRef()
# print('feat', f)

plt.figure(figsize=(14,10))
ax = plt.subplot(111)

import json
jd = json.JSONDecoder()
for i in range(numFeat):
    
    f = l.GetFeature(i)
    
    ws = f.GetField(0)
    area = f.GetField(1)/10000
    # print i, , f.GetField(1), f.GetField(2), f.GetField(3)
    gr = f.GetGeometryRef()
    # print gr
    geom = gr.ExportToJson()


    struct = jd.decode(geom)
    
    coords = struct['coordinates'][0]

    x, y = [[ss[i] for ss in coords] for i in [0,1]]
    
    xc = (min(x) + max(x)) / 2
    yc = (min(y) + max(y)) / 2
    
    ax.plot(x, y, 'r')
    ax.text(xc, yc, 'WS{}\n{}ha'.format(ws, int(area)), horizontalalignment='center', verticalalignment='center')
    

s = oo.Open('coweeta_streams/coweeta_streams.dbf')
l = s.GetLayerByIndex(0)
numFeat = l.GetFeatureCount()

for i in range(numFeat):
    f = l.GetFeature(i)
    gr = f.GetGeometryRef()
    p = np.array(gr.GetPoints())

    x = p[:,0]
    y = p[:,1]

    ax.plot(x, y,'b')

    

# <codecell>


# <codecell>

reload(coweeta)
reload(pres)
reload(cs)
from matplotlib import cm

cow = coweeta.Coweeta()
cow.loadWatersheds()
cow.setWorkingRefPoint((277000, 3880000))

# <codecell>


def myPlot(elev, azim):
    ax = pres.new3d()
    x, y, z = cow.surfaceMesh([0,500], [1500,1500])
    ax.contour(x, y, z, 20, cmap=cm.coolwarm)

    ax.plot_surface(x, y, z, rstride=20, cstride=20, alpha=0.3, linewidth=0)

    x, y, z = cow.wsBoundary(18)

    ax.plot(x, y, z, 'k')
    
    ax.view_init(elev=elev, azim=azim)


from IPython.html.widgets import interact
# p1, p2, p3 = ([2332, 1280], [3175, 1240], [3040, 790])

interact(myPlot, azim=(0, 180), elev=(0, 90))
    

# <codecell>

import installation as inst
from IPython.display import display, HTML

# <codecell>

reload(coweeta)
reload(pres)
reload(inst)
reload(cs)

from matplotlib import cm

cow = coweeta.Coweeta()
cow.loadWatersheds()
cow.loadGradientPlots()
cow.setWorkingRefPoint((277000, 3880000))

gridRes = 10




itcs = inst.InstalledTCS(cow)
p1, p2, p3 = ([332, 1280], [1175, 1240], [1040, 790])
itcs.positionMasts([p1,p2,p3],[40, 40, 50])
itcs.positionPlatform([3000, 1100], 50, 200)


def posPlatform(x, y, height, weight):
    def tableRow(title, form, vals):
        return '<tr><th>' + title + '</th>' + ' '.join([('<td>' + form + '</td>').format(x) for x in vals]) + '</tr>\n'

    okay = itcs.positionPlatform([x, y], height, weight)
    if not okay:
        print 'One or more cables would need to be in compression to position the platform {}m above ({},{})'.format(height,x,y)
        return

    d, zc, zt, zg, mc = itcs.getCableClearance(resolution=10)
    
    if mc < 1.0:
        attr = ' style="color:red;"'
    else:
        attr = ''
    
    s = '<table>\n'
    s += tableRow('Cable', '{}', range(1, 4))
    s += tableRow('Length [m]', '{:0.0f}', [itcs.tcs.c[i].length() for i in range(3)])
    s += tableRow('Tension [N]', '{:0.0f}', itcs.tcs.tensionAtMasts())
    s += '</table>\n'
    s += '<p{}>Minimum canopy clearance: {:0.2f}m</p>\n'.format(attr, mc)

    display(HTML(s))
    
    plt.figure(figsize=(12,8))

    
    ax = plt.subplot(111, aspect='equal')
    pres.showInstallation2d(ax, itcs, [0,500], [1500,1500], showPlat=True)
 
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

        axb[i].plot(d[i], zc[i] - zg[i], 'b')

    

# <markdowncell>

# # Exercising System
# 
# The following is a interactive model of the WS18 TCS.  The position of the platform can be adjusted in all three axes.  The weight can also be controlled.

# <codecell>

from IPython.html.widgets import interact
# p1, p2, p3 = ([2332, 1280], [3175, 1240], [3040, 790])

interact(posPlatform, x=(332,1175), y=(790,1280), height=(0, 200), weight=(0, 1000))

# <markdowncell>

# ##Observations
# 
# * Increasing the payload mass doesn't result in a proportional increase in tension.  This is because there is less cable droop and the platform can be placed lower.
# 
# * The amount the masts extend beyond the canopy is determined largely by the trees near them.  We rely cheifly on topology for clearance away from the  masts. 
# 
# * We can potentially can operate with cable tensions below 2kN or 400lb; well within the tensile strength of the cable used (17kN)
# 
# * With a substantial platform load, the droop of the cables only becomes significant when the platform is positioned close to the line between two masts; requiring the cable to the third mast to not pull too much.  This lower tension means that it droops.  Ground clearance dictates the minimum tension. 

# <markdowncell>

# ##Cable Return Limitations
# 
# If we opt to have all winches located at the one mast then the cables must be run back from the other two masts.  This introduces an extra constraint - there would be a minimum tension acheivable on these cables imposed by the terrain between the pulley masts and the winch mast. 

# <markdowncell>

# # Mapping System Over Range
# 
# Let's automate the above process of positioning the platform at a map reference and finding the z range.  The following generates a grid of (x,y) positions and for each one:
# * determines the maximum elevation attainable by the platform (controlled by maximum cable tension only)
# * determines the minimum elevation attainable by the platform (controlled by cable clearance above canopy)
# * determines the maximum tension in all three cables to hold this minimum elevation
# * determines the canopy and ground height at each of these grid references
# 
# Locations outside the triangle made by the masts are ignored and set to NaN.  Locations where sufficient cable clearance can't be attained with the tension constrains are set to NaN.
# 
# This computation is slow as there are multiple iterations per location.  Each iteration involves solving tension equations with numerical methods.

# <codecell>

import cableStatics as cs
reload(inst)
reload(pres)
reload(cs)
itcs = inst.InstalledTCS(cow)
p1, p2, p3 = ([2332, 1280], [3175, 1240], [3040, 790])
itcs.positionMasts([p1,p2,p3],[10,10,20])
xr, yr, zCeil, zFloor, zGround, floorTen = itcs.platformMap(
   cableRes=5, gridRes=10, heightRes=0.5, minClearance=2, maxTension=1500, weight=200
)

# <codecell>

# airspace volume accessible 

gridRes = 10
colHigh = zCeil - zGround
valid = np.isfinite(colHigh)
area = np.count_nonzero(valid) * gridRes ** 2
volume = np.sum(colHigh[valid]) * gridRes ** 2
s = '''<table>
<tr><th>Accessible ground area</th><td>{:,} $m^2$</td></tr>
<tr><th>Accessible airspace volume</th><td>{:,} $m^3$</td></tr>
'''.format(int(area), int(volume))
HTML(s)

# <codecell>

reload(pres)


def tcsMap(title, arg):
    plt.figure(figsize=(14,10))
    
    plt.jet()

    ax = plt.subplot(111, aspect='equal')
    pres.showInstallation2d(ax, itcs, [200,700], [1300,1500])
    
    cs = plt.contourf(xr, yr, arg)
    ax.set_title(title)

    plt.colorbar(cs, shrink=0.6)


# <codecell>

tcsMap('Maximum Elevation of Platform [m]', zCeil)
tcsMap('Minimum Safe Elevation of Platform [m]', zFloor)
tcsMap('Height Range of Platform [m]', zCeil - zFloor)
tcsMap('Maximum Height of Platform Above Canopy [m]', zCeil - zGround)
tcsMap('Minimum Safe Height of Platform  Above Canopy [m]', zFloor - zGround)
tcsMap('Cable Tension To Hold Platform At Minimum Elevation [N]', floorTen)


# <codecell>

import cableStatics as cs
reload(inst)
reload(pres)
reload(cs)
itcs = inst.InstalledTCS(cow)
p1, p2, p3 = ([332, 1280], [1175, 1240], [1040, 790])
itcs.positionMasts([p1,p2,p3],[10,10,20])
xr, yr, zCeil, zFloor, zGround, floorTen = itcs.platformMap(
   cableRes=5, gridRes=10, heightRes=0.5, minClearance=2, maxTension=2000, weight=500
)

# <codecell>

xws18, yws18, zws18 = itcs.terrain.wsBoundary(18)
tcsMap('Maximum Elevation of Platform [m]', zCeil)
tcsMap('Minimum Safe Elevation of Platform [m]', zFloor)
tcsMap('Height Range of Platform [m]', zCeil - zFloor)
tcsMap('Maximum Height of Platform Above Canopy [m]', zCeil - zGround)
tcsMap('Minimum Safe Height of Platform  Above Canopy [m]', zFloor - zGround)
tcsMap('Cable Tension To Hold Platform At Minimum Elevation [N]', floorTen)

# <codecell>

reload(coweeta)
reload(pres)
reload(cs)
from matplotlib import cm

cow = coweeta.Coweeta()
cow.loadWatersheds()
cow.loadGradientPlots()
cow.setWorkingRefPoint((277000, 3880000))


reload(inst)
reload(pres)
reload(cs)
itcs = inst.InstalledTCS(cow)
p1, p2, p3 = ([332, 1280], [1175, 1240], [1040, 790])
itcs.positionMasts([p1,p2,p3],[10,10,20])

plt.figure(figsize=(14,10))

plt.jet()

ax = plt.subplot(111, aspect='equal')
pres.showInstallation2d(ax, itcs, [200,700], [1300,1500])


# <codecell>


plt.figure(figsize=(14,10))

plt.jet()

ax = plt.subplot(111, aspect='equal')
nwLoc = [200,700]
swLoc = [1300,1500]
x, y, z = itcs.terrain.surfaceMesh(nwLoc, swLoc)
con = ax.contour(x, y, z, 20, cmap=cm.coolwarm)
cb = plt.colorbar(con, shrink=0.6, extend='both')
cb.set_label('Elevation [m]')
x, y, z = itcs.terrain.wsBoundary(18)
ax.plot(x, y, 'k')

x, y, z = itcs.terrain.gpBoundary(118)
ax.plot(x, y, 'k')

x, y, z = itcs.terrain.gpBoundary(218)
ax.plot(x, y, 'k')

x, y, z = itcs.terrain.gpBoundary(318)
ax.plot(x, y, 'k')


ax.set_xlabel('metres east of local reference')
ax.set_ylabel('metres north of local reference')

ax.grid()

pres.showTcsCables2d(ax, itcs.tcs, showPlat=False)

# <codecell>

import cableStatics as cs
reload(inst)
reload(pres)
reload(cs)
itcs = inst.InstalledTCS(cow)
p1, p2, p3 = ([370, 1290], [1175, 1240], [1040, 790])
itcs.positionMasts([p1,p2,p3],[10,10,20])
xr, yr, zCeil, zFloor, zGround, floorTen = itcs.platformMap(
   cableRes=5, gridRes=10, heightRes=0.5, minClearance=2, maxTension=2000, weight=500
)

# <codecell>

def tcsMap(title, arg):
    plt.figure(figsize=(14,10))
    

    ax = plt.subplot(111, aspect='equal')
    pres.showInstallation2d(ax, itcs, [200,700], [1300,1500])
    
    cs = plt.contourf(xr, yr, arg)
    
    ax.set_title(title)

    cb = plt.colorbar(cs, shrink=0.6)
    cb.set_label(title)

def tcsMapAll():

    colHigh = zCeil - zGround
    valid = np.isfinite(colHigh)
    area = np.count_nonzero(valid) * gridRes ** 2
    volume = np.sum(colHigh[valid]) * gridRes ** 2
    s = '''<table>
    <tr><th>Accessible ground area</th><td>{:,} $m^2$</td></tr>
    <tr><th>Accessible airspace volume</th><td>{:,} $m^3$</td></tr>
    '''.format(int(area), int(volume))
    HTML(s)    
    
    tcsMap('Maximum Elevation of Platform [m]', zCeil)
    tcsMap('Minimum Safe Elevation of Platform [m]', zFloor)
    tcsMap('Height Range of Platform [m]', zCeil - zFloor)
    tcsMap('Maximum Height of Platform Above Canopy [m]', zCeil - zGround)
    tcsMap('Minimum Safe Height of Platform  Above Canopy [m]', zFloor - zGround)
    tcsMap('Cable Tension To Hold Platform At Minimum Elevation [N]', floorTen)

    

# <codecell>

tcsMapAll()

# <codecell>

cow = coweeta.Coweeta()
cow.loadWatersheds()
cow.loadGradientPlots()
cow.setWorkingRefPoint((277000, 3880000))

gridRes = 10
itcs = inst.InstalledTCS(cow)
p1, p2, p3 = ([370, 1290], [1175, 1240], [1040, 790])
itcs.positionMasts([p1,p2,p3],[40,40,50])
xr, yr, zCeil, zFloor, zGround, floorTen = itcs.platformMap(
   cableRes=5, gridRes=gridRes, heightRes=0.5, minClearance=2, maxTension=2000, weight=200
)

tcsMapAll()

# <markdowncell>

# ##Further Observations
# 
# Increasing the load from 200N to 500N (40lb to 100lb) resulted in an increase of only 50% in cable tension.  It also lowers the minimum operating envelope by a number of metres over much of the range.

# <markdowncell>

# #Engineering Challenges
# 
# ## Initial Threading Of The Cables
# Care is taken to keep the mast-platform cables above the canopy.  How should the cable be installed in the first place?  
# * Nylon fishing line with helium filled balloons attached at regular intervals to render it neutrally buoyant.  
# * Use a quadrotor to drag the nylon line from one mask to another
# * 
# This would need to occur on a windless, sunless day.
# 

# <headingcell level=2>

# Blimp/ Dirigible

# <markdowncell>

# $20000 for 9m blimp with max 3kg payload http://www.eblimp.com/eblimp/Blimp_Packages.html
# 
# http://www.theblimpworks.com/30blimp.htm 30 ft. Advertising Blimps $4919 LENGTH = 30 FT. VOLUME = 1510 CUBIC FT. DIAMETER = 10' NET LIFT = 47.1 POUNDS
# 
# http://www.galaxyblimps.com/outdoor50.html 50'
# 
# 12m http://www.islinc.com/REAPInformationSheet.pdf
# 
# Underslung raft system http://www.lindstrandtech.com/aerostat-main/airships/thermal-airships/
# 
# http://www.cleyet-marrel.com/site/Arboglisseur-Presentation.41c72.html?lang=en
# 
# ##Issues
# * housing when not in use
# * replacing escaped helium
# * navigating close to canopy
# * retrieval if crashed
# * reacting to looming wind
# * small payload
# * short mission length unless gas engines are used
# * can one be designed to land on canopy?
# * how would it be anchored?

# <codecell>


