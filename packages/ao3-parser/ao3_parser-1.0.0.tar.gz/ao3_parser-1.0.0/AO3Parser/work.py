from .params import Params

from datetime import datetime

class Work:
    ID: int
    Title: str
    Authors: list[str]
    Fandom: list[str]
    Language: str

    Words: int
    Chapters: int
    Expected_Chapters: int
    Comments: int
    Kudos: int
    Bookmarks: int
    Hits: int
    UpdateDate: datetime

    Rating: Params.Rating
    Categories: list[Params.Category]
    Warnings: list[Params.Warning]
    Completed: bool

    Relationships: list[str]
    Characters: list[str]
    Additional_Tags: list[str]

    def __init__(self, ID: int, Title: str, Authors: [str], Fandom: list[str], Language: str,
                 Words: int, Chapters: int, Expected_Chapters: int, Comments: int, Kudos: int, Bookmarks: int, Hits: int, UpdateTime: datetime,
                 Rating: Params.Rating, Categories: list[Params.Category], Warnings: list[Params.Warning], Completed: bool,
                 Relationships: list[str], Characters: list[str], Additional_Tags: list[str]):
        self.ID = ID
        self.Title = Title
        self.Authors = Authors
        self.Fandom = Fandom
        self.Language = Language

        self.Words = Words
        self.Chapters = Chapters
        self.Expected_Chapters = Expected_Chapters
        self.Comments = Comments
        self.Kudos = Kudos
        self.Bookmarks = Bookmarks
        self.Hits = Hits
        self.UpdateDate = UpdateTime

        self.Rating = Rating
        self.Categories = Categories
        self.Warnings = Warnings
        self.Completed = Completed

        self.Relationships = Relationships
        self.Characters = Characters
        self.Additional_Tags = Additional_Tags

    def __str__(self):
        return f"<Work_{self.ID}>"

    def __repr__(self):
        return self.__str__()