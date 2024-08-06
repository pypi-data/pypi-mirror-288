# AO3 Parser
Tools for parsing AO3 pages and creating urls based on requirements.

Main advantage over similar packages is it's complete control over requests to AO3.
Instead of handling requests on it's own, it shifts this to the user, giving more room for optimization.
The main bottleneck for anyone in need of collecting larger amounts of data.
(Scraping data for AI training is discouraged)

If this is not what you're looking for, I'd recommend [ao3_api](https://github.com/ArmindoFlores/ao3_api) that handles requests on it's own.

## Installation
```bash
pip install ao3-parser
```

# Usage
An average user will find themselves using two main modules the most, `Search` and `Page`. 

## Search
Common example of using `Search` would look like this.
Just like on AO3, pages are numbered from 1 and up.

```python
import AO3Parser as AO3P
from AO3Parser import Params
from datetime import datetime

search = AO3P.Search("Original Work", Sort_by=Params.Sort.Kudos,
                     Include_Ratings=[Params.Rating.General_Audiences],
                     Words_From=1000, Words_To=1500,
                     Date_From=datetime(2024, 6, 30))
url = search.GetUrl(page=1)
print(f"URL: {url}")
```
```
URL: https://archiveofourown.org/works?commit=Sort+and+Filter&page=1&work_search%5Bsort_colum%5D=Kudos&tag_id=Original+Work&include_work_search%5Brating_ids%5D%5B%5D=10&work_search%5Bwords_from%5D=1000&work_search%5Bwords_to%5D=1500&work_search%5Bdate_from%5D=2024-06-30
```

## Page

```python
import AO3Parser as AO3P
import requests

search = AO3P.Search("Original Work")
url = search.GetUrl()
page_data = requests.get(url).content

page = AO3P.Page(page_data)
print(f"Total works: {page.Total_Works}")
print(f"Works on page: {len(page.Works)}")
print(f"Title of the first work: [{page.Works[0].Title}]")
```
```
Total works: 282069
Works on page: 20
Title of the first work: [Title Of This Work]
```

### Notes
`Params.Category.No_Category` is not recognized as a valid ID on AO3 and should not be used with `Search`.