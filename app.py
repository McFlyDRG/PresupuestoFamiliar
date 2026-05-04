import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Configuramos la ruta base para que Flask no se pierda en Render
base_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(base_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)
app.secret_key = 'presupuesto_familiar_david_2026'

# Configuración de base de datos persistente en el servidor
db_path = os.path.join(base_dir, 'presupuesto.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Movimiento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(10)) 
    detalle = db.Column(db.String(100))
    monto = db.Column(db.Float)
    icon = db.Column(db.String(50))
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    # Esta es la línea que fallaba en tus logs
    return render_template('index.html')

@app.route('/api/movimientos', methods=['GET'])
def get_movs():
    movs = Movimiento.query.order_by(Movimiento.fecha.desc()).all()
    return jsonify([{'id': m.id, 'tipo': m.tipo, 'detalle': m.detalle, 'monto': m.monto, 'icon': m.icon} for m in movs])

@app.route('/api/movimientos', methods=['POST'])
def add_mov():
    data = request.json
    nuevo = Movimiento(tipo=data['tipo'], detalle=data['detalle'], monto=float(data['monto']), icon=data.get('icon'))
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({'status': 'ok'})

@app.route('/api/movimientos/<int:id>', methods=['DELETE'])
def del_mov(id):
    m = Movimiento.query.get(id)
    if m:
        db.session.delete(m)
        db.session.commit()
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
