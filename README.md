# Viper

*A lightweight Python web API built with Werkzeug.*

## Installation

clone:
```
$ git clone https://github.com/sungeer/viper.git
$ cd otter
```
create & activate virtual env then install dependency:

with venv + pip:
```
$ python -m venv venv
$ source venv/bin/activate  # use `venv\Scripts\activate` on Windows
$ pip install -r requirements.txt
```

run:
```
$ waitress --host=127.0.0.1 --port=7788 viper:wsgi_app
* Running on http://127.0.0.1:8000/
```

## License

This project is licensed under the GPLv3 License (see the
[LICENSE](LICENSE) file for details).
