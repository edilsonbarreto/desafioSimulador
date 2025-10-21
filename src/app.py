from flask import Flask
from flask import Flask, jsonify
from flasgger import Swagger, swag_from


# --- Constantes de Configuração do Jogo ---
NUM_PROPRIEDADES = 20
MAX_RODADAS = 1000
SALDO_INICIAL_JOGADOR = 300
VALOR_VOLTA = 100
DADO_FACES = 6

class Propriedade:
    """Representa uma propriedade no tabuleiro."""

    def __init__(self, id_prop, custo, aluguel):
        self.id = id_prop
        self.custo = custo
        self.aluguel = aluguel
        self.proprietario = None

class Jogador:
    """Representa um jogador com seus comportamentos e estados no jogo"""

    def __init__(self, nome, tipo):
        self.nome = nome
        self.tipo = tipo
        self.saldo = SALDO_INICIAL_JOGADOR
        self.posicao = 0
        self.ativo = True
        self.propriedades = []
        self.voltas = 0

    def joga_dado(self):
        return

    def mover(self):
        return

    def deve_comprar(self):
        return

    def comprar(self):
        return

    def pagar_aluguel(self):
        return

    def perder_jogo(self):
        return


class Partida:
    """Controla o estado e a simulação do jogo em si."""

    def __init__(self):
        return

    def simular(self):

        return
    def finalizar_por_tempo(self):
        return

    def gerar_resultado(self):
        return



app = Flask(__name__)


# Configuração básica do Swagger
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "title": "Simulador de Jogo de Tabuleiro",
    "version": "1.0.0",
    "description": f"API para simular uma partida de um jogo de tabuleiro com 4 estratégias de jogadores. (Max Rodadas: {MAX_RODADAS}, Saldo Inicial: {SALDO_INICIAL_JOGADOR})",
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}
swagger = Swagger(app, config=swagger_config)
@app.route("/jogo/simular", methods=["GET"])
@swag_from({
    'tags': ['Simulação'],
    'summary': 'Executa uma simulação completa do jogo de tabuleiro.',
    'description': 'Roda uma partida única entre os 4 tipos de jogadores (Impulsivo, Exigente, Cauteloso, Aleatório) até a falência de 3 jogadores ou o limite de rodadas.',
    'responses': {
        '200': {
            'description': 'Resultado da simulação.',
            'schema': {
                'type': 'object',
                'properties': {
                    'vencedor': {
                        'type': 'string',
                        'description': 'O nome do jogador vencedor (p. ex., "Cauteloso").'
                    },
                    'jogadores': {
                        'type': 'array',
                        'items': {'type': 'string'},
                        'description': 'Lista de nomes dos jogadores, ordenada pelo saldo final (decrescente).'
                    }
                }
            },
            'examples': {
                'simulacao_exemplo': {
                    "vencedor": "Cauteloso",
                    "jogadores": ["Cauteloso", "Aleatorio", "Exigente", "Impulsivo"]
                }
            }
        }
    }
})
def simular_jogo():
    """Endpoint para rodar a simulação do jogo e retornar o resultado."""

    resultado = "Funcionou!"

    return jsonify({"resultado": resultado})


if __name__ == '__main__':
    # Certifique-se de que instalou: pip install flask flasgger
    print("Servidor Flask rodando...")
    print("Swagger UI em: http://127.0.0.1:5000/apidocs/")
    app.run(debug=True)