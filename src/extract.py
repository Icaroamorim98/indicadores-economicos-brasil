from datetime import date, timedelta
from bcb import sgs

SERIES = {
    "selic": 432,
    "ipca": 433,
    "dolar": 1,
}


def data_inicio(anos: int = 10, margem_dias: int = 30) -> str:
    hoje = date.today()
    inicio = hoje.replace(year=hoje.year - anos) + timedelta(days=margem_dias)
    return inicio.isoformat()


def extrair_todas() -> "pd.DataFrame":
    print("Extraindo séries do Banco Central...")
    inicio = data_inicio()
    print(f"Período: a partir de {inicio}")
    df = sgs.get(SERIES, start=inicio)
    df = df.reset_index().rename(columns={"Date": "data"})
    df = df.melt(id_vars="data", var_name="indicador", value_name="valor")
    df = df.dropna(subset=["valor"]).reset_index(drop=True)
    print(f"Total extraído: {len(df)} registros")
    return df


if __name__ == "__main__":
    dados = extrair_todas()
    print(dados.head())
    print(dados.tail())