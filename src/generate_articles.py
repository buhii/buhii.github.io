import argparse
import re
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from bs4 import BeautifulSoup


def prettify(content):
    soup = BeautifulSoup(content, features="html.parser")
    return soup.prettify()


def render(base_template, content_path, output_path):
    with open(content_path) as f:
        content = f.read()
    rendered = base_template.render(
        content=content,
    )
    with open(output_path, mode="w", encoding="utf-8") as f:
        f.write(rendered)


RE_BLOG = re.compile("(?P<date>\d{8})\-(?P<target>.*)\-(?P<lang>(en|ja))\.md")


def generate_blog(environment, contents_dir, output_dir):

    # Collect blog articles markdown
    targets = []
    for path in contents_dir.glob("*.md"):
        m = RE_BLOG.match(path.name)
        if not m:
            continue
        targets.append(m.groupdict())

    articles = sorted(
        targets,
        key=lambda d: d["date"],
        reverse=True,
    )

    # Generate a list of articles html
    output_dir.mkdir(exist_ok=True)

    index_template = environment.get_template("blog-articles.html.jinja")
    rendered = index_template.render(
        articles=articles,
        lang_option=True,
    )
    with open(output_dir / "index.html", mode="w", encoding="utf-8") as f:
        f.write(rendered)


def main(output_dir, contents_dir="contents"):
    contents_dir = Path(contents_dir)
    output_dir = Path(output_dir)

    environment = Environment(loader=FileSystemLoader("templates/"))

    render(
        environment.get_template("misc.html.jinja"),
        contents_dir / "about.md",
        output_dir / "index.html"
    )
    render(
        environment.get_template("misc.html.jinja"),
        contents_dir / "underconstruction.md",
        output_dir / "projects" / "index.html"
    )
    generate_blog(
        environment,
        contents_dir,
        output_dir / "blog"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="blog generator",
        description="my boring blog generator",
    )

    parser.add_argument("--dest", default="../")
    args = parser.parse_args()
    main(args.dest)
