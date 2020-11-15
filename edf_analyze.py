"""Created by Nolan Jessen for CPR E 558 on 10/20/2020"""
import math
colors = ['red', 'blue', 'green', 'yellow', 'cyan', 'orange', 'fuchsia', 'forestgreen', 'aquamarine']
    
def lcm(taskList):
    lcm = taskList[0].deadline
    for i in taskList[1:]:
        lcm = int(lcm*i.deadline/math.gcd(lcm, i.deadline))
    return lcm
    
def isSchedulable(taskList):
    i = 0
    totalRuntime = 0.0
    for task in taskList:
        totalRuntime += (float(task.runtime))/(float(task.deadline))
    return (totalRuntime <= 1.0)

def generateSchedule(taskList):
    editList = taskList
    scheduleList = []
    deadline = lcm(taskList)
    i = 0
    for task in taskList:
        mult = deadline / task.deadline
        color=colors[i]
        for j in range(int(mult)):
            currDeadline = task.deadline * (j+1)
            startTime = currDeadline - task.deadline
            scheduleList.append([startTime, currDeadline, task.runtime, i, color])
        i += 1
    
    scheduleList.sort(key = lambda x: x[0])
    schedule2 = []
    currentStart = 0
    tempList = []
    for task in scheduleList:
        if currentStart == task[0]:
            tempList.append(task)
        else:
            tempList.sort(key = lambda x: x[1])
            schedule2.extend(tempList)
            tempList.clear()
            tempList.append(task)
            currentStart = task[0]
    schedule2.extend(tempList)

    prev = 0
    for task in schedule2[1:]:
        if task[0] < (schedule2[prev][0]+schedule2[prev][2]):
            task[0] = schedule2[prev][0]+schedule2[prev][2]
        prev += 1
    
    return schedule2

def energyUse(scheduleList):
    totalEnergy = 0
    for event in scheduleList:
        totalEnergy += event[2]
    return totalEnergy