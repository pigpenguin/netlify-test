import util
from yattag import Doc
from model import User, Level

from progressbar import ProgressBar

from itertools import chain

# User html stuff
def user_html(user):
    results = sorted(user.results.items(), key = lambda kv: kv[1])

    doc, tag, text, line = Doc().ttl()
    with tag("header"):
        line("h1", user.display_name)
        doc.stag("hr")
        line("h2", "Summary")
        with tag("ul"):
            with tag("li"):
                line("a", "Steam Community", href=user.community_url())
            line("li", "{} first place times".format(user.first_place))
            line("li", "{} page one times".format(user.page_one))
            line("li", "{} total times".format(len(user.results)))

        doc.stag("hr")
        line("h2", "All Times")
        doc.stag("hr")

    with tag("div", klass="body"):
        with tag("table"):
            doc.asis(result_list(results))

    return template(doc.getvalue(), root="../../../")

def result_list(results):
    doc, tag, text = Doc().tagtext()
    with tag("tb"):
        for level_id, rank in results:
            with tag("tr"):
                level = Level.levels[level_id]
                url = "../../../levels/{}/".format(level.level_id)
                with tag("td"):
                    with tag("a",href=url):
                        text(level.display_name, ":    ")
                    with tag("td"):
                        text(util.format_place(rank))
    return doc.getvalue()

def render_users():
    users, stats = User.compute_stats()
    print("rendering user pages")
    with ProgressBar(max_value = len(users)) as bar:
        for i, data in enumerate(users):
            steam_id = data[0]
            user = data[1]
            path="users/{}/".format(steam_id)
            yield path, user_html(user)
            bar.update(i)

    print("rendering user index page")
    doc, tag, text, line = Doc().ttl()
    with tag("header"):
        line("h1", "Users")
        doc.stag("hr")
        with tag("p"):
            text("There are a total of ")
            line("b", "{:,}".format(stats["total users"]))
            text(" players with a total of ")
            line("b", "{:,}".format(stats["total times"]))
            text(" times set for an average of ")
            line("b", "{:,}".format(stats["average times"]))
            text(" times per player.")
        doc.stag("hr")
    with tag("div", klass="body"):
        with tag("table", klass="user-list"):
            with tag("tb"):
                doc.asis(user_list(users))

    yield "users", template(doc.getvalue())

def user_list(users):
    doc, tag, text = Doc().tagtext()
    for steam_id, user in users:
        with tag("tr"):
            with tag("td", klass="name"):
                with tag("a", href="./{}/".format(steam_id)):
                    text(user.display_name)
            with tag("td", klass="times"):
                text("{:,} times".format(len(user.results)))
    return doc.getvalue()



# Wrapper for generic stuff that needs to happen
def template(html, root=None):
    if root:
        css_url = "\"{}/style.css\"".format(root)
    else:
        css_url = "\"./style.css\""

    doc, tag, text = Doc().tagtext()
    doc.asis("<!DOCTYPE html>")
    with tag("html"):
        with tag("head"):
            doc.asis("<link rel=\"stylesheet\" href={}>".format(css_url))
            doc.asis("<meta charset=\"utf-8\">")
            doc.asis("<link href=\"https://fonts.googleapis.com/css?family=Roboto|Roboto+Mono\" rel=\"stylesheet\">")
        with tag("body"):
            with tag("div", klass="container"):
                doc.asis(html)

    return(doc.getvalue())


