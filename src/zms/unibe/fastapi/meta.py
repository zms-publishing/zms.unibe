from enum import Enum
from Products.zms.standard import pybool
import os


# https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags-with-enums
class Tags(Enum):
    content = "content"
    mobile = "mobile"
    system = "system"
    scheduler = "scheduler"
    redis = "redis"


# https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-tags
tags = [
    {
        "name": "content",
        # "description": "Retrieve Content Objects, Translations, and Data",
        # "externalDocs": {
        #    "description": "GitHub / zms-fastapi / cmsapi / zmscontent",
        #    "url": "https://github.com/idasm-unibe-ch/zms-fastapi/tree/main/cmsapi/zmscontent"
        # },
    },
    {
        "name": "mobile",
        #"description": "Provide News/Events, Announcements, and Service Links",
        #"externalDocs": {
        #    "description": "GitHub / zms-fastapi / cmsapi / mobileapp",
        #    "url": "https://github.com/idasm-unibe-ch/zms-fastapi/tree/main/cmsapi/mobileapp",
        #},
    },
    {
        "name": "system",
    },
    {
        "name": "scheduler",
    },
    {
        "name": "redis",
        "description": f"{"<a href='/rq-dashboard/jobs' target='_blank'>RQ-Dashboard</a>" if pybool(os.getenv("API_RQ")) else ""}",
    },
]
