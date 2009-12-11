import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import xmpp
from google.appengine.ext.webapp import template
from google.appengine.ext import db

class IMPermission(db.Model):
    address = db.StringProperty(required=False)

class SendMessageHandler(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'im.html')
        self.response.out.write(template.render(path, locals()))
        
    def post(self):
        to = self.request.get('to')
        chat_message_sent = False


        print 'Content-Type: text/plain'
        print ''

        if not IMPermission.gql('WHERE address = :1', to).get():
            xmpp.send_invite(to)
            print 'requesting permission.... accept it, then reload this page to send message.'
            IMPermission(address=to).put()
        else:
            if xmpp.get_presence(to):
                status_code_msg = xmpp.send_message(to, 'What is your favorite color?')
                chat_message_sent = (status_code_msg == xmpp.NO_ERROR)

                if chat_message_sent == False:
                    print "Couldn't send it"
                else:
                    print 'Sent.'
            else:
                print '%s not online.  Remember - this has to be running on gae servers and that user must be online for this to work.' % to
                
        

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
