from __future__ import unicode_literals

import youtube_dl


def extractType(infoDict):
    return infoDict.get('_type', None)


def extractDetailsSingle(infoDict, url):
    details = dict()
    details['title'] = infoDict['title']
    details['url'] = url
    for eachFormat in infoDict['formats']:
        if eachFormat['acodec'] != 'none' and (eachFormat['ext'] == 'mp4' or eachFormat['ext'] == 'm4a'):
            detailsEachFormat = dict()
            detailsEachFormat['formatId'] = eachFormat['format_id']
            detailsEachFormat['extension'] = eachFormat['ext']
            detailsEachFormat['videoAvailable'] = eachFormat['vcodec'] != 'none'
            detailsEachFormat['audioAvailable'] = eachFormat['acodec'] != 'none'
            details[eachFormat['format_note']] = detailsEachFormat
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


def extractor(link='https://www.youtube.com/watch?v=oUUyuW5PnhM&list=PL4x7Of-X4XhihdpCA1wCUNB6KEp1FNVms'):
    options = {
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'allsubtitles': True,
        'skip_download': True,
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        infoDict = ydl.extract_info(link, download=False)
    type = extractType(infoDict)
    if type is None:
        details = extractDetailsSingle(infoDict, link)
        printSingleDetails(details)
    else:
        details = extractDetailsPlaylist(infoDict, link)
        printPlaylistDetails(details)


# extractor('https://www.youtube.com/watch?v=oUUyuW5PnhM')
extractor()
