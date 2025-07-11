import abc
import json
import datetime
import logging
import hashlib
import uuid
import re
from argparse import ArgumentParser
from http.server import BaseHTTPRequestHandler, HTTPServer

from scoring import get_score, get_interests

SALT = "Otus"
ADMIN_LOGIN = "admin"
ADMIN_SALT = "42"
OK = 200
BAD_REQUEST = 400
FORBIDDEN = 403
NOT_FOUND = 404
INVALID_REQUEST = 422
INTERNAL_ERROR = 500
ERRORS = {
    BAD_REQUEST: "Bad Request",
    FORBIDDEN: "Forbidden",
    NOT_FOUND: "Not Found",
    INVALID_REQUEST: "Invalid Request",
    INTERNAL_ERROR: "Internal Server Error",
}
UNKNOWN = 0
MALE = 1
FEMALE = 2
GENDERS = {
    UNKNOWN: "unknown",
    MALE: "male",
    FEMALE: "female",
}


class Validated(abc.ABC):
    def __init__(self, required=True, nullable=False):
        self.required = required
        self.nullable = nullable

    def __set_name__(self, owner, name):
        self.name = f'_{name}'

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        setattr(instance, self.name, self.validate(value))

    def validate(self, value):
        if not self.nullable and value is None:
            raise ValueError(f'Invalid value. Not nullable.')
        return value


class CharField(Validated):
    def validate(self, value):
        super().validate(value)
        if value is not None:
            if type(value) is not str:
                raise ValueError(f'Invalid value. Value {self.name[1:]} must be str')
        return value


class EmailField(CharField):
    def validate(self, value):
        super().validate(value)
        if value is not None:
            if not re.match(r"^[^@]+@[^@]+$", value):
                raise ValueError("Invalide email")
        return value


class PhoneField(Validated):
    def validate(self, value):
        super().validate(value)
        if value is not None:
            if not type(value) in (str, int):
                raise ValueError(f'Invalid value. Value {self.name[1:]} to be str or int')
            if not re.match(r"^7\d{10}$", str(value)):
                raise ValueError("Invalid phone number.")
        return value


class DateField(Validated):
    def validate(self, value):
        super().validate(value)
        if value is not None:
            if type(value) is not str:
                raise ValueError(f'Invalid date. Value {self.name[1:]} must be str DD.MM.YYYY')
            if not re.match(r"^\d{2}\.\d{2}\.\d{4}$", str(value)):
                raise ValueError("Invalide date format")
            else:
                try:
                    datetime.date(*map(int, value.split('.')[::-1]))
                except:
                    raise ValueError("Invalide date format")
        return value


class BirthDayField(DateField):
    def validate(self, value):
        super().validate(value)
        if value is not None:
            delta = (datetime.datetime.now() - datetime.datetime(*map(int, value.split('.')[::-1]))).days // 365
            if delta >= 70:
                raise ValueError("Invalid birth day. Date must be between 0 and 70 days.")
        return value


class GenderField(Validated):
    def validate(self, value):
        super().validate(value)
        if value is not None:
            if type(value) is not int:
                raise ValueError(f'Invalid value. Value {self.name[1:]} must be int')
            if not re.match(r"^[0-2]?$", str(value)):
                raise ValueError(f"Invalid value. Value {self.name[1:]} must be between 0 and 2 digits.")
        return value


class ClientIDsField(Validated):
    def validate(self, value):
        super().validate(value)
        if type(value) is not list:
            raise ValueError(f'Invalid value. Value {self.name[1:]} must be list')
        else:
            for item in value:
                if type(item) is not int:
                    raise ValueError(f'Invalid value. Item {item} must be int')
        return value


class ArgumentsField(Validated):
    phone = PhoneField(required=False, nullable=True)
    email = EmailField(required=False, nullable=True)
    first_name = CharField(required=False, nullable=True)
    last_name = CharField(required=False, nullable=True)
    birthday = BirthDayField(required=False, nullable=True)
    gender = GenderField(required=False, nullable=True)
    client_ids = ClientIDsField(required=True)
    date = DateField(required=False, nullable=True)

    def validate(self, value):
        super().validate(value)
        if type(value) is not dict:
            raise ValueError(f'Invalid value. Value to be dict')

        else:
            for key, val in value.items():
                setattr(self, key, val)
        return value


class ClientsInterestsRequest(object):
    client_ids = ClientIDsField(required=True)
    date = DateField(required=False, nullable=True)

    def __init__(self, request, ctx, store):
        self.body = request.get("body")
        arguments = self.body.get("arguments") or dict()
        if not arguments.get("client_ids"):
            raise ValueError(f'Invalid arguments {arguments}')
        self.client_ids = arguments.get("client_ids")
        self.date = arguments.get("date")
        self.ctx = ctx
        self.store = store

    def clients_interests(self):
        client_ids = self.body.get("arguments").get("client_ids")
        self.ctx.update({"nclients": len(client_ids) if client_ids else 0})
        response = {str(idx + 1): get_interests(self.store, client_id) for idx, client_id in enumerate(client_ids)}
        return OK, response, self.ctx


