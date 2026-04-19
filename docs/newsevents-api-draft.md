# News/Events API (Draft)

## Status codes

- `200 OK` Successful request
- `404 Not Found` No such object
- `500 Internal Server Error` Something went wrong
- `503 Service Unavailable` Service is down (maybe for maintenance)

## Localization

Localization is defined in each request with query param or URL param.
Accepted values are:

- `de` - Deutsch
- `en` - English
- `fr` - Français

The fallback language handling should be implemented in the CMS API.

Date and datetime **do not** rely on localization and are always returned in standard format.

## Query Params

All `GET` endpoints which return a list support offset based pagination, `startAt`/`endAt` and `uuids` filters.

### Arguments

|                        Parameter | Description                                                                                                            |
| -------------------------------: | :--------------------------------------------------------------------------------------------------------------------- |
|       `limit`<br> _int optional_ | Maximal number of elements per query. Min: 1.                                                                          |
|      `offset` <br>_int optional_ | Current offset. Default is 0 which is the first element. Must be >= 0.                                                 |
| `startAt` <br>_string optional_ | The date start filter. e.g. "2022-10-06"                                                                                |
|   `endAt` <br>_string optional_ | The date end filter. e.g. "2022-10-30"                                                                                  |
|          `uuids*` <br>_string[]_ | The uuids of the newscontainers. e.g. ["fb3f47eb-f2d3-4889-ae48-c72f24b7900c", "581e2cf8-fe7f-4e72-898d-92512d9596f0"] |

### Example Request

```shell
$ curl https://announcement-api.unibe.ch/events?limit=10&offset=2&startAt=2022-10-06&endAt=2022-10-30&uuids=fb3f47eb-f2d3-4889-ae48-c72f24b7900c&uuids=581e2cf8-fe7f-4e72-898d-92512d9596f0
```

### Example Response

```json
{
  "offset": 5,
  "limit": 10,
  "total": 20,
  "data": [
    //...
  ]
}
```

## Fields

### TIMESTAMPS

All timestamp are returned in ISO8601 format in UTC with fields ending in postfix `At`.
Example: `"publishedAt": "2015-07-01T00:55:47Z"`

## Categories

### Category resource

|                                      Field | Description                         |
| -----------------------------------------: | :---------------------------------- |
|                          `id` <br>_string_ | Category ID                         |
|                       `title` <br>_string_ | Category title                      |
|                        `link` <br>_string_ | Link to category on _unibe.ch_ site |
| `subCategories` <br>_[Category], optional_ | Sub categories of category          |

### Get categories for news

#### HTTP REQUEST

`GET /v2/announcements/categories/news`

#### Example response (200)

```json
{
  "id": "581e2cf8-fe7f-4e72-898d-92512d9596f0",
  "title": "Portal",
  "link": "https://www.unibe.ch/unibe/portal/content/e681",
  "subCategories": [
    {
      "id": "cba8131b-1c7d-4992-82c5-ddfb283fd854",
      "title": "Theologische Fakultät",
      "link": "https://www.theol.unibe.ch/unibe/portal/fak_theologie/content/e650015",
      "subCategories": [
        //...
      ]
    },
    [
      //...
    ]
  ]
}
```

### Get categories for events

#### HTTP REQUEST

`GET /v2/announcements/categories/events`

#### Example response (200)

```json
{
  "id": "581e2cf8-fe7f-4e72-898d-92512d9596f0",
  "title": "Agenda",
  "link": "https://agenda.unibe.ch",
  "subCategories": [
    {
      "id": "cba8131b-1c7d-4992-82c5-ddfb283fd854",
      "title": "Theologische Fakultät",
      "link": "https://www.theol.unibe.ch/unibe/portal/fak_theologie/content/e650015",
      "subCategories": [
        //...
      ]
    },
    [
      //...
    ]
  ]
}
```

## News & Events

### News resource

