SELECT movies.title,
	ratings.rating
FROM movies
JOIN ratings ON movies.id = ratings.movie_id
WHERE movies.id IN (
		SELECT id
		FROM movies
		WHERE year = 2010
		)
ORDER BY ratings.rating DESC,
	title;
