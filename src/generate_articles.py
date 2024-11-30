import argparse
import re
from collections import defaultdict
from pathlib import Path

import mistune
from jinja2 import Environment, FileSystemLoader
from bs4 import BeautifulSoup

from custom_filters import register_custom_filters


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



CONTINUOUS_SEPARATOR = "<!-- more -->"
RE_BLOG = re.compile("(?P<date>\d{8})\-(?P<target>.*)\-(?P<lang>(en|ja))\.md")


def generate_blog(environment, contents_dir, output_dir):

    # Collect blog articles markdown
    targets = defaultdict(list)

    for path in contents_dir.glob("*.md"):
        m = RE_BLOG.match(path.name)
        if not m:
            continue

        article = m.groupdict()
        lang = article["lang"]
        target = article["target"]
        with open(path) as f:
            content = f.read()

        article["content"] = mistune.html(content)
        short_content, _, residual = content.partition(CONTINUOUS_SEPARATOR)
        article["short_content"] = mistune.html(short_content.partition("\n")[2])
        article["residual"] = residual
        title = content.splitlines()[0].replace("#", "").strip()
        article["title"] = title

        filename_suffix = f"_{lang}" if lang != "en" else ""
        article["url"] = f"{target}{filename_suffix}.html"

        targets[lang].append(article)

    # Create blog/ directory
    output_dir.mkdir(exist_ok=True)

    # Generate a list of articles html
    index_template = environment.get_template("blog-articles.html.jinja")

    for lang, filename_suffix in (("en", ""), ("ja", "_ja")):
        articles = sorted(
            targets[lang],
            key=lambda data: data["date"],
            reverse=True
        )
        rendered = index_template.render(
            articles=articles,
            lang_option=True,
            lang=lang,
            url_en="/blog/index.html",
            url_ja="/blog/index_ja.html",
        )
        with open(output_dir / f"index{filename_suffix}.html", mode="w", encoding="utf-8") as f:
            f.write(rendered)

    # Generate articles
    blog_template = environment.get_template("blog.html.jinja")

    for lang, filename_suffix in (("en", ""), ("ja", "_ja")):
        for article in targets[lang]:
            target = article["target"]
            rendered = blog_template.render(
                article=article,
                lang_option=True,
                lang=lang,
                url_en=f"{target}.html",
                url_ja=f"{target}_ja.html",
            )
            with open(output_dir / f"{target}{filename_suffix}.html", mode="w", encoding="utf-8") as f:
                f.write(rendered)


def main(output_dir, contents_dir="contents"):
    contents_dir = Path(contents_dir)
    output_dir = Path(output_dir)

    environment = Environment(loader=FileSystemLoader("templates/"))
    register_custom_filters(environment)

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
