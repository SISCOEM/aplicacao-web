import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
# Obtenha as variáveis de ambiente
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USERNAME")
db_pass = os.getenv("DB_PASS")
db_host = os.getenv(
    "DB_HOST", "db"
)  # Define 'db' como padrão se DB_HOST não estiver definido


# Conectando ao banco de dados
try:
    connection = psycopg2.connect(
        dbname=db_name, user=db_user, password=db_pass, host=db_host, port="5432"
    )

    cursor = connection.cursor()

    create_table_query = """
    
    CREATE TABLE IF NOT EXISTS django_content_type (
    id SERIAL PRIMARY KEY,
    app_label VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    UNIQUE (app_label, model)
    );

    INSERT INTO django_content_type (app_label, model) VALUES
    ('admin', 'logentry'),
    ('auth', 'group'),
    ('auth', 'permission'),
    ('contenttypes', 'contenttype'),
    ('equipment', 'bullet'),
    ('equipment', 'equipment'),
    ('equipment', 'model_accessory'),
    ('equipment', 'model_armament'),
    ('equipment', 'model_grenada'),
    ('equipment', 'model_wearable'),
    ('load', 'equipment_load'),
    ('load', 'load'),
    ('police', 'police'),
    ('sessions', 'session');
    
    """
    cursor.execute(create_table_query)
    connection.commit()

except Exception as e:
    print(f"Ocorreu um erro: {e}")

finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()
