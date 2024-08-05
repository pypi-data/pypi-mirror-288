"""
Number all equations in a document, when converting to latex.
"""

from re import compile

from panflute import run_filter, Element, Doc, Math, RawBlock, RawInline, Para, Str


def is_block_para(elem: Element) -> bool:
    """
    A block paragraph is a paragraph containing only a single element.

    :param elem: The element to test.
    :return: Whether the element is a block paragraph or not.
    """
    if isinstance(elem, Para):
        return len(elem.content) == 1
    return False


EQ_REF = compile(r"\(eq:(?P<eq_id>[^)]+)\)")


def replace_math(elem: Math) -> RawBlock | None:
    """
    If this math element is a display math block, we replace it with the equation environment.

    :param elem: A math block.
    :return: A raw latex block with an equation environment, or ``None`` if elem is no display math block.
    """
    eq_start = r"\begin{equation}"
    eq_stop = r"\end{equation}"

    if elem.format == "DisplayMath":
        eq_text = f"{eq_start}{elem.text}{eq_stop}"
        eq = RawBlock(eq_text, format="latex")
        return eq


def replace_eq_refs(elem: Element, doc: Doc | None = None) -> RawInline | None:
    """

    :param elem:
    :param doc:
    :return:
    """
    if isinstance(elem, Str):
        match = EQ_REF.match(elem.text)
        if match:
            eq_id = match['eq_id']
            eq_ref = RawInline(rf"\eqref{{{eq_id}}}", format="latex")
            return eq_ref


def action(elem: Element, doc: Doc | None = None) -> Element | None:
    """
    The actual filter.
    :param elem: An element in the stream.
    :param doc: Possibly the document we're working on.
    :return: A changed element or nothing.
    """
    if is_block_para(elem):
        child = elem.content[0]
        if isinstance(child, Math):
            return replace_math(child)

    # replace eq_refs in paragraphs
    if isinstance(elem, Para):
        elem.walk(replace_eq_refs)


def main(doc=None, input_stream=None, output_stream=None):
    return run_filter(action, doc=doc, input_stream=input_stream, output_stream=output_stream)


if __name__ == '__main__':
    main()
