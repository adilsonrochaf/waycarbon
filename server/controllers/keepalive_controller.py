from flask_jwt import jwt_required


@jwt_required()
def get_alive():  # noqa: E501
    """Api keepalive

    Api keepalive # noqa: E501


    :rtype: None
    """
    return "pong", 200
