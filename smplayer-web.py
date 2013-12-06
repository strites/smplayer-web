#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       smplayer-web.py
#       
#       Copyright 2010 Keiji Costantini <keiji@strites.net>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import string
import os
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

port = 8080
index = "./home.html"

class MyHandler(BaseHTTPRequestHandler):
            
    def do_GET(self):
        command = self.path[1:]
        
        try:
                if self.path.endswith(".png"):
                    f = open("."+self.path)
                    #beware path
                    self.send_response(200)
                    self.send_header('Content-type',	'image/png')
                    self.end_headers()
                    self.wfile.write(f.read())
                    f.close()
                    return

                #check if it is an smplayer command and process it
                if command in ("play_or_pause", "stop", 
                        "forward1", "forward2", "forward3", 
                        "rewind1", "rewind2", "rewind3", 
                        "increase_volume", "decrease_volume",):
                    print("smplayer -send-action "+command)
                    os.system("smplayer -send-action "+command)
                print(command)
                f = open(index)
                self.send_response(200)
                self.send_header('Content-type',	'text/html')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

def main():
    os.putenv("DISPLAY", ":0")
    try:
        server = HTTPServer(('', port), MyHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()

