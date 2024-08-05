"""
Number all equations in a document, when converting to latex.
"""
from panflute import run_filter, Element, Doc, Math, RawBlock, RawInline, Para, Str

from displaymath2equation.config import Config
from displaymath2equation.types_ import Walker


def is_block_para(elem: Element) -> bool:
    """
    A block paragraph is a paragraph containing only a single element.

    :param elem: The element to test.
    :return: Whether the element is a block paragraph or not.
    """
    if isinstance(elem, Para):
        return len(elem.content) == 1
    return False


def replace_math(elem: Math, config: Config) -> RawBlock | None:
    """
    If this math element is a display math block, we replace it with the equation environment.

    :param elem: A math block.
    :return: A raw latex block with an equation environment, or ``None`` if elem is no display math block.
    """

    if elem.format == "DisplayMath":
        # bail if labeled-only is set in config,
        # but text doesn't contain \label directive
        if config.labeled_only and r"\label" not in elem.text:
            return

        eq_text = f"{config.env_start}{elem.text}{config.env_stop}"
        eq = RawBlock(eq_text, format="latex")
        return eq


def replace_eq_refs(config: Config) -> Walker:
    """
    Generate a walker that replaces equation references.

    :param config: The config object.
    :return: A walker function.
    """

    def replacer(elem: Element, doc: Doc | None = None) -> RawInline | None:
        """
        Function to walk the element tree and replace occurrences of the equation reference pattern.

        :param elem: An element in the stream.
        :param doc: Possibly the document we're working on.
        :return: A changed element or nothing.
        """
        if isinstance(elem, Str):
            match = config.eq_ref_pattern.match(elem.text)
            if match:
                eq_id = match['eq_id']
                eq_ref = RawInline(rf"\eqref{{{eq_id}}}", format="latex")
                return eq_ref

    return replacer


def action(elem: Element, doc: Doc | None = None) -> Element | None:
    """
    The actual filter.
    :param elem: An element in the stream.
    :param doc: Possibly the document we're working on.
    :return: A changed element or nothing.
    """
    config = Config.from_doc(doc)
    if is_block_para(elem):
        child = elem.content[0]
        if isinstance(child, Math):
            return replace_math(child, config=config)

    # replace eq_refs in paragraphs
    if isinstance(elem, Para):
        elem.walk(replace_eq_refs(config))


def main(doc=None, input_stream=None, output_stream=None):
    return run_filter(action, doc=doc, input_stream=input_stream, output_stream=output_stream)


if __name__ == '__main__':
    main()
