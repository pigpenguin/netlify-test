from yattag import Doc
from util import cd, format_time

import os
import json

output_dir = "deploy"
input_dir = "data"

level_index = []

def main():
    for subdir, dirs, names in os.walk(input_dir):
        for name in names:
            with open(os.path.join(subdir, name)) as file:
                data = json.loads(file.read())
                level_page(data)

    index_page()

def index_page():
    levels = sorted(level_index, key = lambda kv: kv[2], reverse=True)

    doc, tag, text = Doc().tagtext()
    with tag("ul"):
        for level in levels:
            steam_id = level[0]
            name = level[1]
            times = level[2]
            with tag("li"):
                with tag("a", href="./levels/{}/".format(steam_id)):
                    text("{}".format(name))
                text(" - {}".format(times))

    with cd(output_dir) as directory:
        with directory.open("index.html", 'w') as file:
            file.write(template(doc.getvalue()))

def level_page(json_data):
    # Get the leaderboard
    leaderboard = json_data["leaderboard"]

    # Register level with index
    level_index.append((json_data["id"],json_data["displayName"], len(leaderboard)))

    # Render the leaderboard
    doc, tag, text = Doc().tagtext()
    with tag("table"):
        for rank, entry in enumerate(leaderboard):
            with tag("tr"):
                with tag("td"):
                    text(rank+1)
                with tag("td"):
                    text(entry["player"]["displayName"])
                with tag("td"):
                    text(format_time(entry["time"]))

    # Write the webpage
    path = os.path.join(output_dir, "level", str(json_data["id"]))
    with cd(path) as directory:
        with directory.open("index.html", 'w') as file:
            file.write(template(doc.getvalue()))

def template(content):
    doc, tag, text = Doc().tagtext()
    doc.asis("<!DOCTYPE html>")
    with tag("html"):
        with tag("body"):
            doc.asis(content)

    return doc.getvalue()

if __name__ == "__main__":
    main()
