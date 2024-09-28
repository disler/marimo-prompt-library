Given this natural language query: 'select user names and emails of non-authed users', generate the SQL using postgres dialect that satisfies the request. Use the TABLE_DEFINITIONS below to satisfy the database query. Follow the INSTRUCTIONS.

INSTRUCTIONS:

- ENSURE THE SQL IS VALID FOR THE DIALECT
- USE THE TABLE DEFINITIONS TO GENERATE THE SQL
- DO NOT CHANGE ANY CONTENT WITHIN STRINGS OF THE Natural Language Query
- Exclusively respond with the SQL query needed to satisfy the request and nothing else
- Prefer * for SELECT statements unless the user specifies a column

TABLE_DEFINITIONS: 

CREATE TABLE users (
    id INT,
    created TIMESTAMP,
    updated TIMESTAMP,
    authed BOOLEAN,
    PLAN TEXT,
    name TEXT,
    email TEXT
);

SQL Statement:
