INSERT INTO
    log.dag_logs (
        data_items,
        start,
        erorr_message,
        processing_time,
        project_name,
        status_code,
        task_id,
        task_name
    )
VALUES
    (
        15,
        '2025-05-28 19:46:16',
        '',
        datetime.timedelta (microseconds = 729975),
        'spotify',
        200,
        'DI8KJQDRQxjv1wcXJOfd0DBSzVsfs8',
        'FetchBatchArtists'
    ),
    (
        15,
        '2025-05-28 19:46:17',
        '',
        datetime.timedelta (microseconds = 760974),
        'spotify',
        200,
        'pxPbhZuVbWty7JrQrsC7eGi2ppNfwd',
        'FetchBatchTracks'
    );