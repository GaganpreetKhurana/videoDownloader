import os
from tkinter import *
from tkinter import filedialog


def printText():
    global link, location
    print(link.get())
    print(location)
    for i in videos:
        print(i, videos[i][1].get(), videos[i][2].get())


def openDialogBox():
    global location, locationEntry
    location = filedialog.askdirectory(parent=root,
                                       initialdir=location,
                                       title="Please select a folder:")
    locationEntry.delete(0, END)
    locationEntry.insert(END, location)


root = Tk()
root.title("Video Downloader")

linkLabel = Label(root, text="URL")
linkLabel.grid(row=0, column=0)
link = Entry(root, width=50)
link.grid(row=0, column=1)

locationLabel = Label(root, text="Location")
locationLabel.grid(row=1, column=0)
location = os.getcwd()
locationEntry = Entry(root, width=50)
locationEntry.insert(END, location)
locationEntry.grid(row=1, column=1)

selectLocation = Button(root, text="Select Location", command=openDialogBox)
selectLocation.grid(row=1, column=3)

submit = Button(root, text="Submit", command=printText)
submit.grid(row=2, columnspan=3)

videos = {
    "Video 1": [['1080p', '720p', '360p'], IntVar(), IntVar(value=1)],
    "Video 2": [['1080p', '720p', '360p'], IntVar(), IntVar(value=1)],
    "Video 3": [['1080p', '720p', '360p'], IntVar(), IntVar(value=1)]
}

videoListBox = Frame(root)
videoListBox.grid(row=4, columnspan=50, rowspan=10)
title = "Dice"
titleLable = Label(videoListBox, text=title)
titleLable.grid(row=4, columnspan=5)
button = list()
row = 5
col = 0
checkBox = list()
for video in videos:
    tempCheckButton = Checkbutton(videoListBox, text=video, variable=videos[video][2])
    tempCheckButton.grid(row=row, column=col)

    col += 1
    for i, format in enumerate(videos[video][0]):
        button.append(Radiobutton(videoListBox, text=format, variable=videos[video][1], value=i))
        button[-1].grid(row=row, column=col)
        col += 1
    row += 1
    col = 0
download = Button(videoListBox, text="Download", command=printText)
download.grid(row=row, columnspan=3)
root.mainloop()
