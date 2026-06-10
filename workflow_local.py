# workflow_local.py

"""
Orquestrador local que simula a máquina de estados AWS Step Functions.
Encadeia as tarefas de leitura, análise e gravação, passando o payload
JSON de uma etapa para a seguinte.
"""

import subprocess
import sys

estados: list[list[str]] = [
    ['python', 'lambda/ler_arquivo.py'],
    ['python', 'lambda/analisar.py'],
    ['python', 'lambda/gravar_resultado.py']
]

payload: str = ""
for i, comando in enumerate(estados):
    nome_estado: str = ['LerArquivo', 'Analisar', 'GravarResultado'][i]
    print(f'\n--- Executando estado: {nome_estado} ---')
    proc: subprocess.CompletedProcess[str] = subprocess.run(
        args=comando,
        input=payload,
        capture_output=True,
        text=True,
        check=False
    )
    if proc.returncode != 0:
        print(f'Erro no estado {nome_estado}: {proc.stderr}')
        sys.exit(1)
    payload = proc.stdout.strip()
    print(payload)

print('\nWorkflow concluído com sucesso! Verifique o resultado em resultado.txt')
