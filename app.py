from chatapp import create_app, socketio

app = create_app() # Create an application

socketio.run(app) # Launch socket.io