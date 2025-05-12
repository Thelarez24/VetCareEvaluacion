from flask import Flask, render_template
from app.models.database import Database
from app.controllers.contacts_controller import contacts_bp
from app.controllers.payments_controller import payments_bp
from datetime import datetime
import os

# Inicializar la base de datos primero
Database.initialize()
db = Database.get_instance()

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.secret_key = os.urandom(24)

# Registrar los blueprints
app.register_blueprint(contacts_bp)
app.register_blueprint(payments_bp)

# Contexto global para las plantillas
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# Ruta raíz
@app.route('/')
def index():
    return render_template('index.html')

# Ruta de administración
@app.route('/admin')
def admin():
    return render_template('admin/index.html')

if __name__ == '__main__':
    # Asegurarse de que los directorios necesarios existen
    os.makedirs('app/database', exist_ok=True)
    os.makedirs('app/static/css', exist_ok=True)
    
    app.run(debug=True)
