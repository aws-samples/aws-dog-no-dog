S3_BUCKET ?= "dog-no-dog-artifacts"
STACK_NAME ?= "dog-no-dog"
ENVIRONMENT ?= "dev"
LOG_PROCESSING_STACK_NAME ?= "serverless-log-processing"

all: package deploy endpoint

package:
	aws cloudformation package --template-file template.yml \
		--s3-bucket $(S3_BUCKET) \
		--output-template-file template.out

deploy:
	aws cloudformation deploy --template-file template.out \
		--stack-name $(STACK_NAME)-$(ENVIRONMENT) \
		--capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND \
		--parameter-overrides Environment=$(ENVIRONMENT) \
		--no-fail-on-empty-changeset

endpoint:
	@echo "$(shell aws cloudformation describe-stacks --stack-name $(STACK_NAME)-$(ENVIRONMENT) --query "Stacks[0].Outputs[?OutputKey=='ApiEndpoint'].OutputValue | [0]" | sed 's/"//g')"

local:
	sam local start-api --env-vars env.json --skip-pull-image
