from .extra import Extra
from .params import Params

from datetime import datetime
import urllib.parse

class Search:

    Fandom: str
    Sort_by: Params.Sort
    Include_Ratings: list[Params.Rating]
    Include_Warnings: list[Params.Warning]
    Include_Categories: list[Params.Category]
    Exclude_Ratings: list[Params.Rating]
    Exclude_Warnings: list[Params.Warning]
    Exclude_Categories: list[Params.Category]
    Crossovers: Params.Crossovers
    Completion_Status: Params.Completion
    Words_From: int
    Words_To: int
    Date_From: datetime
    Date_To: datetime

    def __init__(self, Fandom: str, Sort_by=Params.Sort.Revised,
                 Include_Ratings: list[Params.Rating] = None, Include_Warnings: list[Params.Warning] = None, Include_Categories: list[Params.Category] = None,
                 Exclude_Ratings: list[Params.Rating] = None, Exclude_Warnings: list[Params.Warning] = None, Exclude_Categories: list[Params.Category] = None,
                 Crossovers: Params.Crossovers = Params.Crossovers.Include, Completion_Status: Params.Completion = Params.Completion.All,
                 Words_From: int = None, Words_To: int = None, Date_From: datetime = None, Date_To: datetime = None):
        self.Fandom = Fandom
        self.Sort_by = Sort_by
        self.Include_Ratings = Extra.MakeIter(Include_Ratings)
        self.Include_Warnings = Extra.MakeIter(Include_Warnings)
        self.Include_Categories = Extra.MakeIter(Include_Categories)
        self.Exclude_Ratings = Extra.MakeIter(Exclude_Ratings)
        self.Exclude_Warnings = Extra.MakeIter(Exclude_Warnings)
        self.Exclude_Categories = Extra.MakeIter(Exclude_Categories)
        self.Crossovers = Crossovers
        self.Completion_Status = Completion_Status
        self.Words_From = Words_From
        self.Words_To = Words_To
        self.Date_From = Date_From
        self.Date_To = Date_To

    def getParams(self, page=1) -> dict:
        params = {
            "page": page,
            "work_search[sort_colum]": self.Sort_by.name,
            "tag_id": self.Fandom
        }
        if self.Include_Ratings:
            params["include_work_search[rating_ids][]"] = Extra.EnumsToValues(self.Include_Ratings)
        if self.Include_Warnings:
            params["include_work_search[archive_warning_ids][]"] = Extra.EnumsToValues(self.Include_Warnings)
        if self.Include_Categories:
            params["include_work_search[category_ids][]"] = Extra.EnumsToValues(self.Include_Categories)
        if self.Exclude_Ratings:
            params["exclude_work_search[rating_ids][]"] = Extra.EnumsToValues(self.Exclude_Ratings)
        if self.Exclude_Warnings:
            params["exclude_work_search[archive_warning_ids][]"] = Extra.EnumsToValues(self.Exclude_Warnings)
        if self.Exclude_Categories:
            params["exclude_work_search[category_ids][]"] = Extra.EnumsToValues(self.Exclude_Categories)
        if self.Crossovers and self.Crossovers.value:
            params["work_search[crossover]"] = self.Crossovers.value
        if self.Completion_Status and self.Completion_Status.value:
            params["work_search[complete]"] = self.Completion_Status.value
        if self.Words_From:
            params["work_search[words_from]"] = self.Words_From
        if self.Words_To:
            params["work_search[words_to]"] = self.Words_To
        if self.Date_From:
            params["work_search[date_from]"] = self.Date_From.strftime("%Y-%m-%d")
        if self.Date_To:
            params["work_search[date_to]"] = self.Date_To.strftime("%Y-%m-%d")
        return params

    def GetUrl(self, page=1) -> str:
        return f"https://archiveofourown.org/works?commit=Sort+and+Filter&{urllib.parse.urlencode(self.getParams(page), doseq=True)}"
