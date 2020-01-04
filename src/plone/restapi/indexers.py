# -*- coding: utf-8 -*-
from plone.restapi.behaviors import IBlocks
from plone.indexer.decorator import indexer
from plone.app.contenttypes.indexers import SearchableText
import six


def _extract_text(block):
    result = ""
    for paragraph in block.get("text").get("blocks"):
        text = paragraph["text"]
        if six.PY2:
            if isinstance(text, six.text_type):
                text = text.encode("utf-8", "replace")
            if text:
                result = " ".join((result, text))
        else:
            result = " ".join((result, text))
    return result


@indexer(IBlocks)
def SearchableText_blocks(obj):
    std_text = SearchableText(obj)
    blocks = obj.blocks
    blocks_text = [
        _extract_text(blocks[block_uid])
        for block_uid in obj.blocks
        if blocks[block_uid].get("@type", "") == "text"
    ]
    blocks_text.append(std_text)
    text = " ".join(blocks_text)
    return text
