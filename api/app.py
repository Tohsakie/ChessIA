from flask import Flask, request, jsonify
import commons

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return "Hello World!"

@app.route('/predict/', methods=['POST'])
def process_fen():
    try:
        # Récupérer le paramètre FEN de la requête POST
        fen = request.form['FEN']
        print(f"FEN reçu : {fen}")

        nextMove = commons.predict_next_move(fen)
        print(f"Prochain mouvement prédit : {nextMove}")
        response = {'message': nextMove}
        return jsonify(response), 200

    except KeyError:
        response = {'error': 'Paramètre FEN manquant dans la requête POST'}
        return jsonify(response), 400

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='localhost', port=8000)
