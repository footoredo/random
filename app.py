import web
import re
import requests
import random
import string
from web import form

render = web.template.render('templates')

urls = (
  '/', 'index',
  '/gen', 'gen',
  '/list/(\w{8})', 'handler'
)

app = web.application(urls, globals())
db = web.database(dbn='postgres', user="postgres", pw="postgres", db="random_lists")

list_form = form.Form(
  form.Textarea("list", description="URL list")
)

class index:
	def GET(self):
		f = list_form()
		return render.index(f)

class gen:
	def POST(self):
		r = web.input()
		url_list = r['list'].split('\n')
		for url in url_list:
			if not re.match(r'^https?:/{2}\w.+$', url):
				return render.invalid(url)
		url_list.sort()
		urls = '\n'.join(url_list)
		id = string.join(random.sample('zyxwvutsrqponmlkjihgfedcbaABCDEFGHIJKLMNOPQRSTUVWXYZ',8)).replace(' ','')
		q = db.insert('list', id=id, list=urls)

		return "Your id is %s" % (id)

class handler:
	def GET(self, id):
		urls = db.query('select list from list where id=$id', vars=dict(id=id)).list()[0]['list']
		url_list = urls.split('\n')
		choice = random.randint(0,len(url_list)-1)
		url = "".join(url_list[choice].split())
		web.HTTPError('302', {'Location': url})

if __name__ == "__main__":
	app.run()