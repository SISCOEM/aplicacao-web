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
    


    INSERT INTO police_police VALUES (3,'pbkdf2_sha256$720000$kex2hz8CGHzdTqokHZZFRq$jY2Qq/SAgQoNLYXWSYxia3CTc280DvZG7aJGAVanQmc=','2024-09-02 19:16:57.217383',true,'admin','','','',true,true,'2023-10-06 22:29:56.561030',true,0,'123','','','','Police','Ediel',3,NULL,NULL);
    INSERT INTO equipment_bullet VALUES (5,1,1149,'Modelos/municoes/45acp.png','.45 ACP','Munição ACP',3),(6,1,0,'Modelos/municoes/municao-9mm.jpg','9mm','Munição 9mm',3);

    INSERT INTO equipment_equipment VALUES ('2024-01-19 14:38:44.380773',1,'SVH58737','3000E280699500004003762771ACC343','24H',6,3,3),('2024-01-17 20:17:38.256289',1,'98450605054150','3400E20047066C706821','12H',3,3,3),('2024-02-01 23:42:35.923804',1,'4534','414C5355504552416C7465633132000000008B76','Disponível',3,3,3),('2024-02-01 23:47:01.617886',1,'6894956163451','454C5355504552416C7465633132000000007BD1','Disponível',4,3,3),('2024-01-17 03:58:05.764644',1,'45656485','456','Disponível',3,3,3);

    INSERT INTO equipment_model_accessory VALUES (3,1,'Bastão','Bastão','Modelos/acessorios/bastao.jpg',3),(4,1,'Cone','Cone','Modelos/acessorios/cone.jpg',3),(5,1,'Bastão','Bastão','Modelos/acessorios/bastao.jpg',3),(6,1,'Cone','Cone','Modelos/acessorios/cone.jpg',3);

    INSERT INTO equipment_model_armament VALUES (3,1,'Glok G22','.22 LR','Glok G22, munição .22 LR','Modelos/armamentos/Glock_g22_GNtS5RI.jpg',3),(4,1,'Glok 9mm','9mm','Pistola Glok 9mm','Modelos/armamentos/1016504_pistola-taurus-th380-oxidada-cal-380-cth380-ox_s1_636711376069468013.jpg',3),(5,1,'GLOCK G22 CAL 9MM','9mm','ANO 2013','Modelos/armamentos/pistol-glock.jpg',3),(6,1,'TAURUS PT100','.40 S&W','Pistola - TAURUS PT100','Modelos/armamentos/TaurusPT100.png',3);


    INSERT INTO equipment_model_grenada VALUES (3,1,'Granada de Fumaça','Modelos/granadas/Granada_de_Fumaça.jpg','Granada de Fumaça',3),(4,1,'Granada de Fogo','Modelos/granadas/granada-fogo.jpg','Granada de Fogo',3);


    INSERT INTO equipment_model_wearable VALUES (3,1,'Capacete','M','Capacete','Modelos/vestiveis/capacete.jpg',3),(4,1,'Colete','M','Colete','Modelos/vestiveis/colete.jpg',3);
    INSERT INTO public.police_police ("password",last_login,is_superuser,username,first_name,last_name,email,is_staff,is_active,date_joined,"name",activated,matricula,telefone,lotacao,posto,image_path,tipo,fingerprint,"pushToken",activator_id) VALUES
	 	 ('pbkdf2_sha256$720000$pu2YlNBYmtVU8xRi8M5vR3$sLQm2iWonIZhs0HobAdn4TFYSUs5yy4Rq+MggZ0PcvU=',NULL,true,'fabio','','','',true,true,'2024-10-10 19:14:10.635762-03','',0,'','','','','','Policial',NULL,NULL,NULL);

    
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
