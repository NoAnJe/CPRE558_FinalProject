import task
import edf_analyze as edf
import energy_analyze as energy
import tkinter as tk

# Generate the components that will be needed in the functions, which must be declared before being used
taskList = []
window = tk.Tk()
runEntry = tk.Entry(width=5)
deadlineEntry = tk.Entry(width=5)
removeEntry = tk.Entry(width=5)

edfLabel    = tk.Label(text="")
energyLabel = tk.Label(text="")

scrollbar = tk.Scrollbar(window)
scrollbar.grid(column=0, row=0, columnspan=3, rowspan=3)
taskListPage = tk.Listbox(yscrollcommand=scrollbar.set, width=40)
taskListPage.grid(column=0, row=0, columnspan=3, rowspan=3)
scrollbar.config(command=taskListPage.yview)

canvasWidth=500
canvasHeight=50
offset=10

edfScheduleGraph = tk.Canvas(width=canvasWidth+offset, height=canvasHeight)
energyScheduleGraph = tk.Canvas(width=canvasHeight+offset, height=canvasHeight)

# Next method is the Scrollbox generation, which will generate a scrollbox with the list of tasks that exist
def generateScrollbox():
    print("Generating scrollbox!")
    taskListPage = tk.Listbox(yscrollcommand=scrollbar.set, width=40)
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
    # TODO ADD TASK
    runtime = int(runEntry.get())
    deadline = int(deadlineEntry.get())
    print("{}{}{}{}".format("Runtime: ",runtime," Deadline:",deadline))
    runEntry.delete(0, 'end')
    deadlineEntry.delete(0, 'end')
    tempTask = task.Task(runtime, deadline)
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
    if (not edf.isSchedulable(taskList)):
        print("Not schedulable")
        return

    # Generate the schedules and run the energy usages
    length = edf.lcm(taskList)
    edfSchedule = edf.generateSchedule(taskList)
    for e in edfSchedule:
        print("{}{}{}{}{}{}".format("Task: ", e[3], " Start Time: ", e[0], " End Time: ", e[1]))
    energySchedule = energy.generateSchedule(taskList)
    edfEnergy = edf.energyUse(edfSchedule)
    efficientEnergy = energy.energyUse(energySchedule)

    # Display the generated schedules and energy usages
    edfLabel.config(text="{}{}".format("EDF Energy Usage: ", edfEnergy))
    energyLabel.config(text="{}{}".format("Efficient Energy Usage: ", efficientEnergy))

    edfScheduleGraph.delete("all")
    energyScheduleGraph.delete("all")

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

    # Graph the Energy Schedule
    count = 0
    for event in energySchedule:
        startCoord  = int(event[0]*canvasWidth/length)+int(offset/2)
        endCoord    = startCoord + int(event[2]*canvasWidth/length)
        heightCoord = 20 + int((1.0-event[5])*(canvasHeight-20))
        energyScheduleGraph.create_rectangle(startCoord,heightCoord,endCoord,canvasHeight,fill=event[4])
        if count != 0:
            energyScheduleGraph.create_text(startCoord,10,text=event[0])
        energyScheduleGraph.create_text(endCoord,10,text=(event[0]+event[2]))
        count += 1
    
    energyScheduleGraph.create_text(int(offset/2),10,text="0")
    energyScheduleGraph.create_text(canvasWidth,10,text=length)
    energyScheduleGraph.create_rectangle(int(offset/2),20,canvasWidth+int(offset/2),canvasHeight)

# Generate and set up the main parts of the GUI, and start the window up and running
# Add the necessary labels and put the entries on the grid
taskLabel     = tk.Label(text="Runtime: ")
deadlineLabel = tk.Label(text="Deadline: ")
removeLabel   = tk.Label(text="Task: ")
taskLabel.grid(column=3, row=0)
runEntry.grid(column=4, row=0)
deadlineLabel.grid(column=5, row=0)
deadlineEntry.grid(column=6, row=0)
removeLabel.grid(column=4,row=1)
removeEntry.grid(column=5,row=1)
edfLabel.grid(column=3,row=3, columnspan=2)
energyLabel.grid(column=5,row=3, columnspan=2)
edfScheduleGraph.grid(column=0, row=4, columnspan=6)
energyScheduleGraph.grid(column=0, row=5, columnspan=6)

# Add all the necessary buttons
buttonWidth = 10
buttonHeight = 2
addButton = tk.Button(text="Add Task", width=buttonWidth, height=buttonHeight, bg="green", fg="black", command=addTask, relief="groove")
addButton.grid(column=7, row=0)
removeButton = tk.Button(text="Remove Task", width=buttonWidth+1, height=buttonHeight, bg="red", fg="black", command=removeTask, relief="groove")
removeButton.grid(column=7, row=1)
runButton = tk.Button(text="Schedule Tasks", width=buttonWidth+3, height=buttonHeight, bg="green", fg="black", command=runAnalyses, relief="groove")
runButton.grid(column=1, row=3)

# Start the window and the main program
window.mainloop()
