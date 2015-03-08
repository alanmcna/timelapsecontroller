DROP TABLE IF EXISTS timelapseconfig;
CREATE TABLE timelapseconfig (sleep integer, running integer, target integer, count integer);
INSERT INTO timelapseconfig ('sleep', 'running', 'target', 'count') VALUES (15,0,100,0);
