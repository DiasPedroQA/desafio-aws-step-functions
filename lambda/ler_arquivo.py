# lambda/ler_arquivo.py

"""
Módulo responsável pela leitura do arquivo CSV de entrada.
Simula a primeira etapa de um workflow AWS Step Functions.
"""

import csv
import json


def main() -> None:
    """
    Lê o arquivo vendas.csv e retorna os dados em formato JSON.
    Em caso de arquivo não encontrado, retorna status de erro.
    """
    caminho: str = 'vendas.csv'
    try:
        with open(file=caminho, newline='', encoding='utf-8') as f:
            leitor: csv.DictReader[str] = csv.DictReader(f)
            dados: list[dict[str, str | float]] = list(leitor)
        # Retorna os dados como JSON (para simular o payload entre estados)
        print(json.dumps({'status': 'sucesso', 'dados': dados}))
    except FileNotFoundError:
        print(json.dumps(
            {'status': 'erro', 'mensagem': 'Arquivo não encontrado'}))


if __name__ == '__main__':
    main()
