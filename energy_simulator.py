import task
import edf_analyze as edf
import interEDF_analyze as energy
import intraEDF_analyze as intra
import tkinter as tk

# Generate the components that will be needed in the functions, which must be declared before being used
taskList = []
window = tk.Tk()
runEntry = tk.Entry(width=5)
deadlineEntry = tk.Entry(width=5)
initEntry = tk.Entry(width=5)
initAmtEntry = tk.Entry(width=5)
removeEntry = tk.Entry(width=5)

edfLabel    = tk.Label(text="")
energyLabel = tk.Label(text="")
intraLabel  = tk.Label(text="")

scrollbar = tk.Scrollbar(window)
scrollbar.grid(column=0, row=0, columnspan=3, rowspan=3)
taskListPage = tk.Listbox(yscrollcommand=scrollbar.set, width=30)
taskListPage.grid(column=0, row=0, columnspan=3, rowspan=3)
scrollbar.config(command=taskListPage.yview)

canvasWidth=550
canvasHeight=50
offset=20

edfScheduleGraph = tk.Canvas(width=canvasWidth+offset, height=canvasHeight)
interEDFScheduleGraph = tk.Canvas(width=canvasWidth+offset, height=canvasHeight)
intraEDFScheduleGraph = tk.Canvas(width=canvasWidth+offset, height=canvasHeight)

# Next method is the Scrollbox generation, which will generate a scrollbox with the list of tasks that exist
def generateScrollbox():
    print("Generating scrollbox!")
    taskListPage = tk.Listbox(yscrollcommand=scrollbar.set, width=30)
    taskListPage.grid(column=0, row=0, columnspan=3, rowspan=3)
    scrollbar.config(command=taskListPage.yview)
    for task in taskList:
        s = task.getString()
        t = taskList.index(task)
        taskString = "{}{}{}".format("Task ", t, s)
        taskListPage.insert('end', taskString)

# Next method is the Add Task button, which will add a task using the parameters in boxes 1 and 2 and reset those boxes
def addTask():
    print("Button was pressed!")
    runtime = int(runEntry.get())
    deadline = int(deadlineEntry.get())
    initRuntime = initEntry.get()
    initRunAmt  = initAmtEntry.get()
    if len(initRunAmt) == 0:
        initRunAmt = 0
    if len(initRuntime) == 0:
        initRuntime = 0
    initRunAmt = float(initRunAmt)
    initRuntime = int(initRuntime)
    if initRunAmt > 1:
        initRunAmt = 1
    if initRuntime * initRunAmt > runtime:
        initRuntime = runtime
    print("{}{}{}{}{}{}{}{}".format("Runtime: ",runtime," Deadline:",deadline," Boot Runtime: ",initRuntime," Boot Minimum Amount: ",initRunAmt))
    runEntry.delete(0, 'end')
    deadlineEntry.delete(0, 'end')
    initEntry.delete(0, 'end')
    initAmtEntry.delete(0, 'end')
    tempTask = task.Task(runtime, deadline, initRuntime, initRunAmt)
    taskList.append(tempTask)
    generateScrollbox()

# Next method is the Remove Task button, which will remove task X from the list and refresh the scroll list
def removeTask():
    print("Remove button was pressed!")
    remove = int(removeEntry.get())
    removeEntry.delete(0, 'end')
    taskList.pop(remove)
    generateScrollbox()

