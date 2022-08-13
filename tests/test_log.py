import os
import sys

lobbit_app = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../")
sys.path.append(lobbit_app)

if lobbit_app in sys.path:
    from app.lobbit_server.log import LobbitLog
