#!/usr/bin/env bash

BASE=$(realpath $(dirname $0)/..)

export CLASSPATH=${BASE}/jars/lucene-core-9.1.0.jar:${BASE}/jars/lucene-demo-9.1.0.jar:${BASE}/jars/lucene-queryparser-9.1.0.jar:${BASE}/jars/lucene-analysis-common-9.1.0.jar:${BASE}

if [ -z "${JAVAC}" ]; then
    if [ -x /opt/homebrew/Cellar/openjdk/18/bin/javac ]; then
        JAVAC=/opt/homebrew/Cellar/openjdk/18/bin/javac
    else
        JAVAC=$(which javac)
        if [ $? != 0 ]; then
            echo "ERROR: Unable to locate the javac command.  Set environment variable, JAVAC to the path to the Java compiler."
            exit 1
        fi
    fi
fi

cd ${BASE}
${JAVAC} com/example/ppm/*.java
