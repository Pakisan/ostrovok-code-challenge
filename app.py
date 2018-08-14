import page_parser


def load_html(path_to_html_file):
    with open(path_to_html_file, "r") as html_file:
        return html_file.read()


def main():
    html = load_html('/home/pbodyachevsky/PycharmProjects/untitled/wallpapers.html')
    print(page_parser.parse_page(html))


if __name__ == "__main__":
    main()