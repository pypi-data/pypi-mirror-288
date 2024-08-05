# pandoc-displaymath2equations

Replace blocks of displaymath with the equation environment.

This is a **very** simple filter.
For a solution with all the bells and whistles use the (now seemingly unmaintained) [pandoc-eqnos](https://github.com/tomduck/pandoc-eqnos).

## Effect

Content that would usually generate output like this:

```latex
\[
1 + 1 = 2
\]
```

will instead generate a block like this:

```latex
\begin{equation}
1 + 1 = 2
\end{equation}
```

## Usage

Install the `pandoc-displaymath2equation` package from [PyPI](https://pypi.org/project/pandoc-displaymath2equation/), and add `pandoc-displaymath2equation` to your filters.

## Development

Source-code goes into `displaymath2equation/`, tests go into `tst/`.
Code style should conform to [PEP-8](https://peps.python.org/pep-0008/), and commit messages should follow the [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) spec.

### Dependencies

Dependencies for development can be installed from `requirements-dev.txt`.

New dependencies should go into `pyproject.toml`.
If code in `displaymath2equation/` depends on them, they go into `[project.dependencies]`, otherwise into an environment in `[project.optional-dependencies]`, most likely `dev`.

If dependencies are added, `requirements.txt` and `requirements-dev.txt` should be regenerated.
This can be done with `make requirements.txt` and `make requirements-dev.txt` respectively.

### Testing

Having tests is nice.
Even though the test we have is a little sparse, it's better than no test.

### Docs

Documentation is nice, but doesn't exist yet.
Once it does, it goes into `docs`.

## TODOs

Possible future features that would be nice to have:

- syntax for
  - labeling (determining the label rendered next to the equation)
  - identifying (giving a unique ID to an equation)
  - reference an equation by its ID, such that its label is displayed
  - link an equation by its ID
- logic to deal with split/align environments
