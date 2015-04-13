# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Investigation into Feasibility of a Permanent Cable Based Canopy Access System at Coweeta Hydrologic Laboratory

# <markdowncell>

# Dave Hawthorne 2015

# <headingcell level=2>

# Background

# <markdowncell>

# Collecting data from forests is a labour intensive exercise.  The difficulty increases with vertical distance from the forest floor.  Conducting measurement in and above the canopy is particularly problematic.  What methods exist, such as slingshotting ropes into the canopy, are haphazard and potentially dangerous as operators need to be positioned below.  
# 
# This document investigates the feasability of a permanently installed cable-suspended parallel robot that traverses the airspace above the canopy of a selected study site.
# 
# The system consists of three masts that project above the canopy on hill slopes above the study site.  From each mast a cable runs to a suspended platform.  That platform can be positioned at any point in the airspace above the canopy by combinations of winching in/playing out cable from the masts.  The platform houses a fourth winch that positions a second mobile unit, the bob, below it.  This bob would house measurement equipment and would decend to the canopy and below.
# 
# The lack of obstacles above the canopy permits automated positioning of the platform, and therefore routine automated measurement.  

# <codecell>

%load_ext autoreload
%autoreload 2
%matplotlib inline

# <codecell>

import presentation as pres
pres.showExampleSystem3d()

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
import coweeta

# <codecell>

c = cs.Cable(z1=5, z2=4, w=10,  0.035)
c.setHorizForce(1)  # newtons
pres.showCable(c)

# <markdowncell>

# The horizontal components of each of the three cables' tension must cancel for the platform to be static.
# The ratios between the cables' Th is determined by the horizontal alignment of the system components only.  The three Th values are adjusted up or down by the same amount to control the platform's z value.  Note that the ratios between net tension in the cable will not necessarily remain constant.

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

# The cable used to support the platform needs to have high tensile strength, low elasticity and low mass.  It needs to be abrasion resistant and UV stabilised.  It also needs to be available in a single lengths that can span the installation.  An ideal candidate is polyester/kevlar kernmantle rope such as http://www.pelicanrope.com/kevlarropes.html
# 
# The 1/4" offering from this manufacturer is sufficient for our purposes.  There are able to supply the cable in lengths over 1000m  At these lengths cost is around $1 per metre.
# 
# The cable that the bob decends on does not need to be as high performance.  It will be exposed to greater abrasion through being spoolled more frequently and from contact with vegetation.  Use of a fibre with greater elasticity (dynamic rather than static rope) may protect the bob, platform and kevlar cabling from shock loads such as the bob dropping a short distance from a branch. 

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
"cable weight: {:0.3f}N/m; tensile strength: {:0.3f}kN".format(cw, ts/1000)

# <markdowncell>

# #The Bob
# 
# In a given installation the platform suspended between the masts may not be able to be lowered to the canopy in some or most of the operating range.  This is because of the droop of the cables under their own weight can cause them to be closer to the canopy than the platform - particularly on steep slopes.  The solution is to employ a second mobile unit, the bob which hangs vertically from the platform.
# 

# <markdowncell>

# ##Bob Design
# 
# The design of the cable robot is simplified by the absence of snags.  Tensioning of the cables would keep the platform and all cables at a safe distance above the highest trees to avoid snagging.  If the system is to employ a bob the descends into the canopy and below then care will have to be paid to minimising and managing snags.  
# 
# * Use imaging/lidar to identify clear descent columns
# * Monitor position and tilt of the bob as it descends
# * Have the bob descend on a single line
# * Construct the bob so that its centre of gravity is low
# * Employ a teardrop profile to aid extraction
# * Rate the cables and masts to cater for an extraction force to pull through snags
# * Allow the bob line to be unspooled completely so that if upwards extraction is prevented then the bob might be lowered to the ground for manual retrieval.  Carry enough bob cable to reach the ground.
# 
# If the bob were to be lowered on two reasonably well spaced lines through uninterupted space then the horizontal orientation of the bob might be fixed by those two lines.  The presence of branches and other vegetation would interfer with this arrangement.  Use of two lines increases the likelihood of snagging so this proposal uses a single line.  For all but simple point measurements (temperature/atmosphere samples) the orientation of the bob matters.  
# 
# * Rotate and stabilise the bob using a coaxial reaction wheel.
# * use fans and ducts to blow air to rotate the bob.   
# * allow the bob to rotate freely but record the orientation to allow correction post measurement.
# 
# The design of the bob involves a number of technical risks.

