import musicbrainzngs as mb
import numpy as np
import pandas as pd
import time

mb.set_useragent('robothy bottano', '1.0', 'smsliman@aol.com')
reviews = pd.read_csv('fantano_reviews.csv', encoding = "ISO-8859-1")

title = reviews['title'][0]
release = mb.search_releases(title)
print(release['release-list'][0])

frame = pd.DataFrame(columns=['id','ext:score', 'title', 'status', 'packaging', 'text-representation-language',
'text-representation-script', 'artist-credit-name', 'artist-credit-artist-id',
 'artist-credit-artist-name', 'artist-credit-artist', 'sort-name', 'release-group-id',
  'release-group-type', 'release-group-title', 'release-group-primary-type', 'date', 'country',
 #could be a lot of items in the event list, this just represents the fields for one item of the list
 'release-event-list-date', 'release-event-list-area-id', 'release-event-list-area-name', 'release-event-list-area-sort-name', 'release-event-list-area-iso-3166-1-code-list',
 #same thing here for label info list, but will likely just 0 index on this
 'label-info-list-catalog-number', 'label-info-list-label-id', 'label-info-list-label-name',
 #same thing for meduim list as for label list
 'medium-list-format', 'medium-list-disc-list','medium-list-disc-count', 'medium-list-track-list', 'medium-list-track-count',
 #need to check what tag list is about, sample didn't have anything there
 'medium-track-count', 'medium-count', 'tag-list', 'artist-credit-phrase', 'score'])

count = 0


