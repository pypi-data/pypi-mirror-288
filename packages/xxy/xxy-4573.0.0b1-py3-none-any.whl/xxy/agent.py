from typing import Any, Awaitable, List, Optional, Tuple

from loguru import logger

from xxy.data_source.base import DataSourceBase
from xxy.result_writer.base import ResultWriterBase
from xxy.selector import select_entity
from xxy.types import Entity, Query


async def search_entity(
    data_source: DataSourceBase, query: Query
) -> Tuple[Entity, Entity]:
    result = Entity(value="N/A", reference="N/A")
    reference_eneity = Entity(value="N/A", reference="N/A")
    try:
        candidates = await data_source.search(query)
        if candidates is None or len(candidates) == 0:
            return result, reference_eneity
        logger.trace(f"Candidates for: {query}")
        for candidate in candidates:
            logger.trace(f"ref {candidate.reference}, value: {candidate.value}")
        result, selected_idx = await select_entity(query, candidates)
        if selected_idx == -1:
            return result, reference_eneity

        reference_eneity = candidates[selected_idx]
        logger.info(
            "Get answer based on node {}: {}; {}",
            selected_idx,
            reference_eneity.reference,
            reference_eneity.value,
        )
        print(query)
        print(result)
    except:
        logger.exception("Error in processing query: {}", query)

    return result, reference_eneity


async def build_table(
    data_source: DataSourceBase,
    companys: List[str],
    dates: List[str],
    names: List[str],
    writer: ResultWriterBase,
) -> None:
    companys_to_search = companys if len(companys) > 0 else ["any"]
    for company in companys_to_search:
        for date in dates:
            for name in names:
                query = Query(company=company, date=date, entity_name=name)
                result, reference_eneity = await search_entity(data_source, query)
                writer.write(query, result, reference_eneity)
