
import credentials
import pymongo 


def db_connect():
	conn = pymongo.MongoClient(credentials.MONGODB_CONNECTION)
	db = conn.get_default_database()
	return db

def save_user(user):
	db = db_connect()
	res = db.people.insert(user)
	return res

def list_all_users():
	db = db_connect()
	return db.people.find()	 

def update_user(linkedin_url):
	db = db_connect()
	query = {'linkedin': linkedin_url}
	res = songs.update(query, {'$set': {'artist': 'Mariah Carey ft. Boyz II Men'}})    
	return res

def drop_people_collection():
	db = db_connect()
	db.drop_collection('songs')
    
    
