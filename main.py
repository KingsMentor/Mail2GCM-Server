#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from google.appengine.api import mail

import CommonOperations
import test
from bs4 import BeautifulSoup


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')
        soup = BeautifulSoup("<html><head></head><body>" + test.test + "</body></html>", "html.parser")
        townList = soup.find_all('div')
        self.response.write(townList[0])


import logging
import webapp2
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler


class LogSenderHandler(InboundMailHandler):
    def receive(self, mail_message):
        logging.info("Received a message from: " + mail_message.sender)
        logging.info("Received a message to: " + mail_message.to)
        receiver = CommonOperations.getReceiver(mail_message.to)
        senderEmail = mail_message.sender
        logging.info(receiver)
        html_bodies = mail_message.bodies('text/html')
        message = ""
        for content_type, body in html_bodies:
            decoded_html = body.decode()
            soup = BeautifulSoup("<html><head></head><body>" + decoded_html + "</body></html>", "html.parser")
            incoming = soup.find_all('div')
            message += incoming[0].getText()

        logging.info("send " + receiver + " this message " + message)
        devices = CommonOperations.getDeviceByID(receiver)
        recipients = list()
        if devices is not None:
            for device in devices:
                recipients.append(device.pushKey)
            CommonOperations.sendPushToRecipient(message, senderEmail, recipients)
            # allBodies = "";
            # for body in plaintext_bodies:
            #     logging.info(body[1].decode())
            #     logging.info("<br>")

            # html_bodies = mail_message.bodies('text/html')


class PhoneIncomingReceiver(webapp2.RequestHandler):
    def post(self):
        deviceId = self.request.get("device_id")
        email = str(self.request.get("email"))
        recipient = email if len(email.strip()) > 0 else "nosakharebelvi@gmail.com"
        pushKey = self.request.get("push_key")
        message = self.request.get("message")
        CommonOperations.cacheDevice(deviceId, pushKey)
        sender = deviceId + "@email2gcm.appspotmail.com"
        sendMail(sender, recipient, message)
        self.response.write("200")


def sendMail(sender, recipient, body):
    message = mail.EmailMessage(sender=sender, subject="Email2GCM")
    message.to = recipient
    message.body = str(body)
    message.send()


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/contact', PhoneIncomingReceiver),
    LogSenderHandler.mapping()
], debug=True)
