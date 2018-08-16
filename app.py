import json
import page_parser
import wallpapers_parser


def load_html(path_to_html_file):
    with open(path_to_html_file, "r") as html_file:
        return html_file.read()


def main():
    html = load_html('/home/pbodyachevsky/PycharmProjects/untitled/wallpapers.html')
    wallpapers_nodes = page_parser.parse_page(html)
    wallpapers = wallpapers_parser.parse_wallpapers(wallpapers_nodes)

    print(json.dumps([ob.__dict__ for ob in wallpapers]))


if __name__ == "__main__":
    main()