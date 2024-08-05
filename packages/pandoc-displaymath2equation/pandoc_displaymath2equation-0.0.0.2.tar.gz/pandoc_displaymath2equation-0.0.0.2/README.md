# pandoc-displaymath2equations

Replace blocks of displaymath with the equation environment, and enable links to labeled equations.

This is a **very** simple filter.
For a solution with all the bells and whistles use the (now seemingly unmaintained) [pandoc-eqnos](https://github.com/tomduck/pandoc-eqnos).

## Usage

Install the `pandoc-displaymath2equation` package from [PyPI](https://pypi.org/project/pandoc-displaymath2equation/), and add `pandoc-displaymath2equation` to your filters.

```
python -m pip install pandoc-displaymath2equation
pandoc --filter pandoc-displaymath2equation path/to/file.md -o file.pdf
```

### Display Math Conversion

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

### Referencing Labelled Equations

To reference an equation labeled `id`, use a string of the form `(eq:id)`.
This will be replaced with `\eqref{id}`.

To label an equation, just use `\label{id}` in the display math block.

```latex
$$
E = mc^2 \label{important}
$$
```

With the default `eq-ref` option, this can be referenced in the text by using `(eq:important)`.

### Options

Options can be passed via document metadata.

| Key            | Type   | Default                   | Effect                                                  |
|----------------|--------|---------------------------|---------------------------------------------------------|
| `labeled-only` | `bool` | `false`                   | Do not transform blocks without a `\label`.             |
| `eq-ref`       | `str`  | `\(eq:(?P<eq_id>[^)]+)\)` | Regex to match equation references. Can't match spaces. |
| `env-start`    | `str`  | `\begin{equation}`        | Environment opening statement.                          |
| `env-stop`     | `str`  | `\end{equation}`          | Environment closing statement.                          |

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

- syntax for determining the text/mark/number rendered next to the equation
- logic to deal with split/align environments
