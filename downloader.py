from __future__ import unicode_literals

import youtube_dl

count = 0


def extractType(infoDict):
    return infoDict.get('_type', None)


def extractDetailsSingle(infoDict, url):
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
    details = dict()
    details['playlistTitle'] = infoDict['title']
    details['playlistUrl'] = playlistUrl
    details['singles'] = dict()
    for eachSingle in infoDict['entries']:
        details['singles'][eachSingle['title']] = extractDetailsSingle(eachSingle, eachSingle['webpage_url'])
    return details


def printSingleDetails(details):
    for eachFormat in details:
        print(eachFormat, details[eachFormat])


def printPlaylistDetails(details):
    print('Playlist Title: ', details['playlistTitle'])
    print('Playlist URL: ', details['playlistUrl'])
    print()
    for eachSingle in details['singles']:
        printSingleDetails(details['singles'][eachSingle])
        print()


def printSingleMenu(details):
    print("Title: ", details['title'])
    for eachFormat in details:
        if eachFormat != 'title' and eachFormat != 'url':
            print(eachFormat, details[eachFormat]['format'])


def printPlaylistMenu(details):
    print('Playlist Title: ', details['playlistTitle'])
    print()
    for eachSingle in details['singles']:
        printSingleMenu(details['singles'][eachSingle])
        print()


def download(details, options):
    options['skip_download'] = True
    print()
    try:
        singlesToDownload = list(map(int, input("List ID's of Videos to download separated by space: ").split()))
    except:
        print("Invalid")
        return
    if 'singles' in details:
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
                print('Downloading : ', id)
            options['format'] = urlList[id]['formatId']
            with youtube_dl.YoutubeDL(options) as ydl:
                ydl.download([urlList[id]['url']])
            print('Downloaded : ', id)


def extractor(link):
    options = {
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'writesubtitles': False,
        'writeautomaticsub': False,
        'allsubtitles': False,
        'skip_download': True,
    }
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
    download(details.copy(), options.copy())


print('Press "-" to QUIT')
url = input('Enter Playlist/Video Url: ')
# url='https://www.youtube.com/watch?v=oUUyuW5PnhM&list=PL4x7Of-X4XhihdpCA1wCUNB6KEp1FNVms'
# url='https://www.youtube.com/watch?v=oUUyuW5PnhM'
if url == '-':
    print("Good Bye")
else:
    try:
        extractor(url)
    except:
        print("An Error Occurred")
