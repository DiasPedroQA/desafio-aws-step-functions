# lambda/analisar.py

"""
Módulo que calcula métricas a partir dos dados lidos.
Simula a etapa de análise de um workflow AWS Step Functions.
"""

import json
import sys


def main() -> None:
    """
    Lê um payload JSON com os dados, calcula o total de vendas e a
    quantidade de registros, e retorna essas métricas em JSON.
    """
    try:
        entrada: dict[str, object] = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        print(json.dumps({"status": "erro", "mensagem": "JSON inválido"}))
        return

    if entrada.get("status") != "sucesso":
        print(json.dumps(
            {"status": "erro", "mensagem": entrada.get("mensagem")}
        ))
        return

    dados: object = entrada["dados"]
    assert isinstance(dados, list)

    try:
        total: float = sum(float(linha["valor"]) for linha in dados)
    except (KeyError, ValueError, TypeError) as e:
        print(json.dumps(
            {"status": "erro", "mensagem": f"Erro nos dados: {str(e)}"}
        ))
        return
    quantidade: int = len(dados)
    print(json.dumps(
        {'total_vendas': total,
         'quantidade_registros': quantidade}
    ))


if __name__ == '__main__':
    main()
