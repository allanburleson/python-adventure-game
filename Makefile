all:
	pyinstaller -v && pyinstaller -F scripttocompile.py -n python-adventure-game || echo "There was an error. You may need to install pyinstaller with pip." 
install:
	cp dist/python-adventure-game /usr/local/bin || echo "Must be run as root."
