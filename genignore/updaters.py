import requests


def get(updater_name):
    return github


MASTER_ARCHIVE = "https://github.com/github/gitignore/archive/master.zip"


def github(archive_url, latest_file):
    response = requests.get(archive_url, stream=True)
    print(response)
    total_length = response.headers.get('content-length')

    yield total_length

    with open(latest_file, "wb") as f:
        print(total_length)
        if total_length:
            downloaded = 0
            for chunk in response.iter_content(1024):
                f.write(chunk)
                downloaded += len(chunk)
                yield downloaded
        else:
           f.write(response.content)
