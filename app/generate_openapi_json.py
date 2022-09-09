import json
from pathlib import Path

from fastapi.openapi.utils import get_openapi

from app.main import app

cwd = Path(__file__).cwd()

output_dir = cwd.joinpath("assets")


def main():
    if not output_dir.exists():
        output_dir.mkdir()

    with open(output_dir.joinpath("openapi.json"), "w") as f:
        json.dump(
            get_openapi(
                title=app.title,
                version=app.version,
                openapi_version=app.openapi_version,
                description=app.description,
                routes=app.routes,
            ),
            f,
        )


if __name__ == "__main__":
    main()
