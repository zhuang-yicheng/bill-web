from flask import Flask
from bill import create_app

app = create_app()
if __name__ == '__main__':
    app.run()

