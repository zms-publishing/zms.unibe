# Agenda 2.0 Schemas

## Data Mapping overview of different sources

### Approach
- This is an overview of different input sources to be mapped to the output schema `ZMSAgenda.Event`.
- `ZMSAgenda.Event` is the proposed data format to be used in frontend rendering implementations of unibe.ch.
  - for users/visitors (web) → layout/design
  - for editors/managers (zmi) → edit/manage
- These mapping tables represent the current status.
  - WIP/TBD: Work-In-Progress and To-Be-Discussed
  - All mappings are subject to change: schemas and attributes can be extended, reduced, or altered in any way.
- This work may be the foundation for a refactoring of the corresponding Web/Mobile Hub interface for unibe.app.

### Endpoints
- AgendaFilemaker: `https://agenda.unibe.ch/agenda.json`
  - `TODO`
    - get a persistent ID from AKM-OM
- AgendaLibrary: `https://agenda.ub.unibe.ch/{de|en}/api/event?limit=100`
  - `TODO`
    - get a persistent ID from UB-IT
- AgendaOutlook: `https://graph.microsoft.com/v1.0/users/{user@outlook.com}/calendar/events?$top=100`
  - `TODO` Handle
    - `categories`
    - `recurrence`
    - `location` and `locations` with `coordinates`
    - `attendees` and `status.response`

### External systems as Backend (*required attributes)

