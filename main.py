from website import create_app, models
from argparse import ArgumentParser
from website.database import engine

models.Base.metadata.create_all(bind=engine)

arg_parser = ArgumentParser()

arg_parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")
arg_parser.add_argument(
    "-s", "--scrape", action="store_true", help="Scrape the website."
)

args = arg_parser.parse_args()

if args.scrape:
    from scraper.scrape import scrape

    scrape()

    print("Scraping done.")
    exit()

app = create_app()

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
