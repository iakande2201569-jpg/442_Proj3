from web.app import app

if __name__ == '__main__':
    # Run the application on localhost port 5000
    app.run(debug=True, host='0.0.0.0', port=5000)