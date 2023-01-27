from waitress import serve
from API_Server import app

serve(app, host='192.168.1.34', port=8432)