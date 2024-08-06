from argparse import ArgumentParser
from asyncio import run
from datetime import datetime
from json import dumps as json_dumps

from xanthus.utils.x import get_weekly_bookmarks
from xanthus.utils.x import read_post


async def main(bookmarks_link: str = "https://x.com/i/bookmarks/all") -> None:
    weekly_updates = []
    bookmarks = await get_weekly_bookmarks(bookmarks_link, limit=10)
    for bookmark in bookmarks:
        try:
            post = await read_post(bookmark)
        except Exception as e:
            print(f"Error reading post due to {e}, retrying...")
            try:
                post = await read_post(bookmark)
            except Exception as e:
                print(f"Error reading post due to {e}")
                continue
        weekly_updates.append(post)
    out = json_dumps(weekly_updates, indent=2)
    print(out)

    out_name = f"weekly_updates_{datetime.now().strftime('%Y-%m-%d')}.json"
    with open(out_name, "w") as f:
        f.write(out)
    return


def run_main():
    parser = ArgumentParser(description="Get weekly updates from x.com")
    parser.add_argument("--bookmarks", help="Get weekly bookmarks")
    args = parser.parse_args()

    run(main(args.bookmarks))


if __name__ == "__main__":
    run_main()
