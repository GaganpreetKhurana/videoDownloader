import os
from tkinter import *
from tkinter import filedialog, messagebox

import youtube_dl

import downloader

type = None
'''
specifies type of url
playlist or None(single video)
'''
details = dict()
'''
details:dictionary containing the information about all the videos
'''
options = dict()
'''
options: dictionary containing options to be passed to the youtubeDL object
'''


def onDownload():
    '''
    Starts Downloading the Selected Videos
    
    :return: None
    '''
    global details, options
    singlesToDownload = []  # contains id of videos to be downloaded
    for i in videos:
        if videos[i][2].get() == 1:  # selected videos
            singlesToDownload.append(videos[i][1].get())
    print("DownLoading Started")
    downloader.download(details, options, singlesToDownload)  # call download function from downloader
    print("Downloading Finished")


def openDialogBox():
    '''
    To open file dialog box to select location where files should be saved
    locationEntry : Entry Object for location
    location:actual path
    :return: None
    '''
    global location, locationEntry
    location = filedialog.askdirectory(parent=root,
                                       initialdir=location,
                                       title="Please select a folder:")
    locationEntry.delete(0, END)
    locationEntry.insert(END, location)


def printSingle(details, titleLable):
    '''
    for each format of the video it makes a dictionary with key as video name 
    :param details: details about all videos
    :param titleLable: Label Object for title of playlist/video
    :return: None
    '''
    if type is None:  # if url specified is a single video
        global title
        title = details['title']
        titleLable.config(text=title)

    global videos
    videos[details['title']] = [[], IntVar(), IntVar(value=1), []]
    '''
    videos:key:title of video
            value : list of [formats],variable for radioButton,variable for checkBox,[ids of each format]
    '''
    for eachFormat in details:
        if eachFormat != 'title' and eachFormat != 'url':
            videos[details['title']][0].append(details[eachFormat]['format'])
            videos[details['title']][3].append(eachFormat)
            videos[details['title']][1] = IntVar(value=eachFormat)


def printPlaylist(details, titleLable, urlLable):
    '''
    changes title and url labels to playlists title and url
    For each video in playlist calls printSingle to add video details to videos dictionary
    :param details: dictionary:details of all videos
    :param titleLable: title Label
    :param urlLable: Url Label
    :return: None
    '''
    title = details['playlistTitle']
    titleLable.config(text=title)
    videoLink = details['playlistUrl']
    urlLable.config(text="Url: " + videoLink)

    for eachSingle in details['singles']:
        printSingle(details['singles'][eachSingle], titleLable)


def getUrlLocation():
    '''
    gets URL and path when submit is clicked
    :return: None
    '''
    global videoListBox, details, videos, location, link, options
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

    # Checks Path Validity
    if os.path.isdir(location):
        options['outtmpl'] = location + '/%(title)s.%(ext)s'
    else:
        messagebox.showinfo("ERROR", "INVALID INPUT")
        return

    # extract information
    with youtube_dl.YoutubeDL(options) as ydl:
        infoDict = ydl.extract_info(link.get(), download=False)

    # extracts type by call extract type function
    global type
    type = downloader.extractType(infoDict)

    # Creates Empty Labels
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

    # prints menu:Creates Checkboxes and radioButtons,Download Button

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


# creates Gui

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
