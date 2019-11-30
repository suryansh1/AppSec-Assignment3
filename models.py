from databases import db


class User(db.Model):
	user_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	# password = db.Column(db.String(20))
	pswd_hash = db.Column(db.String(128), nullable=False)
	# two_fa = db.Column(db.String(10), nullable=False)
	two_fa_hash = db.Column(db.String(128), nullable=False)

	def __init__(self, username, pswd_hash, two_fa_hash):
		self.username = username
		self.pswd_hash = pswd_hash
		self.two_fa_hash = two_fa_hash


	def __repr__(self):
		return '<User  >'.format( self.username)