# The final method is the Run method, which will individually call both analyses and print the results
def runAnalyses():
    print("Running analyses!")
    edfScheduleGraph.delete("all")
    interEDFScheduleGraph.delete("all")
    intraEDFScheduleGraph.delete("all")
    if (not edf.isSchedulable(taskList)):
        print("Not schedulable")
        edfLabel.config(text="")
        energyLabel.config(text="")
        intraLabel.config(text="This is not schedulable; try removing some tasks.")
        return

    # Generate the schedules and run the energy usages
    length = edf.lcm(taskList)
    edfSchedule = edf.generateSchedule(taskList)
    for e in edfSchedule:
        print("{}{}{}{}{}{}".format("Task: ", e[3], " Start Time: ", e[0], " End Time: ", e[1]))
    edfEnergy = edf.energyUse(edfSchedule)
    interEDFSchedule = energy.generateSchedule(edfSchedule, edfEnergy, length)
    interEDFEnergy = energy.energyUse(interEDFSchedule)
    intraEDFSchedule = intra.generateSchedule(taskList, interEDFSchedule, interEDFEnergy, length)
    intraEDFEnergy = intra.energyUse(intraEDFSchedule)

    # Display the generated schedules and energy usages
    edfLabel.config(text="{}{}".format("EDF Energy Usage: ", edfEnergy))
    energyLabel.config(text="{}{:.2f}".format("Static Voltage EDF Energy Usage: ", interEDFEnergy))
    intraLabel.config(text="{}{:.2f}".format("Intratask Scheduled EDF Energy Usage: ", intraEDFEnergy))

    # Graph the EDF Schedule
    count = 0
    for event in edfSchedule:
        startCoord = int(event[0]*canvasWidth/length)+int(offset/2)
        endCoord   = int((event[2]+event[0])*canvasWidth/length)+int(offset/2)
        edfScheduleGraph.create_rectangle(startCoord,20,endCoord,canvasHeight,fill=event[4])
        if count != 0:
            edfScheduleGraph.create_text(startCoord,10,text=event[0])
        edfScheduleGraph.create_text(endCoord,10,text=(event[0]+event[2]))
        count += 1
    
    edfScheduleGraph.create_text(int(offset/2),10,text="0")
    edfScheduleGraph.create_text(canvasWidth+int(offset/2),10,text=length)
    edfScheduleGraph.create_rectangle(int(offset/2),20,canvasWidth+int(offset/2),canvasHeight)

    # Graph the Intertask Schedule
    count = 0
    
    for event in interEDFSchedule:
        print(event)
        startCoord = int(event[0]*canvasWidth/length)+int(offset/2)
        endCoord   = int((event[2]+event[0])*canvasWidth/length)+int(offset/2)
        heightCoord = 20 + (canvasHeight-20-int(event[5]*float(canvasHeight-20)))
        interEDFScheduleGraph.create_rectangle(startCoord,heightCoord,endCoord,canvasHeight,fill=event[4])
        print(startCoord)
        print(endCoord)
        print(heightCoord)
        if count != 0:
            interEDFScheduleGraph.create_text(startCoord,10,text=int(event[0]))
        interEDFScheduleGraph.create_text(endCoord,10,text=int(event[0]+event[2]))
        count += 1
    
    interEDFScheduleGraph.create_text(int(offset/2),10,text="0")
    interEDFScheduleGraph.create_rectangle(int(offset/2),20,canvasWidth+int(offset/2),canvasHeight)

    # Graph the Intratask Schedule
    count = 0
    
    for event in intraEDFSchedule:
        print(event)
        startCoord = int(event[0]*canvasWidth/length)+int(offset/2)
        endCoord   = int((event[2]+event[0])*canvasWidth/length)+int(offset/2)
        heightCoord = 20 + (canvasHeight-20-int(event[5]*float(canvasHeight-20)))
        intraEDFScheduleGraph.create_rectangle(startCoord,heightCoord,endCoord,canvasHeight,fill=event[4])
        print(startCoord)
        print(endCoord)
        print(heightCoord)
        if count != 0:
            intraEDFScheduleGraph.create_text(startCoord,10,text=int(event[0]))
        intraEDFScheduleGraph.create_text(endCoord,10,text=int(event[0]+event[2]))
        count += 1
    
    intraEDFScheduleGraph.create_text(int(offset/2),10,text="0")
    intraEDFScheduleGraph.create_rectangle(int(offset/2),20,canvasWidth+int(offset/2),canvasHeight)

