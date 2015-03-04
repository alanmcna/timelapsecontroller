DROP TABLE IF EXISTS timelapseconfig;
CREATE TABLE timelapseconfig (sleep real, running real, target real, count real);
INSERT INTO timelapseconfig ('sleep', 'running', 'target', 'count') VALUES (15,0,100,0);
