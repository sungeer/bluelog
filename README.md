# Viper

*A simple chat interface inspired by DeepSeek.*

> This project is built on the Starlette framework and can be considered a comprehensive backend project template. The main advantage is that it can be conveniently used directly for other new projects.

No Pydantic, no aiomysql, nothing that is poorly maintained or unstable is referenced.

## Installation

clone:
```
$ git clone https://github.com/sungeer/viper.git
$ cd viper
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
$ granian --interface wsgi viper:app
* Running on http://127.0.0.1:8000/
```

## License

This project is licensed under the MIT License (see the
[LICENSE](LICENSE) file for details).
