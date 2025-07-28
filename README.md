# Nucleic

*A backend scaffold depends on the Werkzeug WSGI toolkit.*

## Installation

clone:
```
$ git clone https://github.com/sungeer/nucleic.git
$ cd nucleic
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
$ uvicorn nucleic:app
* Running on http://127.0.0.1:8000/
```

## License

This project is licensed under the MIT License (see the
[LICENSE](LICENSE) file for details).
