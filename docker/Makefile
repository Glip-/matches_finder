.PHONY: clean-python36
clean-python36:
	docker rmi -f glippy/matchesfinder36

.PHONY: clean-python27
clean-python27:
	docker rmi -f glippy/matchesfinder27

.PHONY: build-python36
build-python36:
	docker build -t glippy/matchesfinder36 dockerPython36/

.PHONY: build-python27
build-python27:
	docker build -t glippy/matchesfinder27 dockerPython27/

.PHONY: run-test36
run-test36:
	docker run glippy/matchesfinder36

.PHONY: run-test27
run-test27:
	docker run glippy/matchesfinder27
	

