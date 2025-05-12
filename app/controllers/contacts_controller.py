from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.contacts_model import ContactsModel

contacts_bp = Blueprint('contacts', __name__)

@contacts_bp.route('/contact')
def contact_form():
    return render_template('contact.html')

@contacts_bp.route('/contact/add', methods=['POST'])
def contact_add():
    email = request.form.get('email')
    name = request.form.get('name')
    comment = request.form.get('comment')
    ip_address = request.remote_addr

    # Validación básica
    if not all([email, name, comment]):
        flash('Todos los campos son requeridos', 'error')
        return redirect(url_for('contacts.contact_form'))

    try:
        contact = ContactsModel.create(email, name, comment, ip_address)
        if contact:
            flash('Mensaje enviado correctamente', 'success')
        else:
            flash('Error al enviar el mensaje', 'error')
    except Exception as e:
        flash('Error al enviar el mensaje: ' + str(e), 'error')
    return redirect(url_for('contacts.contact_form'))

@contacts_bp.route('/admin/contacts')
def contact_list():
    contacts = ContactsModel.get_all()
    return render_template('admin/contacts.html', contacts=contacts)
