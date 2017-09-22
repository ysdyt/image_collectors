#-*- coding:utf-8 -*-
import urllib.request
import httplib2
import json
import os
import pickle
import hashlib
import sha3
import configparser # for Python3

from googleapiclient.discovery import build


def make_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def make_correspondence_table(correspondence_table, original_url, hashed_url):
    correspondence_table[original_url] = hashed_url


def getImageUrl(api_key, cse_key, search_word, page_limit, save_dir_path):

    service = build("customsearch", "v1", developerKey=api_key)
    page_limit = page_limit
    startIndex = 1
    response = []

    img_list = []

    make_dir(save_dir_path)
    save_res_path = os.path.join(save_dir_path, 'api_response_file')
    make_dir(save_res_path)

    for nPage in range(0, page_limit):
        print("Reading page number:", nPage + 1)

        try:
            response.append(service.cse().list(
                q=search_word, # Search words
                cx=cse_key, # custom search engine key
                lr='lang_ja', # Search language
                num=10, # Number of images obtained by one request (Max 10)
                start=startIndex,
                searchType='image' # search for images
            ).execute())

            startIndex = response[nPage].get("queries").get("nextPage")[0].get("startIndex")

        except Exception as e:
            print(e)

    with open(os.path.join(save_res_path, 'api_response.pickle'), mode='wb') as f:
        pickle.dump(response, f)

    for one_res in range(len(response)):
        if len(response[one_res]['items']) > 0:
            for i in range(len(response[one_res]['items'])):
                img_list.append(response[one_res]['items'][i]['link'])

    return img_list


def getImage(save_dir_path, img_list):
    make_dir(save_dir_path)
    save_img_path = os.path.join(save_dir_path, 'imgs')
    make_dir(save_img_path)

    opener = urllib.request.build_opener()
    http = httplib2.Http(".cache")

    for i in range(len(img_list)):
        try:
            url = img_list[i]
            extension = os.path.splitext(img_list[i])[-1]
            if extension.lower() in ('.jpg', '.jpeg', '.gif', '.png', '.bmp'):
                encoded_url = url.encode('utf-8')  # required encoding for hashed
                hashed_url = hashlib.sha3_256(encoded_url).hexdigest()
                full_path = os.path.join(save_img_path, hashed_url + extension.lower())

                response, content = http.request(url)
                with open(full_path, 'wb') as f:
                    f.write(content)
                print('saved image... {}'.format(url))

                make_correspondence_table(correspondence_table, url, hashed_url)

        except:
            print("failed to download images.")
            continue


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('authentication.ini')
    google_api_key = config['auth']['google_api_key']
    google_se_key = config['auth']['google_se_key']

    # -------------- Parameter and Path Settings -------------- #
    API_KEY = google_api_key
    CUSTOM_SEARCH_ENGINE = google_se_key

    page_limit = 2
    search_word = '猫'
    save_dir_path = '/root/share/local_data/sandbox'

    correspondence_table = {}

    img_list = getImageUrl(API_KEY, CUSTOM_SEARCH_ENGINE, search_word, page_limit, save_dir_path)
    getImage(save_dir_path, img_list)

    correspondence_table_path = os.path.join(save_dir_path, 'corr_table')
    make_dir(correspondence_table_path)

    with open(os.path.join(correspondence_table_path, 'corr_table.json'), mode='w') as f:
        json.dump(correspondence_table, f)
