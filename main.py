from yattag import Doc
from util import cd, format_time

import os
import json

from view import render_users
from model import Level

output_dir = "deploy"
input_dir = "data"

level_index = []

def main():
    with cd(output_dir):
        with cd("test") as directory:
            with directory.open("ay.txt",'w') as file:
                file.write("success!")

    print("Loading data:")
    for subdir, dirs, names in os.walk(input_dir):
        for name in names:
            with open(os.path.join(subdir, name)) as file:
                data = json.loads(file.read())
                Level.from_json(data)

    for path, html in render_users():
        with cd(output_dir):
            with cd(path) as directory:
                with directory.open("index.html", 'w') as file:
                    file.write(html)


if __name__ == "__main__":
    main()
