from flask import Flask
from redis import Redis

app = Flask(__name__)
redis = Redis(host='meu_banco', port=6379)

@app.get('/')
def home():
    # Incrementa o contador no Redis
    hits = redis.incr('contador')
    
    return f"""
    <html>
        <head>
            <style>
                body {{ background-color: #0d1117; color: white; display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh; font-family: sans-serif; }}
                .box {{ border: 3px solid #009688; padding: 40px; border-radius: 20px; text-align: center; }}
                h1 {{ font-size: 3rem; color: #009688; }}
                span {{ font-size: 5rem; font-weight: bold; color: #ffa600; }}
            </style>
        </head>
        <body>
            <div class="box">
                <h1>Jornada da Informática</h1>
                <p>Este site já foi acessado</p>
                <span>{hits}</span>
                <p>vezes de dentro de um container!</p>
            </div>
        </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)