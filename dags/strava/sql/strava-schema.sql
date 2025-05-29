-- sudo su postgres
-- psql
CREATE DATABASE utilities OWNER csabimvp;

-- \q
-- psql -U csabimvp -d utilities
-- PROD schema
CREATE SCHEMA strava AUTHORIZATION csabimvp;

-- staging schema for testing.
CREATE SCHEMA strava_staging AUTHORIZATION csabimvp;

CREATE TABLE
    IF NOT EXISTS strava.athlete_stats (
        activity_id VARCHAR PRIMARY KEY,
        activity_count INTEGER,
        athlete_id VARCHAR,
        date_refreshed DATE,
        distance NUMERIC,
        elapsed_time INTEGER,
        elevation_gain NUMERIC,
        moving_time INTEGER,
        stat_type VARCHAR,
        sport_type VARCHAR
    );

CREATE TABLE
    IF NOT EXISTS strava.athlete_activities (
        activity_id VARCHAR PRIMARY KEY,
        athlete_id VARCHAR,
        average_speed NUMERIC,
        distance NUMERIC,
        elapsed_time INTEGER,
        elev_high NUMERIC,
        elev_low NUMERIC,
        external_id VARCHAR,
        gear_id VARCHAR,
        kudos_count INTEGER,
        comment_count INTEGER,
        pr_count INTEGER,
        achievement_count INTEGER,
        latitude NUMERIC,
        longitude NUMERIC,
        moving_time INTEGER,
        source_system VARCHAR,
        sport_type VARCHAR,
        start_date DATE,
        total_elevation_gain NUMERIC
    );

CREATE TABLE
    IF NOT EXISTS strava.gear (
        gear_id VARCHAR PRIMARY KEY,
        sport_type VARCHAR,
        total_distance NUMERIC,
        total_moving_time NUMERIC,
        total_elevation_gain NUMERIC,
        started_using DATE,
        last_used DATE
    );

CREATE TABLE
    IF NOT EXISTS strava_staging.athlete_stats (
        activity_id VARCHAR PRIMARY KEY,
        activity_count INTEGER,
        athlete_id VARCHAR,
        date_refreshed DATE,
        distance NUMERIC,
        elapsed_time INTEGER,
        elevation_gain NUMERIC,
        moving_time INTEGER,
        stat_type VARCHAR,
        sport_type VARCHAR
    );

CREATE TABLE
    IF NOT EXISTS strava_staging.athlete_activities (
        activity_id VARCHAR PRIMARY KEY,
        athlete_id VARCHAR,
        average_speed NUMERIC,
        distance NUMERIC,
        elapsed_time INTEGER,
        elev_high NUMERIC,
        elev_low NUMERIC,
        external_id VARCHAR,
        gear_id VARCHAR,
        kudos_count INTEGER,
        comment_count INTEGER,
        pr_count INTEGER,
        achievement_count INTEGER,
        latitude NUMERIC,
        longitude NUMERIC,
        moving_time INTEGER,
        source_system VARCHAR,
        sport_type VARCHAR,
        start_date DATE,
        total_elevation_gain NUMERIC
    );