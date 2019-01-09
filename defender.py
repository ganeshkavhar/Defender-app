#!/usr/bin/env python
__author__ = 'Ron Reiter <ron.reiter@gmail.com>'

from libmproxy import controller, proxy

import argparse
import shelve
import urlparse

# The database which stores the allowed URLs
db = shelve.open('defender')

# Program arguments
parser = argparse.ArgumentParser(description='Run ServerDefender')
parser.add_argument('--incoming_port', type=int, help='Incoming HTTP traffic port', default=8080)
parser.add_argument('--server_port', type=int, help='Port of the server to forward requests to', default=8000)
parser.add_argument('--server_host', type=str, help='Host of the server to forward requests to', default='localhost')
parser.add_argument('--learn_mode', type=bool, help='Run in learning mode', default=False)

args = parser.parse_args()


class ServerDefender(controller.Master):
    """
        ServerDefender controller module

        If learn_mode is on, the proxy will save all paths accessed to the database.
        To run with learn_mode, run:

        ./defender.py --learn_mode=True

        If learn_mode is off, then it will disallow all HTTP requests that were not previously learned.
    """

    def __init__(self, server):
        controller.Master.__init__(self, server)

    def run(self):
        try:
            return controller.Master.run(self)
        except KeyboardInterrupt:
            self.shutdown()

    def handle_request(self, msg):
        # we only check for the path, since we assume that parameters change a lot.
        # in the future, better inspection modules can be implemented 
        # based on the request parameters.
        current_path = urlparse.urlparse(msg.get_url()).path

        # check if we are in protect mode. if we are, we will kill the request
        # if the current path was not saved in the DB.
        if not args.learn_mode and current_path not in db:
            msg.reply(proxy.KILL)
            return

        # learn the current path if needed
        if args.learn_mode:
            if current_path not in db:
                db[current_path] = True

        msg.reply()

    def handle_response(self, msg):
        # always return the server response as-is. 
        msg.reply()        

if __name__ == '__main__':
    # Run in reverse proxy mode
    config = proxy.ProxyConfig(
        reverse_proxy=('http', args.server_host, args.server_port)
    )

    server = proxy.ProxyServer(config, args.incoming_port)
    defender = ServerDefender(server)
    defender.run()

