DROP TABLE IF EXISTS timelapseconfig;
CREATE TABLE timelapseconfig (sleep integer, running integer, target integer, count integer, pid integer);
INSERT INTO timelapseconfig ('sleep', 'running', 'target', 'count', 'pid') VALUES (15,0,100,0,NULL);
