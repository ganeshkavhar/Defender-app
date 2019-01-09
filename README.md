ServerDefender
--------------

ServerDefender is a simple HTTP reverse proxy that protects websites from hackers trying to access illegal paths.

To use, you will need to run ServerDefender in "learning mode" for a while:

    ./defender.py --learn_mode=True

After a while, you can switch to defend mode. This mode will block all HTTP requests to your server that are
trying to access a path that was not previously accessed during the learning phase.

To specify which ports to run on, use the following parameters:

    ./defender.py --incoming_port=80 --server_port=8080

If you want to play around with the defender, you may run a simple HTTP server using the following command:

    python -m SimpleHTTPServer

This will run a server on port 8000 that will serve files from the running directory.
