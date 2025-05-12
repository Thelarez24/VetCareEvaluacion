from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.payments_model import PaymentsModel

payments_bp = Blueprint('payments', __name__)

@payments_bp.route('/payment')
def payment_form():
    return render_template('payment.html')

@payments_bp.route('/payment/add', methods=['POST'])
def payment_add():
    email = request.form.get('email')
    cardholder_name = request.form.get('cardholder_name')
    amount = request.form.get('amount')
    currency = request.form.get('currency', 'USD')
    service = request.form.get('service')

    # Validación detallada
    errors = []
    if not email:
        errors.append('El correo electrónico es requerido')
    elif '@' not in email or '.' not in email:
        errors.append('El correo electrónico no es válido')

    if not cardholder_name:
        errors.append('El nombre del titular es requerido')
    elif len(cardholder_name) < 3:
        errors.append('El nombre del titular es demasiado corto')

    if not amount:
        errors.append('El monto es requerido')
    else:
        try:
            amount = float(amount)
            if amount <= 0:
                errors.append('El monto debe ser mayor a 0')
        except ValueError:
            errors.append('El monto debe ser un número válido')

    if not service:
        errors.append('El servicio es requerido')

    if errors:
        for error in errors:
            flash(error, 'error')
        return redirect(url_for('payments.payment_form'))

    try:
        payment = PaymentsModel.create(email, cardholder_name, amount, currency, service)
        if payment:
            flash('Pago procesado correctamente', 'success')
        else:
            flash('Error al procesar el pago', 'error')
    except Exception as e:
        flash('Error al procesar el pago: ' + str(e), 'error')
    return redirect(url_for('payments.payment_form'))

@payments_bp.route('/admin/payments')
def payment_list():
    payments = PaymentsModel.get_all()
    return render_template('admin/payments.html', payments=payments)