| ZMSAgenda.Event        |                                   AgendaFilemaker.Event                                   |         AgendaLibrary.Event          |                              AgendaOutlook.Event                              |
|:-----------------------|:-----------------------------------------------------------------------------------------:|:------------------------------------:|:-----------------------------------------------------------------------------:|
| eventTitle `str`*      |                                    veranstaltung_titel                                    |                title                 |                                    subject                                    |
| eventStart `datetime`* |                            json_datum_zeit_start (ISO w/o tz)                             |         startsAt (ISO w/ tz)         |                        start.dateTime `TODO` timezone                         |
| eventEnd `datetime`    |                             json_datum_zeit_end (ISO w/o tz)                              |          endsAt (ISO w/ tz)          |                         end.dateTime `TODO` timezone                          |
| eventLocation `str`    | veranstaltung_horsaal<br/>veranstaltung_gebaude_adresse<br/>veranstaltung_gebaude_adresse |                venue                 |                      `TODO` `location` and `coordinates`                      |
| eventTopics `list`     |                                           `n/a`                                           |              [subjects]              |                                 [categories]                                  |    
| eventInfos `str`       |                     veranstaltung_referenten<br/>veranstaltung_zyklus                     |              eventType               |                                 body.content                                  |
| eventImage `str`       |                                           `n/a`                                           |               imageUrl               |                       is inline + `TODO` getAttachments                       |
| eventUrl `str`         |                                  veranstalter_info_link                                   |                 url                  |                       `TODO` extract from body.content                        |
| eventSource `str`*     |                                     agenda_filemaker                                      |            agenda_library            |                                agenda_outlook                                 |
| eventId `UUID`         |                           `n/a`<br/>`TODO` get a persistent ID                            | `n/a`<br/>`TODO` get a persistent ID | [immutable id](https://learn.microsoft.com/en-us/graph/outlook-immutable-id)  |

### Content objects in ZMS as Backend (*required attributes)

| ZMSAgenda.Event        | ZMSObjects.teaser_element_2022 | ZMSObjects.newsbox | ZMSObjects.UniBEEvent |
|:-----------------------|:------------------------------:|:------------------:|:---------------------:|
| eventTitle `str`*      |         getTitle(lang)         |       `TODO`       |        `TODO`         |
| eventStart `datetime`* |             `TODO`             |       `TODO`       |        `TODO`         |
| eventEnd `datetime`    |             `TODO`             |       `TODO`       |        `TODO`         |
| eventLocation `str`    |             `TODO`             |       `TODO`       |        `TODO`         |
| eventTopics `list`     |             `TODO`             |       `TODO`       |        `TODO`         |
| eventInfos `str`       |             `TODO`             |       `TODO`       |        `TODO`         |
| eventImage `str`       |             `TODO`             |       `TODO`       |        `TODO`         |
| eventUrl `str`         |             `TODO`             |       `TODO`       |        `TODO`         |
| eventSource `str`*     |             `TODO`             |       `TODO`       |        `TODO`         |
| eventId `UUID`         |              uid               |        uid         |          uid          |

## Data Schemas examples of different input sources

### Filemaker (Legacy to be phased out)

```json
[
  {
    "json_datum_zeit_start": "2025-04-20T14:00",
    "json_datum_zeit_end": "2025-04-20T15:00",
    "veranstaltung_zyklus": "Öffentliche Führung – BOGA Botanischer Garten Bern",
    "veranstaltung_titel": "Ab in die Pampa – Pflanzen in der Steppe",
    "veranstaltung_referenten": "Fabienne Aebersold",
    "veranstaltung_gebaude_adresse": "Botanischer Garten der Universität Bern, Altenbergrain 21",
    "veranstaltung_horsaal": "Treffpunkt vor dem Palmenhaus",
    "veranstaltung_ort": "3013 Bern",
    "veranstalter_info_link": "http://www.boga.unibe.ch/agenda/oeffentliche_fuehrungen___exkursionen/ab_in_die_pampa_2004/index_ger.html"
  },
  {
    "json_datum_zeit_start": "2025-04-25T15:30",
    "json_datum_zeit_end": "2025-04-25",
    "veranstaltung_zyklus": "Vortragsreihe – Berner Chemische Gesellschaft",
    "veranstaltung_titel": "Monitoring Biomarkers for Brain Disorders: Chemistry to Clinical Impact",
    "veranstaltung_referenten": "Prof. Dr. Nako Nakatsuka",
    "veranstaltung_gebaude_adresse": "Departement für Chemie, Biochemie und Pharmazie, Freiestrasse 3",
    "veranstaltung_horsaal": "EG 16",
    "veranstaltung_ort": "3012 Bern",
    "veranstalter_info_link": "http://www.dcbp.unibe.ch/bcg/agenda"
  }
]
```

### UB-Agenda (In-house development)

```json
{
  "options": {
    "limit": 100,
    "eventType": null,
    "targetAudience": null,
    "subject": null,
    "venue": null,
    "title": null,
    "filterSingleRegistration": true,
    "series": null
  },
  "events": [
    {
      "title": "Create your own online survey or research database in a secure environment",
      "eventType": "Vortrag",
      "subjects": [
        "Forschung",
        "Open Science",
        "Research Data",
        "Wissenschaft"
      ],
      "venue": "Online",
      "startsAt": "2025-04-24T13:00:00+02:00",
      "endsAt": "2025-04-24T13:15:00+02:00",
      "series": "Coffee Lectures Science & Medicine",
      "url": "https://agenda.ub.unibe.ch/de/event/700",
      "imageUrl": null
    },
    {
      "title": "Wen respektiere ich?",
      "eventType": "Erzählcafé",
      "subjects": [],
      "venue": "Bibliothek Münstergasse",
      "startsAt": "2025-04-24T17:00:00+02:00",
      "endsAt": "2025-04-24T18:30:00+02:00",
      "series": "Erzählcafé",
      "url": "https://agenda.ub.unibe.ch/de/event/647",
      "imageUrl": "https://agenda.ub.unibe.ch/image/647"
    }
  ]
}
```

### Outlook (M365 Cloud)

```
[
  {
    '@odata.etag': 'W/"+iZhOlfb/UGQ3i66ewMG9QAAPxO4Uw=="',
    'allowNewTimeProposals': True,
    'attendees': [
      {
        'emailAddress': {
          'address': 'unibeagendasecond@engineerer.ch',
          'name': 'UniBeAgendaSecond'
        },
        'status': {
          'response': 'accepted',
          'time': '2025-04-14T08:59:39.9669303Z'
        },
        'type': 'required'
      }
    ],
    'body': {
      'content': '<html>\r\n<head>\r\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8">\r\n</head>\r\n<body>\r\n</body>\r\n</html>\',
      'contentType': 'html'
    },
    'bodyPreview': 'dsffdsdfs\r\n',
    'calendar@odata.associationLink': "https://graph.microsoft.com/v1.0/users('unibeagenda@engineerer.ch')/calendars('AAkALgAAAAAAHYQDEapmEc2byACqAC-EWg0A_iZhOlfb-UGQ3i66ewMG9QAAAABAAQAA')/$ref",
    'calendar@odata.navigationLink': "https://graph.microsoft.com/v1.0/users('unibeagenda@engineerer.ch')/calendars('AAkALgAAAAAAHYQDEapmEc2byACqAC-EWg0A_iZhOlfb-UGQ3i66ewMG9QAAAABAAQAA')",
    'categories': [
      'Purple UniBeAgenda',
      'Orange UniBeAgenda',
      'Blue UniBeAgenda'
    ],
    'changeKey': '+iZhOlfb/UGQ3i66ewMG9QAAPxO4Uw==',
    'createdDateTime': '2025-04-14T08:53:38.4856601Z',
    'end': {
      'dateTime': '2025-04-23T08:30:00.0000000',
      'timeZone': 'UTC'
    },
    'hasAttachments': False,
    'hideAttendees': False,
    'iCalUId': '040000008200E00074C5B7101A82E0080000000078DE1AB61AADDB0100000000000000001000000025A6D946FD3174478D1221C1EFE2C9B5',
    'id': 'AAkALgAAAAAAHYQDEapmEc2byACqAC-EWg0A_iZhOlfb-UGQ3i66ewMG9QAAPw24DgAA',
    'importance': 'normal',
    'isAllDay': False,
    'isCancelled': False,
    'isDraft': False,
    'isOnlineMeeting': True,
    'isOrganizer': True,
    'isReminderOn': True,
    'lastModifiedDateTime': '2025-04-14T09:00:46.4064502Z',
    'location': {
      'address': {
        'city': 'Bern',
        'countryOrRegion': 'Switzerland',
        'postalCode': '',
        'state': 'Berne',
        'street': 'Gesellschaftsstrasse 49'
      },
      'coordinates': {
        'latitude': 46.9544,
        'longitude': 7.43352
      },
      'displayName': 'Universität Bern: Institut für Erziehungswissenschaft:',
      'locationType': 'default',
      'locationUri': 'https://www.bingapis.com/api/v6/localbusinesses/YN9003x7916953480156697106',
      'uniqueId': 'Universität Bern: Institut für Erziehungswissenschaft:',
      'uniqueIdType': 'private'
    },
    'occurrenceId': None,
    'onlineMeeting': {
      'joinUrl': 'https://teams.microsoft.com/l/meetup-join/19%3ameeting_NDMwZGU3ODktNDc2MC00Zjg1LTkwZDctOTU3ZDA3ZjhlNTA4%40thread.v2/0?context=%7b%22Tid%22%3a%2222d18358-59c4-4691-900d-341ca7884fe7%22%2c%22Oid%22%3a%22abf1efa1-6f54-4d5e-8c7b-504643b78ef9%22%7d'
    },
    'onlineMeetingProvider': 'teamsForBusiness',
    'onlineMeetingUrl': None,
    'organizer': {
      'emailAddress': {
        'address': 'unibeagenda@engineerer.ch',
        'name': 'UniBeAgenda'
      }
    },
    'originalEndTimeZone': 'W. Europe Standard Time',
    'originalStartTimeZone': 'W. Europe Standard Time',
    'recurrence': None,
    'reminderMinutesBeforeStart': 15,
    'responseRequested': True,
    'responseStatus': {
      'response': 'organizer',
      'time': '0001-01-01T00:00:00Z'
    },
    'sensitivity': 'normal',
    'seriesMasterId': None,
    'showAs': 'busy',
    'start': {
      'dateTime': '2025-04-23T08:00:00.0000000',
      'timeZone': 'UTC'
    },
    'subject': 'NEUER VERANSTALTUNG',
    'transactionId': 'localevent:9f353f02-d5bb-fbb5-9426-bd0ffd903944',
    'type': 'singleInstance',
    'uid': '040000008200E00074C5B7101A82E0080000000078DE1AB61AADDB0100000000000000001000000025A6D946FD3174478D1221C1EFE2C9B5',
    'webLink': 'https://outlook.office365.com/owa/?itemid=AAkALgAAAAAAHYQDEapmEc2byACqAC%2FEWg0A%2BiZhOlfb%2FUGQ3i66ewMG9QAAPw24DgAA&exvsurl=1&path=/calendar/item'
  },
  {
    '@odata.etag': 'W/"+iZhOlfb/UGQ3i66ewMG9QAACIRh9A=="',
    'allowNewTimeProposals': True,
    'attendees': [],
    'body': {
      'content': '',
      'contentType': 'html'
    },
    'bodyPreview': '',
    'calendar@odata.associationLink': "https://graph.microsoft.com/v1.0/users('unibeagenda@engineerer.ch')/calendars('AAkALgAAAAAAHYQDEapmEc2byACqAC-EWg0A_iZhOlfb-UGQ3i66ewMG9QAAAABAAQAA')/$ref",
    'calendar@odata.navigationLink': "https://graph.microsoft.com/v1.0/users('unibeagenda@engineerer.ch')/calendars('AAkALgAAAAAAHYQDEapmEc2byACqAC-EWg0A_iZhOlfb-UGQ3i66ewMG9QAAAABAAQAA')",
    'categories': [],
    'changeKey': '+iZhOlfb/UGQ3i66ewMG9QAACIRh9A==',
    'createdDateTime': '2025-01-21T13:56:27.6416113Z',
    'end': {
      'dateTime': '2024-12-01T10:30:00.0000000',
      'timeZone': 'UTC'
    },
    'hasAttachments': False,
    'hideAttendees': False,
    'iCalUId': '040000008200E00074C5B7101A82E00800000000B85C70430C6CDB01000000000000000010000000405A66D89F21BA4D832A0CBA8779BAAD',
    'id': 'AAkALgAAAAAAHYQDEapmEc2byACqAC-EWg0A_iZhOlfb-UGQ3i66ewMG9QAACISoUQAA',
    'importance': 'normal',
    'isAllDay': False,
    'isCancelled': False,
    'isDraft': False,
    'isOnlineMeeting': False,
    'isOrganizer': True,
    'isReminderOn': True,
    'lastModifiedDateTime': '2025-01-21T13:57:01.2715427Z',
    'location': {
      'address': {
        'city': 'Bern',
        'countryOrRegion': 'Switzerland',
        'postalCode': '',
        'state': 'Berne',
        'street': 'Gesellschaftsstrasse 49'
      },
      'coordinates': {
        'latitude': 46.9544,
        'longitude': 7.43352
      },
      'displayName': 'Universität Bern: Institut für Erziehungswissenschaft:',
      'locationType': 'localBusiness',
      'locationUri': 'https://www.bingapis.com/api/v6/localbusinesses/YN9003x7916953480156697106',
      'uniqueId': 'https://www.bingapis.com/api/v6/localbusinesses/YN9003x7916953480156697106',
      'uniqueIdType': 'bing'
    },
    'locations': [
      {
        'address': {
          'city': 'Bern',
          'countryOrRegion': 'Switzerland',
          'postalCode': '',
          'state': 'Berne',
          'street': 'Gesellschaftsstrasse 49'
        },
        'coordinates': {
          'latitude': 46.9544,
          'longitude': 7.43352
        },
        'displayName': 'Universität Bern: Institut für Erziehungswissenschaft:',
        'locationType': 'localBusiness',
        'locationUri': 'https://www.bingapis.com/api/v6/localbusinesses/YN9003x7916953480156697106',
        'uniqueId': 'https://www.bingapis.com/api/v6/localbusinesses/YN9003x7916953480156697106',
        'uniqueIdType': 'bing'
      }
    ],
    'occurrenceId': None,
    'onlineMeeting': None,
    'onlineMeetingProvider': 'unknown',
    'onlineMeetingUrl': None,
    'organizer': {
      'emailAddress': {
        'address': 'unibeagenda@engineerer.ch',
        'name': 'UniBeAgenda'
      }
    },
    'originalEndTimeZone': 'W. Europe Standard Time',
    'originalStartTimeZone': 'W. Europe Standard Time',
    'recurrence': {
      'pattern': {
        'dayOfMonth': 1,
        'firstDayOfWeek': 'sunday',
        'index': 'first',
        'interval': 1,
        'month': 0,
        'type': 'absoluteMonthly'
      },
      'range': {
        'endDate': '2026-01-01',
        'numberOfOccurrences': 0,
        'recurrenceTimeZone': 'W. Europe Standard Time',
        'startDate': '2024-12-01',
        'type': 'endDate'
      }
    },
    'reminderMinutesBeforeStart': 15,
    'responseRequested': True,
    'responseStatus': {
      'response': 'organizer',
      'time': '0001-01-01T00:00:00Z'
    },
    'sensitivity': 'normal',
    'seriesMasterId': None,
    'showAs': 'busy',
    'start': {
      'dateTime': '2024-12-01T10:00:00.0000000',
      'timeZone': 'UTC'
    },
    'subject': 'Serientermin',
    'transactionId': '70ad5c88-d7b7-d2f9-9231-3b6fbe08cbd7',
    'type': 'seriesMaster',
    'uid': '040000008200E00074C5B7101A82E00800000000B85C70430C6CDB01000000000000000010000000405A66D89F21BA4D832A0CBA8779BAAD',
    'webLink': 'https://outlook.office365.com/owa/?itemid=AAkALgAAAAAAHYQDEapmEc2byACqAC%2FEWg0A%2BiZhOlfb%2FUGQ3i66ewMG9QAACISoUQAA&exvsurl=1&path=/calendar/item'
  }
]
```

### TeaserElement2022 (ZMS)

```
teaser_element_2022 {
  description: Aktuell-Teaser 2022
  id*
  meta_id*
  uid*
  getPath*
  teaser_type*
  img	image Bild (768x576px)
  img_alt
  topic
  title*
  url*
  event_date_start
  event_date_end
  event_location
  text
  source
}
```

### Newsbox (ZMS)

```
newsbox {
  description: Newsbox
  id*
  meta_id*
  uid*
  getPath*
  title*
  boxtype
  attr_url
  iframe_height
  attr_type
  img
  img_attrs_spec
  html
  text
  attr_dc_creator
  attr_event_start
  attr_dc_subject
  attr_dc_subject_section
  attr_dc_subject_topic
  name
  telefon
  mail
  function
}
```

### UniBEEvent (ZMS)

```
UniBEEvent {
  description: Detailseite Veranstaltung
  id*
  meta_id*
  uid*
  getPath*
  eventTeaser*
  titlealt*
  title*
  eventStart*
  eventStarttime*
  eventEnd
  eventEndtime
  eventBild
  eventBildAlt
  eventBildText
  eventBildCopyright
  eventText*
  eventVeranstalter*
  eventRedner
  eventRaum*
  eventAreal_Gebaeude*
  eventStrasse*
  eventOrt*
  eventURL
  eventKontaktPerson
  eventKontaktTel
  eventKontaktMailAdr
  veranstaltung_oeffentlich
  veranstaltung_kostenpflichtig
  veranstaltung_anmeldepflichtig
  eventAnmeldung
  eventAnmeldungLink
  attr_dc_description
  attr_dc_creator
  attr_dc_relation_backlink
  attr_dc_accessrights_restricted
  attr_dc_identifier_url_node
  attr_dc_identifier_url_redirect
  attr_robots
  seotitle_tag
  seometa_tag
  attr_dc_subject
  titleimage
}
```
