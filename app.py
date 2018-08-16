import argparse
import urllib
import urllib.request
import os

import storage


def load_html(path_to_html_file):
    with open(path_to_html_file, "r") as html_file:
        return html_file.read()


def main():
    parser = argparse.ArgumentParser(description='Wallpapers downloader')
    parser.add_argument('-y', '--year', required=True)
    parser.add_argument('-m', '--month', required=True)
    parser.add_argument('-r', '--resolution', required=True)
    args = parser.parse_args()

    links = storage.find_wallpapers_links(args.resolution, args.year, args.month)

    if not os.path.exists('./wallpapers'):
        os.makedirs('./wallpapers')

    for link in links:
        download_wallpaper(link)

    print('found %s wallpapers. Downloaded to ./wallpapers' % len(links))


def download_wallpaper(link):
    try:
        # Download the file from `url` and save it locally
        file_extension = link[0].split('/')[-1].split('.')[1]
        urllib.request.urlretrieve(link[0], './wallpapers/%s.%s' % (link[1], file_extension))
    except Exception as e:
        print('Failed to download %s: %s' % (link[0], str(e)))


if __name__ == "__main__":
    main()