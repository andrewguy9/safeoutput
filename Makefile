test:
	tox

lint:
	yapf -i --recursive --style='{based_on_style: chromium, indent_width: 4, column_limit: 80}' \
			$(shell git ls-files | grep '.py')
