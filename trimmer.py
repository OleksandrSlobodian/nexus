#!/usr/bin/env Python
import requests
import optparse
from natsort import natsorted
from xml.etree import ElementTree


def parser(req, li, item):
    resp = requests.get(req)
    tree = ElementTree.fromstring(resp.content)
    text_list = [el.text for elem in tree[0] for el in elem
                 if el.tag == item]
    li.extend(text_list)


def trimmer(req, user, passw, keep, omit):
    list_omit = [e for e in omit.split(',')]
    id_list = []
    parser(req, id_list, 'id')
    repos = [item for item in id_list if item not in list_omit]
    print '\n-> Trimming Repositories:'
    print repos
    for repo in repos:
        _url = req + '/' + repo + '/content/'
        artifacts = []
        parser(_url, artifacts, 'text')
        print '\n-> Repository: ' + repo
        print '\n-> Artifact Groups:'
        print artifacts
        for artifact in artifacts:
            url = _url + artifact + '/'
            versionList = []
            parser(url, versionList, 'text')
            sorted_li = natsorted(versionList)
            if sorted_li[:-keep]:
                dl = sorted_li[:-keep]
                print '\n-> Deleting Artifact ' + artifact + ' Versions:'
                print dl
                print map(lambda x: requests.delete(url + x,
                                                    auth=(user, passw)), dl)
            else:
                print '\n-> Artifact Group ' + artifact + ' already trimmed.'


def main():
    parser = optparse.OptionParser()
    parser.add_option('--user',
                      help='Nexus API username', default='')
    parser.add_option('--passwd',
                      help='Nexus API password', default='')
    parser.add_option('--host',
                      help='Nexus API host', default='127.0.0.1')
    parser.add_option('--port',
                      help='Nexus API port', default='8081')
    parser.add_option('--keep', type='int',
                      help='Nexus Artifact versions to keep', default=500)
    parser.add_option('--omit',
                      help='Coma separated Nexus repositories', default='')
    (options, args) = parser.parse_args()
    path = '/nexus/service/local/repositories'
    url = 'http://' + options.host + ':' + options.port + path
    trimmer(url, options.user, options.passwd, options.keep, options.omit)

if __name__ == '__main__':
    main()
