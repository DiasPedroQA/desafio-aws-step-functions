# lambda/gravar_resultado.py

"""
Módulo que gera o arquivo de relatório de vendas.
Simula a etapa final de um workflow AWS Step Functions.
"""

from textwrap import dedent
import sys
from datetime import datetime
import json

ERRO_JSON_INVALIDO: dict[str, str] = {"status": "erro", "mensagem": "JSON inválido na entrada"}
ERRO_PAYLOAD_INCOMPLETO: dict[str, str] = {"status": "erro", "mensagem": "Payload incompleto"}
SUCESSO_TEMPLATE: dict[str, str] = {"status": "sucesso", "arquivo": "resultado.txt"}


def gerar_resumo(entrada: dict[str, float]) -> str:
    """Gera o texto do relatório a partir das métricas de entrada."""
    data_hora: str = datetime.now().strftime(format="%d/%m/%Y %H:%M")

    return dedent(
        text=f"""\
        Relatório de Vendas
        Gerado em: {data_hora}
        Total de vendas: R$ {entrada['total_vendas']:,.2f}
        Registros processados: {entrada['quantidade_registros']}
        """
    )


def main() -> None:
    """
    Recebe métricas de vendas em JSON, formata um relatório e o salva
    no arquivo resultado.txt.
    """
    try:
        entrada: dict[str, float] = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        print(json.dumps(ERRO_JSON_INVALIDO, ensure_ascii=False))
        return

    if "total_vendas" not in entrada or "quantidade_registros" not in entrada:
        print(json.dumps(ERRO_PAYLOAD_INCOMPLETO, ensure_ascii=False))
        return

    resumo: str = gerar_resumo(entrada=entrada)

    with open(file="resultado.txt", mode="w", encoding="utf-8") as f:
        f.write(resumo)

    print(json.dumps(SUCESSO_TEMPLATE, ensure_ascii=False))


if __name__ == '__main__':
    main()
