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
        
        ("4235e4221n", "619523290#0 619523290#1 619523288 619526570#0 619526570#1 620377514#1 619526569#1 619526568 619526567 619526566 122089528#1 620377517 gneE74 gneE72 gneE80 gneE81 gneE83 669665014 669665015#1 28594060#0 28594060#1 28594060#2 28594060#3 28594060#4", 30., 33.),
        ("4235n4221n", "-628341438#1 -628341438#0 -61645695 619526570#0 619526570#1 620377514#1 619526569#1 619526568 619526567 619526566 122089528#1 620377517 gneE74 gneE72 gneE80 gneE81 gneE83 669665014 669665015#1 28594060#0 28594060#1 28594060#2 28594060#3 28594060#4", 2., 2.),
        ("4235e4221s", "619523290#0 619523290#1 619523288 619526570#0 619526570#1 620377514#1 619526569#1 619526568 619526567 619526566 122089528#1 620377517 gneE74 gneE72 gneE80 gneE81 gneE82 207149704#0 207149704#1 112543664 620377510 620463733", 7., 19.),
        ("4235n4221s", "-628341438#1 -628341438#0 -61645695 619526570#0 619526570#1 620377514#1 619526569#1 619526568 619526567 619526566 122089528#1 620377517 gneE74 gneE72 gneE80 gneE81 gneE82 207149704#0 207149704#1 112543664 620377510 620463733", 0., 1.),
        ("4219s4221n", "620377506 gneE2 620377517 gneE74 gneE72 gneE80 gneE81 gneE83 669665014 669665015#1 28594060#0 28594060#1 28594060#2 28594060#3 28594060#4", 6., 6.),
        ("4219s4221s", "620377506 gneE2 620377517 gneE74 gneE72 gneE80 gneE81 gneE82 207149704#0 207149704#1 112543664 620377510 620463733", 1., 4.),
        ("4219n4221n", "620377515  122089525 122089525.34 122089528#1 620377517 gneE74 gneE72 gneE80 gneE81 gneE83 669665014 669665015#1 28594060#0 28594060#1 28594060#2 28594060#3 28594060#4", 2., 5.),
        ("4219n4221s", "620377515  122089525 122089525.34 122089528#1 620377517 gneE74 gneE72 gneE80 gneE81 gneE82 207149704#0 207149704#1 112543664 620377510 620463733", 0., 3.),
        ("4220s4221n", "gneE10 28641508 gneE80 gneE81 gneE83 669665014 669665015#1 28594060#0 28594060#1 28594060#2 28594060#3 28594060#4", 4., 5.),
        ("4220s4221s", "gneE10 28641508 gneE80 gneE81 gneE82 207149704#0 207149704#1 112543664 620377510 620463733", 1., 3.),
        
        ("4235e4221e", "619523290#0 619523290#1 619523288 619526570#0 619526570#1 620377514#1 619526569#1 619526568 619526567 619526566 122089528#1 620377517 gneE74 gneE72 gneE80 gneE81 gneE82 7637388#0 7637388#1 28573015#0 28573015#1 28573015#2 28573015#3 28573015#4 28573015#5 28573015#6", 47., 18.),
        ("4235n4221e", "-628341438#1 -628341438#0 -61645695 619526570#0 619526570#1 620377514#1 619526569#1 619526568 619526567 619526566 122089528#1 620377517 gneE74 gneE72 gneE80 gneE81 gneE82 7637388#0 7637388#1 28573015#0 28573015#1 28573015#2 28573015#3 28573015#4 28573015#5 28573015#6", 3., 1.),
        ("4219s4221e", "620377506 gneE2 620377517  gneE74 gneE72 gneE80 gneE81 gneE82 7637388#0 7637388#1 28573015#0 28573015#1 28573015#2 28573015#3 28573015#4 28573015#5 28573015#6", 9., 4.),
        ("4219n4221e", "620377515  122089525 122089525.34 122089528#1 620377517 gneE74 gneE72 gneE80 gneE81 gneE82 7637388#0 7637388#1 28573015#0 28573015#1 28573015#2 28573015#3 28573015#4 28573015#5 28573015#6", 3., 3.),
        ("4220s4221e", "gneE10 28641508 gneE80 gneE81 gneE82 7637388#0 7637388#1 28573015#0 28573015#1 28573015#2 28573015#3 28573015#4 28573015#5 28573015#6", 7., 3.),
        
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

        for route in routesList:                                                                # print route list       
                print('    <route id="r%s" edges="%s" />' % (
                    route[0], route[1]), file=routes)

        vehNr = 0
        N = 300  # number of time steps per interval (5 min)
        for i in range(2):
            for j in range(N):
                for route in routesList:                                                        #print vehicle density for each interval for each route                   
                    if random.uniform(0, 1) < (route[i+2]/300):#type currently does not work
                        print('    <vehicle id="%s_%d" type="type1" route="r%s" depart="%d" />' % (
                            route[0], vehNr, route[0], (i*N)+j), file=routes)
                        vehNr += 1
                        
                    
        print("</routes>", file=routes)
                

