import os, os.path, sys
import random
import string
import datetime

import cherrypy

from tools import Tools

from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates'))

template_ext = 'jinja'

class StringGenerator(object):
    @cherrypy.expose
    def index(self, report='y'):
        tmpl = env.get_template(f'index.{template_ext}')
        msg = None

        t = Tools()
        r = t.select_search(0)

        res = 0

        if(r != None):
            res = len(r)

        if(report != 'y'):
            msg = 'Not found'
        return tmpl.render(title='Search Data', msg=msg, res=res)

    @cherrypy.expose
    def result(self, id=0):     
        y = datetime.datetime.now()
        t = Tools()
        if(int(id) > 0):
            tmpl = env.get_template(f'results.{template_ext}')
            
            r = t.select_search(id)

            if(r == None):
                raise cherrypy.HTTPRedirect('/', 301)
            
            images = []
            banner = []

            i = 0
            while i < r[8]:
                images.insert(i, f'data/{r[3]}/images/{r[7]}/{r[3]}_{i}.jpg')

                if i < 6:
                    banner.insert(i, f'data/{r[3]}/images/{r[7]}/{r[3]}_{i}.jpg')                                

                i += 1
                pass        

            data = {
                'search':r[2],
                'id':r[1],
                'banner': banner,
                'result': images,
                'path': r[6],
                'name': r[3],
                'ct': r[9],
                'resume': r[4]
            }

            return tmpl.render(
                title=f'Results about {r[2]}',
                salutation='About', 
                target=r[2],
                yaer=y.year,
                data=data
            )

        else:
            tmpl = env.get_template(f'results-all.{template_ext}')
            r = t.select_search(id)

            if(r == None):
                raise cherrypy.HTTPRedirect('/?report=not', 301)

            data = []

            i = 0
            while i < len(r):

                data.insert(i, {
                    'id': r[i][0],
                    'name': r[i][2],
                    'img': f'data/{r[i][3]}/images/{r[i][7]}/{r[i][3]}_0.jpg',
                    'ct': r[i][9],
                    'resume': r[i][4]
                })

                i += 1
                pass     

            return tmpl.render(
                title=f'Results about all searches',
                salutation='Gallery of', 
                target='All results searched',
                yaer=y.year,
                now=y,
                data=data
            )

    @cherrypy.expose
    def drag(self, length=0):
        return open(f'./templates/drag-and-drop.{template_ext}')


@cherrypy.expose
class StringGeneratorWebService(object):

    @cherrypy.tools.accept(media='text/plain')
    def GET(self, type = ''):
        if(type != ''):
            t = Tools()
            r = t.select_search(0)
            res = 0
            if(r != None):
                res = len(r)

            return str(res)
            
        else:
            return cherrypy.session['mystring']

    def POST(self, type, search_query):                
        
        if(type == 'browser'):
            t = Tools()        
            #t.mainContent(search_query)
            ret = t.mainImages(search_query)
            
            cherrypy.session['mystring'] = ret
            return ret

        else:
            return None


    # def PUT(self, another_string):
    #     cherrypy.session['mystring'] = another_string

    def DELETE(self, key=0):
        if(key != '' and int(key) > 0):
            t = Tools()
            r = t.delete_search(key)
            res = 0
            if(r != None):
                res = r

            return str(res)

        else:
            #cherrypy.session.pop('mystring', None)
            return None        


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