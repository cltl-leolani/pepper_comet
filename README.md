# pepper_comet

REST interface for COMET Commonsense inference https://github.com/atcbosselut/comet-commonsense

The repository provides a Docker container to serve the REST endpoints as well
as a Python client to interact with the REST endpoints.

## Setup

Run the gradle build to create the Docker image and client code:

    > ./gradlew

This will build a docker image named **cltl/pepper_comet** and a **client/** directory containing the generated Python client code, including documentation.

To install the clients in your project run

    > cd <project-root>/client
    > pip install -r requirements.txt
    > python setup.py install

**Note:** If you use _virtualenv_, first activate the environment in your project
before executing the above commands.

## Client

For usage of the Python client see the generated README in the _client/_ directory.