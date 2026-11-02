.PHONY: test lint shellcheck scenarios check ci

test:
	python3 -m unittest discover -s tests -v

lint:
	python3 -m compileall -q app tests

shellcheck:
	bash -n scripts/*.sh
	@if command -v shellcheck >/dev/null 2>&1; then shellcheck scripts/*.sh; else echo "AVISO: shellcheck no está instalado; se ejecutó bash -n."; fi

scenarios:
	python3 -m app.model_checker scenarios/*.json

check: test lint shellcheck scenarios

ci: check
	@if command -v cfn-lint >/dev/null 2>&1; then cfn-lint infra/lab-stack.yaml; else echo "AVISO: cfn-lint no está instalado."; fi
