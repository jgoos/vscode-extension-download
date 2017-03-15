#!/usr/bin/python
"""
Download extensions from the vscode marketplace to use for offline installs
"""
import json
import requests
import yaml
from bs4 import BeautifulSoup

def get_extention(publisher_name, extension_name, version):
    """
    download the extention from the vscode market and rename it
    """
    # format url
    url = "https://{publisher}.gallery.vsassets.io/_apis/public/gallery/publisher/{publisher}/extension/{extension}/{version}/assetbyname/Microsoft.VisualStudio.Services.VSIXPackage".format(publisher=publisher_name, extension=extension_name, version=version)
    request = requests.get(url)

    filename = '{extension}-{version}.VSIX'.format(extension=extension_name, version=version)
    with open(filename, "wb") as code:
        code.write(request.content)
    print "Download Complete: {filename}".format(filename=filename)

def get_metadata(url):
    """
    get version, publisher and extension name from url with BeautifulSoup
    """
    resp = requests.get(url)

    soup = BeautifulSoup(resp.content, "html.parser")
    # get json from soup
    data = json.loads(soup.find('script', type='application/json').text)

    publisher_name = data['publisher']['publisherName']
    extension_name = data['extensionName']
    version = data['versions'][0]['version']

    return (publisher_name, extension_name, version)

def main():
    configfile = 'config.yml'
    # get urls from input file
    with open(configfile, 'r') as filename:
        output = filename.read()

    # get configuration from yml
    config = yaml.load(output)

    for urlname in config['urls']:
        publisher_name, extension_name, version = get_metadata(urlname)
        get_extention(publisher_name, extension_name, version)

if __name__ == "__main__":
    main()
