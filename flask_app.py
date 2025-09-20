from flask import Flask, request, jsonify, render_template, send_from_directory
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

GMAIL_USER = 'Vonbot.001@gmail.com'
GMAIL_PASSWORD = 'bdnl uflk cdxm afzt'
GMAIL_SEND = 'arjunrenvon@gmail.com'

@app.route('/')
def index():
    return render_template('Index.html')

@app.route('/style/<path:filename>')
def style(filename):
    return send_from_directory('style', filename)

@app.route('/script/<path:filename>')
def script(filename):
    return send_from_directory('script', filename)

@app.route('/Portfolio/<path:filename>')
def Portfolio(filename):
    return send_from_directory('Portfolio', filename)

@app.route('/Blogs/<path:filename>')
def Blogs(filename):
    return send_from_directory('Blogs', filename)

@app.route('/Team/<path:filename>')
def Team(filename):
    return send_from_directory('Team', filename)

@app.route('/send-inquiry', methods=['POST'])
def send_inquiry():
    try:
        data = request.get_json()
        full_name = data.get('fullName')
        email = data.get('email')
        description = data.get('description')

        if not (full_name and email and description):
            return jsonify({'message': 'All fields are required'}), 400

        now = datetime.now()
        formatted_time = now.strftime("%I:%M%p")
        formatted_date = now.strftime("%m/%d/%Y")

        # Get client IP
        x_forwarded_for = request.headers.get('X-Forwarded-For', '')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0].strip()
        else:
            ip_address = request.remote_addr

        admin_html = render_template(
            'Send.html',
            full_name=full_name,
            email=email,
            description=description,
            Time=formatted_time,
            Date=formatted_date,
            local_ip=ip_address,
        )

        admin_msg = MIMEMultipart('alternative')
        admin_msg['Subject'] = "New Inquiry Submission"
        admin_msg['From'] = GMAIL_USER
        admin_msg['To'] = GMAIL_SEND
        admin_msg.attach(MIMEText(admin_html, 'html'))

        user_html = render_template('Inquiry.html', full_name=full_name)

        user_msg = MIMEMultipart('alternative')
        user_msg['Subject'] = "Thank You for Your Inquiry"
        user_msg['From'] = GMAIL_USER
        user_msg['To'] = email
        user_msg.attach(MIMEText(user_html, 'html'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_PASSWORD)
            smtp.sendmail(GMAIL_USER, GMAIL_SEND, admin_msg.as_string())
            smtp.sendmail(GMAIL_USER, email, user_msg.as_string())

        return jsonify({'message': 'Inquiry sent successfully!'}), 200

    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)