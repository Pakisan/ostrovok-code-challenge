import AdvancedHTMLParser
import scrapy


def extract_date(html):
    div_with_wallpapers = scrapy.Selector(text=html).css('.c-garfield-the-cat').extract()[0]

    html_parser = AdvancedHTMLParser.AdvancedHTMLParser()
    html_parser.parseStr(div_with_wallpapers)

    dateTime = html_parser.getRootNodes()[0].getElementsByClassName('article__date')[0].dateTime.split('-')

    date = dict()
    date['month'] = dateTime[1]
    date['year'] = dateTime[0]

    return date


def parse_page(html):
    '''
    Extracts wallpapers from given page.
    :param html: page as html
    :return: dom nodes, which contains tags with wallpapers data.
    '''
    div_with_wallpapers = scrapy.Selector(text=html).css('.c-garfield-the-cat').extract()[0]

    html_parser = AdvancedHTMLParser.AdvancedHTMLParser()

    html_parser.parseStr(div_with_wallpapers)
    html_nodes = html_parser.getRootNodes()
    wallpapers_nodes = clean_nodes(html_nodes[0].getChildren())

    return wallpapers_nodes


def clean_nodes(html_nodes):
    '''
    Removes html tags from node, which doesn't belongs to wallpapers.
    :param html_nodes: list<AdvancedTag>
    :return: wallpapers nodes
    '''

    first_wallpaper_index = -1
    last_wallpaper_index = -1

    def first_wallpaper_tag_predicate(html_node):
        return html_node.tagName == 'figure' \
               and html_node.className == '' \
               and first_wallpaper_index == -1

    def last_wallpaper_html_tag_predicate(html_node):
        return html_node.tagName == 'figure' \
               and html_node.className == ''

    def determine_start_of_wallpapers(nodes, index):
        '''
        Iterates over html tags, to find begin of wallpapers.
        Wallpaper has 2 or more tags. But always starts from <h>
        :param nodes: list<AdvancedTag>
        :param index: first_wallpaper_index
        :return: index of <h> tag, or given index if <h> tag was not found
        '''
        for i in range(index, -1, -1):
            node = nodes[i]

            if node.tagName == 'h3' or node.tagName == 'h4':
                return i

        return index

    def determine_end_of_wallpapers(nodes, begin_index):
        '''
        Iterates over html tags, to find end of wallpapers.
        Wallpaper has 2 or more tags under. But always ends with <ul>
        :param nodes: list<AdvancedTag>
        :param begin_index: first_wallpaper_index
        :return: index of <h> tag, or given index if <h> tag was not found
        '''
        for i in range(begin_index, len(nodes)):
            node = nodes[i]

            if node.tagName == 'ul':
                return i

        return index

    for index, html_node in enumerate(html_nodes):
        if first_wallpaper_tag_predicate(html_node):
            first_wallpaper_index = index
        if last_wallpaper_html_tag_predicate(html_node):
            last_wallpaper_index = index

    first_wallpaper_index = determine_start_of_wallpapers(html_nodes, first_wallpaper_index)
    last_wallpaper_index = determine_end_of_wallpapers(html_nodes, last_wallpaper_index)

    # TODO: fix incorrect slice by last index.
    return html_nodes[first_wallpaper_index:last_wallpaper_index]