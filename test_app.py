from unittest import TestCase
from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserTestCase(TestCase):
	"""Tests for users"""
	def setUp(self):
		User.query.delete()
		user = User(first_name='Alan', last_name='Alda', image_url='http://www.pixelstalk.net/wp-content/uploads/2016/12/Color-Splash-Wallpaper-Full-HD.jpg')
		db.session.add(user)
		db.session.commit()
		
		self.user_id = user.id	
	
	def test_user_page(self):
		with app.test_client() as client:
			resp = client.get('/')
			html = resp.get_data(as_text=True)

			self.assertEqual(resp.status_code, 200)
			self.assertIn('Alan', html)

	def test_show_user(self):
		with app.test_client() as client:
			resp = client.get(f'/users/{self.user_id}')
			html = resp.get_data(as_text=True)

			self.assertEqual(resp.status_code, 200)
			self.assertIn('Alda', html)
			self.assertIn('http://www.pixelstalk.net/wp-content/uploads/2016/12/Color-Splash-Wallpaper-Full-HD.jpg', html)
	
	def test_new_page(self):
		with app.test_client() as client:
			resp = client.post('/users/new', 
					   data={'first_name': 'Joel', 'last_name': 'Burton', 'image_url': 'www.image.com'})	
			user = User.query.filter_by(last_name = 'Burton').first()

			self.assertEqual(user.first_name, 'Joel')
			self.assertEqual(user.image_url,'www.image.com')

	def test_edit_user(self):
		with app.test_client() as client:
			resp = client.post(f'/users/{self.user_id}/edit', 
					   data={'first_name': 'Jane', 'last_name': 'Smith', 'image_url': 'www.photos.com'})
			
			user = User.query.get(self.user_id)
			self.assertEqual(user.first_name, 'Jane')
			self.assertEqual(user.last_name, 'Smith')
			self.assertEqual(user.image_url,'www.photos.com')	
	
	def test_delete_user(self):
		with app.test_client() as client:
			resp = client.post(f'/users/{self.user_id}/delete')
			user = User.query.get(self.user_id)

			self.assertFalse(user)			
	
	

    


