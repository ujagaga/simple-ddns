# simple-ddns
This is a python based, one file, single user, dynamic DNS server.
I wrote it for my own home projects, so I can access my home router via internet.
The point of DDNS is that your routers external IP sometimes changes. This server provides a mechanisam to access the current IP address via link you set yourself.
This server can be hosted on an external service or your own machine.

What you have to know to use it is the server secret key, which is a password like, at least 8 (recomended, but not required) characters long, alphanumeric string. Eg. qwerty123.

To add or update a sub-domain, make a get request to something like:
https://mysubdomain.thisddnsservice.com/?secret=qwerty123

to remove a sub-domain, make a get request to:
https://mysubdomain.thisddnsservice.com/?secret=qwerty123&op=remove

