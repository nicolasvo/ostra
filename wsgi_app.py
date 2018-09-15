from app.api.app import application_factory
import os

# Override base application settings here
settings = {}

app = application_factory(settings)

if __name__ == "__main__":
    app.serve('0.0.0.0', port=os.environ.get('PORT'), debug=True)
    # app.serve('0.0.0.0', port=5000, debug=True)
