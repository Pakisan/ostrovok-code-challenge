class Wallpaper:
    name = ''
    description = ''
    preview_url = ''
    links = ''

    def __init__(self):
        pass


def parse_wallpapers(wallpapers_dom_nodes):
    '''
    Parse wallpapers from dom nodes, which contains tags with wallpapers data.
    :param wallpapers_dom_nodes: dom nodes, which contains tags with wallpapers data.
    :return: list of Wallpaper
    '''
    wallpapers = []

    wallpaper = Wallpaper()

    def parse_links(ul_node):
        '''
        Extracts links from <ul>. It can contains links to image in several resolutions, divided
        to next groups - preview, with calendar, without calendar
        :param ul_node: list of AdvancedTag
        :return: dictionary where keys is links group name and value is list of links
        '''
        wallpaper_links = {}
        for links_group in ul_node.getChildren():
            if links_group.text == '':
                wallpaper_links['preview'] = links_group.getChildren()[0].href
            else:
                links_group_name = links_group.text.split(':')[0]
                links = []

                for link in links_group.getChildren():
                    links.append(link.href)

                wallpaper_links[links_group_name] = links

        return wallpaper_links

    for wallpaper_dom_node in wallpapers_dom_nodes:
        if wallpaper_dom_node.tagName == 'h3' or wallpaper_dom_node.tagName == 'h4':
            wallpaper.name = wallpaper_dom_node.text
        if wallpaper_dom_node.tagName == 'p':
            if wallpaper.description != '' and wallpaper_dom_node.text != '':
                wallpaper.description = wallpaper.description + wallpaper_dom_node.text + '\n'
            else:
                wallpaper.description = wallpaper_dom_node.text
        if wallpaper_dom_node.tagName == 'figure':
            # figure contains <a> with link to preview
            wallpaper.preview_url = wallpaper_dom_node.getChildren()[0].href
        if wallpaper_dom_node.tagName == 'ul':
            wallpaper.links = parse_links(wallpaper_dom_node)

            wallpapers.append(wallpaper)
            wallpaper = Wallpaper()

    return wallpapers
