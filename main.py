from app import app

if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0", port=443, ssl_context=('/etc/letsencrypt/live/doge.top/fullchain.pem', '/etc/letsencrypt/live/doge.top/privkey.pem'))