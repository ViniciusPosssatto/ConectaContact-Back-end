import os
from src.app import create_app
from src.app.routes import routes



app = create_app(os.getenv('FLASK_ENV'))

routes(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv("PORT"))
