# Statement for enabling the development environment
import os


# Define the application directory
class BaseConfiguration(object):
    DEBUG = os.environ.get("DEBUG", "True") == "True"
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Define the database - we are working with
    # SQLite for this example
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
                                             'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'))
    DATABASE_CONNECT_OPTIONS = {}
    DEBUG_TB_PROFILER_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_PASSWORD_SALT = "salt"  # os.environ.get("SECURITY_PASSWORD_SALT", "secret_salt")
    # Use a secure, unique and absolutely secret key for signing the data.
    CSRF_SESSION_KEY = os.environ.get("SECURITY_PASSWORD_SALT", "secret")

    # Secret key for signing cookies
    SECRET_KEY = os.environ.get("SECRET_KEY", "secret")

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
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

current_config = BaseConfiguration