FROM python:3.8


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# install package manager
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="${PATH}:/root/.poetry/bin"
RUN echo $PATH

# copy all files to the working directory
WORKDIR /usr/src/ssh-honeypot
COPY . .

# install packages through poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# start the SSH honeypot server
EXPOSE 2222
CMD ["poetry", "run", "python", "honeypot.py"]