# <markdowncell>

# #Cable Winching
# 
# The cables are under significant tension which has an impact on how we manipulate them.  Energy expended moving an object distance $d$ against a force $f$ is the product of the two, i.e. $e = f \dot d$.   To reel in by 1m a cable under 1kN of tension will require 1kJ.  To do this in 1s will require a 1kW rated motor.  At the same time this winch is working the other winches would be reeling out cable under tension.  The energy 'stored'is these cables is either dumped in the winch motors or, ideally, harvested for distribution to the other winches or stored locally for this winch's later use.
# 
# Distribution of the energy electrically would require cabling rated to 1kW.  110V, 9A.  This would need to be mounted on power poles and routed to a common point.  
# 
# Mechanical distrubution of the energy would be achived by running two of the cables to their respective masts and then back to the third mast.  All three winches would be located at this third mast.  The two non-winch masts would simply have pulley assemblies that let the cable run unencumbered.  They might have monitoring equipment such as odometers or cameras but these items could be powered by photovoltaics and batteries.  There are several disadvantages to this arrangement.  First, the vertical load on the unpowered masts is effectively doubled, as whatever tension is present on the section of cable running to the platform will exist on the return cable which will potentially pulling in much the same direction.  The winch mast has around three times the tension of a single cable.  
# 
# The use of return lines introduces an extra constraint on operation - there would be a minimum tension acheivable on these cables imposed by the terrain between the pulley masts and the winch mast. 
# 
# These are significant design issues yet returning all cables to the one mast has one significant advantage.
# 
# ##Mechanical Energy Harvesting Winch Assembly
# 
# If the three cables are all returned to the same winch assembly then the transfer of energy from one cable to the others can be performed purely mechanically; allowing the electric motors to be reduced in power capacity.  
# In theory, a possible arrangement is the three winches interconnected by three differential gear assemblies, an electric motor driving each differential.

# <headingcell level=2>

# Positioning

# <markdowncell>

# The system is suited to cove locations with steep sides. 
# 
# As an exercise, we shall specify a system to provide coverage of some of watershed 18, which contains 3 high value plots.

# <codecell>

pres.coweetaMap()

# <codecell>


# <codecell>

from matplotlib import cm

cow = coweeta.Coweeta()
cow.loadWatersheds()
cow.loadGradientPlots()
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

import tcsInteract

# <codecell>

myi = tcsInteract.InteractiveTscModel(cow)
myi.initialMastPositions([[820, 1430], [1175, 1240], [1040, 790]])
myi.initialMastHeights([40, 50, 50])
myi.initialPlatformLoc([975, 1150], 50)
myi.interact()

# <markdowncell>

# # Modelling an Example System
# As part of a feasibility investigation, we will pick a site within the Coweeta and model an installation that covers it.  Watershed 18 has been identified as a high value site that might warrant such as significant long term investment.  
# 
# * There are three long term study plots in WS18: 118, 218 and 318.  
# * Its steep slopes are favorable to the cable system.  
# * It has reticulated electricity located nearby (where the service road reaches the boundary of WS17)
# * Masts installed on it would have line of sight to the Coweeta buiding complex allowing radio/microwave telemetry
# 
# ## Mast Positioning
# 
# To minimise required mast height, they are best placed on or near ridge lines overlooking the site.  Two locations are apparent for WS18: its southernmost and easternmost corners.  These are both situated high above the catchment.  The south mast is 300m from powerThe third mast location is more tricky.  The northern corner of the catchment is its bottom and provides no advantage of elevation.  A mast at this location would need to extend well above the canopy.  An alternative is to place the third mast well west of WS18.  The obvious location would be near to the ridge of high top.  This is a significant distance from the other two masts - around 850m.  As there is no power at High Top the cable would need to be winched at another mast and run through a pulley at the High Top mast.  So the total cable length would need to be twice this distance, plus allowance for droop, of the order of 2km long.  This would be particularly susceptable to wind effects.  Another disadvantage of using High Top is that the northern third of WS18 is not covered.
# 
# 

# <markdowncell>