def launchHelp():
    helpWindow = tk.Tk()
    S = tk.Scrollbar(helpWindow)
    T = tk.Text(helpWindow, height=12, width=100)
    S.pack(side=tk.RIGHT, fill=tk.Y)
    T.pack(side=tk.LEFT, fill=tk.Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)
    addButtonInfo = """Add Button
    This button adds the task parameters to a new Task, adds the Task to the list of tasks, and
    resets the parameter entry points to 0. There are four parameters, two of which are optional:
        Runtime (Required)
            This determines the runtime of the task at a frequency of 1. This must be less than
            or equal to the deadline.
        Deadline (Required)
            This is the deadline for the Task (and the time at which it repeats). If there are
            multiple tasks, the deadlines are used to calculate the Lowest Common Multiple (such
            as 90 for the deadlines 30 and 45).
        Initial Portion Runtime (Optional)
            If intratask simulations are to be run on this Task, this simulates the first portion,
            which must have a minimum frequency of Initial Portion Min Percent. This also must
            have a runtime less than or equal to the runtime.
        Inital Portion Min Percent (Optional)
            If intratask simulations are to be run on this Task, this simulates the minimum
            frequency for the first portion (the Initial Portion Runtime). If the frequency
            determined by the intertask scheduler is greater than this frequency, this has no
            effect. If this is set to greater than 1, it automatically is set to 1.\n"""
    removeButtonInfo = """\nRemove Task Button
    This button removes the task specified in the field to the left. The number should correspond
    to the value in the list.\n"""
    calculateButtonInfo = """\nSchedule Tasks Button
    This button calculates the schedules using a standard EDF algorithm, an energy-aware intertask
    DVS EDF algorithm, and an energy-aware intratask EDF algorithm. The final energy usages are
    also reported for each schedule.\n"""
    T.insert(tk.END, addButtonInfo)
    T.insert(tk.END, removeButtonInfo)
    T.insert(tk.END, calculateButtonInfo)

    helpWindow.mainloop()

# Generate and set up the main parts of the GUI, and start the window up and running
# Add the necessary labels and put the entries on the grid
taskLabel     = tk.Label(text="Runtime: ")
deadlineLabel = tk.Label(text="Deadline: ")
initLabel     = tk.Label(text="Initial Portion Runtime: ")
initAmtLabel  = tk.Label(text="Initial Portion Min Percent: ")
removeLabel   = tk.Label(text="Task: ")
taskLabel.grid(column=3, row=0,sticky='E')
runEntry.grid(column=4, row=0,sticky='W')
deadlineLabel.grid(column=5, row=0,sticky='E')
deadlineEntry.grid(column=6, row=0,sticky='W')
initLabel.grid(column=3, row=1, sticky='E')
initEntry.grid(column=4, row=1, sticky='W')
initAmtLabel.grid(column=5, row=1, sticky='E')
initAmtEntry.grid(column=6, row=1, sticky='W')
removeLabel.grid(column=3,row=2,columnspan=2,sticky='E')
removeEntry.grid(column=5,row=2,columnspan=2,sticky='W')
edfLabel.grid(column=3,row=3, columnspan=2)
energyLabel.grid(column=5,row=3, columnspan=3)
intraLabel.grid(column=3,row=4, columnspan=5)
edfScheduleGraph.grid(column=0, row=5, columnspan=8)
interEDFScheduleGraph.grid(column=0, row=6, columnspan=8)
intraEDFScheduleGraph.grid(column=0, row=7, columnspan=8)

# Add all the necessary buttons
buttonWidth = 10
buttonHeight = 2
addButton = tk.Button(text="Add Task", width=buttonWidth, height=buttonHeight, bg="green", fg="black", command=addTask, relief="groove")
addButton.grid(column=7, row=0)
helpButton = tk.Button(text="Help", width=buttonWidth, height=buttonHeight, bg="blue", fg="black", command=launchHelp, relief="groove")
helpButton.grid(column=7, row=1)
removeButton = tk.Button(text="Remove Task", width=buttonWidth+1, height=buttonHeight, bg="red", fg="black", command=removeTask, relief="groove")
removeButton.grid(column=7, row=2)
runButton = tk.Button(text="Schedule Tasks", width=buttonWidth+3, height=buttonHeight, bg="green", fg="black", command=runAnalyses, relief="groove")
runButton.grid(column=1, row=3)

# Start the window and the main program
window.mainloop()
