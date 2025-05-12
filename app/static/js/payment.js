document.addEventListener('DOMContentLoaded', function() {
    const serviceSelect = document.getElementById('service');
    const amountInput = document.getElementById('amount');
    const cardNumberInput = document.getElementById('card_number');
    const cvvInput = document.getElementById('cvv');
    const form = document.querySelector('.payment-form');
    const alerts = document.querySelectorAll('.alert');

    // Actualizar monto cuando cambia el servicio
    serviceSelect.addEventListener('change', function() {
        const selectedOption = this.options[this.selectedIndex];
        const price = selectedOption.getAttribute('data-price');
        amountInput.value = price || '';
    });

    // Formatear número de tarjeta
    cardNumberInput.addEventListener('input', function(e) {
        let value = this.value.replace(/\D/g, '');
        if (value.length > 16) value = value.slice(0, 16);
        
        // Agregar espacios cada 4 dígitos
        const parts = [];
        for (let i = 0; i < value.length; i += 4) {
            parts.push(value.slice(i, i + 4));
        }
        this.value = parts.join(' ');
    });

    // Validar CVV
    cvvInput.addEventListener('input', function(e) {
        let value = this.value.replace(/\D/g, '');
        if (value.length > 4) value = value.slice(0, 4);
        this.value = value;
    });

    // Cerrar alertas
    alerts.forEach(alert => {
        const closeButton = alert.querySelector('.close-alert');
        if (closeButton) {
            closeButton.addEventListener('click', () => {
                alert.remove();
            });
        }
    });

    // Validar formulario antes de enviar
    form.addEventListener('submit', function(e) {
        const email = document.getElementById('email').value;
        const cardholderName = document.getElementById('cardholder_name').value;
        const cardNumber = cardNumberInput.value.replace(/\s/g, '');
        const cvv = cvvInput.value;
        const amount = amountInput.value;
        const service = serviceSelect.value;

        let isValid = true;
        const errors = [];

        // Validar email
        if (!email || !email.includes('@') || !email.includes('.')) {
            errors.push('Email inválido');
            isValid = false;
        }

        // Validar nombre del titular
        if (!cardholderName || cardholderName.length < 3) {
            errors.push('Nombre del titular inválido');
            isValid = false;
        }

        // Validar número de tarjeta
        if (!cardNumber || cardNumber.length !== 16 || !/^\d+$/.test(cardNumber)) {
            errors.push('Número de tarjeta inválido');
            isValid = false;
        }

        // Validar CVV
        if (!cvv || cvv.length < 3 || !/^\d+$/.test(cvv)) {
            errors.push('CVV inválido');
            isValid = false;
        }

        // Validar monto y servicio
        if (!amount || amount <= 0) {
            errors.push('Seleccione un servicio válido');
            isValid = false;
        }

        if (!isValid) {
            e.preventDefault();
            const errorDiv = document.createElement('div');
            errorDiv.className = 'alert alert-error';
            errorDiv.innerHTML = `
                ${errors.join('<br>')}
                <button type="button" class="close-alert">&times;</button>
            `;
            form.insertBefore(errorDiv, form.firstChild);

            // Configurar el botón de cierre para la nueva alerta
            const closeButton = errorDiv.querySelector('.close-alert');
            closeButton.addEventListener('click', () => {
                errorDiv.remove();
            });
        }
    });
});
