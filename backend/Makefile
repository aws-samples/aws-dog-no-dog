S3_BUCKET ?= "$(USER)-src"
STACK_NAME ?= "dognodog-backend"

all: package deploy endpoint

package:
	aws cloudformation package --template-file template.yml \
														 --s3-bucket $(S3_BUCKET) \
														 --output-template-file template.out

deploy:
	aws cloudformation deploy --template-file template.out \
														--stack-name $(STACK_NAME) \
														--capabilities CAPABILITY_IAM \
														--no-fail-on-empty-changeset

endpoint:
	@echo "$(shell aws cloudformation describe-stacks --stack-name $(STACK_NAME) --query "Stacks[0].Outputs[?OutputKey=='ApiEndpoint'].OutputValue | [0]" | sed 's/"//g')"

local:
	sam local start-api --env-vars env.json --skip-pull-image
