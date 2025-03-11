#!/bin/sh e-
set -x # this will output the commands being run

ruff check app scripts --fix
ruff format app scripts