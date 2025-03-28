from pathlib import Path

import httpx
import typer
from bs4 import BeautifulSoup
from furl import furl

kgs_url = "https://www.u-go.net/gamerecords/"


def main(output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    for link in tar_links(kgs_url):
        response = httpx.get(link)
        parsed_link = furl(link)
        with open(output_dir / parsed_link.path.segments[-1], "wb") as f:
            f.write(response.content)


def tar_links(url: str):
    response = httpx.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a")
    for link in links:
        href = link.get("href")
        typer.echo(f"Link found: {href}", nl=False)
        if href.endswith(".tar.gz"):
            typer.echo(" ...downloading")
            yield href
        else:
            typer.echo(" ...skipping")


if __name__ == "__main__":
    typer.run(main)