# needs work
def run():

    step = 0
    
    while step < 10000:
        traci.simulationStep()
        
        
        # ----------------------------------------------------------------------SITE 4219--------------------------------------------------------------------------------------------------
        # Demand Scheduling Algorithm using queue lengths
        # Obtain queue length data from SUMO
        #
        # At intersection iterative through competing traffic flows 
        # - selecting largest first until they are all 0
        # - have maximum time period to switch phase
        #
        # At points where there are secondary traffic flows
        # - select phase with the most density 
        #
        # If else statement selecting Phase with maximum density
        # - Exit loop when all cars pass or time limit is reached

        if step > 10:
        
            Phase_A_Queue_4235 = traci.lane.getLastStepHaltingNumber("619523288_0") + traci.lane.getLastStepHaltingNumber("619523290#1_0")
            Phase_A_Queue_4235 += (traci.lane.getLastStepHaltingNumber("619523288_1") + traci.lane.getLastStepHaltingNumber("619523290#1_1"))
            Phase_A_Queue_4235 += (traci.lane.getLastStepHaltingNumber("619523288_2") + traci.lane.getLastStepHaltingNumber("619523290#1_2"))
            Phase_A_Queue_4235 += (traci.lane.getLastStepHaltingNumber("619523286_0") + traci.lane.getLastStepHaltingNumber("122089583#1-AddedOffRampEdge_0"))
            Phase_A_Queue_4235 += (traci.lane.getLastStepHaltingNumber("619523286_1") + traci.lane.getLastStepHaltingNumber("122089583#1-AddedOffRampEdge_1"))
            Phase_A_Queue_4235 += (traci.lane.getLastStepHaltingNumber("619523286_2") + traci.lane.getLastStepHaltingNumber("122089583#1-AddedOffRampEdge_2"))
            
            Phase_B_Queue_4235 = traci.lane.getLastStepHaltingNumber("619523288_0") + traci.lane.getLastStepHaltingNumber("619523290#1_0")
            Phase_B_Queue_4235 += (traci.lane.getLastStepHaltingNumber("619523288_1") + traci.lane.getLastStepHaltingNumber("619523290#1_1"))
            Phase_B_Queue_4235 += (traci.lane.getLastStepHaltingNumber("619523288_2") + traci.lane.getLastStepHaltingNumber("619523290#1_2"))
            Phase_B_Queue_4235 += (traci.lane.getLastStepHaltingNumber("619523288_3") + traci.lane.getLastStepHaltingNumber("619523290#1_3"))
            
            Phase_C_Queue_4235 = traci.lane.getLastStepHaltingNumber("61645695_0") + traci.lane.getLastStepHaltingNumber("628341438#0_0") + traci.lane.getLastStepHaltingNumber("628341438#1_0")
            
            if Phase_A_Queue_4235 > Phase_B_Queue_4235 and Phase_A_Queue_4235 > Phase_B_Queue_4235:
                traci.trafficlight.setPhase("cluster_1707799581_314056954_5931861577", 0)
            elif Phase_B_Queue_4235 > Phase_C_Queue_4235 and Phase_B_Queue_4235 > Phase_C_Queue_4235:
                traci.trafficlight.setPhase("cluster_1707799581_314056954_5931861577", 1)
            else:
                traci.trafficlight.setPhase("cluster_1707799581_314056954_5931861577", 2)
                
            Phase_A_Queue_4219 = traci.lane.getLastStepHaltingNumber("620377506.61_0") + traci.lane.getLastStepHaltingNumber("620377506_0")
            Phase_A_Queue_4219 += (traci.lane.getLastStepHaltingNumber("620377506.61_1") + traci.lane.getLastStepHaltingNumber("620377506_1"))
            Phase_A_Queue_4219 += (traci.lane.getLastStepHaltingNumber("122089525.34_0") + traci.lane.getLastStepHaltingNumber("620377515_0"))
            Phase_A_Queue_4219 += (traci.lane.getLastStepHaltingNumber("122089525.34_1") + traci.lane.getLastStepHaltingNumber("620377515_1"))
            
            Phase_B_Queue_4219 = traci.lane.getLastStepHaltingNumber("620377506.61_0") + traci.lane.getLastStepHaltingNumber("620377506_0")
            Phase_B_Queue_4219 += (traci.lane.getLastStepHaltingNumber("620377506.61_1") + traci.lane.getLastStepHaltingNumber("620377506_1"))
            Phase_B_Queue_4219 += (traci.lane.getLastStepHaltingNumber("620377506.61_2") + traci.lane.getLastStepHaltingNumber("620377506_2"))
            Phase_B_Queue_4219 += traci.lane.getLastStepHaltingNumber("620377506.61_3")
            
            Phase_C_Queue_4219 = (traci.lane.getLastStepHaltingNumber("122089525.34_0") + traci.lane.getLastStepHaltingNumber("620377515_0"))
            Phase_C_Queue_4219 += (traci.lane.getLastStepHaltingNumber("122089525.34_1") + traci.lane.getLastStepHaltingNumber("620377515_1"))
            Phase_C_Queue_4219 += (traci.lane.getLastStepHaltingNumber("122089525.34_2") + traci.lane.getLastStepHaltingNumber("620377515_2"))
            Phase_C_Queue_4219 += traci.lane.getLastStepHaltingNumber("122089525.34_3") 
            
            Phase_D_Queue_4219 = (traci.lane.getLastStepHaltingNumber("547625727_0") + traci.lane.getLastStepHaltingNumber("619526565_1"))
            Phase_D_Queue_4219 += (traci.lane.getLastStepHaltingNumber("547625727_1") + traci.lane.getLastStepHaltingNumber("619526565_2"))
            Phase_D_Queue_4219 += (traci.lane.getLastStepHaltingNumber("547625727_2") + traci.lane.getLastStepHaltingNumber("619526565_3"))
            Phase_D_Queue_4219 += (traci.lane.getLastStepHaltingNumber("547625727_3") + traci.lane.getLastStepHaltingNumber("619526565_4"))
            Phase_D_Queue_4219 += (traci.lane.getLastStepHaltingNumber("547625727_4") + traci.lane.getLastStepHaltingNumber("619526565_2"))
            
            Phase_E_Queue_4219 = (traci.lane.getLastStepHaltingNumber("619526566_0") + traci.lane.getLastStepHaltingNumber("619526567_1"))
            Phase_E_Queue_4219 += (traci.lane.getLastStepHaltingNumber("619526566_1") + traci.lane.getLastStepHaltingNumber("619526567_2"))
            Phase_E_Queue_4219 += (traci.lane.getLastStepHaltingNumber("547625727_0") + traci.lane.getLastStepHaltingNumber("619526565_1"))
            Phase_E_Queue_4219 += (traci.lane.getLastStepHaltingNumber("547625727_1") + traci.lane.getLastStepHaltingNumber("619526565_2"))
            Phase_E_Queue_4219 += (traci.lane.getLastStepHaltingNumber("547625727_2") + traci.lane.getLastStepHaltingNumber("619526565_3"))
            Phase_E_Queue_4219 += traci.lane.getLastStepHaltingNumber("619526568_0")
            Phase_E_Queue_4219 += traci.lane.getLastStepHaltingNumber("619526568_1")
            Phase_E_Queue_4219 += traci.lane.getLastStepHaltingNumber("619526568_2")
            Phase_E_Queue_4219 += traci.lane.getLastStepHaltingNumber("619526569#1_0")
            Phase_E_Queue_4219 += traci.lane.getLastStepHaltingNumber("619526569#1_1")
            Phase_E_Queue_4219 += traci.lane.getLastStepHaltingNumber("619526569#1_2")
            Phase_E_Queue_4219 += traci.lane.getLastStepHaltingNumber("620377514#1_0")
            Phase_E_Queue_4219 += traci.lane.getLastStepHaltingNumber("620377514#1_1")
            Phase_E_Queue_4219 += traci.lane.getLastStepHaltingNumber("620377514#1_2")
            Phase_E_Queue_4219 += traci.lane.getLastStepHaltingNumber("619526570#1_0")
            Phase_E_Queue_4219 += traci.lane.getLastStepHaltingNumber("619526570#1_1")
            Phase_E_Queue_4219 += traci.lane.getLastStepHaltingNumber("619526570#1_2")
            
            Phase_F_Queue_4219 = (traci.lane.getLastStepHaltingNumber("619526566_0") + traci.lane.getLastStepHaltingNumber("619526567_1"))
            Phase_F_Queue_4219 += (traci.lane.getLastStepHaltingNumber("619526566_1") + traci.lane.getLastStepHaltingNumber("619526567_2"))
            Phase_F_Queue_4219 += (traci.lane.getLastStepHaltingNumber("619526566_2") + traci.lane.getLastStepHaltingNumber("619526567_3"))
            Phase_F_Queue_4219 += traci.lane.getLastStepHaltingNumber("619526566_3")
            Phase_F_Queue_4219 += traci.lane.getLastStepHaltingNumber("619526568_0")
            Phase_F_Queue_4219 += traci.lane.getLastStepHaltingNumber("619526568_1")
            Phase_F_Queue_4219 += traci.lane.getLastStepHaltingNumber("619526568_2")
            Phase_F_Queue_4219 += traci.lane.getLastStepHaltingNumber("619526569#1_0")
            Phase_F_Queue_4219 += traci.lane.getLastStepHaltingNumber("619526569#1_1")
            Phase_F_Queue_4219 += traci.lane.getLastStepHaltingNumber("619526569#1_2")
            Phase_F_Queue_4219 += traci.lane.getLastStepHaltingNumber("620377514#1_0")
            Phase_F_Queue_4219 += traci.lane.getLastStepHaltingNumber("620377514#1_1")
            Phase_F_Queue_4219 += traci.lane.getLastStepHaltingNumber("620377514#1_2")
            Phase_F_Queue_4219 += traci.lane.getLastStepHaltingNumber("619526570#1_0")
            Phase_F_Queue_4219 += traci.lane.getLastStepHaltingNumber("619526570#1_1")
            Phase_F_Queue_4219 += traci.lane.getLastStepHaltingNumber("619526570#1_2")

            
            Phase_G_Queue_4219 = (traci.lane.getLastStepHaltingNumber("619526566_2") + traci.lane.getLastStepHaltingNumber("619526567_3"))
            Phase_G_Queue_4219 += traci.lane.getLastStepHaltingNumber("619526566_3")
            Phase_G_Queue_4219 += (traci.lane.getLastStepHaltingNumber("547625727_3") + traci.lane.getLastStepHaltingNumber("619526565_4"))
            Phase_G_Queue_4219 += (traci.lane.getLastStepHaltingNumber("547625727_4") + traci.lane.getLastStepHaltingNumber("619526565_2"))
            
            if Phase_A_Queue_4219 > Phase_B_Queue_4219 and Phase_A_Queue_4219 > Phase_C_Queue_4219 and Phase_A_Queue_4219 > Phase_D_Queue_4219 and Phase_A_Queue_4219 > Phase_E_Queue_4219 and Phase_A_Queue_4219 > Phase_F_Queue_4219 and Phase_A_Queue_4219 > Phase_G_Queue_4219:
                traci.trafficlight.setPhase("cluster_25977365_314059191_314060044_314061754_314061758_314062509_314062525", 0)
                traci.trafficlight.setPhase("5861321343", 0)
            elif Phase_B_Queue_4219 > Phase_A_Queue_4219 and Phase_B_Queue_4219 > Phase_C_Queue_4219 and Phase_B_Queue_4219 > Phase_D_Queue_4219 and Phase_B_Queue_4219 > Phase_E_Queue_4219 and Phase_B_Queue_4219 > Phase_F_Queue_4219 and Phase_B_Queue_4219 > Phase_G_Queue_4219:
                traci.trafficlight.setPhase("cluster_25977365_314059191_314060044_314061754_314061758_314062509_314062525", 1)
                traci.trafficlight.setPhase("5861321343", 1)
            elif Phase_C_Queue_4219 > Phase_A_Queue_4219 and Phase_C_Queue_4219 > Phase_B_Queue_4219 and Phase_C_Queue_4219 > Phase_D_Queue_4219 and Phase_C_Queue_4219 > Phase_E_Queue_4219 and Phase_C_Queue_4219 > Phase_F_Queue_4219 and Phase_C_Queue_4219 > Phase_G_Queue_4219:
                traci.trafficlight.setPhase("cluster_25977365_314059191_314060044_314061754_314061758_314062509_314062525", 2)
                traci.trafficlight.setPhase("5861321343", 0)
            elif Phase_D_Queue_4219 > Phase_A_Queue_4219 and Phase_D_Queue_4219 > Phase_B_Queue_4219 and Phase_D_Queue_4219 > Phase_C_Queue_4219 and Phase_D_Queue_4219 > Phase_E_Queue_4219 and Phase_D_Queue_4219 > Phase_F_Queue_4219 and Phase_D_Queue_4219 > Phase_G_Queue_4219:
                traci.trafficlight.setPhase("cluster_25977365_314059191_314060044_314061754_314061758_314062509_314062525", 3)
                traci.trafficlight.setPhase("5861321343", 0)
            elif Phase_E_Queue_4219 > Phase_A_Queue_4219 and Phase_E_Queue_4219 > Phase_B_Queue_4219 and Phase_E_Queue_4219 > Phase_C_Queue_4219 and Phase_E_Queue_4219 > Phase_D_Queue_4219 and Phase_E_Queue_4219 > Phase_F_Queue_4219 and Phase_E_Queue_4219 > Phase_G_Queue_4219:
                traci.trafficlight.setPhase("cluster_25977365_314059191_314060044_314061754_314061758_314062509_314062525", 4)
                traci.trafficlight.setPhase("5861321343", 1)
            elif Phase_F_Queue_4219 > Phase_A_Queue_4219 and Phase_F_Queue_4219 > Phase_B_Queue_4219 and Phase_F_Queue_4219 > Phase_C_Queue_4219 and Phase_F_Queue_4219 > Phase_E_Queue_4219 and Phase_F_Queue_4219 > Phase_D_Queue_4219 and Phase_F_Queue_4219 > Phase_G_Queue_4219:
                traci.trafficlight.setPhase("cluster_25977365_314059191_314060044_314061754_314061758_314062509_314062525", 5)
                traci.trafficlight.setPhase("5861321343", 1)
            else:
                traci.trafficlight.setPhase("cluster_25977365_314059191_314060044_314061754_314061758_314062509_314062525", 6)
                traci.trafficlight.setPhase("5861321343", 1)
                
            Phase_A_Queue_4220 = traci.lane.getLastStepHaltingNumber("gneE77_0") + traci.lane.getLastStepHaltingNumber("158617319_1")
            Phase_A_Queue_4220 += (traci.lane.getLastStepHaltingNumber("gneE77_1") + traci.lane.getLastStepHaltingNumber("158617319_2"))
            Phase_A_Queue_4220 += traci.lane.getLastStepHaltingNumber("gneE77_2")
            Phase_A_Queue_4220 += traci.lane.getLastStepHaltingNumber("gneE74_1")
            Phase_A_Queue_4220 += traci.lane.getLastStepHaltingNumber("620377517_1")
            Phase_A_Queue_4220 += traci.lane.getLastStepHaltingNumber("620377517_0")
            
            Phase_B_Queue_4220 = traci.lane.getLastStepHaltingNumber("gneE74_1")
            Phase_B_Queue_4220 += traci.lane.getLastStepHaltingNumber("620377517_2")
            Phase_B_Queue_4220 += traci.lane.getLastStepHaltingNumber("620377517_1")
            Phase_B_Queue_4220 += traci.lane.getLastStepHaltingNumber("620377517_0")
            Phase_B_Queue_4220 += traci.lane.getLastStepHaltingNumber("gneE78_0")
            Phase_B_Queue_4220 += traci.lane.getLastStepHaltingNumber("gneE47_0")
            
            Phase_C_Queue_4220 = traci.lane.getLastStepHaltingNumber("gneE77_0") + traci.lane.getLastStepHaltingNumber("158617319_1")
            Phase_C_Queue_4220 += (traci.lane.getLastStepHaltingNumber("gneE77_1") + traci.lane.getLastStepHaltingNumber("158617319_2"))
            Phase_C_Queue_4220 += traci.lane.getLastStepHaltingNumber("gneE77_2")
            Phase_C_Queue_4220 += (traci.lane.getLastStepHaltingNumber("gneE77_3") + traci.lane.getLastStepHaltingNumber("158617319_3"))
            
            Phase_D_Queue_4220 = traci.lane.getLastStepHaltingNumber("gneE73_0")
            Phase_D_Queue_4220 += traci.lane.getLastStepHaltingNumber("gneE10_0")
            
            Phase_E_Queue_4220 = (traci.lane.getLastStepHaltingNumber("gneE77_3") + traci.lane.getLastStepHaltingNumber("158617319_3"))
            Phase_E_Queue_4220 += traci.lane.getLastStepHaltingNumber("620377517_2")
            Phase_E_Queue_4220 += traci.lane.getLastStepHaltingNumber("gneE78_0")
            Phase_E_Queue_4220 += traci.lane.getLastStepHaltingNumber("gneE47_0")
            
            if Phase_A_Queue_4220 > Phase_B_Queue_4220 and Phase_A_Queue_4220 > Phase_C_Queue_4220 and Phase_A_Queue_4220 > Phase_D_Queue_4220 and Phase_A_Queue_4220 > Phase_E_Queue_4220:
                traci.trafficlight.setPhase("gneJ41", 0)
            elif Phase_B_Queue_4220 > Phase_A_Queue_4220 and Phase_B_Queue_4220 > Phase_C_Queue_4220 and Phase_B_Queue_4220 > Phase_D_Queue_4220 and Phase_B_Queue_4220 > Phase_E_Queue_4220:
                traci.trafficlight.setPhase("gneJ41", 1)
            elif Phase_C_Queue_4220 > Phase_A_Queue_4220 and Phase_C_Queue_4220 > Phase_B_Queue_4220 and Phase_C_Queue_4220 > Phase_D_Queue_4220 and Phase_C_Queue_4220 > Phase_E_Queue_4220:
                traci.trafficlight.setPhase("gneJ41", 2)
            elif Phase_D_Queue_4220 > Phase_A_Queue_4220 and Phase_D_Queue_4220 > Phase_B_Queue_4220 and Phase_D_Queue_4220 > Phase_C_Queue_4220 and Phase_D_Queue_4220 > Phase_E_Queue_4220:
                traci.trafficlight.setPhase("gneJ41", 3)
            else:
                traci.trafficlight.setPhase("gneJ41", 4)
                
            Phase_A_Queue_4221 = traci.lane.getLastStepHaltingNumber("28573013_0")
            Phase_A_Queue_4221 += traci.lane.getLastStepHaltingNumber("620377512_0")
            Phase_A_Queue_4221 += traci.lane.getLastStepHaltingNumber("620377512_1")
            Phase_A_Queue_4221 += traci.lane.getLastStepHaltingNumber("28572986_0")
            Phase_A_Queue_4221 += traci.lane.getLastStepHaltingNumber("7635630#1_0")
            Phase_A_Queue_4221 += traci.lane.getLastStepHaltingNumber("7635630#1_1")
            
            Phase_B_Queue_4221 = traci.lane.getLastStepHaltingNumber("28573013_0")
            Phase_B_Queue_4221 += traci.lane.getLastStepHaltingNumber("620377512_0")
            Phase_B_Queue_4221 += traci.lane.getLastStepHaltingNumber("620377512_1")
            Phase_B_Queue_4221 += traci.lane.getLastStepHaltingNumber("620377512_2")
            Phase_B_Queue_4221 += traci.lane.getLastStepHaltingNumber("28573025_0")
            
            Phase_C_Queue_4221 = traci.lane.getLastStepHaltingNumber("28572986_0")
            Phase_C_Queue_4221 += traci.lane.getLastStepHaltingNumber("7635630#1_0")
            Phase_C_Queue_4221 += traci.lane.getLastStepHaltingNumber("7635630#1_1")
            Phase_C_Queue_4221 += traci.lane.getLastStepHaltingNumber("7635630#1_2")
            Phase_C_Queue_4221 += traci.lane.getLastStepHaltingNumber("7635630#1_3")
            Phase_C_Queue_4221 += traci.lane.getLastStepHaltingNumber("gneE83_0")
            Phase_C_Queue_4221 += traci.lane.getLastStepHaltingNumber("gneE83_1")
            
            Phase_D_Queue_4221 = traci.lane.getLastStepHaltingNumber("gneE83_0")
            Phase_D_Queue_4221 += traci.lane.getLastStepHaltingNumber("gneE83_1")
            Phase_D_Queue_4221 += traci.lane.getLastStepHaltingNumber("gneE82_0")
            Phase_D_Queue_4221 += traci.lane.getLastStepHaltingNumber("gneE82_1")
            Phase_D_Queue_4221 += traci.lane.getLastStepHaltingNumber("gneE82_2")
            
            Phase_E_Queue_4221 = traci.lane.getLastStepHaltingNumber("28573025_0")
            Phase_E_Queue_4221 += traci.lane.getLastStepHaltingNumber("28573025.46_0")
            Phase_E_Queue_4221 += traci.lane.getLastStepHaltingNumber("28573025.65_0")
            Phase_E_Queue_4221 += traci.lane.getLastStepHaltingNumber("gneE5_0")
            
            Phase_F_Queue_4221 = traci.lane.getLastStepHaltingNumber("gneE83_0")
            Phase_F_Queue_4221 += traci.lane.getLastStepHaltingNumber("gneE83_1")
            Phase_F_Queue_4221 += traci.lane.getLastStepHaltingNumber("620377512_2")
            Phase_F_Queue_4221 += traci.lane.getLastStepHaltingNumber("28573025_0")
            Phase_F_Queue_4221 += traci.lane.getLastStepHaltingNumber("7635630#1_2")
            Phase_F_Queue_4221 += traci.lane.getLastStepHaltingNumber("7635630#1_3")
            
            if Phase_A_Queue_4221 > Phase_B_Queue_4221 and Phase_A_Queue_4221 > Phase_C_Queue_4221 and Phase_A_Queue_4221 > Phase_D_Queue_4221 and Phase_A_Queue_4221 > Phase_E_Queue_4221 and Phase_A_Queue_4221 > Phase_F_Queue_4221:
                traci.trafficlight.setPhase("cluster_25953432_313863435_313863521_314053282", 0)
                traci.trafficlight.setPhase("313863797", 0)
            elif Phase_B_Queue_4221 > Phase_A_Queue_4221 and Phase_B_Queue_4221 > Phase_C_Queue_4221 and Phase_B_Queue_4221 > Phase_D_Queue_4221 and Phase_B_Queue_4221 > Phase_E_Queue_4221 and Phase_B_Queue_4221 > Phase_F_Queue_4221:
                traci.trafficlight.setPhase("cluster_25953432_313863435_313863521_314053282", 1)
                traci.trafficlight.setPhase("313863797", 0)
            elif Phase_C_Queue_4221 > Phase_A_Queue_4221 and Phase_C_Queue_4221 > Phase_B_Queue_4221 and Phase_C_Queue_4221 > Phase_D_Queue_4221 and Phase_C_Queue_4221 > Phase_E_Queue_4221 and Phase_C_Queue_4221 > Phase_F_Queue_4221:
                traci.trafficlight.setPhase("cluster_25953432_313863435_313863521_314053282", 2)
                traci.trafficlight.setPhase("313863797", 1)
            elif Phase_D_Queue_4221 > Phase_A_Queue_4221 and Phase_D_Queue_4221 > Phase_B_Queue_4221 and Phase_D_Queue_4221 > Phase_C_Queue_4221 and Phase_D_Queue_4221 > Phase_E_Queue_4221 and Phase_D_Queue_4221 > Phase_F_Queue_4221:
                traci.trafficlight.setPhase("cluster_25953432_313863435_313863521_314053282", 3)
                traci.trafficlight.setPhase("313863797", 1)
            elif Phase_E_Queue_4221 > Phase_A_Queue_4221 and Phase_E_Queue_4221 > Phase_B_Queue_4221 and Phase_E_Queue_4221 > Phase_C_Queue_4221 and Phase_E_Queue_4221 > Phase_D_Queue_4221 and Phase_E_Queue_4221 > Phase_F_Queue_4221:
                traci.trafficlight.setPhase("cluster_25953432_313863435_313863521_314053282", 4)
                traci.trafficlight.setPhase("313863797", 0)
            elif Phase_F_Queue_4221 > Phase_A_Queue_4221 and Phase_F_Queue_4221 > Phase_B_Queue_4221 and Phase_F_Queue_4221 > Phase_C_Queue_4221 and Phase_F_Queue_4221 > Phase_D_Queue_4221 and Phase_F_Queue_4221 > Phase_E_Queue_4221:
                traci.trafficlight.setPhase("cluster_25953432_313863435_313863521_314053282", 5)
                traci.trafficlight.setPhase("313863797", 1)
            else:
                traci.trafficlight.setPhase("cluster_25953432_313863435_313863521_314053282", 0)
                traci.trafficlight.setPhase("313863797", 0)
            
            print(Phase_A_Queue_4221)
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
    traci.start([sumoBinary, "-c", "simulation/osm.sumocfg",
                             "--tripinfo-output", "output/tripinfoEDF.xml", "--no-internal-links", "--summary", "output/summary.xml", "--queue-output","output/queue.xml"])
    run()
