from email.message import EmailMessage
from pydantic import EmailStr


def create_registration_confirmation_template(email_to: EmailStr, code: str):
    msg = EmailMessage()
    msg["Subject"] = "Подтверждение регистрации inPDF"
    msg["From"] = "support@inpdf.ru"
    msg["To"] = email_to
    msg.set_content(
        f"""
        <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Подтверждение регистрации</title>
</head>
<body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
    <div style="background-color: white; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); padding: 30px; max-width: 500px; width: 100%; text-align: center; margin: 20px auto;">
        <div style="color: #2c3e50; font-size: 24px; margin-bottom: 20px; font-weight: bold;">inPDF</div>
        <h2 style="color: #2c3e50; line-height: 1.6;">Добро пожаловать на наш сервис!</h2>
        <p style="color: #7f8c8d; margin-bottom: 15px;">{email_to}</p>
        <div style="background-color: #f0f0f0; padding: 15px; border-radius: 8px; font-size: 24px; letter-spacing: 5px; margin: 20px 0; color: #333;">{code}</div>
        <p style="color: #2c3e50; line-height: 1.6;">
            Для завершения регистрации введите код подтверждения на странице регистрации.<br>
            Код действителен в течение 15 минут.
        </p>
    </div>
</body>
</html>
        """,
        subtype="html",
    )
    return msg
