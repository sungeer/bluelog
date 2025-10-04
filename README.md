# Viper

*Async backend depends on the Starlette ASGI toolkit.*

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
$ granian --interface wsgi otter:app
* Running on http://127.0.0.1:8000/
```

## License

This project is licensed under the GPLv3 License (see the
[LICENSE](LICENSE) file for details).
