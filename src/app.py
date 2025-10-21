from flask import Flask
import random
from flask import Flask, jsonify
from flasgger import Swagger, swag_from


# --- Constantes de Configuração do Jogo ---
NUM_PROPRIEDADES = 20
CUSTO_MIN_PROPRIEDADE = 50
CUSTO_MAX_PROPRIEDADE = 200
ALUGUEL_MIN_PROPRIEDADE = 20
ALUGUEL_MAX_PROPRIEDADE = 100

MAX_RODADAS = 1000
SALDO_INICIAL_JOGADOR = 300
VALOR_VOLTA = 100

ALUGUEL_EXIGENTE_MINIMO = 50
RESERVA_CAUTELOSO = 80
PROBABILIDADE_ALEATORIO = 0.5
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
        """Simula o lançamento de um dado equiprovável de 6 faces."""
        return random.randint(1, DADO_FACES)

    def mover(self, dado, num_propriedades):
        """Move o jogador e verifica se completou uma volta."""
        pos_anterior = self.posicao
        self.posicao = (self.posicao + dado) % num_propriedades

        if self.posicao < pos_anterior and self.posicao != 0:
            self.voltas += 1
            self.saldo += VALOR_VOLTA

    def deve_comprar(self, propriedade):
        """Lógica de decisão de compra baseada no tipo de jogador."""
        custo = propriedade.custo
        saldo_apos_compra = self.saldo - custo

        if custo > self.saldo:
            return False

        if self.tipo == "impulsivo":
            # Impulsivo: compra qualquer propriedade
            return True

        elif self.tipo == "exigente":
            # Exigente: compra se o aluguel > 50 (ALUGUEL_EXIGENTE_MINIMO)
            return propriedade.aluguel > ALUGUEL_EXIGENTE_MINIMO

        elif self.tipo == "cauteloso":
            # Cauteloso: compra se sobrar pelo menos 80 (RESERVA_CAUTELOSO)
            return saldo_apos_compra >= RESERVA_CAUTELOSO

        elif self.tipo == "aleatorio":
            # Aleatório: PROBABILIDADE_ALEATORIO (50%) de chance de compra
            return random.random() < PROBABILIDADE_ALEATORIO

        return False

    def comprar(self,propriedade):
        """Realiza a compra da propriedade."""
        self.saldo -= propriedade.custo
        propriedade.proprietario = self.nome
        self.propriedades.append(propriedade)

    def pagar_aluguel(self, proprietario_aluguel, aluguel):
        """Paga o aluguel e verifica se ficou negativo."""
        self.saldo -= aluguel

        if proprietario_aluguel:
            proprietario_aluguel.saldo += aluguel

        if self.saldo < 0:
            self.perder_jogo()

    def perder_jogo(self):
        """Remove o jogador do jogo e libera suas propriedades."""
        self.ativo = False
        for prop in self.propriedades:
            prop.proprietario = None
        self.propriedades = []


class Partida:
    """Controla o estado e a simulação do jogo em si."""

    def __init__(self):
        # Cria as propriedades usando as constantes
        self.propriedades = [
            Propriedade(
                i,
                random.randint(CUSTO_MIN_PROPRIEDADE, CUSTO_MAX_PROPRIEDADE),
                random.randint(ALUGUEL_MIN_PROPRIEDADE, ALUGUEL_MAX_PROPRIEDADE)
            )
            for i in range(NUM_PROPRIEDADES)
        ]
        self.tipos_jogadores = ["impulsivo", "exigente", "cauteloso", "aleatorio"]

        # Cria e embaralha os jogadores
        self.jogadores = [
            Jogador(tipo.capitalize(), tipo) for tipo in self.tipos_jogadores
        ]
        random.shuffle(self.jogadores)

        self.num_propriedades = len(self.propriedades)
        self.turno_atual = 0
        self.max_rodadas = MAX_RODADAS
        self.rodadas_jogadas = 0

    def simular(self):
        """Executa a simulação completa da partida."""

        while self.rodadas_jogadas < self.max_rodadas:
            jogador = self.jogadores[self.turno_atual % len(self.jogadores)]

            if jogador.ativo:
                dado = jogador.joga_dado()
                jogador.mover(dado, self.num_propriedades)
                propriedade_atual = self.propriedades[jogador.posicao]

                if propriedade_atual.proprietario is None:
                    if jogador.deve_comprar(propriedade_atual):
                        jogador.comprar(propriedade_atual)

                elif propriedade_atual.proprietario != jogador.nome:
                    proprietario = next((p for p in self.jogadores if p.nome == propriedade_atual.proprietario), None)
                    if proprietario and proprietario.ativo:
                        jogador.pagar_aluguel(proprietario, propriedade_atual.aluguel)

                # Checa vitória por falência
                jogadores_ativos = [j for j in self.jogadores if j.ativo]
                if len(jogadores_ativos) == 1:
                    vencedor = jogadores_ativos[0].nome
                    return self.gerar_resultado(vencedor)

            self.turno_atual += 1
            if self.turno_atual % len(self.jogadores) == 0:
                self.rodadas_jogadas += 1

        # Finaliza por limite de rodadas
        return self.finalizar_por_tempo()

    def finalizar_por_tempo(self):
        """Determina o vencedor pelo maior saldo (critério de desempate: ordem de turno)."""
        jogadores_ativos = [j for j in self.jogadores if j.ativo]

        jogadores_ordenados = sorted(
            jogadores_ativos,
            key=lambda j: (-j.saldo, self.jogadores.index(j))
        )

        vencedor = jogadores_ordenados[0].nome if jogadores_ordenados else "Nenhum"
        return self.gerar_resultado(vencedor)

    def gerar_resultado(self, vencedor):
        """Formata o resultado final da simulação."""
        # Ordena a lista de jogadores ativos por saldo final (decrescente)
        jogadores_finais = sorted(
            [j for j in self.jogadores if j.ativo],
            key=lambda j: j.saldo,
            reverse=True
        )
        nomes_ordenados = [j.nome for j in jogadores_finais]

        # Inclui jogadores falidos no final
        jogadores_inativos = sorted(
            [j for j in self.jogadores if not j.ativo],
            key=lambda j: j.nome
        )
        nomes_ordenados.extend([j.nome for j in jogadores_inativos])

        return {
            "vencedor": vencedor,
            "jogadores": nomes_ordenados
        }

# --- Configuração do Flask e Swagger ---

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

    partida = Partida()
    resultado = partida.simular()

    return jsonify(resultado)


if __name__ == '__main__':
    app.run(debug=True)