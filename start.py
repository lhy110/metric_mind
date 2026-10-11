"""Public-host launcher: use the platform's PORT or 8501 locally."""
import os
import sys


def server_command():
    port = int(os.environ.get('PORT', '8501'))
    if not 1 <= port <= 65535:
        raise ValueError('PORT must be an integer between 1 and 65535')
    return [sys.executable, '-m', 'streamlit', 'run', 'app.py',
            '--server.address=0.0.0.0', f'--server.port={port}',
            '--server.headless=true']


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.execv(sys.executable, server_command())
