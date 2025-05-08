from flask import Flask, send_from_directory, request, abort
import os
import socket 

app = Flask(__name__, static_folder='.', static_url_path='')

def get_local_ip():
    """Спроба отримати локальну IP-адресу комп'ютера."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        s.connect(('10.254.254.254', 1)) 
        IP = s.getsockname()[0]
        s.close()
        return IP
    except Exception:
        return '127.0.0.1' 

@app.route('/')
def index():
    if not os.path.exists('index.html'):
        abort(404, description="Файл index.html не знайдено.")
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_files(filename):
    allowed_extensions = ['.html', '.css', '.png', '.otf', '.ico']
    file_ext = os.path.splitext(filename)[1].lower()

    if not os.path.exists(filename):
        abort(404, description=f"Ресурс '{filename}' не знайдено.")

    if file_ext in allowed_extensions or filename == 'favicon.ico':
        return send_from_directory('.', filename)
    else:
        abort(403, description="Доступ до цього типу файлу заборонено.")

if __name__ == '__main__':
    port = 5000
    host_ip_for_network = get_local_ip()
    host_listen_on = '0.0.0.0'

    print(f" * Сервер запущено!")
    print(f" * Щоб отримати доступ:")
    print(f" *   - На цьому комп'ютері: http://127.0.0.1:{port} або http://localhost:{port}")
    if host_ip_for_network != '127.0.0.1':
        print(f" *   - З інших пристроїв у вашій локальній мережі: http://{host_ip_for_network}:{port}")
        print(f" *     (Переконайтеся, що брандмауер дозволяє з'єднання на порт {port})")
    else:
        print(" *   Не вдалося визначити локальну IP-адресу для доступу з мережі.")

    print(f" * Сервер слухає на всіх інтерфейсах ({host_listen_on}).")
    app.run(debug=True, host=host_listen_on, port=port)