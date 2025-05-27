-- sudo su postgres
-- psql
CREATE DATABASE spotify OWNER csabimvp;

-- \q
-- psql -U csabimvp -d spotify
-- psql -U csabimvp -d rolling_stones
-- PROD schema
CREATE SCHEMA user_top_items AUTHORIZATION csabimvp;

CREATE TABLE
    IF NOT EXISTS user_top_items.tracks (
        track_id VARCHAR PRIMARY KEY,
        track_name VARCHAR,
        artist_ids VARCHAR ARRAY,
        is_explicit BOOLEAN,
        popularity NUMERIC,
        duration_ms NUMERIC,
        track_number_on_album NUMERIC,
        external_url VARCHAR,
        uri VARCHAR,
        released_year INTEGER,
        album_id VARCHAR,
        thumbnail VARCHAR
    );

CREATE TABLE
    IF NOT EXISTS user_top_items.artists (
        artist_id VARCHAR PRIMARY KEY,
        artist_name VARCHAR,
        albums VARCHAR ARRAY,
        genres VARCHAR ARRAY,
        total_followers NUMERIC,
        popularity NUMERIC,
        external_url VARCHAR,
        uri VARCHAR,
        thumbnail VARCHAR
    );