
# Miracle: Browser

*The data exploration component of the 
[SCARV](https://github.com/scarv) Miracle project.*

---

## Overview

This tool is a web-app developed as part of the SCARV Miracle project.
It is used to browse the large numbers of leakage experiment results
generated, and compare the results of experiments across devices.

This repository is not designed to be used as a standalone tool, but
as a sub-component of the
[miracle-experiments](https://github.com/scarv/miracle-experiments)
repository.

## Getting Started

- The results browser is a very simple web app built using the
  [Flask](https://flask.palletsprojects.com/en/1.1.x/)
  Python application framework.

- It interfaces with a 
  [trace database](https://github.com/scarv/miracle-db) to present
  information on target devices, experiments, captured data
  and analyses.

  - You will need to clone the 
    [miracle-db](https://github.com/scarv/miracle-db)
    repository in order to use the browser.

- The browser can be starting by running the following commands
  from the root of the repository:

  ```sh
  $> source bin/conf.sh
  $> export MIR_DB_REPO_HOME=<path to miracle-db repo>
  $> python3 ./browser/wsgi.py <path to leakage database to browse>
  INFO:root:Database file: '<path to leakage database to browse>'
  Serving on http://0.0.0.0:8080
  ```

- This will start the server running.
  Navigating to the "Running on" address in a web-browser will show
  the app landing page.

- The database the app connects too is specified on the command line.

## Acknowledgements

This work has been supported in part by EPSRC via grant 
[EP/R012288/1](http://gow.epsrc.ac.uk/NGBOViewGrant.aspx?GrantRef=EP/R012288/1), under the [RISE](http://www.ukrise.org) programme.

