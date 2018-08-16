# ostrovok-code-challenge

## challenge:
> Есть прекрасный сайт Smashing Magazine, который каждый месяц выкладывает отличные обои для десктопа. Заходить каждый месяц и проверять, что там нового дело не благородное, поэтому давайте попробуем автоматизировать эту задачу. Требуется написать cli утилиту, которая будет качать все обои в требуемом разрешение за указанный месяц-год в текущую директорию пользователя. Вот тут находятся все обои, а здесь находятся обои за май 2017.
> Условия:
>     Python 3.5+
>     Любые сторонние библиотеки
>     PEP8
>     Если останется время, то можете покрыть её тестами с помощью py.test (:


## solution:

Preparation:
1. Collect all pages
2. Extract from each page links to wallpaper sets
3. Handle each wallpaper sets page:
    * Extract wallpapers
    * Store in sqllite

CLI implementation for wallpapers searching in DB by given criteria.

wallpaper consists of next HTML tags:
* single `<h>` - name
* several `<p>` - description
* single `<figure>` - preview
* single `<ul>` - links to different variants

## Dependencies:
```
scrapy
AdvancedHTMLParser
```

## How to work with:
Repo contains pre-filled sqlite database, which you can use for wallpaper downloading.

To download images posted on 12 2017 in full-size resolution
```python
python app.py -y 2017 -m 12 -r full
```

To dump wallpapers from https://www.smashingmagazine.com/category/wallpapers
```sh
scrapy runspider spider.py 
```
