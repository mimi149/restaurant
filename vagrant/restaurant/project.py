from flask import Flask, render_template, request, redirect, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants/')
def seeRestaurants():
	restaurants = session.query(Restaurant).all()
	return render_template('restaurant.html', restaurants = restaurants)

@app.route('/newRestaurant/', methods=['GET','POST'])
def newRestaurant():
	if request.method == 'POST':
		newRestaurant = Restaurant(name = request.form['name'])
		session.add(newRestaurant)
		session.commit()
		return redirect(url_for('seeRestaurants'))
	else:
		return render_template('newrestaurant.html')

@app.route('/seeMenu/<int:restaurantID>')
def seeMenu(restaurantID):
	restaurant = session.query(Restaurant).filter_by(id = restaurantID).one()
	menu = session.query(MenuItem).filter_by(restaurant_id = restaurantID).all()
	return render_template('menu.html',restaurant = restaurant, menu = menu)

	
@app.route('/restaurants/<int:restaurantID>/<int:menuID>/delete')
def deleteMenu(restaurantID, menuID):
	menu = session.query(MenuItem).filter_by(id = menuID).first()
	session.delete(menu)
	session.commit
	return redirect(url_for('seeMenu', restaurantID = restaurantID))

@app.route('/restaurants/<int:restaurantID>/<int:menuID>/edit', methods=['GET','POST'])
def editMenu(restaurantID, menuID):
	editedMenu = session.query(MenuItem).filter_by(id = menuID).one()

	if request.method == 'POST':
		editedMenu.name = request.form['menuName']
		editedMenu.price = request.form['price']
		editedMenu.description = request.form['description']
		editedMenu.course = request.form['course']
		session.add(editedMenu)
		session.commit()
		flash("Menu has been edited")
		return redirect(url_for('seeMenu', restaurantID = restaurantID))
	else:
		return render_template('editmenu.html', restaurantID = restaurantID, editedMenu = editedMenu)    
	
@app.route('/restaurants/<int:restaurantID>/new', methods=['GET','POST'])
def newMenu(restaurantID):
	if request.method == 'POST':
		newItem = MenuItem(name = request.form['menuName'],
							restaurant_id = restaurantID,
							price = request.form['price'],
							description = request.form['description'],
							course = request.form['course'])
		session.add(newItem)
		session.commit()
		flash("New menu has been added")
		return redirect(url_for('seeMenu', restaurantID = restaurantID))
	else:
		return render_template('newmenu.html', restaurantID = restaurantID)

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)

