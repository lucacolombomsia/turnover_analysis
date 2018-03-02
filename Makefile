develop/logs/makedb.log:
	python develop/src/makedb.py

db: develop/logs/makedb.log

develop/models/logistic.pkl: develop/logs/makedb.log
	python develop/src/model.py

model: develop/models/logistic.pkl

clean:
	rm develop/logs/makedb.log develop/models/logistic.pkl

all: db model

.PHONY: all