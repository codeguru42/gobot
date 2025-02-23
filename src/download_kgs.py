import httpx
import typer

url = "https://www.u-go.net/gamerecords/"

def main():
    response = httpx.get(url)
    typer.echo(response.status_code)
    typer.echo(response.text)

if __name__ == '__main__':
    typer.run(main)