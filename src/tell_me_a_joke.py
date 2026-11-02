import json
import logging
import sys
from pathlib import Path

import requests


def main():
    repo_dir = Path(__file__).resolve().parents[1]
    data_dir = repo_dir / "data"
    log_dir = repo_dir / "logs"
    data_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        filename=log_dir / "lab4.log",
        level=logging.INFO,
        format="%(message)s",
    )

    try:
        response = requests.get(
            "https://icanhazdadjoke.com/",
            headers={"Accept": "application/json"},
            timeout=10,
        )
    except requests.RequestException:
        logging.error("LAB4_ERR")
        return 1

    if response.status_code != 200:
        logging.error("LAB4_ERR")
        return 1
    logging.info("LAB4_JOKE_HTTP_OK")

    try:
        data = response.json()
    except ValueError:
        logging.error("LAB4_ERR")
        return 1

    joke = data.get("joke") if isinstance(data, dict) else None
    if not isinstance(joke, str) or not joke:
        logging.error("LAB4_ERR")
        return 1
    logging.info("LAB4_JOKE_JSON_OK")

    try:
        with (data_dir / "joke.json").open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)
        with (data_dir / "joke.txt").open("w", encoding="utf-8") as file:
            file.write(joke)
    except OSError:
        logging.error("LAB4_ERR")
        return 1

    print(joke)
    logging.info("LAB4_JOKE_PRINTED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
