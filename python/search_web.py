#!/usr/bin/env python3

from flask import request, render_template, Response
from flask import Flask
from subprocess import Popen, PIPE
import shlex
import os
import pathlib
import logging.config
import logging
from config import Config

os.chdir('/home/searchindex/devnet-doc-search-frontend/python')

logging.config.fileConfig(os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + "/logger.conf"))
logger = logging.getLogger(__name__)

APP_NAME = "DevNet Expert Documentation Search"
ROOT = os.path.dirname(os.path.realpath(__file__)) + "/.."
JARS = [
    "lucene-core-9.1.0.jar",
    "lucene-demo-9.1.0.jar",
    "lucene-queryparser-9.1.0.jar",
    "lucene-analysis-common-9.1.0.jar",
]

CLASSPATH = ":".join([ROOT + "/jars/" + j for j in JARS])
CLASSPATH += f":{ROOT}"

app = Flask(APP_NAME)
config = None


@app.route("/")
def show_homepage() -> Response:
    """Show the basic search homepage."""

    return render_template("index.html", app_name=APP_NAME, mimetype="text/html")


@app.route("/search", methods=["POST"])
def search() -> Response:
    """Search using Lucene and display results."""
    query = request.form.get("query")
    if query.strip() == "":
        return render_template("bad_query.html", mimetype="text/html")

    index_dir = ROOT + "/" + config.index_path

    if not os.path.isdir(index_dir):
        logger.error(f"Bad config, invalid index directory, {index_dir}")
        return render_template(
            "bad_search.html",
            error_msg=f"Invalid index directory: {index_dir}",
            mimetype="text/html",
        )

    cmd = f"{config.java} -classpath {CLASSPATH} com.example.ppm.SearchFiles -index {index_dir} -query {shlex.quote(query)}"
    # print(f"XXX: cmd = {cmd}")

    proc = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    if proc.returncode != 0:
        logger.error(f"Bad query '{query}': {err.decode('utf-8')}")
        return render_template("bad_query.html", error_msg=err.decode("utf-8"), mimetype="text/html")

    results = out.decode("utf-8")
    web_result_map = {}
    web_results = []
    for result in results.split("\n"):
        if result.strip() == "":
            continue

        doc_path = pathlib.Path(result.strip())
        i = 0
        for pp in doc_path.parts:
            if pp != config.path_token:
                i = i + 1
                continue

            break

        web_result = f"{config.doc_root}/{os.path.sep.join(doc_path.parts[i:])}"

        web_results.append(web_result)
        web_result_map[web_result] = f"{' > '.join(doc_path.parts[i+1:])}"

    return render_template(
        "search_results.html",
        web_results=web_results,
        web_result_map=web_result_map,
        query=query,
        mimetype="text/html",
    )


if __name__ == "__main__":
    config = Config("search-conf.yaml")
    done = False
    while not done:
        try:
            app.run(port=config.listen_port)
            done = True
        except Exception as e:
            logger.exception(f"Application crashed; restarting: {e}")