for title in reviews['title']:
    search = mb.search_releases(title)
    if search['release-list']:
        release = search['release-list'][0]
    else:
        release = {}
    if reviews['score'][count] is not None:
        score = reviews['score'][count]
    elif reviews['word_score'][count] is not None:
        score = reviews['word_score'][count]
    else:
        score = 'Unknown'

    dict = {}
    if count is not None:
        dict['index'] = count
    if 'id' in release:
        dict['id'] = release['id']
    if 'ext:score' in release:
        dict['ext:score'] = release['ext:score']
    if 'title' in release:
        dict['title'] = release['title']
    if 'status' in release:
        dict['status'] = release['status']
    if 'packaging' in release:
        dict['packaging'] = release['packaging']
    if 'text-representation' in release:
        if 'language' in release['text-representation']:
            dict['text-representation-language'] = release['text-representation']['language']
    if 'text-representation' in release:
        if 'script' in release['text-representation']:
            dict['text-representation-script'] = release['text-representation']['script']
    if 'artist-credit' in release:
        if release['artist-credit']:
            if 'name' in release['artist-credit'][0]:
                dict['artist-credit-name'] = release['artist-credit'][0]['name']
    if 'artist-credit' in release:
        if release['artist-credit']:
            if 'artist' in release['artist-credit'][0]:
                if 'id' in release['artist-credit'][0]['artist']:
                    dict['artist-credit-artist-id'] = release['artist-credit'][0]['artist']['id']
    if 'artist-credit' in release:
        if release['artist-credit']:
            if 'artist' in release['artist-credit'][0]:
                if 'name' in release['artist-credit'][0]['artist']:
                    dict['artist-credit-artist-name'] = release['artist-credit'][0]['artist']['name']
    if 'artist-credit' in release:
        if release['artist-credit']:
            if 'artist' in release['artist-credit'][0]:
                if 'sort-name' in release['artist-credit'][0]['artist']:
                    dict['artist-credit-artist-sort-name'] = release['artist-credit'][0]['artist']['sort-name']
    if 'release-group' in release:
        if 'id' in release['release-group']:
            dict['release-group-id'] = release['release-group']['id']
    if 'release-group' in release:
        if 'type' in release['release-group']:
            dict['release-group-type'] = release['release-group']['type']
    if 'release-group' in release:
        if 'title' in release['release-group']:
            dict['release-group-title'] = release['release-group']['title']
    if 'release-group' in release:
        if 'primary-type' in release['release-group']:
            dict['release-group-primary-type'] = release['release-group']['primary-type']
    if 'date' in release:
        dict['date'] = release['date']
    if 'country' in release:
        dict['country'] = release['country']
    if 'release-event-list' in release:
        if release['release-event-list']:
            if 'date' in release['release-event-list'][0]:
                dict['release-event-list-date'] = release['release-event-list'][0]['date']
    if 'release-event-list' in release:
        if release['release-event-list']:
            if 'area' in release['release-event-list'][0]:
                if 'id' in release['release-event-list'][0]['area']:
                    dict['release-event-list-area-id'] = release['release-event-list'][0]['area']['id']
    if 'release-event-list' in release:
        if release['release-event-list']:
            if 'area' in release['release-event-list'][0]:
                if 'name' in release['release-event-list'][0]['area']:
                    dict['release-event-list-area-name'] = release['release-event-list'][0]['area']['name']
    if 'release-event-list' in release:
        if release['release-event-list']:
            if 'area' in release['release-event-list'][0]:
                if 'sort-name' in release['release-event-list'][0]['area']:
                    dict['release-event-list-area-sort-name'] = release['release-event-list'][0]['area']['sort-name']
    if 'release-event-list' in release:
        if release['release-event-list']:
            if 'area' in release['release-event-list'][0]:
                if 'iso-3166-1-code-list' in release['release-event-list'][0]['area']:
                    dict['release-event-list-area-iso-3166-1-code-list'] = release['release-event-list'][0]['area']['iso-3166-1-code-list'][0]
    if 'label-info-list' in release:
        if release['label-info-list']:
            if 'catalog-number' in release['label-info-list'][0]:
                dict['label-info-list-catalog-number'] = release['label-info-list'][0]['catalog-number']
    if 'label-info-list' in release:
        if release['label-info-list']:
            if 'label' in release['label-info-list'][0]:
                if 'id' in release['label-info-list'][0]['label']:
                    dict['label-info-list-label-id'] = release['label-info-list'][0]['label']['id']
    if 'label-info-list' in release:
        if release['label-info-list']:
            if 'label' in release['label-info-list'][0]:
                if 'name' in release['label-info-list'][0]['label']:
                    dict['label-info-list-label-name'] = release['label-info-list'][0]['label']['name']
    if 'medium-list' in release:
        if release['medium-list']:
            if 'format' in release['medium-list'][0]:
                dict['medium-list-format'] = release['medium-list'][0]['format']
    if 'medium-list' in release:
        if release['medium-list']:
            if 'disc-list' in release['medium-list'][0]:
                dict['medium-list-disc-list'] = release['medium-list'][0]['disc-list']
    if 'medium-list' in release:
        if release['medium-list']:
            if 'disc-count' in release['medium-list'][0]:
                dict['medium-list-disc-count'] = release['medium-list'][0]['disc-count']
    if 'medium-list' in release:
        if release['medium-list']:
            if 'track-list' in release['medium-list'][0]:
                dict['medium-list-track-list'] = release['medium-list'][0]['track-list']
    if 'medium-list' in release:
        if release['medium-list']:
            if 'track-count' in release['medium-list'][0]:
                dict['medium-list-track-count'] = release['medium-list'][0]['track-count']
    if 'medium-track-count' in release:
        dict['medium-track-count'] = release['medium-track-count']
    if 'medium-count' in release:
        dict['medium-count'] = release['medium-count']
    if 'tag-list' in release:
        dict['tag-list'] = release['tag-list']
    if 'artist-credit-phrase' in release:
        dict['artist-credit-phrase'] = release['artist-credit-phrase']

    #gotta get empty scores figured out
    dict['score'] = score

    frame = frame.append(dict, ignore_index=True)


    # frame = frame.append({
    # 'index': count,
    # 'id': release['id'],
    # 'ext:score': release['ext:score'],
    # 'title': release['title'],
    # 'status': release['status'],
    # 'packaging': release['packaging'],
    # 'text-representation-language': release['text-representation']['language'],
    # 'text-representation-script': release['text-representation']['script'],
    # 'artist-credit-name': release['artist-credit'][0]['name'],
    # 'artist-credit-artist-id': release['artist-credit'][0]['artist']['id'],
    # 'artist-credit-artist-name': release['artist-credit'][0]['artist']['name'],
    # 'artist-credit-artist-sort-name': release['artist-credit'][0]['artist']['sort-name'],
    # 'release-group-id': release['release-group']['id'],
    # 'release-group-type': release['release-group']['type'],
    # 'release-group-title': release['release-group']['title'],
    # 'release-group-primary-type': release['release-group']['primary-type'],
    # 'date': release['date'],
    # 'country': release['country'],
    # 'release-event-list-date': release['release-event-list'][0]['date'],
    # 'release-event-list-area-id': release['release-event-list'][0]['area']['id'],
    # 'release-event-list-area-name': release['release-event-list'][0]['area']['name'],
    # 'release-event-list-area-sort-name': release['release-event-list'][0]['area']['sort-name'],
    # 'release-event-list-area-iso-3166-1-code-list': release['release-event-list'][0]['area']['iso-3166-1-code-list'][0],
    # 'label-info-list-catalog-number': release['label-info-list'][0]['catalog-number'],
    # 'label-info-list-label-id': release['label-info-list'][0]['label']['id'],
    # 'label-info-list-label-name': release['label-info-list'][0]['label']['name'],
    # 'medium-list-format': release['medium-list'][0]['format'],
    # 'medium-list-disc-list': release['medium-list'][0]['disc-list'],
    # 'medium-list-disc-count': release['medium-list'][0]['disc-count'],
    # 'medium-list-track-list': release['medium-list'][0]['track-list'],
    # 'medium-list-track-count': release['medium-list'][0]['track-count'],
    # 'medium-track-count': release['medium-track-count'],
    # 'medium-count': release['medium-count'],
    # 'tag-list': release['tag-list'],
    # 'artist-credit-phrase': release['artist-credit-phrase'],
    # 'score': score
    # }, ignore_index=True)

    count = count + 1
    print(count)
    time.sleep(1)


try:
    frame.to_csv('data.csv', index=False)
except Exception:
    print('error writing to file')
    breakpoint()
