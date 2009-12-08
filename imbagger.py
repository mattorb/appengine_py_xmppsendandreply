import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import xmpp
from google.appengine.ext.webapp import template
import logging

class SendMessageHandler(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'im.html')
        self.response.out.write(template.render(path, locals()))
        
    def post(self):
        user_address = self.request.get('email')
        chat_message_sent = False

        if not xmpp.get_presence(user_address): #todo, not really a good way to decide to invite, just happens to work first time.
            status_code_from_invite = xmpp.send_invite(user_address)  # only need to do this once really.
        
        if xmpp.get_presence(user_address):
            msg = "What is your favorite color?"
            status_code_msg = xmpp.send_message(user_address, msg)
            chat_message_sent = (status_code_msg != xmpp.NO_ERROR)
        
            if not chat_message_sent:
                logging.error('Could not send message to %s.  status_code=%s' % (user_address, status_code_msg))
        else:
            logging.error('%s not online' % user_address)
        
        print 'Content-Type: text/plain'
        print ''
        print 'Sent.'
        

class InboundMessageHandler(webapp.RequestHandler):
    def post(self):
        message = xmpp.Message(self.request.POST)
        if message.body[0:5].lower() == 'red':
            message.reply("Me too!")
        else:
            message.reply("Lame!")

application = webapp.WSGIApplication(
                                     [('/', SendMessageHandler),
                                      ('/_ah/xmpp/message/chat/', InboundMessageHandler)], 
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
