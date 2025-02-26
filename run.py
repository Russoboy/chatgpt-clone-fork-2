import logging
from server.app import app
from server.website import Website
from server.backend import Backend_Api
from json import load

# Setup logging
logging.basicConfig(
    filename='server.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

if __name__ == '__main__':
    try:
        config = load(open('config.json', 'r'))
        site_config = config['site_config']

        site = Website(app)
        for route in site.routes:
            try:
                app.add_url_rule(
                    route,
                    view_func=site.routes[route]['function'],
                    methods=site.routes[route]['methods'],
                )
                logging.info(f"Added website route: {route}")
            except Exception as e:
                logging.error(f"Error adding website route {route}: {e}")

        backend_api = Backend_Api(app, config)
        for route in backend_api.routes:
            try:
                app.add_url_rule(
                    route,
                    view_func=backend_api.routes[route]['function'],
                    methods=backend_api.routes[route]['methods'],
                )
                logging.info(f"Added backend API route: {route}")
            except Exception as e:
                logging.error(f"Error adding backend API route {route}: {e}")

        logging.info(f"Server starting on port {site_config['port']}")
        app.run(**site_config)
        logging.info(f"Server stopped on port {site_config['port']}")

    except Exception as e:
        logging.critical(f"Fatal error: {e}")
