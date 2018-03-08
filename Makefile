develop/logs/develop.log:
	python develop/src/makedb.py params.yaml 

db: develop/logs/develop.log

develop/models/logistic.pkl: develop/logs/develop.log
	python develop/src/model.py params.yaml 

model: develop/models/logistic.pkl

clean:
	rm develop/logs/develop.log develop/models/logistic.pkl

all: db model

.PHONY: all