from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Restaurant, Base, MenuItem
 
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:         
			if self.path.endswith("/restaurants"):
                
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "<a href='/restaurants/new'>Add a new restaurant</a>"
				output += "</br>"
				output += "</br>"

				output += "<h1> Restaurant: </h1>"

				items = session.query(Restaurant).all()
				for item in items:
					output += item.name
					output += "</br>"
					output += "<a href='#'>Edit</a>"
					output += "</br>"
					output += "<a href='#'>Delete</a>"
					output += "</br>"
					output += "</br>"
					
				output += "</body></html>" 

				self.wfile.write(output)

				for item in items:
					print item.name

				return

 			if self.path.endswith("/restaurants/new"):
				
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "<h1>Add a new restaurant</h1>"
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
				output += "<h2>Input the name of a new Restaurant: </h2>"
				output += "<input name='newRestaurantName' type='text' placeholder = 'New Restaurant Name'>"
				output += "<input type='submit' value='Create'> </form>"
				output += "</body></html>"
				self.wfile.write(output)
				return


		except IOError:
			self.send_error(404, 'File Not Found: %s' % self.path)


	def do_POST(self):
		try:
			if self.path.endswith("/restaurants/new"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields=cgi.parse_multipart(self.rfile, pdict)
					newName = fields.get('newRestaurantName')

				newRestaurant = Restaurant(name = newName[0])
				session.add(newRestaurant)
				session.commit()

				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', '/restaurants')
				self.end_headers()
				return

		except:
			pass


def main():
	try:
		port = 8080
		server = HTTPServer(('', port), webServerHandler)
		print "Web Server running on port %s"  % port
		server.serve_forever()
	except KeyboardInterrupt:
		print " ^C entered, stopping web server...."
		server.socket.close()

if __name__ == '__main__':
	main()
