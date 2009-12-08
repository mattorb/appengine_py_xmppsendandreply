from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import xmpp
import logging

class SendMessage(webapp.RequestHandler):
    def get(self):
        user_address = 'putyourgmailaddresshere@gmail.com'
        chat_message_sent = False

        if not xmpp.get_presence(user_address):
            status_code_from_invite = xmpp.send_invite(user_address)  # only need to do this once really.
        
        if xmpp.get_presence(user_address):
            msg = "Hey, something was created for you!"
            status_code_msg = xmpp.send_message(user_address, msg)
            chat_message_sent = (status_code_msg != xmpp.NO_ERROR)
        
            if not chat_message_sent:
                logging.error('Could not send message to %s.  status_code=%s' % (user_address, status_code_msg))
        else:
            logging.error('%s not online' % user_address)

application = webapp.WSGIApplication(
                                     [('/', SendMessage)], 
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
