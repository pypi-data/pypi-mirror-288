from .init_client import sciDXClient
from .register_organization import register_organization
from .search_resource import search_resource
from .search_organization import search_organization
from .register_url import register_url
from .register_s3 import register_s3
from .register_kafka import register_kafka
from .get_api_token import get_api_token
from .login import login
from .logout import logout
from .create_kafka_stream import create_kafka_stream
from .consume_kafka_messages import consume_kafka_messages

# Add the methods to sciDXClient
sciDXClient.register_organization = register_organization
sciDXClient.search_organization = search_organization
sciDXClient.search_resource = search_resource
sciDXClient.register_url = register_url
sciDXClient.register_kafka = register_kafka
sciDXClient.register_s3 = register_s3
sciDXClient.get_api_token = get_api_token
sciDXClient.login = login
sciDXClient.logout = logout

sciDXClient.create_kafka_stream = create_kafka_stream
sciDXClient.consume_kafka_messages = consume_kafka_messages
