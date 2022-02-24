FROM python:3.8-slim-bullseye

COPY requirements.txt .

RUN apt-get update && \
    # install gcc and python3-dev as dependency of
    # psutil package
    apt-get install -y --no-install-recommends \
    git gcc python3-dev && \
    # clean up
    apt-get -y clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    # pip installs
    pip install --upgrade pip && \
    pip install -r requirements.txt

ENV PREFECT_HOME=/opt/prefect \
    PYTHONPATH=$PREFECT_HOME

# copy source files into the image
COPY dbt/ $PREFECT_HOME/dbt
COPY flows/ $PREFECT_HOME/flows

WORKDIR  $PREFECT_HOME/dbt

# install dbt deps if there are any required
RUN dbt deps --target=null

WORKDIR $PREFECT_HOME

# Make sure to be able to run as non-root
RUN useradd -m prefect-user && \
    # make it so that the directories in $PREFECT_HOME (including $PREFECT_HOME)
    # are world readable (and executable)
    find $PREFECT_HOME -type d -exec chmod -R 0755 {} \; && \
    # make it so that the files in $PREFECT_HOME are world readable
    find $PREFECT_HOME -type f -exec chmod -R 0644 {} \; && \
    # create directories for dbt and Prefect to store its output
    # and make sure they have the correct permissions
    mkdir -p $PREFECT_HOME/dbt/target && chmod -R 0777 $PREFECT_HOME/dbt/target && \
    mkdir -p $PREFECT_HOME/dbt/logs && chmod -R 0777 $PREFECT_HOME/dbt/logs && \
    chmod 777 $PREFECT_HOME && \
    # Make sure the dbt profiles have the correct permissions:
    chmod 666 $PREFECT_HOME/dbt/profiles.yml

USER prefect-user
ENTRYPOINT /bin/sh -c bash
