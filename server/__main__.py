import os

from server import init_api

HOST = os.getenv("HOST") or "127.0.0.1"


def main():
    """
    Main function for fileuploader server
    """
    app = init_api()
    app.run(host=HOST, port=8080, debug=False)


if __name__ == "__main__":
    main()
