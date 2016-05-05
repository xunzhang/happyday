-- sql file for demo

-- import tuple data
DROP TABLE netflix_sample;
CREATE TABLE netflix_sample (uid INT, mid INT, rating REAL);
COPY netflix_sample FROM '/xxx/sample_fmt' delimiter ',';

SELECT max(uid) from netflix_sample; -- 10727
SELECT max(mid) from netflix_sample; -- 2244

-- matrix factorization
SELECT madlib.lmf_igd_run('netflix_sample_model',
                          'netflix_sample',
                          'uid',
                          'mid',
                          'rating',
                          10727,
                          2244,
                          80,
                          0.02,
                          0.1,
                          20,
                          1e-4); 

-- validate rating 5
SELECT madlib.array_dot(
    matrix_u[1:1][1:80],
    matrix_v[1:1][1:80]
    ) AS r 
FROM netflix_sample_model
WHERE id = 1;

-- define unnest func
CREATE OR REPLACE FUNCTION unnest_2d_1d(anyarray)
  RETURNS SETOF anyarray AS
$BODY$
SELECT array_agg($1[d1][d2])
FROM generate_series(array_lower($1,1), array_upper($1,1)) d1, 
     generate_series(array_lower($1,2), array_upper($1,2)) d2
GROUP BY d1
ORDER BY d1
$BODY$
LANGUAGE sql IMMUTABLE;

-- unfold 2d array
CREATE TABLE netflix_sample_model_structured AS (
SELECT generate_series(1, 2244) as mid, unnest_2d_1d(matrix_u[1:2244][1:80]) as fac
FROM netflix_sample_model WHERE id = 1
);

-- compute similarity
CREATE TABLE netflix_sample_movie_similarity AS (
SELECT t1.mid AS mid1 ,
       t2.mid As mid2,
      madlib.cosine_similarity(t1.fac, t2.fac) as sim
FROM netflix_sample_model_structured AS t1,
     netflix_sample_model_structured AS t2
WHERE t1.mid < t2.mid
ORDER BY t1.mid, sim DESC, t2.mid
);

-- validate rows: 2516646
SELECT count(*) from netflix_sample_movie_similarity;
SELECT 2244 * (2244-1) / 2;

-- I. directly recommendation: similarity

-- II. recommendation: dot product recommendation
CREATE TABLE netflix_sample_model_structured_u1 AS (
SELECT generate_series(1, 1) as uid, unnest_2d_1d(matrix_u[1:1][1:80]) as fac
FROM netflix_sample_model WHERE id = 1
);

SELECT t1.uid,
       t2.mid,
       madlib.array_dot(t1.fac, t2.fac) AS dp
FROM netflix_sample_model_structured_u1 AS t1,
     netflix_sample_model_structured AS t2
ORDER BY t1.uid, dp DESC, t2.mid
LIMIT 100;

-- III. recommendation: rating predict using similarity
-- TODO

-- clean up
DROP TABLE netflix_sample;
DROP TABLE netflix_sample_model;
DROP TABLE netflix_sample_model_structured;
DROP TABLE netflix_sample_movie_similarity;
DROP TABLE netflix_sample_model_structured_u1;
