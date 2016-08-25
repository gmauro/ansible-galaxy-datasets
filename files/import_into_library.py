#!/usr/bin/env python
import argparse
import yaml
# from bioblend import galaxy
from bioblend.galaxy.objects import *


def main():
    """
        This script uses bioblend to import datasets into a library of a running
        instance of Galaxy
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--datasets_list", required=True,
                        help='Path to the yaml file with the datasets list')
    parser.add_argument("-g", "--galaxy",
                        dest="galaxy_url",
                        help="Target Galaxy instance URL/IP address (required "
                             "if not defined in the tools list file)",)
    parser.add_argument("-a", "--apikey",
                        dest="api_key",
                        help="Galaxy admin user API key (required if not "
                             "defined in the tools list file)",)
    args = parser.parse_args()

    with open(args.datasets_list) as f:
      datasets = yaml.load(f)

    gi = GalaxyInstance(args.galaxy_url, args.api_key)

    for d in datasets['datasets']:
        libraries = gi.libraries.list(name=d['library_label'])
        library = None
        for l in libraries:
            print l.name
            if l.name == d['library_label']:
                library = l
        if not library:
            library = gi.libraries.create(name=d['library_label'])

        results = library.upload_from_url(d['url'])
        print results


if __name__ == '__main__':
    main()
