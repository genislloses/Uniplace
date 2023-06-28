-- name: get_num_graus
SELECT graus FROM test.unis where uni_ID = :uni_ID

-- name: get_masters
SELECT masters FROM test.unis where uni_ID = :uni_ID

-- name: get_estudiants
SELECT estudiants FROM test.unis where uni_ID = :uni_ID

-- name: get_rector
SELECT rector FROM test.unis where uni_ID = :uni_ID

-- name: get_web_uni
SELECT web_uni FROM test.unis WHERE uni_ID = :uni_ID

-- name: get_ambits
SELECT DISTINCT test.graus.ambit_name
FROM test.graus
INNER JOIN test.uni_grau ON test.graus.grau_ID = test.uni_grau.grau_ID
WHERE test.uni_grau.uni_ID = :uni_ID

-- name: get_graus
SELECT test.graus.grau_ID, test.graus.grau_name
FROM test.graus
INNER JOIN test.uni_grau ON test.graus.grau_ID = test.uni_grau.grau_ID
WHERE test.uni_grau.uni_ID = :uni_ID AND test.graus.ambit_name = :ambit_name

-- name: get_assignatures
SELECT assig_name
FROM test.assignatures
WHERE grau_ID = :grau_ID AND curs = :curs

-- name: get_web_grau
select web_grau
from test.graus
where grau_ID = :grau_ID

-- name: get_web_ubi
select web_ubi
from test.graus
where grau_ID = :grau_ID

-- name: get_web_ind
select web_ind
from test.graus
where grau_ID = :grau_ID

-- name: search_graus
select test.graus.grau_name, test.unis.uni_ID, test.graus.grau_ID
from test.graus
inner join test.uni_grau on test.graus.grau_ID = test.uni_grau.grau_ID
inner join test.unis on test.uni_grau.uni_ID = test.unis.uni_ID
where test.graus.grau_name like :grau_name