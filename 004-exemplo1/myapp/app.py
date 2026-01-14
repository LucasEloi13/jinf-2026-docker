from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    # Adicionando um estilo inline para garantir que todos vejam bem
    return """
    <html>
        <head>
            <title>Minha Palestra Docker</title>
            <style>
                body { 
                    background-color: #003f5c; 
                    color: white; 
                    display: flex; 
                    justify-content: center; 
                    align-items: center; 
                    height: 100vh; 
                    margin: 0; 
                    font-family: sans-serif; 
                }
                h1 { 
                    font-size: 5rem; 
                    border: 5px solid #ffa600; 
                    padding: 20px; 
                    border-radius: 15px; 
                }
            </style>
        </head>
        <body>
            <h1>🐳 Olá, Jornada da Informática!</h1>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)