.PHONY: typing

typing:
 docker run --rm \\
 -v $(shell pwd):/ \\
 python:3.13 \\
 sh -c "pip install -r ./requirements.txt && cd / && mypy .

