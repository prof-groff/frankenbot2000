#!/usr/bin/python3

import requests
import os
import numpy as np
from PIL import Image
import time
import tweepy

def get_storage(storage_url):
    r = requests.get(storage_url)
    if r.status_code == 200:
        data = r.json()
        success = True
    else:
        data = []
        success = False

    return success, data

def get_newest_token_data(tokens_url, data, wait=0):
    time.sleep(wait)
    next_token_id = data['children'][1]['value'] # string
    newest_token_id = int(next_token_id) - 1
    r = requests.get(tokens_url)
    if r.status_code == 200:
        token_data = r.json()
        try: # may fail since /storage updates before /tokens
            newest_token_data = next(item for item in token_data if item['token_id'] == newest_token_id)
            success = True
        except:
            newest_token_data = []
            success = False
    else:
        newest_token_data = []
        success = False

    return success, newest_token_id, newest_token_data

def get_newest_token_info(newest_token_id, newest_token_data):
    artifact_uri = newest_token_data['token_info']['artifactUri'].split('//')[1]
    artifact_url = 'https://cloudflare-ipfs.com/ipfs/' + artifact_uri
    nft_title = newest_token_data['name']
    nft_url = 'https://hicetnunc.xyz/objkt/' + str(newest_token_id)
    nft_filetype = newest_token_data['token_info']['formats'][0]['mimeType']
    nft_description = newest_token_data['token_info']['description']

    return {'id': newest_token_id, 'art_uri': artifact_uri, 'art_url': artifact_url, 'title': nft_title, 
            'nft_url': nft_url, 'filetype': nft_filetype, 'description': nft_description}

def prepare_media(newest_token_info):
    art_uri = newest_token_info['art_uri']
    art_url = newest_token_info['art_url']
    filetype = newest_token_info['filetype']

    if filetype in ['image/jpeg', 'image/png', 'image/gif']:
        os.system('wget ' + art_url) # download artwork
        picture = Image.open(art_uri) # open using Pillow
        img_ext = picture.format # determine appropriate file extension (format)
        img_filesize = os.path.getsize(art_uri) # determine filesize
        width, height = picture.size # determine dimenstions
        max_size = int(3072000*0.95) # approx. max image size for twitter post (kB)
        new_filename = art_uri + '.' + img_ext  # new name and save
        os.system('mv ' + art_uri + ' ' + new_filename)

        while img_filesize > max_size:
            scale_factor = np.sqrt(img_filesize / max_size) # this is pretty primitive way of doing this
            width = int(width/scale_factor)
            height = int(height/scale_factor)
            picture = picture.resize((width, height)) # resize
            picture.save(new_filename)
            img_filesize = os.path.getsize(new_filename)

        # os.remove(art_uri) # clean up
        success = True

    else:
        new_filename = ''
        success = False

    return success, new_filename

def send_tweet(message, new_filename):
    try:
        auth = tweepy.OAuthHandler("0f2WIXwLebY5wIfeGwFEoZYrR", "TRe9KBVMPCB0l0AmVMkXG8zaUfUTh0RcbqLQJ45nbwa1gHvQwq")
        auth.set_access_token("1206950129468616704-7UWSKqdUuLM9bxWWisrwl5ZzwMpOty", "rcsKad78QuG7n5YlxdyjYUyoyRoQlMkLOr8f5oXM5sb5r")
        api = tweepy.API(auth)
        reply = api.update_with_media(filename=new_filename, status=message)
        # print(reply)
        success = True
    except:
        success = False

    os.remove(new_filename)

    return success

contract_address = "KT1RJ6PbjHpwc3M5rw5s2Nbmefwbuwbdxton"
storage_url = 'https://better-call.dev/v1/contract/mainnet/' + contract_address + '/storage'
tokens_url = 'https://better-call.dev/v1/contract/mainnet/' + contract_address + '/tokens'
last_token_id = 0 # the id of the last token tweeted

while(1):

    try:
        print("Getting current block data from chain...")
        success, data = get_storage(storage_url)
        if success:
            print("Getting token data from chain...")
            success, newest_token_id, newest_token_data = get_newest_token_data(tokens_url, data, 5)
            print(success)
            if newest_token_id > last_token_id:
                last_token_id = newest_token_id
            else:
                success = False
            print(success)
        if success:
            print("Getting info about newest minted token...")
            newest_token_info = get_newest_token_info(newest_token_id, newest_token_data)
            success, new_filename = prepare_media(newest_token_info)
            print(success)
        if success:
            print("Sending tweet...")
            message = 'Oh Goody! A newly minted Tezos NFT titled "' + newest_token_info['title'] + '" on hic et nunc! ' + newest_token_info['description'] + ' ' + newest_token_info['nft_url']
            success = send_tweet(message, new_filename)
            print(success)
    except:
        pass

    time.sleep(120)
