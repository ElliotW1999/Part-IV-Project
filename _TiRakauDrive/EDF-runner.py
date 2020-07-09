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
    # TODO: refactor all routes into 1 route matrix (noOfRoutes x noOfTimesteps) using numpy 
    routesList = [ # route name, route edges, vehicle density at interval i, i+1, i+2...
        ("se4235", "619523290#0 619523290#1 619523288 61645695 628341438#0 628341438#1", 32., 23.),
        ("nw4235", "-628341438#1 -628341438#0 gneE6 619523287#0.17 619523287#1", 19., 19.),
        ("north4219", "620377515  122089525 122089525.34 620377496 620377502#0 620377502#1 620377501#0", 64., 79.),
        ("south4219", "620377506 620377506.61 28597169 620377494 547625725", 50., 41.),
        ("south4220", "gneE10 gneE73 gneE79 gneE41", 33., 37.),
        ("north4221", "-620463733 -620377511 -112543664 28573008 547793367 620377512 28573048 669665014 669665015#1 28594060#0 28594060#1 28594060#2 28594060#3 28594060#4", 84., 64.),
        ("south4221", "-28594060#4 -28594060#3 -28594060#2 -28594060#1 -28594060#0 669665013 669665011 7635630#0 7635630#1 207149704#0 207149704#1 112543664 620377510 620463733", 31., 17.),
        ("ne4221", "-620463733 -620377511 -112543664 28573008 547793367 620377512 7637388#0 7637388#1 28573015#0 28573015#1 28573015#2 28573015#3 28573015#4 28573015#5 28573015#6", 5., 4.),
        ("se4221", "-28594060#4 -28594060#3 -28594060#2 -28594060#1 -28594060#0 669665013 669665011 7635630#0 28572986 7637388#1 28573015#0 28573015#1 28573015#2 28573015#3 28573015#4 28573015#5 28573015#6", 2., 1.),
        ("nw4221", "-28573015#6 -28573015#5 -28573015#4 -28573015#3 -28573015#2 -28573015#1 -28573015#0 28573025 28573025.46 28573025.65 28573048 669665014 669665015#1 28594060#0 28594060#1 28594060#2 28594060#3 28594060#4", 0, 4.),
        ("4235e4219n", "619523290#0 619523290#1 619523288 619526570#0 619526570#1 620377514#1 619526569#1 619526568 619526567 gneE1 gneE1.31 620377502#0 620377502#1 620377501#0", 99., 90.),
        ("4235n4219n", "-628341438#1 -628341438#0 -61645695 619526570#0 619526570#1 620377514#1 619526569#1 619526568 619526567 gneE1 gneE1.31 620377502#0 620377502#1 620377501#0", 6., 5.),
        ("4235e4219s", "619523290#0 619523290#1 619523288 619526570#0 619526570#1 620377514#1 619526569#1 619526568 619526567 619526566 28597169 620377494 547625725", 30., 24.),
        ("4235n4219s", "-628341438#1 -628341438#0 -61645695 619526570#0 619526570#1 620377514#1 619526569#1 619526568 619526567 619526566 28597169 620377494 547625725", 2., 1.),
        
        ("4235e4220n", "619523290#0 619523290#1 619523288 619526570#0 619526570#1 620377514#1 619526569#1 619526568 619526567 619526566 122089528#1 620377517 gneE3 gneE44", 4., 19.),
        ("4235n4220n", "-628341438#1 -628341438#0 -61645695 619526570#0 619526570#1 620377514#1 619526569#1 619526568 619526567 619526566 122089528#1 620377517 gneE3 gneE44", 0, 1.),
        ("4235e4220s", "619523290#0 619523290#1 619523288 619526570#0 619526570#1 620377514#1 619526569#1 619526568 619526567 619526566 122089528#1 620377517 gneE74 gneE79 gneE41", 4., 3.),
        ("4235n4220s", "-628341438#1 -628341438#0 -61645695 619526570#0 619526570#1 620377514#1 619526569#1 619526568 619526567 619526566 122089528#1 620377517 gneE74 gneE79 gneE41", 0., 0.),
        ("4219s4220n", "620377506 gneE2 620377517 gneE3 gneE44", 1., 4.),
        ("4219s4220s", "620377506 gneE2 620377517 gneE74 gneE79 gneE41", 0., 1.),
        ("4219n4220n", "620377515  122089525 122089525.34 122089528#1 620377517 gneE3 gneE44", 0., 3.),
        ("4219n4220s", "620377515  122089525 122089525.34 122089528#1 620377517 gneE74 gneE79 gneE41", 0., 0.),
        
        ("4235e4221n", "619523290#0 619523290#1 619523288 619526570#0 619526570#1 620377514#1 619526569#1 619526568 619526567 619526566 122089528#1 620377517 gneE74 gneE72 620377518 28573047 669665014 669665015#1 28594060#0 28594060#1 28594060#2 28594060#3 28594060#4", 30., 33.),
        ("4235n4221n", "-628341438#1 -628341438#0 -61645695 619526570#0 619526570#1 620377514#1 619526569#1 619526568 619526567 619526566 122089528#1 620377517 gneE74 gneE72 620377518 28573047 669665014 669665015#1 28594060#0 28594060#1 28594060#2 28594060#3 28594060#4", 2., 2.),
        ("4235e4221s", "619523290#0 619523290#1 619523288 619526570#0 619526570#1 620377514#1 619526569#1 619526568 619526567 619526566 122089528#1 620377517 gneE74 gneE72 620377518 159605088 207149704#0 207149704#1 112543664 620377510 620463733", 7., 19.),
        ("4235n4221s", "-628341438#1 -628341438#0 -61645695 619526570#0 619526570#1 620377514#1 619526569#1 619526568 619526567 619526566 122089528#1 620377517 gneE74 gneE72 620377518 159605088 207149704#0 207149704#1 112543664 620377510 620463733", 0., 1.),
        ("4219s4221n", "620377506 gneE2 620377517 gneE74 gneE72 620377518 28573047 669665014 669665015#1 28594060#0 28594060#1 28594060#2 28594060#3 28594060#4", 6., 6.),
        ("4219s4221s", "620377506 gneE2 620377517 gneE74 gneE72 620377518 159605088 207149704#0 207149704#1 112543664 620377510 620463733", 1., 4.),
        ("4219n4221n", "620377515  122089525 122089525.34 122089528#1 620377517 gneE74 gneE72 620377518 28573047 669665014 669665015#1 28594060#0 28594060#1 28594060#2 28594060#3 28594060#4", 2., 5.),
        ("4219n4221s", "620377515  122089525 122089525.34 122089528#1 620377517 gneE74 gneE72 620377518 159605088 207149704#0 207149704#1 112543664 620377510 620463733", 0., 3.),
        ("4220s4221n", "gneE10 28641508 620377518 28573047 669665014 669665015#1 28594060#0 28594060#1 28594060#2 28594060#3 28594060#4", 4., 5.),
        ("4220s4221s", "gneE10 28641508 620377518 159605088 207149704#0 207149704#1 112543664 620377510 620463733", 1., 3.),
        
        ("4235e4221e", "619523290#0 619523290#1 619523288 619526570#0 619526570#1 620377514#1 619526569#1 619526568 619526567 619526566 122089528#1 620377517 gneE74 gneE72 620377518 159605088 7637388#0 7637388#1 28573015#0 28573015#1 28573015#2 28573015#3 28573015#4 28573015#5 28573015#6", 47., 18.),
        ("4235n4221e", "-628341438#1 -628341438#0 -61645695 619526570#0 619526570#1 620377514#1 619526569#1 619526568 619526567 619526566 122089528#1 620377517 gneE74 gneE72 620377518 159605088 7637388#0 7637388#1 28573015#0 28573015#1 28573015#2 28573015#3 28573015#4 28573015#5 28573015#6", 3., 1.),
        ("4219s4221e", "620377506 gneE2 620377517  gneE74 gneE72 620377518 159605088 7637388#0 7637388#1 28573015#0 28573015#1 28573015#2 28573015#3 28573015#4 28573015#5 28573015#6", 9., 4.),
        ("4219n4221e", "620377515  122089525 122089525.34 122089528#1 620377517 gneE74 gneE72 620377518 159605088 7637388#0 7637388#1 28573015#0 28573015#1 28573015#2 28573015#3 28573015#4 28573015#5 28573015#6", 3., 3.),
        ("4220s4221e", "gneE10 28641508 620377518 159605088 7637388#0 7637388#1 28573015#0 28573015#1 28573015#2 28573015#3 28573015#4 28573015#5 28573015#6", 7., 3.),
        
        ("4221s4220n", "-28594060#4 -28594060#3 -28594060#2 -28594060#1 -28594060#0 669665013 669665011 7635630#0 7635630#1 624439627 547793365 158617319 gneE77 gneE76 gneE44", 1., 2.),
        ("4221n4220n", "-620463733 -620377511 -112543664 28573008 28573013 547793365 158617319 gneE77 gneE76 gneE44", 3., 4.),
        ("4221w4220n", "-28573015#6 -28573015#5 -28573015#4 -28573015#3 -28573015#2 -28573015#1 -28573015#0 28573025 28573025.46 28573025.65 624439627 547793365 158617319 gneE77 gneE76 gneE44", 1., 1.),
        ("4221s4220s", "-28594060#4 -28594060#3 -28594060#2 -28594060#1 -28594060#0 669665013 669665011 7635630#0 7635630#1 624439627 547793365 158617319 620377513 gneE41", 3., 2.),
        ("4221n4220s", "-620463733 -620377511 -112543664 28573008 28573013 547793365 158617319 620377513 gneE41", 5., 6.),
        ("4221w4220s", "-28573015#6 -28573015#5 -28573015#4 -28573015#3 -28573015#2 -28573015#1 -28573015#0 28573025 28573025.46 28573025.65 624439627 547793365 158617319 620377513 gneE41", 2., 1.),
        
        ("4220s4219n", "gneE10 gneE73 gneE75 619526565 547625727 620377496 620377502#0 620377502#1 620377501#0", 22., 13.),
        ("4220n4219n", "gneE47 gneE78 gneE75 619526565 547625727 620377496 620377502#0 620377502#1 620377501#0", 8., 9.), 
        ("4221s4219n", "-28594060#4 -28594060#3 -28594060#2 -28594060#1 -28594060#0 669665013 669665011 7635630#0 7635630#1 624439627 547793365 158617319 gneE77 gneE75 619526565 547625727 620377496 620377502#0 620377502#1 620377501#0", 6., 4.),
        ("4221n4219n", "-620463733 -620377511 -112543664 28573008 28573013 547793365 158617319 gneE77 gneE75 619526565 547625727 620377496 620377502#0 620377502#1 620377501#0", 11., 10.),
        ("4221w4219n", "-28573015#6 -28573015#5 -28573015#4 -28573015#3 -28573015#2 -28573015#1 -28573015#0 28573025 28573025.46 28573025.65 624439627 547793365 158617319 gneE77 gneE75 619526565 547625727 620377496 620377502#0 620377502#1 620377501#0", 4., 2.),
        
        ("4220s4219s", "gneE10 gneE73 gneE75 619526565 28592678 620377494 547625725", 3., 4.),
        ("4220n4219s", "gneE47 gneE78 gneE75 619526565 28592678 620377494 547625725", 1., 3.),  
        ("4221s4219s", "-28594060#4 -28594060#3 -28594060#2 -28594060#1 -28594060#0 669665013 669665011 7635630#0 7635630#1 624439627 547793365 158617319 gneE77 gneE75 619526565 28592678 620377494 547625725", 1., 1.),
        ("4221n4219s", "-620463733 -620377511 -112543664 28573008 28573013 547793365 158617319 gneE77 gneE75 619526565 28592678 620377494 547625725", 2., 3.),
        ("4221w4219s", "-28573015#6 -28573015#5 -28573015#4 -28573015#3 -28573015#2 -28573015#1 -28573015#0 28573025 28573025.46 28573025.65 624439627 547793365 158617319 gneE77 gneE75 619526565 28592678 620377494 547625725", 1., 1.),
        
        ("4219s4235s", "620377506 620377506.61 122089526 122089583#0 122089583#1 122089583#1-AddedOffRampEdge 620377490 628341438#0 628341438#1", 1., 0.),
        ("4219n4235s", "620377515 28592666 122089583#0 122089583#1 122089583#1-AddedOffRampEdge 620377490 628341438#0 628341438#1", 1., 0.),
        ("4221s4235s", "-28594060#4 -28594060#3 -28594060#2 -28594060#1 -28594060#0 669665013 669665011 7635630#0 7635630#1 624439627 547793365 158617319 gneE77 gneE75 619526565 547625727 122089526 122089583#0 122089583#1 122089583#1-AddedOffRampEdge 620377490 628341438#0 628341438#1", 0., 0.),
        ("4221n4235s", "-620463733 -620377511 -112543664 28573008 28573013 547793365 158617319 gneE77 gneE75 619526565 547625727 122089526 122089583#0 122089583#1 122089583#1-AddedOffRampEdge 620377490 628341438#0 628341438#1", 0., 0.),
        ("4221w4235s", "-28573015#6 -28573015#5 -28573015#4 -28573015#3 -28573015#2 -28573015#1 -28573015#0 28573025 28573025.46 28573025.65 624439627 547793365 158617319 gneE77 gneE75 619526565 547625727 122089526 122089583#0 122089583#1 122089583#1-AddedOffRampEdge 620377490 628341438#0 628341438#1", 0., 0.),
        ("4220s4235s", "gneE10 gneE73 gneE75 619526565 547625727 122089526 122089583#0 122089583#1 122089583#1-AddedOffRampEdge 620377490 628341438#0 628341438#1", 1., 0.),
        ("4220n4235s", "gneE47 gneE78 gneE75 619526565 547625727 122089526 122089583#0 122089583#1 122089583#1-AddedOffRampEdge 620377490 628341438#0 628341438#1", 0., 0.),
        
        ("4219s4235w", "620377506 620377506.61 122089526 122089583#0 122089583#1 122089583#1-AddedOffRampEdge 619523286 619523287#0 619523287#0.17 619523287#1", 13., 16.),
        ("4219n4235w", "620377515 28592666 122089583#0 122089583#1 122089583#1-AddedOffRampEdge 619523286 619523287#0 619523287#0.17 619523287#1", 5., 3.),
        ("4221s4235w", "-28594060#4 -28594060#3 -28594060#2 -28594060#1 -28594060#0 669665013 669665011 7635630#0 7635630#1 624439627 547793365 158617319 gneE77 gneE75 619526565 547625727 122089526 122089583#0 122089583#1 122089583#1-AddedOffRampEdge 619523286 619523287#0 619523287#0.17 619523287#1", 3., 3.),
        ("4221n4235w", "-620463733 -620377511 -112543664 28573008 28573013 547793365 158617319 gneE77 gneE75 619526565 547625727 122089526 122089583#0 122089583#1 122089583#1-AddedOffRampEdge 619523286 619523287#0 619523287#0.17 619523287#1", 6., 8.),
        ("4221w4235w", "-28573015#6 -28573015#5 -28573015#4 -28573015#3 -28573015#2 -28573015#1 -28573015#0 28573025 28573025.46 28573025.65 624439627 547793365 158617319 gneE77 gneE75 619526565 547625727 122089526 122089583#0 122089583#1 122089583#1-AddedOffRampEdge 619523286 619523287#0 619523287#0.17 619523287#1", 2., 2.),
        ("4220s4235w", "gneE10 gneE73 gneE75 619526565 547625727 122089526 122089583#0 122089583#1 122089583#1-AddedOffRampEdge 619523286 619523287#0 619523287#0.17 619523287#1", 12., 10.),
        ("4220n4235w", "gneE47 gneE78 gneE75 619526565 547625727 122089526 122089583#0 122089583#1 122089583#1-AddedOffRampEdge 619523286 619523287#0 619523287#0.17 619523287#1", 4., 7.)
    ]
    
    
    with open("data/osm.rou.xml", "w") as routes: 
        print("""<routes>
		<vType id="type1" lcStrategic="100" lcKeepRight="100" lcSpeedGain="100" lcCooperative="1" lcSublane="100" />""", file=routes)

        for route in routesList:             													# print route list       
                print('    <route id="r%s" edges="%s" />' % (
                    route[0], route[1]), file=routes)

        vehNr = 0
        N = 300  # number of time steps per interval (5 min)
        for i in range(2):
            for j in range(N):
                for route in routesList:  														#print vehicle density for each interval for each route                   
                    if random.uniform(0, 1) < (route[i+2]/300):#type currently does not work
                        print('    <vehicle id="%s_%d" type="type1" route="r%s" depart="%d" />' % (
                            route[0], vehNr, route[0], (i*N)+j), file=routes)
                        vehNr += 1
                        
                    
        print("</routes>", file=routes)
                

