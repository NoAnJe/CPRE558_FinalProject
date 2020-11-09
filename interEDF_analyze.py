"""Created by Nolan Jessen for CPR E 558 on 10/20/2020"""


# This generates an EDF-based, intertask energy aware scheduler. It takes the previously
# generated EDF schedule and first multiplies each task by the amount that they can expand
# by. If any task is found to exceed its limits, it is shrunk accordingly (and the next
# task expanded by the same amount).
def generateSchedule(edfSchedule, edfEnergy, lcm):
    scheduleList = []
    if edfEnergy == lcm:
        return edfSchedule
    percent = edfEnergy / lcm
    invPercent = 1.0 / percent
    prevEnd = 0
    for item in edfSchedule:
        print(item)
        start = item[0] * invPercent
        runtime = item[2] * invPercent
        thisPercent = percent
        if prevEnd != start:    # If it starts later than the previous ending, move it up
            start = prevEnd
            thisPercent = (item[2]) / (runtime)
        if (runtime + start) > item[1]:       # If it exceeds the allowable runtime, move up the ending
            runtime = item[1] - start
            thisPercent = (item[2]) / (runtime)
        prevEnd = runtime + start
        scheduleList.append([start, item[1], runtime, item[3], item[4], thisPercent])
    return scheduleList

def energyUse(scheduleList):
    totalEnergy = 0
    for event in scheduleList:
        totalEnergy += (event[2] * (event[5] ** 2))
    return totalEnergy