class OnlineScoreRequest(object):
    first_name = CharField(required=False, nullable=True)
    last_name = CharField(required=False, nullable=True)
    email = EmailField(required=False, nullable=True)
    phone = PhoneField(required=False, nullable=True)
    birthday = BirthDayField(required=False, nullable=True)
    gender = GenderField(required=False, nullable=True)

    def __init__(self, request, ctx, store):
        self.body = request.get("body")
        arguments = self.body.get("arguments") or dict()
        if (bool(arguments.get("email")) + bool(arguments.get("phone"))) != 2 and \
                (bool(arguments.get("first_name")) + bool(arguments.get("last_name"))) != 2 and \
                (bool(arguments.get("birthday")) + (arguments.get("gender") in GENDERS)) != 2:
            raise ValueError(f'Invalid arguments {arguments}')
        self.first_name = arguments.get("first_name")
        self.last_name = arguments.get("last_name")
        self.email = arguments.get("email")
        self.phone = arguments.get("phone")
        self.birthday = arguments.get("birthday")
        self.gender = arguments.get("gender")
        self.ctx = ctx
        self.store = store

    def online_score(self):
        response = {"score": get_score(self.store, **self.body.get("arguments"))}
        self.ctx.update({"has": [item for item in self.body.get("arguments") if item]})
        return OK, response, self.ctx


class MethodRequest(object):
    account = CharField(required=False, nullable=True)
    login = CharField(required=True, nullable=True)
    token = CharField(required=True, nullable=True)
    arguments = ArgumentsField(required=True, nullable=True)
    method = CharField(required=True, nullable=True)

    def __init__(self, **kwargs):
        attr_ignore = set(["account", "is_admin"])
        attrs = set(attr for attr in vars(MethodRequest).keys() if not attr.startswith('__'))
        attrs_kwargs = [k for k in (attrs - set(kwargs) - attr_ignore)]
        if len(attrs_kwargs):
            raise ValueError(f"Missing arguments {attrs_kwargs}")
        self.account = kwargs.get("account") if kwargs.get("account") else ""
        self.login = kwargs.get("login")
        self.method = kwargs.get("method")
        self.token = kwargs.get("token")
        self.arguments = kwargs.get("arguments")

    @property
    def is_admin(self):
        return self.login == ADMIN_LOGIN


def check_auth(request):
    if request.is_admin:
        digest = hashlib.sha512((datetime.datetime.now().strftime("%Y%m%d%H") + ADMIN_SALT).encode('utf-8')).hexdigest()
    else:
        digest = hashlib.sha512((request.account + request.login + SALT).encode('utf-8')).hexdigest()
    return digest == request.token


def method_handler(request, ctx, store):
    response, code = None, None
    body = request.get("body")
    if not body:
        code = INVALID_REQUEST
        response = {"error": ERRORS[code]}
    else:
        try:
            method_request = MethodRequest(**body)
            if check_auth(method_request):
                current_method = body.get("method")
                if current_method == "online_score":
                    code, response, ctx = OnlineScoreRequest(request, ctx, store).online_score()
                    if method_request.is_admin:
                        response = {"score": 42}
                elif current_method == "clients_interests":
                    code, response, ctx = ClientsInterestsRequest(request, ctx, store).clients_interests()
                else:
                    code = BAD_REQUEST
                    response = {"error": ERRORS[code]}
            else:
                code = FORBIDDEN
                response = {"error": ERRORS[code]}
        except ValueError as e:
            code = INVALID_REQUEST
            response = {"error": ERRORS[code] + f" {e}"}
    return response, code


class MainHTTPHandler(BaseHTTPRequestHandler):
    router = {
        "method": method_handler
    }
    store = None

    def get_request_id(self, headers):
        return headers.get('HTTP_X_REQUEST_ID', uuid.uuid4().hex)

    def do_POST(self):
        response, code = {}, OK
        context = {"request_id": self.get_request_id(self.headers)}
        request = None
        try:
            data_string = self.rfile.read(int(self.headers['Content-Length']))
            request = json.loads(data_string)
        except:
            code = BAD_REQUEST

        if request:
            path = self.path.strip("/")
            logging.info("%s: %s %s" % (self.path, data_string, context["request_id"]))
            if path in self.router:
                try:
                    response, code = self.router[path]({"body": request, "headers": self.headers}, context, self.store)
                except Exception as e:
                    logging.exception("Unexpected error: %s" % e)
                    code = INTERNAL_ERROR
            else:
                code = NOT_FOUND

        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        if code not in ERRORS:
            r = {"response": response, "code": code}
        else:
            r = {"error": response or ERRORS.get(code, "Unknown Error"), "code": code}
        context.update(r)
        logging.info(context)
        self.wfile.write(json.dumps(r).encode('utf-8'))
        return


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-p", "--port", action="store", type=int, default=8080)
    parser.add_argument("-l", "--log", action="store", default=None)
    args = parser.parse_args()
    logging.basicConfig(filename=args.log, level=logging.INFO,
                        format='[%(asctime)s] %(levelname).1s %(message)s', datefmt='%Y.%m.%d %H:%M:%S')
    server = HTTPServer(("localhost", args.port), MainHTTPHandler)
    logging.info("Starting server at %s" % args.port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