# # Exercising System
# 
# The following is a interactive model of the WS18 TCS.  The position of the platform can be adjusted in all three axes.  The weight can also be controlled.

# <codecell>

myi = tcsInteract.InteractiveTscModel(cow)
myi.initialMastPositions([[332, 1280], [1175, 1240], [1040, 790]])
myi.initialMastHeights([40, 40, 50])
myi.initialPlatformLoc([975, 1150], 50)
myi.interact()


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

cow = coweeta.Coweeta()
cow.loadWatersheds()
cow.loadGradientPlots()
cow.setWorkingRefPoint((277000, 3880000))

gridRes = 10
itcs = inst.InstalledTCS(cow)
p1, p2, p3 = ([332, 1280], [1175, 1240], [1040, 790])

itcs.positionMasts([p1,p2,p3],[40,40,50])
xr, yr, zCeil, zFloor, zGround, floorTen, ceilTen = itcs.platformMap(
   cableRes=5, gridRes=10, heightRes=0.5, minClearance=2, maxTension=1500, weight=200,
   showProgress=True
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

def tcsMap(title, arg):
    plt.figure(figsize=(16,10))
    
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
tcsMap('Cable Tension To Hold Platform At Minimum Elevation [N]', floorTen[:,:,0])
tcsMap('Cable Tension To Hold Platform At Minimum Elevation [N]', floorTen[:,:,1])
tcsMap('Cable Tension To Hold Platform At Minimum Elevation [N]', floorTen[:,:,2])


# <codecell>


itcs = inst.InstalledTCS(cow)
p1, p2, p3 = ([332, 1280], [1175, 1240], [1040, 790])
itcs.positionMasts([p1,p2,p3],[40,40,50])
xr, yr, zCeil, zFloor, zGround, floorTen, ceilTen = itcs.platformMap(
   cableRes=5, gridRes=10, heightRes=0.5, minClearance=2, maxTension=2000, weight=500,
   showProgress=True
)

# <codecell>

xws18, yws18, zws18 = itcs.terrain.wsBoundary(18)
tcsMap('Maximum Elevation of Platform [m]', zCeil)
tcsMap('Minimum Safe Elevation of Platform [m]', zFloor)
tcsMap('Height Range of Platform [m]', zCeil - zFloor)
tcsMap('Maximum Height of Platform Above Canopy [m]', zCeil - zGround)
tcsMap('Minimum Safe Height of Platform  Above Canopy [m]', zFloor - zGround)
tcsMap('Cable Tension To Hold Platform At Minimum Elevation [N]', floorTen[:,:,0])
tcsMap('Cable Tension To Hold Platform At Minimum Elevation [N]', floorTen[:,:,1])
tcsMap('Cable Tension To Hold Platform At Minimum Elevation [N]', floorTen[:,:,2])

# <codecell>

from matplotlib import cm

cow = coweeta.Coweeta()
cow.loadWatersheds()
cow.loadGradientPlots()
cow.setWorkingRefPoint((277000, 3880000))

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
xr, yr, zCeil, zFloor, zGround, floorTen, ceilTen = itcs.platformMap(
   cableRes=5, gridRes=gridRes, heightRes=0.5, minClearance=2, maxTension=2000, weight=200,
   showProgress=True

)

tcsMapAll()

# <markdowncell>

# ##Further Observations
# 
# * Increasing the load from 200N to 500N (40lb to 100lb) resulted in an increase of only 50% in cable tension.  It also lowers the minimum operating envelope by a number of metres over much of the range.
# 

# <markdowncell>

# #Masts
# The masts would need to be steadied by guy lines, particularly to resist the pull from the kevlar cable.  A candidate would be the Rohn 45G guyed tower system (http://www.rohnnet.com/rohn-45g-tower).  A structural engineer would need to be retained to design the masts.  The mast may need to be positioned below ridge lines to allow the guys to be adequately anchored.  There is also an approval process that must be followed to ensure public safety and protection of cultural and natural values.
# 

# <markdowncell>

# 
# ##Occupational Health and Safety Considerations
# 
# A cable suspended robot operating in a forest introduces some additional OHS considerations:
# 
# * Hazard from platform and bob falling on someone
# * Hazard of branches falling
# * Cables snapping
# * unauthorised access of masts
# * electrical safety around winches
# * OHS during installation
# * fire hazard
# 
# The system and its operation would need to comply with FS OHS requirements. 
# 
# ### Overhead Hazards
# 
# Should a system failure cause the platform/bob assembly to free fall to the ground it would hit at $v = \sqrt{ 2 g h }$ with $g = 9.8ms^2$ and h being height in $m$.  So for a drop of 50m, the impact speed is $v \approx 30 ms^{-1} \approx 71mph$
# 
# The system operating overhead may increase the likelihood of branches being dislodged and falling.  A protocol would need to be developed to exclude staff from the area that the platform is operating.  Should human intervention be required - for example unsnagging the bob then the system would need to be under manual control.
# 
# Stategies to protecting the general public from falling hazards might include:
# 
# * installing the system in a rarely visited watershed
# * placing warning signs on access roads and tracks to the site
# * potentially fitting a beeper to the platform or bob that is sounded when the unit is in motion - similar to the reverse indicator on motor vehicles.
# 
# In the example WS18 installation, the heavily utilized Ball Creek Road sits underneath the western reach of the platform range.  The platform and bob could potentially sit 100m above the road surface.  For a 20kg assembly, the gravitational potential energy is $20 * 9.8 * 100 \approx 520kJ$.  The impact speed would be $v \approx 45 ms^{-1} \approx 100mph$.  Keeping the platform west of the road by a safety margin might be a necessary requirement.
# 
# ### Cable Snapping
# 
# The stored energy in the system can also hazardous through the whiplash of a cable failing.  The strategies employed to limit risk from falling objects will reduce this risk.  In addition:
# 
# * We would operate the cables well within their rated limits.  
# * The platform and bob would be housed during high wind days.
# * The cables would be automatically monitored for elongation over time by correlating platform position with winch rotation counts.  Wear and damage of the cables' polyester mantle could be performed by cameras located at the mast.

# <markdowncell>

# #Other Considerations
# 
# ## Visual Ammenity
# A cable robot installation will be visible to forest users:
# * masts are positioned on ridge lines and project well above the canopy
# * the cables are located well above the canopy, particular in valleys.  Although the platform and bob can be housed when not in operation the cable must still be exposed.
# * When in operation, the platform and bob would be visible from a distance.
# 
# The default cable colour is white.  Less pronounced colours may be available, but impact on UV stability would need to be investigated.  At a distance 1/4" cable may not necessarily be perceivable.  Given that Coweeta is a research forest having a highly visible experiment is not necessarily detrimental.
# 
# ## Vandalism
# The visibility of the installation will attract the curiousity of forest users and potentially attract vandalism.  The thousands of dollars of kevlar cabling might be stolen.  The masts would need to have anticlimb panels fitted.
# From a security perspective winch assembly would idealy be located above these panels - so long as this doesn't compromise operator safety during servicing.  Given this would be a networked device the threat of remote hacking needs to be considered.
# 
# 
# 
# ## Animal Attack and Infestation
# Other than the mast bases and guy lines, no component of the installation would be in contact with the ground.  The guys and anticlimb panels would need to prevent animal access in addition to unauthorised human access.
# 
# The only ground located component of the system would be the winch assembly.  This might need to be armoured to prevent bear damage.
# 

# <markdowncell>

# #Electronics and Communications
# 
# The platform, bob and each of the masts would house embedded computers, all interconnected via a Wi-Fi network.  Directional antennas may be required. Each would have GPS recievers.  The masts receivers would provide realtime differential GPS capability to the platform and bob.  Each node would have video camera for monitoring.  The masts and platform would have anemometers to monitor local winds.   
# 
# Although power and data cabling could be routed to the platform and then to the bob these would dramatically increase the complexity of the system and impact on reliability.  The conductors could conceviably be embedded in the kevlar cable however this would be a custom manufacture, it would impact on the cable mass.  Accessing the terminals from the cable drum would be difficult.  A separate non-loaded cable could be used but this would still pose issues.  System design is far easier if the mobile components each have their own energy store in the form of batteries and rely on radio communications to the masts.  These batteries can be recharged automatically when the units are housed.  The platform battery must be sized to power the bob winch.  The vertical travel of the bob would be greater than the horizontal travel of the platform.  Ideally this battery would not need recharging more than once a day.   
# 
# Reliable electrical contact for recharging would need to be investigated.
# 
# * Radio link between Coweeta office complex and the powered mast.  This might be microwave if a appropriately priced system is available.  Alternatively an IEEE 802.11 Wi-Fi link could serve if directional antennas are used.  If the powered mast doesn't have line-of-sight to the offices then communications would be relayed through an unpowered mast.  A suitably sized photovoltaic system would be needed.
# * Radio link between the platform and the powered mast
# * Radio link between bob and platform
# * data storage should the uplink be degraded due to atmospheric conditions.

# <markdowncell>

# # Software
# The system would be built with open source software and all design would in turn be open source.
# 
# Besides the work needed for the scientific data gathering effort these are some of the components of software design:
# 
# * positioning awareness, GPS, cable spool tracking, machine vision
# * winch control
# * path calculation
# * communication management
# * human interface/manual override process
# * system shutdown and housing process (including emergency shutdown due to winds)
# * control and data security - prevent hacking
# * power monitoring
# * software upgrade - try to avoid having people climbing the masts to upgrade software.
# * bob descent algorithm: checking that there is a clear pathand/or identifying interference
# * bob direction control
# * cable elongation monitoring.
# * data storage and management 

# <markdowncell>

# ##System costs
# 
# ###Costing of the masts
# Design, approval, purchase and installation of the three masts is likely to be single greatest initial outlay for the system.  The masts and their guy wires will need to be designed to withstand the significant sideways forces imparted by the cables.  Wind load on the cables as well as directly on the tower must be allowed for.  Being positioned on ridge lines, access for construction is likely to add cost.  The Forest Service mandated inspection and maintenance regime will contribute an ongoing cost.
# 
# ### Provision of electrical power
# The tensioning of the kevlar cables mean that substantial energy is required to position the platform, even if a central winch assembly allows energy harvesting from unwinding cables.  To facilitate reasonable platform travel speeds we would need mains power.  For the example WS18 system this would involve extending the powerline to WS17 by another 300m.
# 
# ### Winch Assembly
# The three cables all terminate at a series of interconnected winches located on one of the masts.  This is powered by three electrical motors and each winch would have an electronic brake that can withstand forces imparted by worst case wind events.  The design and manufacture of such an assembly is outside my competency.
# 
# ### Electronics and Communications
# Weight and energy storage are not limiting factors freeing us to use off-the-shelf system components for much of the control system.  The rechargable batteries on the mobile components will need periodic replacement.
# 
# 
# ### Cable Purchase and Replacement
# The system exposes long lengths of kelvar cable to the elements.  The BOM cost of this cable is around $1 per metre.  The polyester mantle is UV stabilized but will ultimately degrade.  The cable would need to be replaced long before the kevlar core becomes compromised.
# 

# <markdowncell>

# #Engineering Challenges
# 
# ## Site Identification
# 
# 
# ## Initial Threading of the Cables
# Care is taken to keep the mast-platform cables above the canopy.  How should the cable be installed in the first place?  
# * Nylon fishing line with helium filled balloons attached at regular intervals to render it neutrally buoyant.  
# * Use a quadrotor to drag the nylon line from one mask to another
# * 
# This would need to occur on a windless, sunless day.
# 
# This is a high technical risk.  A trial/experiment needs to be conducted prior to undertaking the project.
# 
# ## Bob Design/Snag Mitigation
# 
# ## Winch Assembly
# 
# ## Wind Loading
# 
# ## Software
# 
# 

# <markdowncell>

# # Measurements Enabled by the System
# * temperature and windspeed measurements without air column disturbance
# * atmospheric composition measurements ($CO_2$, $H_2O$)
# * LiDAR from above and below canopy
# * photographic LAI
# * forest floor photography and data extraction through postprocessing image processing and machine vision  This might be used to suppliment manual characterisation of gradient plots.
# * leaf and branch collection for sampling
# * in situ LiCOR leaf measurement 
# * permanent positioning of instrumentation in canopy such as lysemeters and insect traps.
# * Remote visual inspection of experiments in the field.
# * autonomous resupply of experiments in the field such as replacement batteries.  This would introduce design challenges.
# 
# 
# # Additional Utility
# * Provide a communications network for other instrumentation in the field
# * masts can be used for other experiments.
# 
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


