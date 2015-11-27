#!/usr/bin/env python
#Username = DrunkandSuch
#Password = ps2weirdo24
#AppName = mychatbot
#Redirect URL = http://www.ryangaudy.pythonanywhere.com
#Client ID = b69qxr73yp8w2qzndu0uf33kfcg4ej7
#Client Secret = k52i0txi4yznjvgs8wi4a40gb8xfaij
#Oauth = oauth:3kf2n0z24rg5ghttypstftudjt2huk

# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

# system imports
import time, sys
import threading
from datetime import date, datetime, timedelta

NICKNAME = "DrunkandSuch"
PASSWORD = "oauth:3kf2n0z24rg5ghttypstftudjt2huk"

class MessageLogger:
    """
    An independent logger class (because separation of application
    and protocol logic is a good thing).
    """
    def __init__(self, file):
        self.file = file
        
    def log(self, message):
        """Write a message to the file."""
        timestamp = time.strftime("[%H:%M:%S]", time.localtime(time.time()))
        self.file.write('%s %s\n' % (timestamp, message))
        self.file.flush()

    def close(self):
        self.file.close()


class LogBot(irc.IRCClient):
    """A logging IRC bot."""
    
    nickname = NICKNAME
    password = PASSWORD
    
    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        self.logger = MessageLogger(open(self.factory.filename, "a"))
        self.logger.log("[connected at %s]" % 
                        time.asctime(time.localtime(time.time())))
        if not self.factory.silent_console:
            print "Connected!"

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        self.logger.log("[disconnected at %s]" % 
                        time.asctime(time.localtime(time.time())))
        self.logger.close()
        if not self.factory.silent_console:
            print "Disconnected!"

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        self.join(self.factory.channel)
        if not self.factory.silent_console:
            print "Signed on to the server!"

    def joined(self, channel):
        """This will get called when the bot joins the channel."""
        self.logger.log("[I have joined %s]" % channel)

    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message."""
        user = user.split('!', 1)[0]
        self.logger.log("<%s> %s" % (user, msg))
        if not self.factory.silent_console:
            print (user, msg)

    def action(self, user, channel, msg):
        """This will get called when the bot sees someone do an action."""
        user = user.split('!', 1)[0]
        self.logger.log("* %s %s" % (user, msg))


class LogBotFactory(protocol.ClientFactory):
    """A factory for LogBots.

    A new protocol instance will be created each time we connect to the server.
    """

    def __init__(self, channel, filename, silent_console):
        self.channel = channel
        self.filename = filename
        self.silent_console = silent_console

    def buildProtocol(self, addr):
        p = LogBot()
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        if not self.factory.silent_console:
            print "connection failed:", reason
        reactor.stop()


#if __name__ == '__main__':


#     # initialize logging
#     log.startLogging(sys.stdout)

#     # create factory protocol and application
#     bot_instance = LogBotFactory("#clgdoublelift", "myfile.txt")

#     # connect factory to this host and port
#     reactor.connectTCP("irc.twitch.tv", 6667, bot_instance)

#     # run bot
#     reactor.run()
  
class ChatCollector:

    def __init__(self, channel, output_filename, seconds_runtime, silent_console=False):

        if channel.startswith("#"):
            self.channel = channel
        else:
            self.channel = "#" + channel
        self.outfile = output_filename
        self.timer = int(seconds_runtime)
        self.silent_console = silent_console

        if not self.silent_console:
            log.startLogging(sys.stdout)
        else:
            pass
        bot_instance = LogBotFactory(self.channel, self.outfile, self.silent_console)
        reactor.connectTCP("irc.twitch.tv", 6667, bot_instance)

    def start(self):
        ircsuicide = threading.Timer(self.timer, reactor.stop)
        ircsuicide.start()
        reactor.run()

if __name__ == '__main__':

    mybot = ChatCollector("c9sneaky", "firsttry.txt", 30, silent_console=True)
    mybot.start()