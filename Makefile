all: deploy

check:
	python -m py_compile *.py
	rm -f *.pyc	

deploy: check
	serverless deploy

destroy:
	serverless remove

invoke:
	serverless invoke --function scrap_metric --path data.json

local_run:
	python3 handler.py