from typing import Any, Awaitable, List, Optional

from loguru import logger

from xxy.data_source.base import DataSourceBase
from xxy.result_writer.base import ResultWriterBase
from xxy.selector import select_entity
from xxy.types import Entity, Query


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
                candidates = await data_source.search(query)
                logger.trace(f"Candidates for: {query}")
                for candidate in candidates:
                    logger.trace(f"ref {candidate.reference}, value: {candidate.value}")
                result, selected_idx = await select_entity(query, candidates)
                reference_eneity = candidates[selected_idx]
                logger.info(
                    "Get answer based on node {}: {}; {}",
                    selected_idx,
                    reference_eneity.reference,
                    reference_eneity.value,
                )
                writer.write(query, result, reference_eneity)
                print(result)
