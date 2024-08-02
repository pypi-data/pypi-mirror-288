# GoFundMeScrapper
A small library to scrap GoFundMe campaigns. 

To install
```
pip insall gofundmescraper
```


Use as follows:
```python

from scraper import GoFundMeScraper

urls = [
    "https://gofund.me/5ac19b38",
    "https://gofund.me/c53cf071",
    "https://gofund.me/5ac19b38",
    "https://gofund.me/474eed77",
    "https://gofund.me/ceef5eae"
]

scraper = GoFundMeScraper(class_values = {
                "title": "p-campaign-title",
                "description": "p-campaign-description",
                "progress": "progress-meter_progressMeter",
                "hero_image": "campaign-hero_image",
                "creation_date": "m-campaign-byline-created"
            },
            json_filename="campaigns.json"
            )

scraper.get_many_gofundme_details(urls)

```