|                              Field | Description                       |
| ---------------------------------: | :-------------------------------- |
|                `title`<br>_string_ |  News title                       |
| `imageUrl` <br> _string, optional_ | News cover image                  |
|      `publishedAt`<br> _timestamp_ | Publish date                      |
|               `link` <br> _string_ | Link to news item                 |
|        `categoryLink`<br> _string_ | Link to the category of news item |
|             `content`<br> _string_ | Content of news item              |

### EventExtraInfo resource

|                              Field | Description                      |
| ---------------------------------: | :------------------------------- |
|   `building`<br>_string, optional_ | Building where event may happen. |
| `location` <br> _string, optional_ | Address of event                 |
|      `room`<br> _string, optional_ | Room of event                    |
|  `speakers`<br> _string, optional_ | Speakers of event                |

### Event resource

|                              Field | Description                      |
| ---------------------------------: | :------------------------------- |
|                `title`<br>_string_ | Event title                      |
| `imageUrl` <br> _string, optional_ | Event cover image                |
|          `startAt`<br> _timestamp_ | Start date                       |
|            `endAt`<br> _timestamp_ | End date                         |
|   `extraInfo`<br> _EventExtraInfo_ | More information about the event |
|               `link` <br> _string_ | Link to event                    |
|        `categoryLink`<br> _string_ | Link to the category of event    |
|     `topic`<br> _string, optional_ | Topic of event item              |

### Get news of categories

#### HTTP REQUEST

`GET /v2/announcements/news`

#### ARGUMENTS

| Parameter          | Type       | Required | Description                               |
| :----------------- | :--------- | :------- | :---------------------------------------- |
| `categories`       | [string]   | Required | Array of category ids (UUIDs)             |
| `publishedBeforAt` | timestamp  | Required | Show news published before this timestamp |

**Arguments for pagination apply too!**

#### Example response (200)

```json
{
  "offset": 5,
  "limit": 10,
  "total": 20,
  "data": [
    {
      "title": "Wartungsarbeiten der Webseiten der UB Bern",
      "image_url": "https://www.unibe.ch/unibe/portal/content/e681/e1087345/ub_alert1_ger.jpg",
      "published_at": "2021-06-09T15:34:42+02:00",
      "link": "https://www.unibe.ch/universitaet/dienstleistungen/universitaetsbibliothek/index_ger.html",
      "category_link": "https://www.unibe.ch/unibe/portal/content/e681",
      "content": "Wegen Wartungsarbeiten am Dienstag, 15.06.2021 von 7:00 bis 9:00 können die Webseiten der Universitätsbibliothek Bern in diesem Zeitfenster kurzzeitig nicht erreichbar sein."
    }
    //...
  ]
}
```

### Get events of categories

#### HTTP REQUEST

`GET /v2/announcements/events`

#### ARGUMENTS

| Parameter      | Type       | Required | Description                      |
| :------------- | :--------- | :------- | :------------------------------- |
| `categories`   | [string]   | Required | Array of category ids (UUIDs)    |
| `startAfterAt` | timestamp  | Required | Show events after this timestamp |

**Arguments for pagination apply too!**

#### Example response (200)

```json
{
  "offset": 5,
  "limit": 10,
  "total": 20,
  "data": [
    {
      "title": "MIC Research Day 2021",
      "image_url": "https://www.unibe.ch/unibe/portal/content/e681/e1087345/ub_alert1_ger.jpg",
      "start_at": "2021-07-07T12:00",
      "end_at": "2021-07-07T18:00",
      "extra_info": {
        "building": "UniS, Schanzeneckstrasse 1",
        "location": "3012 Bern",
        "room": "Vorlesungsraum S003"
      },
      "link": "https://www.mic.unibe.ch…ts/mic_research_day_2021",
      "category_link": "https://agenda.unibe.ch",
      "topic": "Event – Microscopy Imaging Center"
    }
    //...
  ]
}
```
