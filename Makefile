PY := .venv/bin/python

.PHONY: setup test experiments status figures export site all
setup:            ## create the venv and install pinned deps
	uv venv --python 3.11 .venv && uv pip install --python .venv -e ".[dev]"
test:             ## unit tests (about 20 s)
	$(PY) -m pytest -q
experiments:      ## the whole suite: 8 configs x 3 seeds, then figures (~12 h on a laptop CPU; resumes where it stopped)
	$(PY) experiments/run_all.py
status:           ## progress of every run in the suite, with time left
	$(PY) experiments/run_all.py --status
figures:          ## regenerate results/ and figures/ from runs/
	$(PY) experiments/make_figures.py
export:           ## export seed-0 PEARL agents + results for the website
	$(PY) -m pearl.export runs/point/pearl/seed0 site/data/point.json
	$(PY) -m pearl.export runs/sparse_point/pearl/seed0 site/data/sparse_point.json
	$(PY) -m pearl.export runs/point_wind/pearl/seed0 site/data/point_wind.json
	cp results/summary.json site/data/summary.json
site:             ## serve the website locally at http://localhost:8431
	cd site && python3 -m http.server 8431
all: test experiments export
