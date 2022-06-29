TEST_CONFIG = {
    "project": "Bob Ross",
    "folder": "def",
    "environment": "default",
    "parameters": [
        {
            "name": "Season 1 Episode 1",
            "value": "A walk in the woods",
            "sensitive": False,
        },
        {"name": "Season 1 Episode 2", "value": "Mt. McKinley", "sensitive": True},
    ],
    "job": {
        "name": "Season 1 Episode 3",
        "description": "Ebony Sunset",
        "enabled": True,
        "notification_email_address": "Bob.Ross@thedatashed.co.uk",
        "steps": [
            {
                "name": "Season 1 Episode 4",
                "type": "SSIS",
                "ssis_package": "WinterMist.dtsx",
            },
            {
                "name": "Season 1 Episode 5",
                "type": "SSIS",
                "ssis_package": "QuietStream.dtsx",
            },
        ],
        "schedules": [
            {"name": "Winter Moon", "every_n_minutes": 30},
            {"name": "Autumn Mountain", "every_n_minutes": 1440},
        ],
    },
}
