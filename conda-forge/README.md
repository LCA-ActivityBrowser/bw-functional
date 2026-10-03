# conda-forge submission checklist for `bw_functional`

Copy the contents of [`bw_functional/`](bw_functional/) into a PR against
[conda-forge/staged-recipes](https://github.com/conda-forge/staged-recipes).

## Before opening the PR

1. Confirm `bw-functional==0.1.0` is on PyPI:
   https://pypi.org/project/bw-functional/0.1.0/
2. Open [`bw_functional/meta.yaml`](bw_functional/meta.yaml) and confirm
   `extra.recipe-maintainers` lists the right GitHub usernames (currently
   `bsteubing`; add co-maintainers if needed).
3. Optionally re-check the sdist sha256:

   ```bash
   curl -sL https://pypi.org/pypi/bw-functional/0.1.0/json | python -c "import sys,json; print([u['digests']['sha256'] for u in json.load(sys.stdin)['urls'] if u['packagetype']=='sdist'][0])"
   ```

## Submit to staged-recipes

1. Fork https://github.com/conda-forge/staged-recipes
2. Create a branch, e.g. `add-bw-functional`
3. Copy this directory to `recipes/bw_functional/` in the fork (so the path is
   `recipes/bw_functional/meta.yaml`)
4. Open a PR against `conda-forge/staged-recipes` with a short description:
   pure-Python Brightway package for multifunctional activities; deps already
   on conda-forge
5. Wait for CI (linter + builds). Fix any review comments from conda-forge
   maintainers

## After merge

1. conda-forge creates a feedstock (typically
   `conda-forge/bw-functional-feedstock` or `bw_functional-feedstock`)
2. Install with:

   ```console
   conda install -c conda-forge bw-functional
   ```

3. Later releases: push a new git tag here (e.g. `v0.2.0`); the feedstock
   autotick bot usually opens a version bump PR, or you update `version` /
   `sha256` manually in the feedstock

## Note on the legacy LCA channel

The private LCA Anaconda upload in this repo is **deprecated** but still runs.
Prefer conda-forge once the feedstock is live. See [`../recipe/meta.yaml`](../recipe/meta.yaml)
for the legacy channel-only recipe (not for staged-recipes).
