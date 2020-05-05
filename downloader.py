from __future__ import unicode_literals

import os

import youtube_dl

count = 0
'''
stores number of videos*formats for id 
'''


def extractType(infoDict):
    '''
    return type of link(playlist/None(single video))
    :param infoDict: Dictionary of details from
    :return: type
    '''
    return infoDict.get('_type', None)


def extractDetailsSingle(infoDict, url):
    '''
    extract video details from info dict
    :param infoDict: details extracted by youtube_dl
    :param url: url provided
    :return: details: dictionary containing video details
                    title
                    url
                    id(count) :dictionary: formatId,format,extension,url,bool videoAvailable,bool audioAvailable,
    '''
    details = dict()
    global count
    details['title'] = infoDict['title']
    details['url'] = url
    for eachFormat in infoDict['formats']:
        if eachFormat['acodec'] != 'none' and (eachFormat['ext'] == 'mp4' or eachFormat['ext'] == 'm4a'):
            detailsEachFormat = dict()
            detailsEachFormat['formatId'] = eachFormat['format_id']
            detailsEachFormat['format'] = eachFormat['format_note']
            detailsEachFormat['extension'] = eachFormat['ext']
            detailsEachFormat['url'] = url
            detailsEachFormat['videoAvailable'] = eachFormat['vcodec'] != 'none'
            detailsEachFormat['audioAvailable'] = eachFormat['acodec'] != 'none'
            details[count] = detailsEachFormat

            count += 1
    return details


def extractDetailsPlaylist(infoDict, playlistUrl):
    '''
    extract playlist details from info dict and call extractDetailsSingle for each video

    :param infoDict: details extracted by youtube_dl
    :param playlistUrl: url of playlist
    :return: details: playlist title
                      playlist Url
                      singles: dictionary
                                title of video: dictionary containing video details
                                                title
                                                url
                                                id(count) :dictionary: formatId,format,extension,url,bool videoAvailable,bool audioAvailable,
    '''
    details = dict()
    details['playlistTitle'] = infoDict['title']
    details['playlistUrl'] = playlistUrl
    details['singles'] = dict()
    for eachSingle in infoDict['entries']:
        details['singles'][eachSingle['title']] = extractDetailsSingle(eachSingle, eachSingle['webpage_url'])
    return details


def printSingleDetails(details):
    '''
    Print details of each video
    :param details: dictionary of details of each single
    :return: None
    '''
    for eachFormat in details:
        print(eachFormat, details[eachFormat])


def printPlaylistDetails(details):
    '''
    print details of each playlist and call printSingleDetails for each video
    :param details: dictionary of details of playlist
    :return: None
    '''
    print('Playlist Title: ', details['playlistTitle'])
    print('Playlist URL: ', details['playlistUrl'])
    print()
    for eachSingle in details['singles']:
        printSingleDetails(details['singles'][eachSingle])
        print()


def printSingleMenu(details):
    '''
    Print Menu for video
    id format
    :param details: dictionary about video
    :return: None
    '''
    print("Title: ", details['title'])
    for eachFormat in details:
        if eachFormat != 'title' and eachFormat != 'url':
            print(eachFormat, details[eachFormat]['format'])


def printPlaylistMenu(details):
    '''
    Print Menu for playlist and call printSingleMenu for each video
    :param details: dictionary about playlist
    :return: None
    '''
    print('Playlist Title: ', details['playlistTitle'])
    print()
    for eachSingle in details['singles']:
        printSingleMenu(details['singles'][eachSingle])
        print()


def download(details, options, singlesToDownload=None):
    '''
    Download videos
    :param details: dictionary about playlist/video
    :param options: dictionary of options for youtubeDL
    :param singlesToDownload: list of ids of format (video) to download
    :return: None
    '''
    options['skip_download'] = False
    print()
    if singlesToDownload is None:  # for non gui
        try:
            singlesToDownload = list(map(int, input("List ID's of Videos to download separated by space: ").split()))
        except:
            print("Invalid")
            return
    if 'singles' in details:  # for playlist
        urlList = dict()
        details = details['singles']
        for titles in details:
            for id in details[titles]:
                if id == 'title' or id == 'url':
                    continue
                urlList[id] = {'url': details[titles][id]['url'], 'title': titles,
                               'formatId': details[titles][id]['formatId']}
    else:
        urlList = details
    for id in singlesToDownload:
        print("Trying", id)
        if id in urlList:
            if 'title' in urlList[id]:
                print('Downloading : ', urlList[id]['title'], " :: ", id)
            else:
                print('Downloading : ', urlList['title'])
            options['format'] = urlList[id]['formatId']
            with youtube_dl.YoutubeDL(options) as ydl:
                ydl.download([urlList[id]['url']])
            if 'title' in urlList[id]:
                print('Download Complete : ', urlList[id]['title'], " :: ", id)
            else:
                print('Download Complete : ', urlList['title'])
            continue
        print("Failed", id)


def extractor(link, pathToBeSaved=None):
    '''
    extracts details
    :param link: url of link of playlist
    :param pathToBeSaved: path where videos will be saved
    :return: None
    '''
    options = {
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'writesubtitles': False,
        'writeautomaticsub': False,
        'allsubtitles': False,
        'skip_download': True
    }
    gui = True
    if pathToBeSaved is None:
        gui = False
        pathToBeSaved = input('Enter Download Path: ')
    if os.path.isdir(pathToBeSaved):  # check is directory exists
        options['outtmpl'] = pathToBeSaved + '/%(title)s.%(ext)s'
    else:
        print("Invalid Path ")
        return

    with youtube_dl.YoutubeDL(options) as ydl:
        infoDict = ydl.extract_info(link, download=False)
    type = extractType(infoDict)

    if type is None:
        details = extractDetailsSingle(infoDict, link)
        # printSingleDetails(details)
        printSingleMenu(details)
    else:
        details = extractDetailsPlaylist(infoDict, link)
        # printPlaylistDetails(details)
        printPlaylistMenu(details)

    if gui is False:
        download(details.copy(), options.copy())


if __name__ == '__main__':
    print('Press "-" to QUIT')
    url = input('Enter Playlist/Video Url: ')
    if url == '-':
        print("Good Bye")
    else:
        try:
            extractor(url)
        except:
            print("An Error Occurred")
