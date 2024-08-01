# -*- coding: UTF-8 -*-

import typing

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from starlette.datastructures import State, URLPath
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.errors import ServerErrorMiddleware
from starlette.middleware.exceptions import ExceptionMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import BaseRoute, Router
from starlette.types import ASGIApp, ExceptionHandler, Receive, Scope, Send

from muso.response import ORJSONResponse
from muso.route import RouteGroup
from muso.schema import StarletteFileField


class Muso:

    def __init__(self, *, name: str, version: str, description: str,
                 debug: bool = False) -> None:
        self.name = name
        self.version = version
        self.description = description
        self.debug = debug
        self.state = State()
        self.on_startup_func_list: list[typing.Callable[[], typing.Any]] = []
        self.on_shutdown_func_list: list[typing.Callable[[], typing.Any]] = []
        self.route_group_list: list[RouteGroup] = []
        self.router: Router | None = None
        self.exception_handlers: dict[typing.Any, ExceptionHandler] = dict()
        self.user_middleware: list[Middleware] = []
        self.middleware_stack: ASGIApp | None = None

    def add_route_group(self, route_group: RouteGroup) -> None:
        if self.middleware_stack is not None:
            raise RuntimeError(
                'Cannot add route group after an application has started')
        self.route_group_list.append(route_group)

    def _apispec(self):
        marshmallow_plugin = MarshmallowPlugin()
        spec = APISpec(
            title=self.name, version=self.version, openapi_version='3.1.0',
            plugins=[marshmallow_plugin],
            info=dict(description=self.description))
        marshmallow_plugin.converter.add_attribute_function(
            _file_field_to_properties)

        for route_group in self.route_group_list:
            spec.tag(dict(name=route_group.tag,
                          description=route_group.description))
            for route in route_group.route_list:
                method = route.method.lower()
                operations = {route.method.lower(): dict(
                    tags=[route_group.tag],
                    description=(route.endpoint.__doc__ or '').strip(),
                )}
                if route.query_args_schema:
                    operations[method]['parameters'] = [
                        {'in': 'query', 'schema': route.query_args_schema}]
                if route.form_data_schema:
                    fds = route.form_data_schema
                    operations[method]['requestBody'] = dict(content=dict())
                    exist_file_upload = any(
                        isinstance(field, StarletteFileField)
                        for field in fds.fields.values())
                    if exist_file_upload:
                        operations[method]['requestBody']['content'] = {
                            'multipart/form-data': dict(
                                schema=fds,
                                # encoding={
                                #     field.data_key: {
                                #         'contentType': ', '.join(
                                #             field.content_type_list)}
                                #     for field in fds.fields.values()
                                #     if isinstance(field, StarletteFileField)}
                            )}
                    else:
                        operations[method]['requestBody']['content'] = {
                            'application/x-www-form-urlencoded': dict(
                                schema=route.form_data_schema),
                        }
                if route.json_body_schema:
                    operations[method]['requestBody'] = dict(
                        content={'application/json': dict(
                            schema=route.json_body_schema)})
                if route.streaming_response:
                    pass
                else:
                    if not route.response_schema:
                        data_spec = dict(
                            example=dict(code=0, msg='', data=None))
                    else:
                        data_spec = dict(schema=route.response_schema)

                    operations[method]['responses'] = {
                        200: dict(content={'application/json': data_spec})}

                spec.path(path=route.path, operations=operations)

        self.router.add_route(
            path='/openapi.json',
            endpoint=lambda _: ORJSONResponse(spec.to_dict()),
            methods=['GET'])

    def build_middleware_stack(self) -> ASGIApp:
        self.router = Router(on_startup=self.on_startup_func_list,
                             on_shutdown=self.on_shutdown_func_list)
        for route_group in self.route_group_list:
            for route in route_group.route_list:
                self.router.add_route(
                    path=route.path, endpoint=route.endpoint,
                    methods=[route.method])

        if self.debug:
            self._apispec()

        error_handler = None
        exception_handlers: dict[
            typing.Any, typing.Callable[[Request, Exception], Response]
        ] = {}

        for key, value in self.exception_handlers.items():
            if key in (500, Exception):
                error_handler = value
            else:
                exception_handlers[key] = value

        middleware = (
                [Middleware(ServerErrorMiddleware, handler=error_handler,
                            # noqa
                            debug=self.debug)] +
                self.user_middleware +
                [Middleware(ExceptionMiddleware, handlers=exception_handlers,
                            # noqa
                            debug=self.debug)])

        app = self.router
        for cls, args, kwargs in reversed(middleware):
            app = cls(app=app, *args, **kwargs)
        return app

    @property
    def routes(self) -> list[BaseRoute]:
        return self.router.routes

    def url_path_for(self, name: str, **path_params: typing.Any) -> URLPath:
        return self.router.url_path_for(name, **path_params)

    async def __call__(self, scope: Scope, receive: Receive,
                       send: Send) -> None:
        scope['app'] = self
        if self.middleware_stack is None:
            self.middleware_stack = self.build_middleware_stack()
        await self.middleware_stack(scope, receive, send)

    def mount(self, path: str, app: ASGIApp, name: str | None = None) -> None:
        self.router.mount(path, app=app, name=name)  # pragma: no cover

    def host(self, host: str, app: ASGIApp, name: str | None = None) -> None:
        self.router.host(host, app=app, name=name)  # pragma: no cover

    def exception_handler(
            self, exc_class_or_status_code: int | type[Exception]
    ) -> typing.Callable:  # type: ignore[type-arg]

        def decorator(
                func: typing.Callable) -> typing.Callable:  # type: ignore[type-arg]  # noqa: E501
            self.exception_handlers[exc_class_or_status_code] = func
            return func

        return decorator

    def middleware(self, middleware_type: str) -> typing.Callable:
        assert (
                middleware_type == "http"
        ), 'Currently only middleware("http") is supported.'

        def decorator(func: typing.Callable) -> typing.Callable:
            if self.middleware_stack is not None:  # pragma: no cover
                raise RuntimeError(
                    "Cannot add middleware after an application has started")
            self.user_middleware.insert(
                0, Middleware(BaseHTTPMiddleware, dispatch=func))  # noqa
            return func

        return decorator

    def on_startup(self, func):
        self.on_startup_func_list.append(func)
        return func

    def on_shutdown(self, func):
        self.on_shutdown_func_list.append(func)
        return func


def _file_field_to_properties(self, field, **kwargs):
    if isinstance(field, StarletteFileField):
        return dict(type='string', format='binary')
    return dict()
