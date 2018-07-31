.PHONY: clean
clean:
	docker rmi -f glippy/matchesfinder

.PHONY: build
build:
	docker build -t glippy/matchesfinder docker/

.PHONY: run-test
run-test:
	docker run glippy/matchesfinder
	

