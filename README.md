# TESTE-CODEX

Exemplo de aplicativo para processar extratos bancários em PDF e gerar uma planilha Excel com classificação de entradas e saídas.

## Requisitos

Instale as dependências em um ambiente Python:

```bash
pip install -r requirements.txt
```

## Uso

Execute o script informando o caminho do PDF do extrato e o caminho do arquivo Excel de saída:

```bash
python bank_statement_processor.py meu_extrato.pdf relatorio.xlsx
```

O arquivo gerado conterá as colunas `date`, `description`, `amount` e `category`.
