--'insert_ring.sql' writes 'ring' table using 'distance' and 'point' tables. Two distinct source-destination points are selected and coresponding ring number is calculated using factor exported from pytho script

INSERT INTO ring
SELECT DISTINCT
    p1.sd_id,
    p2.sd_id,
    (SELECT
        cast(weight*(:factor) as int)
    FROM
        distance as d
    WHERE
        d.start_id=p1.id AND
        d.end_id=p2.id
    LIMIT 1)
FROM
    point as p1,
    point as p2
WHERE
    p1.sd_id NOT NULL AND
    p2.sd_id NOT NULL;