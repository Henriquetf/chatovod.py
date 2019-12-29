from chatovod.api.endpoints import Route


def test_path():
    method = "POST"
    path = "/login"

    login_route = Route(method, path)

    assert login_route.method == method
    assert login_route.path == path
