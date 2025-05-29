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
        '2025-05-29 10:42:55',
        'auth-spotify',
        '2025-05-29 10:42:55',
        200,
        'URZwWIPC6RNnUBH7yKaxWWCs242edZ',
        'RequestRefreshToken'
    ),
    (
        15,
        'OK',
        '2025-05-29 10:42:55',
        'spotify',
        '2025-05-29 10:42:55',
        200,
        'oIwFwj3k4r6jlCVAlfWjMuqeYAjB8A',
        'FetchBatchArtists'
    ),
    (
        15,
        'OK',
        '2025-05-29 10:42:56',
        'spotify',
        '2025-05-29 10:42:55',
        200,
        'atQFTgo1i0D73lVVtbpemgPORTuCRY',
        'FetchBatchTracks'
    );