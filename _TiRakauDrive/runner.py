#!/usr/bin/env python
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2009-2020 German Aerospace Center (DLR) and others.
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# https://www.eclipse.org/legal/epl-2.0/
# This Source Code may also be made available under the following Secondary
# Licenses when the conditions for such availability set forth in the Eclipse
# Public License 2.0 are satisfied: GNU General Public License, version 2
# or later which is available at
# https://www.gnu.org/licenses/old-licenses/gpl-2.0-standalone.html
# SPDX-License-Identifier: EPL-2.0 OR GPL-2.0-or-later

# @file    runner.py
# @author  Lena Kalleske
# @author  Daniel Krajzewicz
# @author  Michael Behrisch
# @author  Jakob Erdmann
# @date    2009-03-26

from __future__ import absolute_import
from __future__ import print_function

import numpy as np
import os
import sys
import optparse
import random
array = (3, 4)
print(array[0])
# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # noqa
import traci  # noqa

# needs work
def generate_routefile():
    random.seed(42)  # make tests reproducible
    
    # demand per second from different directions
    pse4235 = (32. / 300, 23. / 300)
    pnw4235 = (19. / 300, 19. / 300)
    pnorth4219 = (64. / 300, 79. / 300)
    psouth4219 = (50. / 300, 41. / 300)
    psouth4220 = (33. / 300, 37. / 300)
    pnorth4221 = (84. / 300, 64. / 300)
    psouth4221 = (31. / 300, 17. / 300)
    pne4221 = (5. / 300, 4. / 300)
    pse4221 = (2. / 300, 1. / 300)
    pnw4221 = (0, 4. / 300)
    p4235e4219n = (99. / 300, 90. / 300)
    p4235n4219n = (6. / 300, 5. / 300)
    p4235e4219s = (30. / 300, 24. / 300)
    p4235n4219s = (2. / 300, 1. / 300)
    
    p4235e4220n = (4. / 300, 19. / 300)
    p4235n4220n = (0, 1. / 300)
    p4235e4220s = (4. / 300, 3. / 300)
    p4235n4220s = (0. / 300, 0. / 300)
    p4219s4220n = (1. / 300, 4. / 300)
    p4219s4220s = (0. / 300, 1. / 300)
    p4219n4220n = (0. / 300, 3. / 300)
    p4219n4220s = (0. / 300, 0. / 300)
    
    p4235e4221n = (30. / 300, 33. / 300)
    p4235n4221n = (2. / 300, 2. / 300)
    p4235e4221s = (7. / 300, 19. / 300)
    p4235n4221s = (0. / 300, 1. / 300)
    p4219s4221n = (6. / 300, 6. / 300)
    p4219s4221s = (1. / 300, 4. / 300)
    p4219n4221n = (2. / 300, 5. / 300)
    p4219n4221s = (0. / 300, 3. / 300)
    p4220s4221n = (4. / 300, 5. / 300)
    p4220s4221s = (1. / 300, 3. / 300)
    
    p4235e4221e = (47. / 300, 18. / 300)
    p4235n4221e = (3. / 300, 1. / 300)
    p4219s4221e = (9. / 300, 4. / 300)
    p4219n4221e = (3. / 300, 3. / 300)
    p4220s4221e = (7. / 300, 3. / 300)
    
    with open("data/osm.rou.xml", "w") as routes:
        print("""<routes>

        <route id="se4235" edges="619523290#0 619523290#1 619523288 61645695 628341438#0 628341438#1" />
        <route id="nw4235" edges="-628341438#1 -628341438#0 gneE6 619523287#0.17 619523287#1" />
        <route id="north4219" edges="620377515  122089525 122089525.34 620377496 620377502#0 620377502#1 620377501#0" />
        <route id="south4219" edges="620377506 620377506.61 28597169 620377494 547625725" />
        <route id="south4220" edges="gneE7 gneE12 624439643 66457665 665260214#0" />
        <route id="north4221" edges="-620463733 -620377511 -112543664 28573008 620377512 28573048 669665014 669665015#1 28594060#0 28594060#1 28594060#2 28594060#3 28594060#4" />
        <route id="south4221" edges="-28594060#4 -28594060#3 -28594060#2 -28594060#1 -28594060#0 669665013 669665011 7635630#0 7635630#1 207149704#0 207149704#1 112543664 620377510 620463733" />
        <route id="ne4221" edges="-620463733 -620377511 -112543664 28573008 620377512 7637388#0 7637388#1 28573015#0 28573015#1 28573015#2 28573015#3 28573015#4 28573015#5 28573015#6" />
        <route id="se4221" edges="-28594060#4 -28594060#3 -28594060#2 -28594060#1 -28594060#0 669665013 669665011 7635630#0 28572986 7637388#1 28573015#0 28573015#1 28573015#2 28573015#3 28573015#4 28573015#5 28573015#6" />
        <route id="nw4221" edges="-28573015#6 -28573015#5 -28573015#4 -28573015#3 -28573015#2 -28573015#1 -28573015#0 28573025 28573025.46 28573025.65 28573048 669665014 669665015#1 28594060#0 28594060#1 28594060#2 28594060#3 28594060#4" />
        
        <route id="r4235e4219n" edges="619523290#0 619523290#1 619523288 619526570#0 619526570#1 620377514#1 619526569#1 619526568 619526567 gneE1 gneE1.31 620377502#0 620377502#1 620377501#0" />
        <route id="r4235n4219n" edges="-628341438#1 -628341438#0 -61645695 619526570#0 619526570#1 620377514#1 619526569#1 619526568 619526567 gneE1 gneE1.31 620377502#0 620377502#1 620377501#0" />
        <route id="r4235e4219s" edges="619523290#0 619523290#1 619523288 619526570#0 619526570#1 620377514#1 619526569#1 619526568 619526567 619526566 28597169 620377494 547625725" />
        <route id="r4235n4219s" edges="-628341438#1 -628341438#0 -61645695 619526570#0 619526570#1 620377514#1 619526569#1 619526568 619526567 619526566 28597169 620377494 547625725" />
        
        <route id="r4235e4220n" edges="619523290#0 619523290#1 619523288 619526570#0 619526570#1 620377514#1 619526569#1 619526568 619526567 619526566 122089528#1 620377517 gneE3 28641509" />
        <route id="r4235n4220n" edges="-628341438#1 -628341438#0 -61645695 619526570#0 619526570#1 620377514#1 619526569#1 619526568 619526567 619526566 122089528#1 620377517 gneE3 28641509" />     
        <route id="r4235e4220s" edges="619523290#0 619523290#1 619523288 619526570#0 619526570#1 620377514#1 619526569#1 619526568 619526567 619526566 122089528#1 620377517 620377517.54 624439643 66457665 665260214#0" />
        <route id="r4235n4220s" edges="-628341438#1 -628341438#0 -61645695 619526570#0 619526570#1 620377514#1 619526569#1 619526568 619526567 619526566 122089528#1 620377517 620377517.54 624439643 66457665 665260214#0" />
        <route id="r4219s4220n" edges="620377506 gneE2 620377517 gneE3 28641509" />
        <route id="r4219s4220s" edges="620377506 gneE2 620377517 620377517.54 624439643 66457665 665260214#0" />
        <route id="r4219n4220n" edges="620377515  122089525 122089525.34 122089528#1 620377517 gneE3 28641509" />
        <route id="r4219n4220s" edges="620377515  122089525 122089525.34 122089528#1 620377517 620377517.54 624439643 66457665 665260214#0" />
        
        <route id="r4235e4221n" edges="619523290#0 619523290#1 619523288 619526570#0 619526570#1 620377514#1 619526569#1 619526568 619526567 619526566 122089528#1 620377517 620377517.54 624439645 620377518 28573047 669665014 669665015#1 28594060#0 28594060#1 28594060#2 28594060#3 28594060#4" />
        <route id="r4235n4221n" edges="-628341438#1 -628341438#0 -61645695 619526570#0 619526570#1 620377514#1 619526569#1 619526568 619526567 619526566 122089528#1 620377517 620377517.54 624439645 620377518 28573047 669665014 669665015#1 28594060#0 28594060#1 28594060#2 28594060#3 28594060#4" />      
        <route id="r4235e4221s" edges="619523290#0 619523290#1 619523288 619526570#0 619526570#1 620377514#1 619526569#1 619526568 619526567 619526566 122089528#1 620377517 620377517.54 624439645 620377518 159605088 207149704#0 207149704#1 112543664 620377510 620463733" />
        <route id="r4235n4221s" edges="-628341438#1 -628341438#0 -61645695 619526570#0 619526570#1 620377514#1 619526569#1 619526568 619526567 619526566 122089528#1 620377517 620377517.54 624439645 620377518 159605088 207149704#0 207149704#1 112543664 620377510 620463733" />
        <route id="r4219s4221n" edges="620377506 gneE2 620377517 gneE3 28641509 620377517 620377517.54 624439645 620377518 28573047 669665014 669665015#1 28594060#0 28594060#1 28594060#2 28594060#3 28594060#4" />
        <route id="r4219s4221s" edges="620377506 gneE2 620377517 gneE3 28641509 620377517 620377517.54 624439645 620377518 159605088 207149704#0 207149704#1 112543664 620377510 620463733" />
        <route id="r4219n4221n" edges="620377515  122089525 122089525.34 122089528#1 620377517 620377517.54 624439645 620377518 28573047 669665014 669665015#1 28594060#0 28594060#1 28594060#2 28594060#3 28594060#4" />
        <route id="r4219n4221s" edges="620377515  122089525 122089525.34 122089528#1 620377517 620377517.54 624439645 620377518 159605088 207149704#0 207149704#1 112543664 620377510 620463733" />
        <route id="r4220s4221n" edges="gneE7 28641508 620377518 28573047 669665014 669665015#1 28594060#0 28594060#1 28594060#2 28594060#3 28594060#4" />
        <route id="r4220s4221s" edges="gneE7 28641508 620377518 159605088 207149704#0 207149704#1 112543664 620377510 620463733" />
        
        <route id="r4235e4221e" edges="619523290#0 619523290#1 619523288 619526570#0 619526570#1 620377514#1 619526569#1 619526568 619526567 619526566 122089528#1 620377517 620377517.54 624439645 620377518 159605088 7637388#0 7637388#1 28573015#0 28573015#1 28573015#2 28573015#3 28573015#4 28573015#5 28573015#6" />
        <route id="r4235n4221e" edges="-628341438#1 -628341438#0 -61645695 619526570#0 619526570#1 620377514#1 619526569#1 619526568 619526567 619526566 122089528#1 620377517 620377517.54 624439645 620377518 159605088 7637388#0 7637388#1 28573015#0 28573015#1 28573015#2 28573015#3 28573015#4 28573015#5 28573015#6" />
        <route id="r4219s4221e" edges="620377506 gneE2 620377517  620377517.54 624439645 620377518 159605088 7637388#0 7637388#1 28573015#0 28573015#1 28573015#2 28573015#3 28573015#4 28573015#5 28573015#6" />
        <route id="r4219n4221e" edges="620377515  122089525 122089525.34 122089528#1 620377517 620377517.54 624439645 620377518 159605088 7637388#0 7637388#1 28573015#0 28573015#1 28573015#2 28573015#3 28573015#4 28573015#5 28573015#6" />
        <route id="r4220s4221e" edges="gneE7 28641508 620377518 159605088 7637388#0 7637388#1 28573015#0 28573015#1 28573015#2 28573015#3 28573015#4 28573015#5 28573015#6" />""", file=routes)
        vehNr = 0
        N = 300  # number of time steps
        for i in range(2):
            for j in range(N):
                if random.uniform(0, 1) < pse4235[i]:
                    print('    <vehicle id="se4235_%i" route="se4235" depart="%i" />' % (
                        vehNr, (i*N)+j), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < pnw4235[i]:
                    print('    <vehicle id="nw4235_%i" route="nw4235" depart="%i" />' % (
                        vehNr, (i*N)+j), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < pnorth4219[i]:
                    print('    <vehicle id="north4219_%i" route="north4219" depart="%i" />' % (
                        vehNr, (i*N)+j), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < psouth4219[i]:
                    print('    <vehicle id="south4219_%i" route="south4219" depart="%i" />' % (
                        vehNr, (i*N)+j), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < psouth4220[i]:
                    print('    <vehicle id="south4220_%i" route="south4220" depart="%i" />' % (
                        vehNr, (i*N)+j), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < pnorth4221[i]:
                    print('    <vehicle id="north4221_%i" route="north4221" depart="%i" />' % (
                        vehNr, (i*N)+j), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < psouth4221[i]:
                    print('    <vehicle id="south4221_%i" route="south4221" depart="%i" />' % (
                        vehNr, (i*N)+j), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < pne4221[i]:
                    print('    <vehicle id="ne4221_%i" route="ne4221" depart="%i" />' % (
                        vehNr, (i*N)+j), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < pse4221[i]:
                    print('    <vehicle id="se4221_%i" route="se4221" depart="%i" />' % (
                        vehNr, (i*N)+j), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < pnw4221[i]:
                    print('    <vehicle id="nw4221_%i" route="nw4221" depart="%i" />' % (
                        vehNr, (i*N)+j), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < p4235e4219n[i]:
                    print('    <vehicle id="r4235e4219n_%i" route="r4235e4219n" depart="%i" />' % (
                        vehNr, (i*N)+j), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < p4235n4219n[i]:
                    print('    <vehicle id="r4235n4219n_%i" route="r4235n4219n" depart="%i" />' % (
                        vehNr, (i*N)+j), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < p4235e4219s[i]:
                    print('    <vehicle id="r4235e4219s_%i" route="r4235e4219s" depart="%i" />' % (
                        vehNr, (i*N)+j), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < p4235n4219s[i]:
                    print('    <vehicle id="r4235n4219s_%i" route="r4235n4219s" depart="%i" />' % (
                        vehNr, (i*N)+j), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < p4235e4220n[i]:
                    print('    <vehicle id="r4235e4220n_%i" route="r4235e4220n" depart="%i" />' % (
                        vehNr, (i*N)+j), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < p4235n4220n[i]:
                    print('    <vehicle id="r4235n4220n_%i" route="r4235n4220n" depart="%i" />' % (
                        vehNr, (i*N)+j), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < p4235e4220s[i]:
                    print('    <vehicle id="r4235e4220s_%i" route="r4235e4220s" depart="%i" />' % (
                        vehNr, (i*N)+j), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < p4235n4220s[i]:
                    print('    <vehicle id="r4235n4220s_%i" route="r4235n4220s" depart="%i" />' % (
                        vehNr, (i*N)+j), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < p4219s4220n[i]:
                    print('    <vehicle id="r4219s4220n_%i" route="r4219s4220n" depart="%i" />' % (
                        vehNr, (i*N)+j), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < p4219s4220s[i]:
                    print('    <vehicle id="r4219s4220s_%i" route="r4219s4220s" depart="%i" />' % (
                        vehNr, (i*N)+j), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < p4219n4220n[i]:
                    print('    <vehicle id="r4219n4220n_%i" route="r4219n4220n" depart="%i" />' % (
                        vehNr, (i*N)+j), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < p4219n4220s[i]:
                    print('    <vehicle id="r4219n4220s_%i" route="r4219n4220s" depart="%i" />' % (
                        vehNr, (i*N)+j), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < p4235e4221n[i]:
                    print('    <vehicle id="r4235e4221n_%i" route="r4235e4221n" depart="%i" />' % (
                        vehNr, (i*N)+j), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < p4235n4221n[i]:
                    print('    <vehicle id="r4235n4221n_%i" route="r4235n4221n" depart="%i" />' % (
                        vehNr, (i*N)+j), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < p4235e4221s[i]:
                    print('    <vehicle id="r4235e4221s_%i" route="r4235e4221s" depart="%i" />' % (
                        vehNr, (i*N)+j), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < p4235n4221s[i]:
                    print('    <vehicle id="r4235n4221s_%i" route="r4235n4221s" depart="%i" />' % (
                        vehNr, (i*N)+j), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < p4219s4221n[i]:
                    print('    <vehicle id="r4219s4221n_%i" route="r4219s4221n" depart="%i" />' % (
                        vehNr, (i*N)+j), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < p4219s4221s[i]:
                    print('    <vehicle id="r4219s4221s_%i" route="r4219s4221s" depart="%i" />' % (
                        vehNr, (i*N)+j), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < p4219n4221n[i]:
                    print('    <vehicle id="r4219n4221n_%i" route="r4219n4221n" depart="%i" />' % (
                        vehNr, (i*N)+j), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < p4219n4221s[i]:
                    print('    <vehicle id="r4219n4221s_%i" route="r4219n4221s" depart="%i" />' % (
                        vehNr, (i*N)+j), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < p4220s4221n[i]:
                    print('    <vehicle id="r4220s4221n_%i" route="r4220s4221n" depart="%i" />' % (
                        vehNr, (i*N)+j), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < p4220s4221s[i]:
                    print('    <vehicle id="r4220s4221s_%i" route="r4220s4221s" depart="%i" />' % (
                        vehNr, (i*N)+j), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < p4235e4221e[i]:
                    print('    <vehicle id="r4235e4221e_%i" route="r4235e4221e" depart="%i" />' % (
                        vehNr, (i*N)+j), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < p4235n4221e[i]:
                    print('    <vehicle id="r4235n4221e_%i" route="r4235n4221e" depart="%i" />' % (
                        vehNr, (i*N)+j), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < p4219s4221e[i]:
                    print('    <vehicle id="r4219s4221e_%i" route="r4219s4221e" depart="%i" />' % (
                        vehNr, (i*N)+j), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < p4219n4221e[i]:
                    print('    <vehicle id="r4219n4221e_%i" route="r4219n4221e" depart="%i" />' % (
                        vehNr, (i*N)+j), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < p4220s4221e[i]:
                    print('    <vehicle id="r4220s4221e_%i" route="r4220s4221e" depart="%i" />' % (
                        vehNr, (i*N)+j), file=routes)
                    vehNr += 1
        print("</routes>", file=routes)
                

# needs work
def run():
    """execute the TraCI control loop"""
    step = 0
    # we start with phase 2 where EW has green
    traci.trafficlight.setPhase("cluster_1707799581_314056954_5931861577", 4) # site 4235, phase C
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        if traci.trafficlight.getPhase("cluster_1707799581_314056954_5931861577") == 6:
            traci.trafficlight.setPhase("cluster_1707799581_314056954_5931861577", 3)
        step += 1

    traci.close()
    sys.stdout.flush()


def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options


# this is the main entry point of this script
if __name__ == "__main__":
    options = get_options()

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # first, generate the route file for this simulation
    generate_routefile()

    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    traci.start([sumoBinary, "-c", "data/osm.sumocfg",
                             "--tripinfo-output", "tripinfo.xml"])
    run()
