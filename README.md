# DevNet Expert Search Frontend

This repo contains the code used in the DevNet Expert in-lab documentation search engine.
The primary code pieces are taken from the Lucene search example code with a few tweaks
for running it out of a Flask service.

## Building the Java Classes

Combined the backend, the frontend Java code will scan the index for matching hits.
To build the frontend search code, run the `scripts/compile-classes.sh` script.

## Running the Frontend

First create a `python/search-conf.yaml` file.  Typically you can just copy the example.  You
won't have access to the actual docs, so the docroot doesn't matter.

However, if you're building a custom index, you must adjust the last element in the docroot path as well
as customize the path\_token so that they are the same.  For example, if you're indexing a directory,
`~/src/git/DocTree`, make the docroot `"https://lds-stg.ccie.cisco.com/static/docs/DocTree"` and the
path\_token `DocTree`.

Copy the directory that holds the generated index from the backend to this directory.  Best to call the
directory `docs-index` so no other config change is required.

The frontend runs as a Flask/WSGI service.  Create a Python virtual environment, `pip install -r requirements`,
and then you can run `cd python && ./search_web.py` and then
connect to <https://127.0.0.1:8080>.  Note: for the search to work, you must first
have the index from the backend repo.
