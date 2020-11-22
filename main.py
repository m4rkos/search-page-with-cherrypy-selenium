import os, os.path, sys
import cv2
import random
import string
import datetime

import cherrypy

from tools import Tools

from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates'))

class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        tmpl = env.get_template('index.html')
        return tmpl.render(title='Search Data')

    @cherrypy.expose
    def info(self, id=1):
        tmpl = env.get_template('results.html')
        y = datetime.datetime.now().year

        t = Tools()
        r = t.select_search(id)

        if(r == None):
            raise cherrypy.HTTPRedirect('/', 301)
        
        images = []
        banner = []

        i = 0
        while i < r[7]:
            images.insert(i, f'data/{r[3]}/images/{r[6]}/{r[3]}_{i}.jpg')

            if i < 3:
                banner.insert(i, f'data/{r[3]}/images/{r[6]}/{r[3]}_{i}.jpg')                                

            i += 1
            pass        

        data = {
            'search':r[2],
            'id':r[1],
            'banner': banner,
            'result': images,
            'path': r[5],
            'name': r[3],
            'ct': r[8]
        }
        #print(data)

        return tmpl.render(
            title=f'Results about {r[2]}',
            salutation='About', 
            target=r[2],
            yaer=y,
            data=data
        )

    @cherrypy.expose
    def drag(self, length=0):
        return open('./templates/drag-and-drop.html')

    @cherrypy.expose
    def data(self, length=0):

        # images = []
        # folder = './public/data/fernandinha_fernandes/images/DuckDuckGo/'
        # for filename in os.listdir(folder):
        #     img = cv2.imread(os.path.join(folder,filename))
        #     if img is not None:
        #         images.append(img)

        # return images

        return open('./template/result-images.html')


@cherrypy.expose
class StringGeneratorWebService(object):

    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        return cherrypy.session['mystring']

    def POST(self, search_query):                
        
        t = Tools()        
        t.mainContent(search_query)
        ret = t.mainImages(search_query)
        
        cherrypy.session['mystring'] = ret
        return ret



    # def PUT(self, another_string):
    #     cherrypy.session['mystring'] = another_string

    # def DELETE(self):
    #     cherrypy.session.pop('mystring', None)


if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/generator': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    webapp = StringGenerator()
    webapp.generator = StringGeneratorWebService()
    cherrypy.quickstart(webapp, '/', conf)