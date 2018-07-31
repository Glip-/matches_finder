FROM python:3.6

# install system-wide deps for python and node

RUN git clone https://github.com/Glip-/matches_finder
RUN ls -la && cd matches_finder/tests/

# copy our application code
WORKDIR matches_finder/tests/

# start app
CMD [ "python", "tests.py" ]

