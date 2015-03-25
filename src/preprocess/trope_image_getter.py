# A module to download tv trope images
from bs4 import BeautifulSoup
import requests
import requests_cache
import shutil
from os.path import splitext, basename
import os
import time
from src import util

requests_cache.install_cache('tv_tropes_web_cache')


def get_images(trope_names, dest_folder, sleep_interval=0.5, skipExisting=False):
    records = []

    for trope in trope_names:
        res = get_image(trope)

        if res[1] is not None:
            write_image(res[2], trope, res[1], dest_folder)

        records.append((res[0], res[1]))
        time.sleep(sleep_interval)

    return records


def get_image(trope_name):
    print('get_image', trope_name)
    # Get the html page for the trope
    url = 'http://tvtropes.org/pmwiki/pmwiki.php/Main/' + trope_name

    r = requests.get(url)
    body = r.text
    soup = BeautifulSoup(body)
    image_links = soup.select('#wikitext .quoteright img')

    results = list()

    for il in image_links:
        resp = requests.get(il['src'], stream=False)
        results.append((trope_name, il['src'], resp.raw))

    if len(results) > 0:
        return results[0]
    else:
        return (trope_name, None, None)


def write_image(img_stream, trope_name, trope_url, dest_folder):
    extension = splitext(basename(trope_url))[1]
    path = os.path.join(dest_folder, trope_name + extension)
    with open(path, 'wb') as out_file:
        shutil.copyfileobj(img_stream, out_file)


if __name__ == "__main__":
    results = get_images(['ChildSoldiers'], 'images')
    util.write_json('images/imagedownloadres.json', results)

