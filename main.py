from yattag import Doc
import os

output_dir = "deploy"

def main():
    print("Hello")
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    with open("{}/index.html".format(output_dir), 'w') as file:
        file.write(sample_page())

def sample_page():
    doc, tag, text = Doc().tagtext()

    doc.asis("<!DOCTYPE html>")
    with tag("html"):
        with tag("body"):
            with tag("p"):
                text("Hello World!")
    return doc.getvalue()

if __name__ == "__main__":
    main()
