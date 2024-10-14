from celery import shared_task
import time
from flask import Flask
app = Flask(__name__)
from flask_mail import Mail, Message
import csv
from io import StringIO

from datetime import timedelta,datetime

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = '21f3001238@ds.study.iitm.ac.in'
app.config['MAIL_PASSWORD'] = 'fxxh qnlp bfnd zuls' # app password created in google not the gmail password
app.config['MAIL_DEFAULT_SENDER'] = '21f3001238@ds.study.iitm.ac.in'

mail = Mail(app)



@shared_task(ignore_result=False)
def celery_beat():
    return "Hi! Veena!! Your Celery Beat is working fine."



@shared_task(ignore_result=False)
def schedule_daily_reminders():
    print(f"Executing schedule_daily_reminders")
    from app import User,Role
    user_role = Role.query.filter_by(name='user').first()
    users = User.query.filter_by(role_id=user_role.id).all()
    today = datetime.today().date()
    for user in users:
        if user.current_login_at is None or user.current_login_at.date() != today:
            daily_reminder.apply_async(args=[user.email, user.username], countdown=5)

@shared_task(ignore_result=False)
def schedule_return_reminders():
    print(f"Executing schedule_return_reminders")
    from app import db, User,Role,Section,Book,Request,Feedback,Buy
    from sqlalchemy import func
    start_date = datetime.now()
    end_date = start_date + timedelta(days=1)
    print(f"Checking for requests between: {start_date} and {end_date}")
    requests = Request.query.filter(Request.status == 'granted').all()
    
    valid_requests = []

    for request in requests:
        granted_on = request.granted_on
        days = request.days
        
        print(f"Request ID: {request.id}, Granted On: {granted_on}, Days: {days}")
        
        if granted_on is not None and days is not None:
            return_date = granted_on + timedelta(days=days)
            if start_date <= return_date <= end_date:
                user = User.query.get(request.user_id)
                book = Book.query.get(request.book_id)
                
                if user and book:
                    valid_requests.append({
                        'user': user,
                        'book': book,
                        'request': request,
                        'return_date': return_date
                    })
        else:
            print(f"Skipping request with ID {request.id} due to None values.")

    print(f"Requests Found: {len(valid_requests)}")
    
    for entry in valid_requests:
        user = entry['user']
        request = entry['request']
        return_date = entry['return_date']
        
        print(f"Request User: {user.username}")
        return_reminder.apply_async(
            args=[
                user.email,
                user.username,
                request.book_title,
                request.granted_on,
                return_date
            ],
            countdown=5
        )

@shared_task(ignore_result=False)
def schedule_monthly_report():
    print(f"Executing schedule_monthly_report")
    from app import db, User,Role,Section,Book,Request,Feedback,Buy
    user_role = Role.query.filter_by(name='user').first()
    librarian_role = Role.query.filter_by(name='librarian').first()
    librarian = User.query.filter_by(role_id=librarian_role.id).first()
    today = datetime.today()
    start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_month = (start_of_month + timedelta(days=31)).replace(day=1) - timedelta(seconds=1) 
    new_users_this_month = db.session.query(User).filter(
        User.registered_at >= start_of_month,
        User.registered_at <= end_of_month,
        User.role_id == user_role.id
    ).count()   
    sections_created_this_month = db.session.query(Section).filter(
        Section.date_created >= start_of_month,
        Section.date_created <= end_of_month
    ).count()
    requests_this_month = db.session.query(Request).filter(
        Request.requested_on >= start_of_month,
        Request.requested_on <= end_of_month
    ).count()
    buys_this_month = db.session.query(Buy).filter(
        Buy.bought_on >= start_of_month,
        Buy.bought_on <= end_of_month
    ).count()
    requests_with_days = Request.query.filter(
    Request.status.in_(['granted', 'returned', 'Access Revoked']),
    Request.granted_on >= start_of_month,
    Request.granted_on <= end_of_month
    ).all()
    request_details = [{'request_id': req.id,'username': req.username,'book_title': req.book_title,'granted_on':req.granted_on,'days': req.days,'end_date':req.granted_on+timedelta(days=req.days), 'days_remaining': (req.granted_on + timedelta(days=req.days) - datetime.now()).days} for req in requests_with_days]
    monthly_report.apply_async(args=[librarian.email,
                                     sections_created_this_month,
                                     requests_this_month,
                                     buys_this_month,
                                     new_users_this_month,
                                     request_details], countdown=5)

