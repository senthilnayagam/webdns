#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function
import argparse
import os

try:
    from bottle import route, run, response

except ImportError:
    raise ImportError("Please install bottle.py, exiting.")

try:
    import dns.resolver
except ImportError:
    raise ImportError("Please install dnspython, exiting")


# Globals
RESOLVER = dns.resolver.Resolver()


def set_nameservers(servers):
    if isinstance(servers, list):
        print("Using %s as nameservers." % str(servers))
        RESOLVER.nameservers = servers

    else:
        raise TypeError("'server' must be a list")


@route('/favicon.ico')
def favicon():
    return ''


@route('/')
@route('/<name>')
@route('/<record_type>/<name>')
def index(record_type='A', name='www.google.com'):
    response.content_type = 'text/plain'

    try:
        results = str(RESOLVER.query(name, record_type).response)

    except dns.resolver.NXDOMAIN:
        results = 'NXDOMAIN'

    except dns.resolver.NoAnswer:
        results = 'NoAnswer'

    except:
        results = 'Unknown'

    finally:
        return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--nameserver',
        default=[],
        required=False,
        action='append',
        dest='nameservers',
        help="Set various DNS servers to use by IP address")

    parser.add_argument(
        '--port',
        default=8080,
        type=int,
        required=False,
        help="Port to listen on")

    args = parser.parse_args()
    if args.nameservers:
        set_nameservers(args.nameservers)

    run(host='0.0.0.0', port=os.environ.get('PORT', args.port))
