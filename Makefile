.PHONY: help pre-commit-install

# Help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Setup
pre-commit-install:
	pre-commit install --hook-type pre-commit --hook-type commit-msg --hook-type pre-push
