all:
	pyinstaller -v && pyinstaller -F scripttocompile.py -n python-adventure-game || echo "There was an error. You may need to install pyinstaller with pip." 
