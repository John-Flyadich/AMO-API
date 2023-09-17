from flask import Flask, request, jsonify
from api import *


app = Flask(__name__)

# Главная страница
@app.route('/')
def main_page():
    return '<h1>Перейдите на api/v1/get_data и сделайте get запрос <br> Например: http://127.0.0.1:5000/api/v1/get_data?phone=79996264726&mail=pochta@yahoo.com&name=Valera</h1>'

# Страница get запроса
@app.route('/api/v1/get_data', methods=['GET'])
def response_page():
    take_tokens()
    check_time()

    phone = request.args.get('phone')
    mail = request.args.get('mail')
    name = request.args.get('name')

    if phone is None or mail is None or name is None:
        return '<h1>Cделайте get запрос <br> Например: http://127.0.0.1:5000/get_data?phone=79996264726&mail=pochta@yahoo.com&name=Valera</h1>'

    contact_id = None
    phone_contact = get_contacts_by_phone(phone=phone)
    mail_contact = get_contacts_by_mail(mail=mail)

    if phone_contact:
        contact_id = phone_contact

    elif mail_contact:
        contact_id = mail_contact

    if contact_id:
        update_contact(mail=mail, phone=phone, name=name, contact_id=contact_id)
        create_lead(contact_id=contact_id)
        return jsonify({'status': 'contact found', 'response': 'data updated'})
    else:
        contact_id = create_contact(name=name,phone=phone,mail=mail)
        create_lead(contact_id=contact_id)
        return jsonify({'status': 'contact not found', 'response': 'contact created'})
    
if __name__ == '__main__':
    app.run(debug=True)
