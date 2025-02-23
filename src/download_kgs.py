from pathlib import Path

import httpx
import typer
from bs4 import BeautifulSoup

kgs_url = "https://www.u-go.net/gamerecords/"


def main(output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    for link in tar_links(kgs_url):
        response = httpx.get(link)
        with open(output_dir / link.split("/")[-1], "wb") as f:
            f.write(response.content)


def tar_links(url: str):
    response = httpx.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a")
    for link in links:
        href = link.get("href")
        if href.endswith(".tar.gz"):
            yield href


if __name__ == "__main__":
    typer.run(main)
