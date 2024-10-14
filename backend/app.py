#<----------------------imports------------------------------------->
from flask import Flask, request, jsonify,make_response, session
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from functools import wraps
from flask_cors import CORS
from datetime import timedelta,datetime
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, roles_required
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import os
from flask import send_from_directory
from flask_caching import Cache
from flask_mail import Mail, Message
from worker import celery_init_app
from tasks import  celery_beat, daily_reminder,welcome_email,request_alert, monthly_report, export_csv, schedule_daily_reminders, schedule_monthly_report,schedule_return_reminders
from celery.result import AsyncResult
from sqlalchemy.ext.hybrid import hybrid_property
import logging


db = SQLAlchemy()

#<--------------------------------Models----------------------------->

roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }


class User(db.Model):
    __tablename__ = 'user' 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255))
    requests = db.Column(db.Integer)
    buys = db.Column(db.Integer)
    registered_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    subscription = db.Column(db.Boolean(), default = False)
    subscribed_at = db.Column(db.DateTime())
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', backref=db.backref('users', lazy=True))
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role.to_dict() if self.role else None,
            'requests': self.requests,
            'last_login_at': self.last_login_at,
            'current_login_at': self.current_login_at,
            'subscription': self.subscription,
            'registered_at': self.registered_at,
            'subscribed_at': self.subscribed_at,
        }

class Book(db.Model):
    __tablename__ = 'book' 
    id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String)
    book_description = db.Column(db.String)
    author = db.Column(db.String)
    price = db.Column(db.Float)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))
    file_path = db.Column(db.String(255), nullable=True)
    image_path = db.Column(db.String(255), nullable=True)

class Section(db.Model):
    __tablename__ = 'section' 
    id = db.Column(db.Integer, primary_key=True)
    sec_title = db.Column(db.String)
    sec_description = db.Column(db.String)
    date_created = db.Column(db.DateTime())
    book = db.relationship('Book', backref='section', lazy=True)

