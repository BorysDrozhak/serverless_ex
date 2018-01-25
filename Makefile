all: deploy

deploy:
	serverless deploy

destroy:
	serverless remove

invoke:
	serverless invoke --function scrap_metric --path data.json

local_run:
	python3 handler.py