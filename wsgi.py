from app.router.router import Router

router = Router()


def application(environ, start_response):
    request_method = environ["REQUEST_METHOD"]
    path_info = environ["PATH_INFO"]
    query_string = environ["QUERY_STRING"]

    content_length = environ.get("CONTENT_LENGTH", None)
    body = str()
    if content_length is not None:
        content_length = int(content_length)
        body = environ["wsgi.input"].read(content_length).decode()

    controller_method = router.get_controller_method(request_method, path_info)
    response = controller_method(query_string, body)

    resp_body = response.to_str().encode()
    content_length = str(len(resp_body))

    start_response(
        response.get_status(),
        [
            ("Content-Length", content_length),
            ("Content-Type", "application/json"),
            ("Access-Control-Allow-Origin", "*"),
        ],
    )
    return [resp_body]
