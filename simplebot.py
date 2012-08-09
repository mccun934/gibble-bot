
import sys
import socket
import string 
from megahal import *


# HOST="irc.eversible.com"
HOST="irc-2.devel.redhat.com"
PORT=6667
NICK="gankle"
IDENT="gankle"
REALNAME="gankle"
readbuffer=""

s=socket.socket( )
s.connect((HOST, PORT))
s.send("NICK %s\r\n" % NICK)
s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
CHAN="#mmccune"

megahal = MegaHAL()
megahal.train('/home/mmccune/megahal-0.2/zomg-filtered3.out')

print "Done loading megahal, joining channel"
# KEY = "crossroads"
# s.send("JOIN :%s %s\r\n" % (CHAN, KEY))
s.send("JOIN :%s\r\n" % CHAN)

while 1:
    readbuffer=readbuffer+s.recv(1024)
    temp=string.split(readbuffer, "\n")
    readbuffer=temp.pop( )

    for line in temp:
        lineparts=string.rstrip(line)
        lineparts=string.split(lineparts)
        
        if(lineparts[0]=="PING"):
            s.send("PONG %s\r\n" % lineparts[1])            
        
        # If it is in a channel or priv message and address to the bot
        if lineparts[1] == ('PRIVMSG') and line.find(NICK) >= 0:
          body = string.strip(line.split(':')[-1])
          # s.send("PRIVMSG %s :%s\r\n" % (CHAN, body))
          megahal.learn(body)
          s.send("PRIVMSG %s :%s\r\n" % (CHAN, megahal.get_reply(body)))
          megahal.sync()
        
