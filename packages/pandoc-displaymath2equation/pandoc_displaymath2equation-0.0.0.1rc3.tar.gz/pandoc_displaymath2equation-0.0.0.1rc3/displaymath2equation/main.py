"""
Number all equations in a document, when converting to latex.
"""

from panflute import run_filter, Element, Doc, Math, RawBlock, Para

_eq_start = r"\begin{equation}"
_eq_stop = r"\end{equation}"

def action(elem: Element, doc: Doc | None = None) -> Element | None:
    if isinstance(elem, Para):
        possible_block_wrapper = len(elem.content) == 1
        if possible_block_wrapper:
            child = elem.content[0]
            is_displaymath = isinstance(child, Math) and child.format == "DisplayMath"

            if is_displaymath:
                eq_text = f"{_eq_start}{child.text}{_eq_stop}"
                eq = RawBlock(eq_text, format="latex")

                return eq


def main(doc=None, input_stream=None, output_stream=None):
    return run_filter(action, doc=doc, input_stream=input_stream, output_stream=output_stream)


if __name__ == '__main__':
    main()