@shared_task(ignore_result=False)
def welcome_email(email,username):
    print(f"Sending Welcome Email to {email} for user {username}")
    with app.app_context():
        html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            .container {{
                width: 100%;
                padding: 20px;
                background-color: #fff;
                margin: 0 auto;
                max-width: 600px;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            h1 {{
                color: #333;
                font-size: 24px;
                text-align: center;
            }}
            p {{
                color: #555;
                font-size: 16px;
            }}
            .footer {{
                margin-top: 20px;
                font-size: 12px;
                color: #888;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="container">
        <p>Hello {username}!!</p>
            <h1>Greetings from <b>M.P.S.S. Knowledge Junction!!</b></h1>
            <p>We welcome you to our e-library!!</p>
            <p>We are so happy to have you as our new user.. Enjoy reading our books</p>
            <p><b>Happy Learning</b></p>
            <div class="footer">
                <p>&copy; 2024 M.P.S.S Knowledge Junction. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """

        msg = Message(
         'Welcome Email',
          recipients=[email],
          html=html_content
        )   

        mail.send(msg)
    return 'Welcome mail sent successfully!'

@shared_task(ignore_result=False)
def request_alert(email,username,book_title,days):
    print(f"Sending request alert to {email} from user {username}")
    with app.app_context():
        html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            .container {{
                width: 100%;
                padding: 20px;
                background-color: #fff;
                margin: 0 auto;
                max-width: 600px;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            h1 {{
                color: #333;
                font-size: 24px;
                text-align: center;
            }}
            p {{
                color: #555;
                font-size: 16px;
            }}
            .footer {{
                margin-top: 20px;
                font-size: 12px;
                color: #888;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>New Request Alert</h1>
            <p>Hello Librarian,</p>
            <p>A new request has been made now. Details are given below. You are requested to take action</p>
            <p>Username:<b>{username}</b></p>
            <p>Book Title:<b>{book_title}</b></p>
            <p>Days:<b>{days}</b></p>
            <div class="footer">
                <p>&copy; 2024 M.P.S.S Knowledge Junction. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """

        msg = Message(
         'Request Alert',
          recipients=[email],
          html=html_content
        )   

        mail.send(msg)
    return 'Request Alert mail sent successfully!'

@shared_task(ignore_result=False)
def daily_reminder(email,username):
    print(f"Sending daily reminder to {email} for user {username}")
    with app.app_context():
        html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            .container {{
                width: 100%;
                padding: 20px;
                background-color: #fff;
                margin: 0 auto;
                max-width: 600px;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            h1 {{
                color: #333;
                font-size: 24px;
                text-align: center;
            }}
            p {{
                color: #555;
                font-size: 16px;
            }}
            .footer {{
                margin-top: 20px;
                font-size: 12px;
                color: #888;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Daily Reminder</h1>
            <p>Hey {username}!! Seems like you haven't visited our website. Please do visit our website.</p>
            <div class="footer">
                <p>&copy; 2024 M.P.S.S Knowledge Junction. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """

        msg = Message(
         'Daily Reminder',
          recipients=[email],
          html=html_content
        )   

        mail.send(msg)
    return 'Daily Reminder mail sent successfully!'

@shared_task(ignore_result=False)
def monthly_report(email, sections_created_this_month, requests_this_month, buys_this_month,new_users_this_month,request_details):
    print(f"Setting up monthly report tasks")
    table_rows = ""
    for req in request_details:
        table_rows += f"""
        <tr>
            <td>{req['request_id']}</td>
            <td>{req['username']}</td>
            <td>{req['book_title']}</td>
            <td>{req['granted_on']}</td>
            <td>{req['days']}</td>
            <td>{req['end_date']}</td>
        </tr>
        """
    with app.app_context():
        html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            .container {{
                width: 100%;
                padding: 20px;
                background-color: #fff;
                margin: 0 auto;
                max-width: 600px;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            h1 {{
                color: #333;
                font-size: 24px;
                text-align: center;
            }}
            p {{
                color: #555;
                font-size: 16px;
            }}
            .footer {{
                margin-top: 20px;
                font-size: 12px;
                color: #888;
                text-align: center;
            }}
            table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            font-family: Arial, sans-serif;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px 15px;
            text-align: left;
        }}
        th {{
            background-color: #8B4513;
            color: white;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        tr:nth-child(odd) {{
            background-color: #ffffff;
        }}
        tr:hover {{
            background-color: #ddd;
        }}
        td {{
            color: #333;
            font-size: 14px;
        }}
        table thead {{
            background-color: #333;
            color: #ffffff;
            text-transform: uppercase;
        }}
        table tbody tr td:first-child {{
            font-weight: bold;
        }}
        table tbody tr td:last-child {{
            text-align: right;
        }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Monthly Report</h1>
            <p><b>Hey Librarian!!</b>!</p>
            <p>Greeting from <b>M.P.S.S. Knowledge Junction</b>!!</p>
            <p>Here is your Monthly Report</P>
            <p>New Users this month : {new_users_this_month}</p>
            <p>Sections created this month : {sections_created_this_month}</p>
            <p>Requests this month : {requests_this_month}</p>
            <p>Books bought this month : {buys_this_month}</p>
            <h2>Granted Book Details</h2>
                <table>
                    <tr>
                        <th>ID</th>
                        <th>Username</th>
                        <th>Book Title</th>
                        <th>Granted On</th>
                        <th>Days Requested</th>
                        <th>End Date</th>
                    </tr>
                    {table_rows}  <!-- Insert the dynamically generated rows here -->
                </table>
            <div class="footer">
                <p>&copy; 2024 M.P.S.S Knowledge Junction. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
       
        msg = Message(
          'Monthly Report',
            recipients=[email],
           html=html_content
        )

        mail.send(msg)
    return 'Monthly Report email sent successfully!'

@shared_task(ignore_result=False)
def return_reminder(email, username,book_title, granted_on, return_date):
    print(f"Setting up return remainder to {email}")
    with app.app_context():
        html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            .container {{
                width: 100%;
                padding: 20px;
                background-color: #fff;
                margin: 0 auto;
                max-width: 600px;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            h1 {{
                color: #333;
                font-size: 24px;
                text-align: center;
            }}
            p {{
                color: #555;
                font-size: 16px;
            }}
            .footer {{
                margin-top: 20px;
                font-size: 12px;
                color: #888;
                text-align: center;
            }}
            
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Return Remainder</h1>
            <p><b>Hey {username}!!</b>!</p>
            <p>Greeting from <b>M.P.S.S. Knowledge Junction</b>!!</p>
            <p>Seems like you have a return date approaching for the book you requested for.</P>
            <p>Book Title : {book_title}</p>
            <p>Granted On : {granted_on}</p>
            <p>Return Date : {return_date}</p>
            <p>You are requested to read your book {book_title} fast and return it before the access being revoked.</p>
            <div class="footer">
                <p>&copy; 2024 M.P.S.S Knowledge Junction. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
       
        msg = Message(
          'Return Remainder',
            recipients=[email],
           html=html_content
        )

        mail.send(msg)
    return 'Return Remainder email sent successfully!'

@shared_task(ignore_result=False)
def export_csv(email):
    from app import db, User,Role,Section,Book,Request,Feedback,Buy
    books = Book.query.all()
    requests = Request.query.all()
    buys = Buy.query.all()
    books_csv = StringIO()
    requests_csv = StringIO()
    buys_csv = StringIO()
    books_writer = csv.writer(books_csv)
    books_writer.writerow(['ID', 'Title', 'Description', 'Author', 'Price', 'Section ID'])
    for book in books:
        books_writer.writerow([book.id, book.book_title, book.book_description, book.author, book.price, book.section_id])
    requests_writer = csv.writer(requests_csv)
    requests_writer.writerow(['ID', 'User ID', 'Username', 'Book ID', 'Book Title', 'Days', 'Requested On', 'Granted On', 'Returned On', 'Status'])
    for request in requests:
        requests_writer.writerow([request.id, request.user_id, request.username, request.book_id, request.book_title, request.days, request.requested_on, request.granted_on, request.returned_on, request.status])
    buys_writer = csv.writer(buys_csv)
    buys_writer.writerow(['ID','username', 'Book Title', 'Price', 'Bought On'])
    for buy in buys:
        buys_writer.writerow([buy.id,buy.username, buy.book_title, buy.price, buy.bought_on])
    books_csv.seek(0)
    requests_csv.seek(0)
    buys_csv.seek(0)
    with app.app_context():
        msg = Message(
            subject="Export CSV - Details of Books, Requests and Buys",
            recipients=[email]
        )
        msg.body = "Hey Librarian!! Here are your requested exported CSV files."

        msg.attach("books_export.csv", "text/csv", books_csv.getvalue())
        msg.attach("requests_export.csv", "text/csv", requests_csv.getvalue())
        msg.attach("buys_export.csv", "text/csv", buys_csv.getvalue())

        mail.send(msg)

    return 'CSV export and email sent successfully!'