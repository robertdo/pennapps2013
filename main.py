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
from google.appengine.ext import ndb

import jinja2
import os
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
  extensions=['jinja2.ext.autoescape'])

### Database models ###
def list_key():
  return ndb.Key('Item', 'default_list')

class Item(ndb.Model):
  created = ndb.DateTimeProperty(auto_now_add=True)
  title = ndb.StringProperty()
  description = ndb.StringProperty()


class MainHandler(webapp2.RequestHandler):
  def get(self):
    items = Item.query(ancestor=list_key()).fetch(10)

    template_values = {
      'items': items
    }

    template = JINJA_ENVIRONMENT.get_template('index.html')
    self.response.write(template.render(template_values))

class AddHandler(webapp2.RequestHandler):
  def post(self):
    title = self.request.get('title')
    description = self.request.get('description')
    newItem = Item(
      parent=list_key(),
      title=title,
      description=description)
    newItem.put()
    self.redirect('/')


class DeleteHandler(webapp2.RequestHandler):
  def get(self):
    urlsafe_key = self.request.get('key')
    item_key = ndb.Key(urlsafe=urlsafe_key)
    item_key.delete()
    self.redirect('/')

app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/add', AddHandler),
  ('/delete', DeleteHandler)
], debug=True)
