# pepper_comet

REST interface for COMET Commonsense inference https://github.com/atcbosselut/comet-commonsense

The repository provides a Docker container to serve the REST endpoints as well
as a Python client to interact with the REST endpoints.

## Setup

Run the gradle build to create the Docker image and client code:

    > ./gradlew

This will build a docker image named **cltl/pepper_comet** and a **client/** directory containing generated Python client code, including documentation.

To install the client in your project run

    > source install_client.sh path/to/pepper_comet

**Note:** If you use _virtualenv_, first activate the environment in your project
before executing the above command.

## Docker

The Docker image exposes the following REST endpoints on port `5000`:
* `/api/atomic/infer`: Infer based on pretrained data from ATOMIC
* `/api/conceptnet/infer`: Infer based on pretrained data from ConceptNet
* `/`: [OpenAPI](https://www.openapis.org/) spec of the above endpoints

both accepting an event phrase and optionally a list of relations as well as a sample algorithm
selection as query parameters. For details see the generated OpenAPI specification available at the application root `/`.

Run the container e.g. with

    > docker run --rm -p 5000:5000

and test the endpoints with
* http://localhost:5000/api/atomic/infer?event=PersonX%20goes%to%20the%20mall
* http://localhost:5000/api/conceptnet/infer?event=go%20to%20the%20mall

## Client

For usage of the Python client see the generated README in the _client/_ directory.
