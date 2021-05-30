CREATE TABLE bees (
    Program VARCHAR(255),
    Year INT,
    Period VARCHAR(255),
    State VARCHAR(255),
    ANSI INT,
    Affected_by VARCHAR(255),
    Pct_of_Colonies_Impacted FLOAT,
    state_code VARCHAR(50)
);

COPY bees FROM 'intro_bees.csv' DELIMITER ',' CSV HEADER;