import os
from tkinter import *
from tkinter import filedialog, messagebox

import youtube_dl

import downloader

type = None
details = {}



def onDownload():
    options = {
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'writesubtitles': False,
        'writeautomaticsub': False,
        'allsubtitles': False,
        'skip_download': True
    }
    global details
    singlesToDownload = []
    for i in videos:
        if videos[i][2].get() == 1:
            singlesToDownload.append(videos[i][1].get())
    print("DownLoading Started")
    downloader.download(details, options, singlesToDownload)
    print("Downloading Finished")


def openDialogBox():
    global location, locationEntry
    location = filedialog.askdirectory(parent=root,
                                       initialdir=location,
                                       title="Please select a folder:")
    locationEntry.delete(0, END)
    locationEntry.insert(END, location)


def printSingle(details, titleLable):
    if type is None:
        global title
        title = details['title']
        titleLable.config(text=title)

    global videos
    videos[details['title']] = [[], IntVar(), IntVar(value=1), []]
    for eachFormat in details:
        if eachFormat != 'title' and eachFormat != 'url':
            videos[details['title']][0].append(details[eachFormat]['format'])
            videos[details['title']][3].append(eachFormat)
            videos[details['title']][1] = IntVar(value=eachFormat)


def printPlaylist(details, titleLable, urlLable):
    title = details['playlistTitle']
    titleLable.config(text=title)
    videoLink = details['playlistUrl']
    urlLable.config(text="Url: " + videoLink)

    for eachSingle in details['singles']:
        printSingle(details['singles'][eachSingle], titleLable)


def getUrlLocation():
    global videoListBox, details, videos, location, link
    videoListBox.destroy()
    canvas = Canvas(baseFrame)
    canvas.grid(row=4, columnspan=50, rowspan=10)
    # scrollBar=Scrollbar(baseFrame,orient="vertical", command=canvas.yview)
    # scrollBar.grid(row=4,column=10)
    # canvas.configure(yscrollcommand=scrollBar.set)
    videoListBox = Frame(canvas)
    videoListBox.grid(row=4, columnspan=50, rowspan=10)
    videos = dict()
    details = dict()

    options = {
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'writesubtitles': False,
        'writeautomaticsub': False,
        'allsubtitles': False,
        'skip_download': True
    }
    if os.path.isdir(location):
        options['outtmpl'] = location + '/%(title)s.%(ext)s'
    else:
        messagebox.showinfo("ERROR", "INVALID INPUT")
        return
    with youtube_dl.YoutubeDL(options) as ydl:
        infoDict = ydl.extract_info(link.get(), download=False)
    global type
    type = downloader.extractType(infoDict)

    titleLable = Label(videoListBox, text="")
    urlLable = Label(videoListBox, text="")

    if type is None:
        details = downloader.extractDetailsSingle(infoDict, link.get())
        printSingle(details, titleLable)
    else:
        details = downloader.extractDetailsPlaylist(infoDict, link.get())
        printPlaylist(details, titleLable, urlLable)

    titleLable.grid(row=4, columnspan=5)
    urlLable.grid(row=5, columnspan=5)
    button = list()
    row = 6
    col = 0
    checkBox = list()
    for video in videos:
        checkBox.append(Checkbutton(videoListBox, text=video, variable=videos[video][2]))
        checkBox[-1].grid(row=row, column=col)

        col += 1
        for i, format in enumerate(videos[video][0]):
            button.append(Radiobutton(videoListBox, text=format, variable=videos[video][1], value=videos[video][3][i]))
            button[-1].grid(row=row, column=col)
            col += 1
        row += 1
        col = 0

    download = Button(videoListBox, text="Download", command=onDownload)
    download.grid(row=row, columnspan=3)


root = Tk()
root.title("Video Downloader")
videos = dict()

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

submit = Button(root, text="Submit", command=getUrlLocation)
submit.grid(row=2, columnspan=3)

baseFrame = Frame(root)
baseFrame.grid(row=4, columnspan=50, rowspan=10)
videoListBox = Frame(baseFrame)
videoListBox.grid(row=4, columnspan=50, rowspan=10)

root.mainloop()
