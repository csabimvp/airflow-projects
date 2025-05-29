INSERT INTO
    logs.dag_logs (
        data_items,
        description,
        finished,
        project_name,
        start,
        status_code,
        task_id,
        task_name
    )
VALUES
    (
        0,
        'OK',
        '2025-05-29 08:43:12',
        'auth-strava',
        '2025-05-29 08:43:11',
        200,
        '3qGVXmEEysixkX56Q9gQuHLjcDd84Q',
        'RequestRefreshToken'
    ),
    (
        9,
        'OK',
        '2025-05-29 08:43:12',
        'strava',
        '2025-05-29 08:43:12',
        200,
        'PwmaJlHU6kK9oldPPGrNgsraFNdTpo',
        'FetchAthleteStats'
    ),
    (
        787,
        'OK',
        '2025-05-29 08:43:47',
        'strava',
        '2025-05-29 08:43:12',
        200,
        'kFrY4IaUHGBiSIg3MHELr4PUXnH3NL',
        'FetchAllAthleteActivities'
    );