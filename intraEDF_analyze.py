# This generates an EDF-based, intertask energy aware scheduler. It takes the previously
# generated EDF schedule and first multiplies each task by the amount that they can expand
# by. If any task is found to exceed its limits, it is shrunk accordingly (and the next
# task expanded by the same amount).
def generateSchedule(taskList, edfSchedule, edfEnergy, lcm):
    scheduleList = []
    if edfEnergy == lcm:
        for item in edfSchedule:
            item.append(1)
        return edfSchedule
    for item in edfSchedule:
        print(item)
        task = taskList[item[3]]
        if task.minpercent < item[5]:
            scheduleList.append(item)
        else:
            scheduleList.append([item[0], item[1], task.minruntime, item[3], item[4], task.minpercent])
            newStart = item[0] + task.minruntime
            remainArea = (item[2] * item[5]) - (task.minruntime * task.minpercent)
            if remainArea > 0:
                runtime = (item[2] - task.minruntime)
                percent = remainArea / runtime
                scheduleList.append([newStart, item[1], runtime, item[3], item[4], percent])
    return scheduleList

def energyUse(scheduleList):
    totalEnergy = 0
    for event in scheduleList:
        totalEnergy += (event[2] * (event[5] ** 2))
    return totalEnergy