class Request(db.Model):
    __tablename__ = 'request' 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    username = db.Column(db.String, unique=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    book_title = db.Column(db.String)
    file_path = db.Column(db.String(255), nullable=True)
    days = db.Column(db.Integer)
    requested_on = db.Column(db.DateTime())
    granted_on = db.Column(db.DateTime())
    rejected_on = db.Column(db.DateTime())
    returned_on = db.Column(db.DateTime())
    status = db.Column(db.String)
    
class Buy(db.Model):
    __tablename__ = 'buy' 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    username = db.Column(db.String, unique=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    book_title = db.Column(db.String)
    price = db.Column(db.Float)
    file_path = db.Column(db.String(255), nullable=True)
    bought_on = db.Column(db.DateTime())

class Feedback(db.Model):
    __tablename__ = 'feedback' 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    username = db.Column(db.String)
    received_on = db.Column(db.DateTime())
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    feedback = db.Column(db.String)
    

    
app = Flask(__name__)


UPLOAD_FOLDER = 'uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

celery_app = celery_init_app(app)

CORS(app, origins='*')

#<-----------------------------Configurations--------------------------->

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mad2db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['SECRET_KEY'] = 'secretkey'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_PASSWORD_SALT'] = 'somesalt'
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'

datastore = SQLAlchemyUserDatastore(db, User, Role)


app.config['JWT_SECRET_KEY'] = 'my-secret-key'
jwt = JWTManager(app)

app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_HOST'] = 'localhost' 
app.config['CACHE_REDIS_PORT'] = 6380   
app.config['CACHE_REDIS_DB'] = 0        
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0' 


cache = Cache(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = '21f3001238@ds.study.iitm.ac.in'
app.config['MAIL_PASSWORD'] = 'fxxh qnlp bfnd zuls'
app.config['MAIL_DEFAULT_SENDER'] = '21f300128@ds.study.iitm.ac.in'

mail = Mail(app)

def roles_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            identity = get_jwt_identity()
            if not isinstance(identity, dict):
                return jsonify({"message": "Invalid identity format"}), 401
            
            
            if identity.get('role') not in roles:
                return jsonify({"message": "Access forbidden: insufficient role"}), 403
            
            response = fn(*args, **kwargs)
    
            
            return response
        return wrapper
    return decorator

@app.before_request
def before_request_func():
    if request.method == 'OPTIONS':
        return build_cors_preflight_response()

def build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
    return response


    
from celery.schedules import crontab

@app.route('/cache')
@cache.cached(timeout=30)
def index():
    return "<h1>Welcome to M.P.S.S. Knowledge Junction's Cached page!! </h1>" + str(datetime.now())

#<------------------------------------Backend Jobs----------------------------------->

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    #Executes every 20 seconds just to clarify the working of celery-beat
    sender.add_periodic_task(20.0, celery_beat.s(), name='Working Status every 20 seconds', expires=100)
    #Executes Every Month 25 at 08.00 p.m IST
    sender.add_periodic_task(
        crontab(minute=30, hour=14,day_of_month=25),
        schedule_monthly_report.s(), 
        name='Sending monthly report to librarian',
    )
    #Executes Everyday at 08.01 p.m IST
    sender.add_periodic_task(
        crontab(minute=31, hour=14),
        schedule_daily_reminders.s(),
        name='Schedule daily reminders to non-visited users',
    )
    #Executes Everyday at 08.02 p.m IST
    sender.add_periodic_task(
        crontab(minute=32, hour=14),
        schedule_return_reminders.s(),
        name='Schedule return reminders to requested users',
    )

@app.route('/export_csv', methods=['POST'])
def trigger_exportCSV():
    user_role = Role.query.filter_by(name='librarian').first()
    user = User.query.filter_by(role_id=user_role.id).first()
    export_csv.apply_async(args=[user.email])
    return jsonify({"success": True}), 200

db.init_app(app)

#<--------------------Common Routes--------------------->

@app.route('/register', methods=['POST'])
def register():
    data =  request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if not username:
        return jsonify({"message":"Username not provided"}), 400
    if not email:
        return jsonify({"message":"Email not provided"}), 400
    if not password:
        return jsonify({"message":"Password not provided"}), 400
    password = generate_password_hash(password)
    role_name = data.get('role')  

  
    role = Role.query.filter_by(name=role_name).first() 
    registered_at=datetime.now()
    requests = 0
    buys=0
    new_user = User(username=username,email=email,password=password,role=role,requests=requests,buys=buys,registered_at=registered_at)
    
    db.session.add(new_user)
    db.session.commit()
    welcome_email.delay(email,username)
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    user = User.query.filter_by(email=email).first()
    if not email:
        return jsonify({"message":"Email not provided"}), 400
    if not data.get("password"):
        return jsonify({"message":"Password not provided"}), 400   
    if not user:
        return jsonify({"message":"User not found"}), 404
    if check_password_hash(user.password, data.get("password")): 
        user.last_login_at=user.current_login_at
        user.current_login_at=datetime.now()
        db.session.commit()

        access_token = create_access_token(identity={"role": user.role.name}, expires_delta = timedelta(days=1))
        user_info = {
            'user_id' : user.id,
            'username' : user.username,
            'role' :user.role.to_dict(),
            'email' : user.email,
            'requests': user.requests,
            'buys': user.buys,
            'subscription':user.subscription,
        }
        return jsonify({'access_token':access_token, 'user': user_info}), 200   
    else:
        return jsonify({"message":"Wrong Password"}), 400
    

@app.route('/home', methods=['GET'])
@jwt_required()
def get_sections():
    recent_books = Book.query.order_by(Book.id.desc()).limit(5).all()
    sections = Section.query.all()
    if not sections:
        return jsonify({"message": "No sections found"}), 404
    recent_books_list = [{'id': book.id, 'book_title': book.book_title, 'book_description': book.book_description, 'author': book.author,'price': book.price,'image_path': book.image_path, 'file_path': book.file_path, 'section_id': book.section_id} for book in recent_books]
    section_list = [{'id': section.id, 'sec_title': section.sec_title, 'sec_description': section.sec_description, 'date_created': section.date_created} for section in sections]
    return jsonify({'sections': section_list, 'recent_books': recent_books_list})

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({'message':'Logged out successfully'})
    unset_jwt_cookies(response)
    return response,200

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

#<------------------------Librarian Functionalities-------------------->

@app.route('/createsection', methods=['POST'])
@jwt_required()
@roles_required('librarian')
def createsection():
    data =  request.get_json()
    sec_title = data.get('sec_title')
    sec_description = data.get('sec_description')
    if not sec_title:
        return jsonify({"message":"Title not provided"}), 400
    if not sec_description:
        return jsonify({"message":"Description not provided"}), 400
    new_section = Section(sec_title=sec_title, sec_description=sec_description, date_created=datetime.now())
    
    db.session.add(new_section)
    db.session.commit()

    return jsonify({'message': 'Section created successfully'}), 201


@app.route('/requests', methods=['GET'])
@jwt_required()
@roles_required('librarian')
def get_requests():
    requests = Request.query.all()
    if not requests:
        return jsonify({"message": "No request found"}), 404
    for request in requests:
        granted_on = request.granted_on
        returned_on = request.returned_on
        if granted_on is not None:
            if returned_on is None:
                day = request.days
                days = timedelta(days=day)
                current_date = datetime.now()
                end_date = granted_on + days
    
                accessrevoke = (current_date >= end_date)
                if accessrevoke:
                    request.status = 'Access Revoked'
                    db.session.commit()
    request_list = [{'id': request.id, 'user_id': request.user_id,'username': request.username, 'book_id': request.book_id, 'book_title': request.book_title, 'days': request.days, 'status': request.status, 'requested_on': request.requested_on, 'granted_on': request.granted_on,'rejected_on': request.rejected_on,'returned_on': request.returned_on} for request in requests]
    return jsonify({'requests': request_list})

@app.route('/buybooks', methods=['GET'])
@jwt_required()
@roles_required('librarian')
def get_buybooks():
    buybooks = Buy.query.all()
    if not buybooks:
        return jsonify({"message": "No book bought yet"}), 404
    buybook_list = [{'id': buybook.id, 'user_id': buybook.user_id,'username': buybook.username, 'book_id': buybook.book_id, 'book_title': buybook.book_title,'price': buybook.price, 'bought_on': buybook.bought_on} for buybook in buybooks]
    return jsonify({'buybooks': buybook_list})

@app.route("/deletesection/<int:section_id>/", methods=['DELETE'])
@jwt_required()
@roles_required('librarian')
def deletesection(section_id):
    books = db.session.query(Book).filter(Book.section_id == section_id).all()
    section = db.session.query(Section).filter(Section.id == section_id).first()
    for i in books:
        db.session.delete(i)
    db.session.delete(section)
    db.session.commit()
    return jsonify({"message":"Section Deleted!!"})

@app.route('/searchl', methods=['GET', 'POST'])
@jwt_required()
@roles_required('librarian')
def searchl():
    if request.method == 'POST':
        data = request.get_json()
        field = data.get('field')
        search = data.get('search')
        if field == 'section':
            sections = Section.query.filter(Section.sec_title.like('%' + search + '%')).all()
            section_list = [{'id': section.id, 'sec_title': section.sec_title, 'sec_description': section.sec_description, 'date_created': section.date_created} for section in sections]
            return jsonify({'field': field, 'search': search, 'results': section_list})
        elif field == 'book':
            books = Book.query.filter(Book.book_title.like('%' + search + '%')).all()
            book_list = []
            for book in books:
                book_data = {
            'id': book.id,
            'book_title': book.book_title,
            'book_description': book.book_description,
            'author': book.author,
            'price': book.price,
            'image_path': book.image_path,
            'file_path': book.file_path,
        }
                book_list.append(book_data)
            return jsonify({'field': field, 'search': search, 'results': book_list})
        elif field == 'author':
            books = Book.query.filter(Book.author.like('%' + search + '%')).all()
            book_list = []
            for book in books:
                book_data = {
            'id': book.id,
            'book_title': book.book_title,
            'book_description': book.book_description,
            'author': book.author,
            'price': book.price,
            'image_path': book.image_path,
            'file_path': book.file_path,
        }
                book_list.append(book_data)
            return jsonify({'field': field, 'search': search, 'results': book_list})
    elif request.method == 'GET':
        search_results = session.get('search_results')
        if search_results:
            return jsonify(search_results)
        return jsonify({'error': 'No search results found'}), 404

@app.route('/section/<int:section_id>/book', methods=['GET'])
@jwt_required()
@roles_required('librarian')
@cache.cached(timeout=10)
def viewbooks(section_id):
    section = Section.query.filter_by(id=section_id).first()    
    books = db.session.query(Book).filter(Book.section_id == section_id).all()
    section_title = section.sec_title
    if not books:
        book_list = []
        return jsonify({'books': book_list,'section_title': section_title}), 200
    book_list = [{'id': book.id, 'book_title': book.book_title, 'book_description': book.book_description,'price': book.price, 'author': book.author,'image_path': book.image_path, 'file_path':book.file_path} for book in books]
    return jsonify({'books': book_list,'section_title': section_title})

@app.route('/allbooks', methods=['GET'])
@jwt_required()
@roles_required('librarian')
def allbooks():
    books = Book.query.all()
    if not books:
        book_list = []
        return jsonify({'books': book_list}), 200
    book_list = [{'id': book.id, 'book_title': book.book_title, 'book_description': book.book_description,'price': book.price, 'author': book.author,'image_path': book.image_path, 'file_path':book.file_path} for book in books]
    return jsonify({'books': book_list})

@app.route('/section/<int:section_id>/createbook', methods=['POST'])
@jwt_required()
@roles_required('librarian')
def createbook(section_id):
    if 'bookpdf' not in request.files or 'bookimage' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    book_file = request.files['bookpdf']
    image_file = request.files['bookimage']

    if book_file.filename == '' or image_file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if book_file and image_file:
        book_filename = secure_filename(book_file.filename)
        image_filename = secure_filename(image_file.filename)
        book_file_path = os.path.join(app.config['UPLOAD_FOLDER'], book_filename)
        image_file_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
        book_file.save(book_file_path)
        image_file.save(image_file_path)
        
        data = request.form
        book_title = data.get('book_title')
        book_description = data.get('book_description')
        author = data.get('author')
        price = data.get('price')
        new_book = Book(
            book_title=book_title, 
            book_description=book_description,
            section_id=section_id,
            author=author,
            price=price,
            file_path=book_file_path,
            image_path=image_file_path
        )
        
        db.session.add(new_book)
        db.session.commit()

        return jsonify({'message': 'Book created successfully'}), 201
    
@app.route("/deletebook/<int:book_id>/", methods=['GET','DELETE'])
@jwt_required()
@roles_required('librarian')
def deletebook(book_id):
    book = db.session.query(Book).filter(Book.id == book_id).first()
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message":"Book Deleted Successfully!!"})

@app.route('/section/edit/<int:section_id>', methods=['PUT'])
@jwt_required()
@roles_required('librarian')
def editsection(section_id):
    section = Section.query.filter_by(id=section_id).first()
    sec_title = request.form.get('sec_title')
    sec_description = request.form.get('sec_description')
    section.sec_title = sec_title
    section.sec_description = sec_description

    db.session.commit()
    return jsonify({'message': 'Section updated successfully'}), 200

@app.route('/book/edit/<int:book_id>', methods=['PUT'])
@jwt_required()
@roles_required('librarian')
def editbook(book_id):
    book = Book.query.filter_by(id=book_id).first()
    if 'bookpdf' in request.files:
        book_file = request.files['bookpdf']
        if book_file:
            book_filename = secure_filename(book_file.filename)
            book_file_path = os.path.join(app.config['UPLOAD_FOLDER'], book_filename)
            book_file.save(book_file_path)
            book.file_path = book_file_path
    if 'bookimage' in request.files:
        image_file = request.files['bookimage']
        if image_file:
            image_filename = secure_filename(image_file.filename)
            image_file_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            image_file.save(image_file_path)
            book.image_path = image_file_path

    book_title = request.form.get('book_title')
    book_description = request.form.get('book_description')
    author = request.form.get('author')
    price = request.form.get('price')
    if price:
        book.price = price
    book.book_title = book_title
    book.book_description = book_description
    book.author = author

    db.session.commit()
    return jsonify({'message': 'Book updated successfully'}), 200

@app.route('/viewdetailslib/<int:book_id>/', methods=['GET'])
@jwt_required()
@roles_required('librarian')
def viewdetailslib(book_id):
    book = Book.query.filter_by(id=book_id).first()
    feedbacks = Feedback.query.filter_by(book_id=book_id).all()
    feedback_list = []
    for feedback in feedbacks:
        
        feedback_data = {
            'id': feedback.id,
            'user_id': feedback.user_id,
            'username': feedback.username,
            'received_on': feedback.received_on,
            'section_id': feedback.section_id,
            'book_id': feedback.book_id,
            'feedback': feedback.feedback,
        }
        feedback_list.append(feedback_data)

    details = {
                'id': book.id,
                'book_title': book.book_title,
                'book_description': book.book_description,
                'author': book.author,
                'price': book.price,
                'section_id':book.section_id,
                'image_path': book.image_path,
                'file_path': book.file_path,
            }
    return jsonify({'details': details,'feedbacks': feedback_list})

@app.route('/grantrequest/<int:request_id>', methods=['PUT'])
@jwt_required()
@roles_required('librarian')
def grantrequest(request_id):
    request = Request.query.filter_by(id=request_id).first()
    request.status = 'granted'
    request.granted_on = datetime.now()
    db.session.commit()
    return jsonify({'message': 'Request granted successfully'}), 200

@app.route('/rejectrequest/<int:request_id>', methods=['PUT'])
@jwt_required()
@roles_required('librarian')
def rejectrequest(request_id):
    request = Request.query.filter_by(id=request_id).first()
    request.status = 'rejected'
    request.rejected_on=datetime.now()
    db.session.commit()
    return jsonify({'message': 'Request rejected successfully'}), 200

@app.route('/revokerequest/<int:request_id>', methods=['PUT'])
@jwt_required()
@roles_required('librarian')
def revokerequest(request_id):
    request = Request.query.filter_by(id=request_id).first()
    request.status = 'Access Revoked'
    db.session.commit()
    return jsonify({'message': 'Request revoked successfully'}), 200

@app.route('/accessrevoke/<int:myrequest_id>/', methods=['GET', 'PUT'])
@jwt_required()
@roles_required('librarian')
def accessrevoke(myrequest_id):
    myrequest = Request.query.filter_by(id=myrequest_id).first()
    
    granted_on = myrequest.granted_on
    if granted_on is None:
        return jsonify({'accessrevoke': False})  

    day = myrequest.days
    days = timedelta(days=day)
    current_date = datetime.now()
    end_date = granted_on + days
    
    accessrevoke = (current_date >= end_date)
    if accessrevoke:
        myrequest.status = 'Access Revoked'
        db.session.commit()
    return jsonify({'accessrevoke': accessrevoke})

@app.route('/getlibstats/', methods=['GET'])
@jwt_required()
@roles_required('librarian')
def get_libstats():
    today = datetime.now()
    user_role = Role.query.filter_by(name='user').first()
    total_users = User.query.filter_by(role_id=user_role.id).count()
    time_period = today - timedelta(days=7)
    active_users = User.query.filter(User.current_login_at >= time_period, User.role_id == user_role.id).count()
    popular_requested_books = db.session.query(
        Request.book_title,
        db.func.count(Request.id).label('request_count')
    ).group_by(Request.book_title).order_by(db.func.count(Request.id).desc()).limit(2).all()
    popular_bought_books = db.session.query(
        Buy.book_title,
        db.func.count(Buy.id).label('buy_count')
    ).group_by(Buy.book_title).order_by(db.func.count(Buy.id).desc()).limit(2).all()
    popular_requested_books_list = [{'book_title': book.book_title, 'request_count': book.request_count} for book in popular_requested_books]
    popular_bought_books_list = [{'book_title': book.book_title, 'buy_count': book.buy_count} for book in popular_bought_books]    
    total_requests = Request.query.count()
    total_buys = Buy.query.count()
    buys = Buy.query.all()
    subscribes = User.query.filter_by(subscription=True).count()
    revenue_by_books = 0
    for buy in buys:
        revenue_by_books = revenue_by_books+buy.price
    total_revenue = revenue_by_books + subscribes*2000
    pending_requests = Request.query.filter_by(status='pending').count()
    return jsonify({
        'total_users': total_users,
        'active_users': active_users,
        'popular_requested_books': popular_requested_books_list,
        'popular_bought_books': popular_bought_books_list,
        'total_requests':total_requests,
        'total_buys':total_buys,
        'total_revenue':total_revenue,
        'subscribes':subscribes,
        'revenue_by_books':revenue_by_books,
        'pending_requests':pending_requests,

    })

#<--------------------------User Functionalities---------------------------->

@app.route('/myrequests/', methods=['GET'])
@jwt_required()
@roles_required('user')
def get_myrequests():
    user_id = request.args.get('user_id')
    if user_id is None:
        return jsonify({"message": "user_id parameter is required"}), 400

    myrequests = db.session.query(Request).filter(Request.user_id == user_id).all()
    if not myrequests:
        return jsonify({"message": "No requests found for this user"}), 404
    for myrequest in myrequests:
        granted_on = myrequest.granted_on
        returned_on = myrequest.returned_on
        if granted_on is not None:
            if returned_on is None:
                day = myrequest.days
                days = timedelta(days=day)
                current_date = datetime.now()
                end_date = granted_on + days
    
                accessrevoke = (current_date >= end_date)
                if accessrevoke:
                    myrequest.status = 'Access Revoked'
                    db.session.commit()
    myrequest_list = [{'id': myrequest.id, 'book_id': myrequest.book_id, 'book_title': myrequest.book_title, 'days': myrequest.days, 'status': myrequest.status, 'requested_on': myrequest.requested_on, 'granted_on': myrequest.granted_on,'rejected_on': myrequest.rejected_on,'returned_on': myrequest.returned_on} for myrequest in myrequests]
    return jsonify({'myrequests': myrequest_list})

@app.route('/mybooks/', methods=['GET'])
@jwt_required()
@roles_required('user')
def get_mybooks():
    user_id = request.args.get('user_id')
    if user_id is None:
        return jsonify({"message": "user_id parameter is required"}), 400

    mybooks = db.session.query(Buy).filter(Buy.user_id == user_id).all()
    if not mybooks:
        return jsonify({"message": "No books bought by this user"}), 404
    mybook_list = [{'id': mybook.id,
                     'book_id': mybook.book_id,
                       'book_title': mybook.book_title,
                       'price': mybook.price,
                         'bought_on': mybook.bought_on} for mybook in mybooks]
    return jsonify({'mybooks': mybook_list})

    
@app.route('/search', methods=['GET', 'POST'])
@jwt_required()
@roles_required('user')
def search():
    if request.method == 'POST':
        data = request.get_json()
        field = data.get('field')
        search = data.get('search')
        user_id = data.get('user_id')
        if field == 'section':
            sections = Section.query.filter(Section.sec_title.like('%' + search + '%')).all()
            section_list = [{'id': section.id, 'sec_title': section.sec_title, 'sec_description': section.sec_description, 'date_created': section.date_created} for section in sections]
            return jsonify({'field': field, 'search': search, 'results': section_list})
        elif field == 'book':
            books = Book.query.filter(Book.book_title.like('%' + search + '%')).all()
            book_list = []
            for book in books:
                request_status = db.session.query(Request).filter_by(user_id=user_id, book_id=book.id).first()
                if request_status:
                    status = request_status.status
                else:
                    status = 'not_requested'

                book_data = {
            'id': book.id,
            'book_title': book.book_title,
            'book_description': book.book_description,
            'author': book.author,
            'price': book.price,
            'image_path': book.image_path,
            'file_path': book.file_path,
            'request_status': status
        }
                book_list.append(book_data)
            return jsonify({'field': field, 'search': search, 'results': book_list})
        elif field == 'author':
            books = Book.query.filter(Book.author.like('%' + search + '%')).all()
            book_list = []
            for book in books:
                request_status = db.session.query(Request).filter_by(user_id=user_id, book_id=book.id).first()
                if request_status:
                    status = request_status.status
                else:
                    status = 'not_requested'

                book_data = {
            'id': book.id,
            'book_title': book.book_title,
            'book_description': book.book_description,
            'author': book.author,
            'price': book.price,
            'image_path': book.image_path,
            'file_path': book.file_path,
            'request_status': status
        }
                book_list.append(book_data)
            return jsonify({'field': field, 'search': search, 'results': book_list})
    elif request.method == 'GET':

        search_results = session.get('search_results')
        if search_results:
            return jsonify(search_results)
        return jsonify({'error': 'No search results found'}), 404


@app.route('/section/<int:section_id>/books', methods=['GET'])
@jwt_required()
@roles_required('user')
@cache.cached(timeout=10)
def userviewbooks(section_id):
    section = Section.query.filter_by(id=section_id).first()
    books = db.session.query(Book).filter(Book.section_id == section_id).all()
    section_title = section.sec_title
    if not books:
        book_list = []
        return jsonify({'books': book_list, 'section_title': section_title}), 200

    book_list = []
    for book in books:
        
        book_data = {
            'id': book.id,
            'book_title': book.book_title,
            'book_description': book.book_description,
            'author': book.author,
            'price': book.price,
            'image_path': book.image_path,
            'file_path': book.file_path,
        }
        book_list.append(book_data)
    
    return jsonify({'books': book_list, 'section_title': section_title}), 200

    
@app.route('/book/<int:book_id>', methods=['GET'])
@cache.cached(timeout=10)
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify({
        'id': book.id,
        'book_title': book.book_title,
        'book_description': book.book_description,
        'author': book.author,
        'price': book.price,
        'image_path': book.image_path,
        'file_path': book.file_path
    })


@app.route("/withdrawrequest/<int:request_id>/", methods=['PUT','DELETE'])
@jwt_required()
@roles_required('user')
def withdrawrequest(request_id):
    user_id = request.args.get('user_id')
    user = db.session.query(User).filter(User.id == user_id).first()
    request_to_be_withdrawn = db.session.query(Request).filter(Request.id == request_id).first()
    user.requests = user.requests-1
    db.session.delete(request_to_be_withdrawn)
    db.session.commit()
    user_info = {
            'user_id' : user.id,
            'username' : user.username,
            'role' :user.role.to_dict(),
            'email' : user.email,
            'requests': user.requests,
            'buys': user.buys,
            'subscription':user.subscription,
        }
    return jsonify({"message":"Request Withdrawn Successfully!!",'user':user_info})

@app.route('/viewdetails/<int:book_id>/', methods=['GET'])
@jwt_required()
@roles_required('user')
def viewdetails(book_id):
    user_id = request.args.get('user_id')
    book = Book.query.filter_by(id=book_id).first()
    feedbacks = Feedback.query.filter_by(book_id=book_id).all()
    feedback_list = []
    for feedback in feedbacks:
        
        feedback_data = {
            'id': feedback.id,
            'user_id': feedback.user_id,
            'username': feedback.username,
            'received_on': feedback.received_on,
            'section_id': feedback.section_id,
            'book_id': feedback.book_id,
            'feedback': feedback.feedback,
        }
        feedback_list.append(feedback_data)
    request_status = db.session.query(Request).filter_by(user_id=user_id, book_id=book.id).first()
    if request_status:
        status = request_status.status
    else:
        status = 'not_requested'
    buy_status = db.session.query(Buy).filter_by(user_id=user_id, book_id=book.id).first()
    if buy_status:
        status = 'bought'
    details = {
                'id': book.id,
                'book_title': book.book_title,
                'book_description': book.book_description,
                'author': book.author,
                'price': book.price,
                'section_id':book.section_id,
                'image_path': book.image_path,
                'file_path': book.file_path,
                'request_status': status
            }
    return jsonify({'details': details,'feedbacks': feedback_list})


@app.route('/requestbook/<int:book_id>/', methods=['GET'])
@jwt_required()
@roles_required('user')
def requestbook(book_id):
    book = Book.query.filter_by(id=book_id).first()
    user_id = request.args.get('user_id')
    user = User.query.filter_by(id=user_id).first()
    requests = user.requests
    if requests<5 or user.subscription:
        requestedbook = {'id': book.id, 'book_title': book.book_title,'price': book.price, 'book_description': book.book_description, 'author': book.author,'section_id':book.section_id,'image_path': book.image_path,'file_path': book.file_path}
        return jsonify({'requestedbook': requestedbook})
    else:
        return jsonify({'message':'You cannot request more than 5 books!! Subscribe for unlimited requests'}), 404
    
@app.route('/buybook/<int:book_id>/', methods=['GET'])
@jwt_required()
@roles_required('user')
def buybook(book_id):
    book = Book.query.filter_by(id=book_id).first()
    buybookdetails = {'id': book.id, 'book_title': book.book_title, 'book_description': book.book_description, 'author': book.author,'price': book.price,'section_id':book.section_id,'image_path': book.image_path,'file_path': book.file_path}
    return jsonify({'buybookdetails': buybookdetails})


@app.route('/requestbook/', methods=['POST'])
@jwt_required()
@roles_required('user')
def request_book_with_days():
    data = request.get_json()
    book_id = data.get('book_id')
    book_title = data.get('book_title')
    days = data.get('days')
    user_id = data.get('user_id')
    username = data.get('username')
    requested_on = datetime.now()
    status = 'pending'
    if user_id is None:
        return jsonify({'error': 'User ID not provided'}), 400
    new_request = Request(user_id = user_id,username = username, book_id = book_id,book_title = book_title, days = days, status = status, requested_on = requested_on)
    user = User.query.filter_by(id=user_id).first()
    user.requests = user.requests + 1
    user_info = {
            'user_id' : user.id,
            'username' : user.username,
            'role' :user.role.to_dict(),
            'email' : user.email,
            'requests': user.requests,
            'buys': user.buys,
            'subscription':user.subscription,
        }
    db.session.add(new_request)
    db.session.commit()
    librarian_role = Role.query.filter_by(name='librarian').first()
    librarian = User.query.filter_by(role_id=librarian_role.id).first()
    request_alert.delay(librarian.email,username,book_title,days)
    return jsonify({'message': 'Request placed successfully', 'user': user_info}), 201 

@app.route('/buybook/', methods=['POST'])
@jwt_required()
@roles_required('user')
def buybookpost():
    data = request.get_json()
    book_id = data.get('book_id')
    book_title = data.get('book_title')
    user_id = data.get('user_id')
    username = data.get('username')
    price = data.get('price')
    bought_on = datetime.now()
    if user_id is None:
        return jsonify({'error': 'User ID not provided'}), 400
    new_buy = Buy(user_id = user_id,username = username, book_id = book_id,book_title = book_title,price=price, bought_on = bought_on)
    user = User.query.filter_by(id=user_id).first()
    user.buys = user.buys + 1
    user_info = {
            'user_id' : user.id,
            'username' : user.username,
            'role' :user.role.to_dict(),
            'email' : user.email,
            'requests': user.requests,
            'buys': user.buys,
            'subscription':user.subscription,
        }
    db.session.add(new_buy)
    db.session.commit()
    return jsonify({'message': 'Book bought successfully', 'user': user_info}), 201   


@app.route('/returnbook/<int:request_id>', methods=['PUT'])
@jwt_required()
@roles_required('user')
def returnbook(request_id):
    request = Request.query.filter_by(id=request_id).first()
    request.status = 'returned'
    request.returned_on=datetime.now()
    db.session.commit()
    return jsonify({'message': 'Book returned successfully'}), 200


@app.route('/sendfeedback/', methods=['POST'])
@jwt_required()
@roles_required('user')
def sendfeedback():
    data =  request.get_json()
    feedback = data.get('feedback')
    book_id = data.get('book_id')
    book = Book.query.filter_by(id=book_id).first()
    section_id = book.section_id
    user_id = data.get('user_id')
    user = User.query.filter_by(id=user_id).first()
    username = user.username
    new_feedback = Feedback(user_id=user_id,username=username,received_on=datetime.now(),section_id=section_id,book_id=book_id,feedback=feedback)
    
    db.session.add(new_feedback)
    db.session.commit()

    return jsonify({'message': 'Feedback sent successfully'}), 201

@app.route('/getuserstats/<int:user_id>', methods=['GET'])
@jwt_required()
@roles_required('user')
def get_userstats(user_id):
    user = User.query.filter_by(id=user_id).first()
    last_login_at = user.last_login_at
    current_login_at = user.current_login_at
    requests = Request.query.filter_by(user_id=user_id).count()
    if user.subscription:
        requests_remaining = "unlimited"
    else:
        requests_remaining = 5-requests
    total_read_from_requests = Request.query.filter(Request.user_id == user_id, Request.status.in_(['granted', 'returned', 'Access Revoked'])).count()    
    buys = Buy.query.filter_by(user_id=user_id).count()
    total_read = total_read_from_requests+buys
    requests_with_days = Request.query.filter_by(user_id=user_id, status='granted').all()
    request_details = [{'book_title': req.book_title,'days': req.days, 'days_remaining': (req.granted_on + timedelta(days=req.days) - datetime.now()).days} for req in requests_with_days]
    pending = Request.query.filter_by(user_id=user_id, status='pending').count()
    
    return jsonify({
        'last_login_at': last_login_at,
        'current_login_at': current_login_at,
        'requests': requests,
        'total_read': total_read,
        'requests_remaining':requests_remaining,
        'request_details': request_details,
        'pending':pending,
        'buys':buys,
    })

@app.route('/subscribe/<int:user_id>', methods=['PUT'])
@jwt_required()
@roles_required('user')
def subscribe(user_id):
    user = User.query.filter_by(id=user_id).first()
    user.subscription = True
    user.subscribed_at = datetime.now()
    user_info = {
            'user_id' : user.id,
            'username' : user.username,
            'role' :user.role.to_dict(),
            'email' : user.email,
            'requests': user.requests,
            'buys': user.buys,
            'subscription':user.subscription,
        }
    db.session.commit()
    return jsonify({'message': 'Subscribed successfully','user':user_info}), 200


with app.app_context():
    db.create_all()

#<-----------------------Creating Roles and Librarian-------------------------->

    datastore.find_or_create_role(name="librarian")
    datastore.find_or_create_role(name="user")
    db.session.commit()
    if not User.query.filter_by(username="librarian").first():
        librarian = User(
                username="librarian",
                email="21f3001238@ds.study.iitm.ac.in",
                password=generate_password_hash('librarian'),
                role = Role.query.filter_by(name='librarian').first(),
                requests = 0,
                buys = 0,
                registered_at = datetime.now(),
            )
        db.session.add(librarian)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug = True)

#<-----------------------Completed------------------------>