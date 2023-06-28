-- CREATE test.uni
DROP TABLE IF EXISTS test.unis;
CREATE TABLE test.unis(
	uni_ID INT PRIMARY KEY,
    uni_name VARCHAR(40),
    graus INT,
    masters INT,
    estudiants INT,
    rector VARCHAR(30),
    web_uni VARCHAR(100)
);

-- CREATE test.grau
DROP TABLE IF EXISTS test.graus;
CREATE TABLE test.graus(
	grau_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    grau_name VARCHAR(100),
    ambit_name VARCHAR(100),
    places INT,
    credits INT,
    web_grau VARCHAR(100),
    web_ind VARCHAR(100),
    web_ubi VARCHAR(300)
);

-- CREATE test.uni_grau
DROP TABLE IF EXISTS test.uni_grau;
CREATE TABLE test.uni_grau(
	uni_ID INT NOT NULL,
    grau_ID INT NOT NULL,
    PRIMARY KEY (uni_ID, grau_ID),
    FOREIGN KEY (uni_ID) REFERENCES test.unis(uni_ID),
    FOREIGN KEY (grau_ID) REFERENCES test.graus(grau_ID)
);

-- CREATE test.assignatures
DROP TABLE IF EXISTS test.assignatures;
CREATE TABLE test.assignatures(
    grau_ID INT,
    assig_name VARCHAR (150),
    curs INT,
    FOREIGN KEY (grau_ID) REFERENCES test.graus(grau_ID)
);


-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

