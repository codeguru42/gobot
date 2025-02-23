import httpx
import typer
from bs4 import BeautifulSoup

url = "https://www.u-go.net/gamerecords/"

def main():
    response = httpx.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.findAll("a")
    for link in links:
        typer.echo(link.get("href"))

if __name__ == '__main__':
    typer.run(main)