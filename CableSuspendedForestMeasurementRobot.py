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
c.solveParams()
cs.showCable(c)

# <markdowncell>

# The horizontal components of each of the three cables' tension must cancel for the platform to be static.
# The ratios between the cables' Th is determined by the horizontal alignment of the system components only.  The three Th values are adjusted up or down by the same amount to control the platform's z value.  Note that the ratios between net tension in the cable will not necessarily remain constant.

# <codecell>

import presentation as pres
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
# As an exercise, we shall specify a system to provide coverage of most of watershed 18, which contains 3 high value plots.

# <codecell>

import coweeta
import osgeo.ogr as oo
sws = oo.Open('coweeta_subwatersheds/coweeta_subwatersheds.dbf')
l = sws.GetLayerByIndex(0)
numFeat = l.GetFeatureCount()
# print('numFeat', numFeat)
f = l.GetFeature(0)
gr = f.GetGeometryRef()
# print('feat', f)

plt.figure(figsize=(12,8))
ax = plt.subplot(111)
# c.combPlot([0,0], [1e7,1e7], ax)

import json
jd = json.JSONDecoder()
for i in range(numFeat):
    
    f = l.GetFeature(i)
    gr = f.GetGeometryRef()
    # print gr
    geom = gr.ExportToJson()


    struct = jd.decode(geom)
    
    coords = struct['coordinates'][0]

    x, y = [[ss[i] for ss in coords] for i in [0,1]]

    ax.plot(x, y) # , z,'r')

# <codecell>

import coweeta
plt.figure(figsize=(12,8))
coweeta.doWire()

# <codecell>

plt.figure(figsize=(12,8))
coweeta.doStream()

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

# <codecell>


