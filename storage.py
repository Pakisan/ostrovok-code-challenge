import sqlite3


def create():
    conn = sqlite3.connect("mydatabase.db")  # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()

    # Создание таблицы
    cursor.execute("""CREATE TABLE IF NOT EXISTS albums
                      (title text, artist text, release_date text,
                       publisher text, media_type text)
                   """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS wallpapers (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name text,
                  description text,
                  year text,
                  month text
                );""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS wallpaper_links (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  wallpaper_id INTEGER,
                  resolution text,
                  link text,
                  with_calendar int,
                  FOREIGN KEY(wallpaper_id) REFERENCES wallpapers(id)
                );""")


    # Вставляем данные в таблицу
    cursor.execute("""INSERT INTO albums
                      VALUES ('Glow', 'Andy Hunter', '7/24/2012',
                      'Xplore Records', 'MP3')"""
                   )
    # Сохраняем изменения
    conn.commit()
    conn.close()

def save(wallpapers):
    print('saving...')

    conn = sqlite3.connect("mydatabase.db")  # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()

    for wallpaper in wallpapers:
        print(' %s' % wallpaper.name)
        cursor.execute("""INSERT INTO wallpapers(name, description, year, month) VALUES (?, ?, ?, ?);""",
                       (wallpaper.name, wallpaper.description, wallpaper.year, wallpaper.month))
        conn.commit()
        wallpaper_id = cursor.lastrowid

        if 'preview' in wallpaper.links:
            cursor.execute("""INSERT INTO wallpaper_links(wallpaper_id, resolution, link, with_calendar) VALUES (?, 'full', ?, 0);""",
                           (wallpaper_id, wallpaper.links['preview']))
            conn.commit()
        if 'without calendar' in wallpaper.links:
            for links in wallpaper.links['without calendar']:
                for resolution in links.keys():
                    cursor.execute(
                        """INSERT INTO wallpaper_links(wallpaper_id, resolution, link, with_calendar) VALUES (?, ?, ?, 0);""",
                        (wallpaper_id, resolution, links[resolution]))
                    conn.commit()
        if 'with calendar' in wallpaper.links:
            for links in wallpaper.links['with calendar']:
                for resolution in links.keys():
                    cursor.execute(
                        """INSERT INTO wallpaper_links(wallpaper_id, resolution, link, with_calendar) VALUES (?, ?, ?, 1);""",
                        (wallpaper_id, resolution, links[resolution]))
                    conn.commit()

    conn.close()


def find_wallpapers_links(resolution, year, month):
    conn = sqlite3.connect("mydatabase.db")  # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()

    cursor.execute(
        """SELECT wallpaper_links.link, wallpapers.name FROM wallpapers
                LEFT JOIN wallpaper_links ON wallpaper_links.wallpaper_id = wallpapers.id
            WHERE wallpapers.year = ? and wallpapers.month = ? and wallpaper_links.resolution = ?""",
        (year, month, resolution))

    return cursor.fetchall()