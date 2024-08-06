from .extra import RateLimitException
from .params import Params
from .work import Work

import bs4
from datetime import datetime

class Page:
    Total_Works: int
    Works: list[Work]

    def __init__(self, html: bytes):
        if html == b"Retry later\n":
            raise RateLimitException
        html = bs4.BeautifulSoup(html, "html.parser")
        self.Total_Works = int(html.find("h2", class_="heading").text.strip().split(' ')[4].replace(',', ''))

        self.Works = []
        for work in html.findAll(role="article"):
            authors: list[str] = []
            for author in work.find("h4", class_="heading").findAll("a", rel="author"):
                authors.append(author.text)

            fandoms: list[str] = []
            for fandom in work.find("h5", class_="fandoms heading").findAll("a", class_="tag"):
                fandoms.append(fandom.text)

            stats = work.find(class_="stats")
            chapters, expected_chapters = stats.find("dd", class_="chapters").text.split('/')

            req_tags = work.find("ul", class_="required-tags").findAll("span", class_="text")

            tags = work.find("ul", class_="tags commas").findAll("li")
            relationships: list[str] = []
            characters: list[str] = []
            freeforms: list[str] = []
            for tag in tags:
                name = tag.find("a", class_="tag").text
                if tag["class"] == ['relationships']:
                    relationships.append(name)
                elif tag["class"] == ['characters']:
                    characters.append(name)
                elif tag["class"] == ['freeforms']:
                    freeforms.append(name)

            def parseStats(stat: bs4.element.Tag | None) -> int:
                return int(stat.text.replace(',', '')) if stat and stat.text else 0

            self.Works.append(
                Work(int(work["id"].split('_')[1]),                                         # ID
                work.find("a").text,                                                        # Title
                authors,                                                                    # Authors
                fandoms,                                                                    # Fandoms
                stats.find("dd", class_="language").text,                                   # Language
                parseStats(stats.find("dd", class_="words")),                               # Words
                int(chapters.replace(',', '')),                                             # Chapters
                int(expected_chapters.replace(',', '') if expected_chapters != '?' else 0), # nChapters
                parseStats(stats.find("dd", class_="comments")),                            # Comments
                parseStats(stats.find("dd", class_="kudos")),                               # Kudos
                parseStats(stats.find("dd", class_="bookmarks")),                           # Bookmarks
                parseStats(stats.find("dd", class_="hits")),                                # Hits
                datetime.strptime(work.find(class_="datetime").text, "%d %b %Y"),   # UpdateDate
                Params.parseRating(req_tags[0].text),                                       # Rating
                Params.parseCategories(req_tags[2].text.split(", ")),                       # Categories
                Params.parseWarnings(req_tags[1].text.split(", ")),                         # Warnings
                True if work.find("span", class_="complete-yes iswip") else False,          # Completed
                relationships, characters, freeforms))                                      # Tags