import logging
import logging.config
# ------------------------SQL---------------------------------
SQL_FILE = './sql/get_routes_moscow.sql'
UPLOAD_FILE = './files/Moscow'


# ------------------------ELASTICSEARCH---------------------------------
elastic_index_name = 'aviasales'
elastic_data_mapping = {
    "properties": {
        "airline": {"type": "text"},
        "arrival_iata": {"type": "text"},
        "country": {"type": "text"},
        "departure_at": {"type": "date"},
        "expires_at": {"type": "date"},
        "feelslike": {"type": "long"},
        "flight_number": {"type": "long"},
        "lat": {"type": "text"},
        "lon": {"type": "text"},
        "name": {"type": "text"},
        "price": {"type": "long"},
        "return_at": {"type": "date"},
        "temperature": {"type": "long"}
    }
}
doc_type = 'fly_info'
elastic_url = 'https://vpc-production-elasticsearch-fuc6vzlsrdejg637pq3557fgei.ap-south-1.es.amazonaws.com'

# ------------------------LOGGING---------------------------------
logging.config.fileConfig('logging.conf')
main_logger = logging.getLogger('mainExample')

