import os.path
import secrets
from PIL import Image
from flask_mail import Message
from flask import url_for, current_app
from flask_blog import mail


def save_picture(form_picture):
    secret_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = f"{secret_hex}{f_ext}"
    picture_path = os.path.join(current_app.root_path, "static/profile_pics", picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    message = Message(
        "Password Reset Request",
        sender="kiran.kumar@hashedin.com",
        recipients=[user.email],
    )
    message.body = f"""To reset your password, visit the following link:
    {url_for('users.reset_token', token=token, _external=True)}


    If you did not make this request then simply ignore this email and no changes will be made.
    """
    mail.send(message)