# needs work
def run():
    """execute the TraCI control loop"""
    step = 0
    YELLOW_PHASE = 4
    RED_PHASE = 2
    traci.trafficlight.setPhase("cluster_1707799581_314056954_5931861577", 0)
    site4235_detector_delay = []     
    site4235_LOOP_COUNT = 11 
    for i in range(0, site4235_LOOP_COUNT+1): 													# initiliaze array of 0s
        site4235_detector_delay.append(0)
    lanesForPhases_s4235 = {        															# key = phase, values = lanes with green lights
        0 : [1, 2, 3, 9, 10, 11],   															#A      
        1 : [1, 2, 3, 4],           															#B
        2 : [6, 7]                  															#C
    }   
    
    site4219_detector_delay = []     
    site4219_LOOP_COUNT = 21
    site4219_ignored_phases = [20, 21, 22]# could automate this I guess? if not in dict
    for i in range(0, site4219_LOOP_COUNT+1): # initiliaze array of 0s
        site4219_detector_delay.append(0)
    laneGroupsForPhases_s4219 = {        # key = phase, values = lanes with green lights
        0 : [0, 1],                     #A    
        1 : [1, 6, 7],                  #B
        2 : [0, 2],                     #C
        3 : [3, 8],                     #D
        4 : [3, 4, 7],                  #E
        5 : [4, 5, 7],                  #F
        6 : [6, 2, 7]                   #G
    }   

    laneGroups_s4219 = {                # which lanes are grouped together, this is useful for finding when a lane group is no longer active
        0 : [11, 12],                   # such that, a right turn lane can be replaced by oncoming traffic 
        1 : [1, 2],         
        2 : [13, 14],           
        3 : [15, 16, 17],       
        4 : [7, 8],   
        5 : [9, 10],        
        6 : [3, 4],
        7 : [5, 6],
        8 : [18, 19]        
    }
    activeTraffic_s4219 = []
    for i in range(0, len(laneGroups_s4219)): # initiliaze array of 99s
        activeTraffic_s4219.append(99)
                
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        # for each intersection
        #   for each loop detector
        #       if getLastStepVehicleNumber>0, increment loopDetectorDelay
        #       if in current phase, reset loopDetectorDelay
        
        #   if active phase is not transition phase
        #                 
        #       currentPhase = getphase
        #       activeTraffic = 0
        #       for loopDet in currentPhase
        #           activeTraffic += loopDet.getLastStepVehicleNumber
        #       if activeTraffic == 0       # if no traffic through active lanes, switch to transition phase for max(loopDetectorDelay) (HOW?) #first, build next phase
        #           reset transitionCounter 
        #   
        #           if max(loopDetectorDelay) == 9|10|11        
        #               nextPhase = 1                       #A
        #               if currentPhase = 2                 #B-A
        #                   setPhase(B-A)
        #               elif currentPhase = 3            #C-A
        #                   setPhase(C-A)
        #           elif max(loopDetectorDelay) == 4
        #               nextPhase = 2                       #B
        #               if currentPhase = 1                 #A-B
        #                   setPhase(A-B)
        #               elif currentPhase = 3            #C-B
        #                   setPhase(C-B)
        #           elif max(loopDetectorDelay) == 6|7
        #               nextPhase = 3                       #C
        #               if currentPhase = 1                 #A-C
        #                   setPhase(A-C)
        #               elif currentPhase = 2            #B-C
        #                   setPhase(B-C)
        #           elif max(loopDetectorDelay) == 1|2|3
        #               if max(loopDetectorDelay[4,9,10,11]) == 4   # compare conflicting lanes
        #                   nextPhase = 2
        #                   if currentPhase = 1             #A-B
        #                       setPhase(A-B)
        #                   elif currentPhase = 3        #C-B
        #                       setPhase(C-B)
        #               else 
        #                   nextPhase = 1
        #                   if currentPhase = 2             #B-A
        #                       setPhase(B-A)
        #                   elif currentPhase = 3        #C-A
        #                       setPhase(C-A)
        #  
        #   if active phase is transition phase
        #       increment transitionCounter
        #           if transitionCounter == 6
        #               switch to nextPhase
        #
        
        # add in other traffic lightsite4219_phase = traci.trafficlight.getPhase("cluster_25977365_314059191_314060044_314061754_314061758_314062509_314062525")
        #static edf algo
        
        # ----------------------------------------------------------------------SITE 4235--------------------------------------------------------------------------------------------------
        site4235_phase = traci.trafficlight.getPhase("cluster_1707799581_314056954_5931861577") # phase indexing starts at 0 
        for i in range(1,site4235_LOOP_COUNT):                                                  # for each loop detector
            if (i != 5) and (i != 8):                                                           # ignore lanes 5 and 8
                if int(traci.inductionloop.getLastStepVehicleNumber("site4235_" + str(i))) > 0 or site4235_detector_delay[i] > 0:      # if getLastStepVehicleNumber>0, 
                    site4235_detector_delay[i] = site4235_detector_delay[i] + 1                 # increment loopDetectorDelay
                
        if (site4235_phase in lanesForPhases_s4235.keys()):                 # if not a transition phase
            activeTraffic = 99 
            
            for i in lanesForPhases_s4235[site4235_phase]:
                site4235_detector_delay[i] = 0                                                  # reset loopDetectorDelay for loops in current phase
                if i != 1 and i != 2 and i != 3:                                                # ignore non conflicting traffic
                    if int(traci.inductionloop.getTimeSinceDetection("site4235_" + str(i))) < activeTraffic:
                        activeTraffic = int(traci.inductionloop.getTimeSinceDetection("site4235_" + str(i)))
                             
            if activeTraffic > 4:                                                              # if no traffic through active lanes, switch to transition phase for max(loopDetectorDelay)
                activeTraffic = 0 
                transitionCounter = 0
                site4235_prev_phase = site4235_phase
                # build next phase
                if site4235_detector_delay.index(max(site4235_detector_delay)) == 9 or site4235_detector_delay.index(max(site4235_detector_delay)) == 10 or site4235_detector_delay.index(max(site4235_detector_delay)) == 11:
                    site4235_next_phase = 0                                                     #A
                    if site4235_phase == 1:
                        traci.trafficlight.setPhase("cluster_1707799581_314056954_5931861577", 7)   #change to B-A
                    elif site4235_phase == 2:
                        traci.trafficlight.setPhase("cluster_1707799581_314056954_5931861577", 11)   #change to C-A
                
                elif site4235_detector_delay.index(max(site4235_detector_delay)) == 4:          # loop detector no. 4
                    site4235_next_phase = 1                                                     #B
                    if site4235_phase == 0:
                        traci.trafficlight.setPhase("cluster_1707799581_314056954_5931861577", 3)   #change to A-B
                    elif site4235_phase == 2:
                        traci.trafficlight.setPhase("cluster_1707799581_314056954_5931861577", 13)   #change to C-B
                        
                elif site4235_detector_delay.index(max(site4235_detector_delay)) == 6 or site4235_detector_delay.index(max(site4235_detector_delay)) == 7:
                    site4235_next_phase = 2                                                     #C
                    if site4235_phase == 0:
                        traci.trafficlight.setPhase("cluster_1707799581_314056954_5931861577", 5)   #change to A-C
                    elif site4235_phase == 1:
                        traci.trafficlight.setPhase("cluster_1707799581_314056954_5931861577", 9)   #change to B-C
                        
                elif site4235_detector_delay.index(max(site4235_detector_delay)) == 1 or site4235_detector_delay.index(max(site4235_detector_delay)) == 2 or site4235_detector_delay.index(max(site4235_detector_delay)) == 3:
                    if site4235_detector_delay[4] > max(site4235_detector_delay[9:11]):         # compare conflicting lanes
                        site4235_next_phase = 1                                                     #B
                        if site4235_phase == 0:
                            traci.trafficlight.setPhase("cluster_1707799581_314056954_5931861577", 3)   #change to A-B
                        elif site4235_phase == 2:
                            traci.trafficlight.setPhase("cluster_1707799581_314056954_5931861577", 13)   #change to C-B
                        
                    else:
                        site4235_next_phase = 0                                                     #A
                        if site4235_phase == 1:
                            traci.trafficlight.setPhase("cluster_1707799581_314056954_5931861577", 7)   #change to B-A
                        elif site4235_phase == 2:
                            traci.trafficlight.setPhase("cluster_1707799581_314056954_5931861577", 11)   #change to C-A
                            
        else:                                                                                       #   if active phase is transition phase
            
            if transitionCounter < YELLOW_PHASE:           # while lights are still yellow
                for i in lanesForPhases_s4235[site4235_prev_phase]:
                    site4235_detector_delay[i] = 0  
            elif transitionCounter == YELLOW_PHASE + RED_PHASE:
                traci.trafficlight.setPhase("cluster_1707799581_314056954_5931861577", site4235_next_phase) #change to next phase
            transitionCounter = transitionCounter + 1
                #add for case where lights change with no traffic?

              
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
                             "--tripinfo-output", "tripinfoEDF.xml", "--no-internal-links"])
    run()
