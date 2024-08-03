"""Provide miscellaneous tools for fusion modeling."""

import logging

from biocommons.seqrepo.seqrepo import SeqRepo
from gene.schemas import CURIE

from fusor.exceptions import IDTranslationException

_logger = logging.getLogger(__name__)


def translate_identifier(
    seqrepo: SeqRepo, ac: str, target_namespace: str = "ga4gh"
) -> CURIE:
    """Return ``target_namespace`` identifier for accession provided.

    :param ac: Identifier accession
    :param target_namespace: The namespace of identifiers to return.
        Default is ``ga4gh``
    :return: Identifier for ``target_namespace``
    :raise: IDTranslationException if unable to perform desired translation
    """
    try:
        target_ids = seqrepo.translate_identifier(
            ac, target_namespaces=target_namespace
        )
    except KeyError as e:
        _logger.warning("Unable to get translated identifier: %s", e)
        raise IDTranslationException from e

    if not target_ids:
        raise IDTranslationException
    return target_ids[0]
