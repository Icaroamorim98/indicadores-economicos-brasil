import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

from extract import extrair_todas

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def criar_tabela(engine):
    ddl = text("""
        CREATE TABLE IF NOT EXISTS indicadores (
            id SERIAL PRIMARY KEY,
            data DATE NOT NULL,
            indicador VARCHAR(20) NOT NULL,
            valor NUMERIC(12, 4) NOT NULL,
            UNIQUE (data, indicador)
        );
    """)
    with engine.begin() as conn:
        conn.execute(ddl)
    print("Tabela 'indicadores' pronta.")


def carregar_dados(engine, df):
    registros = df.to_dict(orient="records")

    insert_stmt = text("""
        INSERT INTO indicadores (data, indicador, valor)
        VALUES (:data, :indicador, :valor)
        ON CONFLICT (data, indicador) DO UPDATE
        SET valor = EXCLUDED.valor;
    """)

    with engine.begin() as conn:
        conn.execute(insert_stmt, registros)

    print(f"{len(registros)} registros carregados/atualizados.")


if __name__ == "__main__":
    engine = create_engine(DATABASE_URL)
    criar_tabela(engine)

    df = extrair_todas()
    carregar_dados(engine, df)