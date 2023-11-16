DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uuid TEXT NOT NULL,
    name TEXT NOT NULL,
    region TEXT NOT NULL,
    platforms TEXT NOT NULL,
    active BOOLEAN NOT NULL DEFAULT true,
    vdi BOOLEAN NOT NULL DEFAULT false,
    autodeferral BOOLEAN NOT NULL DEFAULT false,
    CONSTRAINT unique_uuid_name UNIQUE(uuid, name)
);

DROP TABLE IF EXISTS lists;

CREATE TABLE lists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    query TEXT NOT NULL,
    description TEXT NOT NULL,
    CONSTRAINT unique_name_query UNIQUE(name, query)
);

INSERT INTO customers (id, uuid, name, region, platforms, active, vdi, autodeferral) VALUES
(1,	'116715ab-4318-40c4-99a5-3874bf821047',	'CompanyA',	'us001', 'windows', 't', 't', 'f'),
(2,	'18542702-aaf7-4e19-b1a6-ec4d75592a3e',	'CompanyB',	'us001', 'windows', 't', 'f', 't'),
(3,	'ca22a760-be84-4ce5-b6f5-bb99cfb6fb27',	'CompanyC',	'ca001', 'windows,linux', 't', 'f', 'f'),
(4,	'efd36aaf-e631-4093-b432-18e6fd667ebb',	'CompanyD',	'eu001', 'linux,mac', 't', 'f', 'f'),
(5,	'989e0cc5-f805-4a7f-899a-66cdbb3b180f',	'CompanyE',	'au001', 'windows,mac', 't', 'f', 't');

INSERT INTO lists (id, name, query, description) VALUES
(1,	'Phase 0',	'/list/phase0', 'Internal and Friendly Customers'),
(2,	'Phase 1',	'/list/phase1', 'Linux Platform Only'),
(3,	'Phase 2',	'/list/phase2', 'VDI Only'),
(4,	'Phase 3',	'/list/phase3', 'US, CA and EU Regions Only');