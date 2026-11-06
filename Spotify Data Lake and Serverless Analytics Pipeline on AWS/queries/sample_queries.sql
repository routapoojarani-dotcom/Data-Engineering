-- List the top 5 most popular tracks
SELECT track_name, track_popularity
FROM spotify_db.datawarehouse
ORDER BY track_popularity DESC
LIMIT 5;

-- Count the number of unique artists
SELECT COUNT(DISTINCT artist_id) AS unique_artists
FROM spotify_db.datawarehouse;

-- Get the average popularity of albums
SELECT AVG(album_popularity) AS avg_album_popularity
FROM spotify_db.datawarehouse;

-- See how many tracks exist per genre
SELECT genre, COUNT(track_id) AS total_tracks
FROM spotify_db.datawarehouse
GROUP BY genre
ORDER BY total_tracks DESC
LIMIT 10;

-- Sample 10 rows to preview data
SELECT *
FROM spotify_db.datawarehouse
LIMIT 10;
