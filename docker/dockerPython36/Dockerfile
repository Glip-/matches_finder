FROM python:3.6

ADD https://github.com/Glip-/matches_finder/blob/master/version version
RUN git clone https://github.com/Glip-/matches_finder

WORKDIR matches_finder/tests/

CMD [ "python", "tests.py", "-b" ]

