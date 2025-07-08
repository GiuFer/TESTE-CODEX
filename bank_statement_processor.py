import argparse
from dataclasses import dataclass
from typing import List, Dict

import pandas as pd
import pdfplumber


@dataclass
class Transaction:
    date: str
    description: str
    amount: float
    category: str


CATEGORY_KEYWORDS: Dict[str, str] = {
    "supermercado": "Alimentacao",
    "mercado": "Alimentacao",
    "restaurante": "Restaurantes",
    "salario": "Salario",
    "aluguel": "Moradia",
    "combustivel": "Transporte",
}


def parse_transactions(pdf_path: str) -> List[Transaction]:
    transactions: List[Transaction] = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            for line in text.splitlines():
                parts = line.split()
                if len(parts) < 3:
                    continue
                date, description, amount_str = parts[0], " ".join(parts[1:-1]), parts[-1]
                try:
                    amount = float(amount_str.replace(".", "").replace(",", "."))
                except ValueError:
                    continue

                category = categorize(description)
                transactions.append(Transaction(date, description, amount, category))
    return transactions


def categorize(description: str) -> str:
    desc_lower = description.lower()
    for keyword, category in CATEGORY_KEYWORDS.items():
        if keyword in desc_lower:
            return category
    return "Outros"


def transactions_to_dataframe(transactions: List[Transaction]) -> pd.DataFrame:
    return pd.DataFrame([t.__dict__ for t in transactions])


def save_to_excel(transactions: List[Transaction], output_path: str) -> None:
    df = transactions_to_dataframe(transactions)
    df.to_excel(output_path, index=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Processa extrato bancario em PDF e gera planilha Excel.")
    parser.add_argument("pdf", help="Caminho para o arquivo PDF do extrato")
    parser.add_argument("saida", help="Caminho para o arquivo Excel de saida")
    args = parser.parse_args()

    transactions = parse_transactions(args.pdf)
    save_to_excel(transactions, args.saida)


if __name__ == "__main__":
    main()
