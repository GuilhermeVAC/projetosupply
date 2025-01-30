from flask import Flask, request, jsonify, render_template
import pymysql
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilita CORS para permitir requisições de diferentes origens

# Configuração do banco de dados
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "<2010.guicae",  # Substitua pela sua senha
    "database": "movimentacao"
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
        # Obter os dados do JSON enviado
        data = request.get_json()  # Aqui o request está sendo utilizado corretamente
        posicao = data.get('posicao_movimentada')
        estado = data.get('estado_sensor')

        # Verificar se os campos foram enviados
        if not posicao or estado is None:
            return jsonify({"error": "Dados inválidos. Certifique-se de enviar 'posicao_movimentada' e 'estado_sensor'."}), 400

        # Inserir dados no banco de dados
        with get_db_connection() as connection:  # Usando context manager para garantir que a conexão será fechada
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO movimentacao (posicao_movimentada, estado_sensor)
                    VALUES (%s, %s)
                """
                cursor.execute(query, (posicao, estado))
                connection.commit()

        return jsonify({"message": "Dados inseridos com sucesso!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Resposta JSON para erro

# Rota para obter movimentações do banco de dados
@app.route('/api/movimentacoes', methods=['GET'])
def get_movimentacoes():
    try:
        # Conectar ao banco de dados
        with get_db_connection() as connection:  # Usando context manager para garantir que a conexão será fechada
            with connection.cursor() as cursor:
                query = "SELECT posicao_movimentada, estado_sensor, data_hora FROM movimentacao"
                cursor.execute(query)
                result = cursor.fetchall()

        # Preparar dados para o frontend, convertendo estado_sensor para texto legível
        movimentacoes = []
        for row in result:
            estado_sensor = row[1]
            # Converter 1 para "Ativado" e outros valores para "Desativado"
            if estado_sensor == 1:
                estado_sensor = "Parado"
            else:
                estado_sensor = "Movimentado"  # Ou outro valor dependendo do seu caso

            movimentacoes.append({
                'posicao_movimentada': row[0],
                'estado_sensor': estado_sensor,
                'data_hora': row[2].strftime("%Y-%m-%d %H:%M:%S")  # Formatar data
            })

        return jsonify({"movimentacoes": movimentacoes}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para renderizar o arquivo index.html
@app.route('/')
def index():
    return render_template('index.html')  # Isso renderiza o arquivo HTML da pasta templates

# Inicia o servidor Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Roda o servidor Flask na porta 5000




