from flask import Flask, request, jsonify, render_template
import pymysql
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuração do banco de dados usando variáveis de ambiente
db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "projetosupply")
}

# Conexão com o banco de dados
def get_db_connection():
    return pymysql.connect(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"]
    )

# Rota para inserir dados do sensor
@app.route('/api/sensor', methods=['POST'])
def sensor_data():
    try:
        data = request.get_json()
        posicao = data.get('posicao_movimentada')
        estado = data.get('estado_sensor')

        if not posicao or estado is None:
            return jsonify({"error": "Dados inválidos. Certifique-se de enviar 'posicao_movimentada' e 'estado_sensor'."}), 400

        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO movimentacao (posicao_movimentada, estado_sensor)
                    VALUES (%s, %s)
                """
                cursor.execute(query, (posicao, estado))
                connection.commit()

        return jsonify({"message": "Dados inseridos com sucesso!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para obter movimentações do banco de dados
@app.route('/api/movimentacoes', methods=['GET'])
def get_movimentacoes():
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                query = "SELECT posicao_movimentada, estado_sensor, data_hora FROM movimentacao"
                cursor.execute(query)
                result = cursor.fetchall()

        movimentacoes = []
        for row in result:
            estado_sensor = "Movimentado" if row[1] == 1 else "Parado"
            movimentacoes.append({
                'posicao_movimentada': row[0],
                'estado_sensor': estado_sensor,
                'data_hora': row[2].strftime("%Y-%m-%d %H:%M:%S")
            })

        return jsonify({"movimentacoes": movimentacoes}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para renderizar o arquivo index.html
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.getenv("PORT", 5000)),
        debug=False  # Desabilita o debug em produção
    )