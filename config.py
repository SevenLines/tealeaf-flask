# Statement for enabling the development environment
import json
import os

with open("parameters.json") as f:
    parameters = json.load(f)


# Define the application directory
class BaseConfiguration(object):
    DEBUG = parameters.get("DEBUG", False)
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Define the database - we are working with
    # SQLite for this example
    SQLALCHEMY_DATABASE_URI = parameters.get('DATABASE_URL', 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'))
    DATABASE_CONNECT_OPTIONS = {}
    DEBUG_TB_PROFILER_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    TEMPLATES_AUTO_RELOAD = True

    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_PASSWORD_SALT = "salt"
    # Use a secure, unique and absolutely secret key for signing the data.
    CSRF_SESSION_KEY = parameters.get("SECURITY_PASSWORD_SALT", "secret")

    # Secret key for signing cookies
    SECRET_KEY = parameters.get("SECRET_KEY", "secret")

    LOG_PATH = os.path.join(BASE_DIR, "logs/flask.log")

    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2

    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True

    # Assets config
    ASSETS_DEBUG = DEBUG
    ASSETS_CACHE = False
    ASSETS_MANIFEST = False
    if not DEBUG:
        ASSETS_AUTO_BUILD = False

    # file uploads
    UPLOAD_FOLDER = os.path.abspath(os.path.join(BASE_DIR, 'app/public'))
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx', 'doc', 'xls', 'xlsx', 'djvu'}

current_config = BaseConfiguration