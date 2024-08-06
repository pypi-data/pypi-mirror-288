# practice-poetry-project-release

## Overview
This is the repository for Poetry project releases and package management PoCs.

## How to release and publish package
We use [poetry-dynamic-versioning](https://github.com/mtkennerly/poetry-dynamic-versioning) for generate package version from git release version tag.

We have implemented a [github actions workflow](./.github/workflows/publish.yml) that triggers a git release to publish the package.

## Where to publish
PyPI: https://pypi.org/project/practice-poetry-project-release/
