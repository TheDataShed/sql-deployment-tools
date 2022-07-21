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
            {"name": "Winter Moon", "unit": "DAY", "every_n_units": 30, "schedule_time": 200000},
            {"name": "Autumn Mountain", "unit": "MINUTE", "every_n_units": 1440},
            {"name": "Peaceful Valley", "unit": "WEEK", "every_n_units": 1, "run_days": ["MONDAY","FRIDAY"]},
            {"name": "Snowfall", "unit": "MONTH", "every_n_units": 1, "day_of_month": 15},
        ],
    },
}
