FROM python:2.7

# install system-wide deps for python and node

ADD https://github.com/Glip-/matches_finder/blob/master/version version
RUN git clone https://github.com/Glip-/matches_finder

# copy our application code
WORKDIR matches_finder/tests/

# start app
CMD [ "python", "tests.py", "-b" ]

