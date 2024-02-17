USE CAFA;

-- removing safe mode
SET SQL_safe_updates =0;

-- Removing sequenes with X or unknown amino acids
SELECT COUNT(*)
FROM sequence
WHERE seq LIKE '%X%' OR seq LIKE '%x%';

-- removes 1572 sequences with partial sequence
DELETE FROM Sequence
WHERE seq LIKE '%X%' OR seq LIKE '%x%';

-- Used for eda
SELECT taxonomy.tax_id, taxon_names.sci_name, taxon_names.com_name
FROM taxonomy
JOIN taxon_names ON taxonomy.tax_id = taxon_names.taxid;

-- Count the number of seuqences within our data
SELECT count(*)
FROM sequence;

-- Finding min, max and average sequnece lenght
SELECT AVG(LENGTH(seq)) AS Average, Max(LENGTH(seq)) AS Max, Min(LENGTH(seq)) AS Min
FROM sequence;

-- Checking to see if this is an error
SELECT seq_id, seq
FROM sequence
GROUP BY seq_id
HAVING AVG(LENGTH(seq)) = '3';

-- Checking to see if this is an error as well
SELECT seq_id, seq
FROM sequence
GROUP BY seq_id
HAVING AVG(LENGTH(seq)) = '35375';

-- Is a type of a mashroom plant that has this short protein. It could make sense that such a protein would exist
SELECT go_seqs.go_seq_id, go_seqs.go_go_id , go_functions.go_function, taxon_names.sci_name, taxon_names.com_name
FROM go_seqs
JOIN go_functions ON go_seqs.go_go_id = go_functions.go_id
JOIN taxonomy ON go_seqs.go_seq_id = taxonomy.tax_seq_id
JOIN taxon_names ON taxonomy.tax_id = taxon_names.taxid
WHERE go_seq_id = 'P84761';

-- Wonder what this is
SELECT go_seqs.go_seq_id, go_seqs.go_go_id , go_functions.go_function, taxon_names.sci_name, taxon_names.com_name
FROM go_seqs
JOIN go_functions ON go_seqs.go_go_id = go_functions.go_id
JOIN taxonomy ON go_seqs.go_seq_id = taxonomy.tax_seq_id
JOIN taxon_names ON taxonomy.tax_id = taxon_names.taxid
WHERE go_seq_id = 'A0A8I5ZUN3';

-- Get Taxon
SELECT DISTINCT COUNT(*)
FROM taxonomy;

-- Functions
SELECT COUNT(*)
FROM go_functions;

SELECT go_seqs.go_seq_id, go_functions.go_id, go_functions.go_function
FROM go_seqs
JOIN go_functions ON go_seqs.go_go_id = go_functions.go_id;

-- Getting a single seq
WITH single_tax_seqs AS(
	SELECT tax_id, tax_seq_id
	FROM (
		SELECT tax_id, tax_seq_id,
        ROW_NUMBER() OVER (PARTITION BY tax_id ORDER BY RAND()) AS rn
        FROM taxonomy) AS ranked
		WHERE rn = 1)

SELECT single_tax_seqs.tax_id, single_tax_seqs.tax_seq_id, sequence.seq
FROM sequence
JOIN single_tax_seqs ON sequence.seq_id = single_tax_seqs.tax_seq_id;

-- Making sure there are no errors
WITH single_tax_seqs AS(
	SELECT tax_id, tax_seq_id
	FROM (
		SELECT tax_id, tax_seq_id,
			ROW_NUMBER() OVER (PARTITION BY tax_id ORDER BY RAND()) AS rn
		FROM taxonomy
	) AS ranked
	WHERE rn = 1
)

SELECT COUNT(*)
FROM sequence
JOIN single_tax_seqs ON sequence.seq_id = single_tax_seqs.tax_seq_id;

-- Find seqs with 1 taxon
SELECT COUNT(*) AS count_of_single_appearances
FROM (
    SELECT count(*)
    FROM taxonomy
    GROUP BY tax_id
) AS subquery;

-- Function For sample
SELECT count(distinct.go_seqs.go_go_id)
FROM sample
JOIN go_seqs ON sample.t_tax_seq_id = go_seqs.go_seq_id;

--------------------------------------------------
SELECT test.id, sequence.seq, go_seqs.go_go_id
FROM test
JOIN sequence ON test.id = sequence.seq_id
JOIN go_seqs ON sequence.seq_id = go_seqs.go_seq_id;

SELECT test.id, go_seqs.go_go_id
FROM test
JOIN go_seqs ON test.id = go_seqs.go_seq_id;

SELECT test.id, sequence.seq
FROM test
JOIN sequence ON test.id = sequence.seq_id;

WITH CombinedData AS (
    SELECT go_seqs.go_go_id
    FROM test
    JOIN go_seqs ON test.id = go_seqs.go_seq_id
    UNION
    SELECT go_seqs.go_go_id
    FROM sample
    JOIN go_seqs ON sample.t_tax_seq_id = go_seqs.go_seq_id
)
SELECT COUNT(DISTINCT go_go_id) AS unique_go_go_ids
FROM CombinedData;





