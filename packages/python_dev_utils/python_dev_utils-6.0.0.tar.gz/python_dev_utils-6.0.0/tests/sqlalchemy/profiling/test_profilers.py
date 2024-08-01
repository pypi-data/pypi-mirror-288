from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from sqlalchemy import select

from dev_utils.core.utils import trim_and_plain_text
from dev_utils.sqlalchemy.profiling import profilers
from tests.utils import MyModel

if TYPE_CHECKING:
    from sqlalchemy import Engine
    from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
    from sqlalchemy.orm import Session


def test_sync_sql_alchemy_query_profiler(
    db_sync_engine: "Engine",
    db_sync_session: "Session",
) -> None:
    profiler = profilers.SQLAlchemyQueryProfiler(db_sync_engine)
    profiler.start()
    stmt = select(MyModel)
    db_sync_session.execute(stmt)
    profiler.stop()
    report = profiler.collect()
    assert len(report) == 1
    assert isinstance(report[0], profilers.QueryInfo)
    assert report[0].text == trim_and_plain_text(str(stmt))


def test_sync_sql_alchemy_query_profiler_double_start(
    db_sync_engine: "Engine",
) -> None:
    profiler = profilers.SQLAlchemyQueryProfiler(db_sync_engine)
    profiler.start()
    profiler.start()
    profiler.stop()


def test_sync_sql_alchemy_query_profiler_report(
    db_sync_engine: "Engine",
) -> None:
    profiler = profilers.SQLAlchemyQueryProfiler(db_sync_engine)
    profiler.start()
    profiler.stop()
    file = Path("report.txt")
    profiler.report(file)
    assert file.exists()


def test_sync_sql_alchemy_query_profiler_double_stop(
    db_sync_engine: "Engine",
) -> None:
    profiler = profilers.SQLAlchemyQueryProfiler(db_sync_engine)
    profiler.start()
    profiler.stop()
    profiler.stop()


def test_sync_sql_alchemy_query_profiler_context_manager(
    db_sync_engine: "Engine",
    db_sync_session: "Session",
) -> None:
    with profilers.SQLAlchemyQueryProfiler(db_sync_engine) as profiler:
        stmt = select(MyModel)
        db_sync_session.execute(stmt)
    report = profiler.collect()
    assert len(report) == 1
    assert isinstance(report[0], profilers.QueryInfo)
    assert report[0].text == trim_and_plain_text(str(stmt))


@pytest.mark.asyncio()
async def test_async_sql_alchemy_query_profiler(
    db_async_engine: "AsyncEngine",
    db_async_session: "AsyncSession",
) -> None:
    profiler = profilers.SQLAlchemyQueryProfiler(db_async_engine)
    profiler.start()
    stmt = select(MyModel)
    await db_async_session.execute(stmt)
    profiler.stop()
    report = profiler.collect()
    assert len(report) == 1
    assert isinstance(report[0], profilers.QueryInfo)
    assert report[0].text == trim_and_plain_text(str(stmt))


@pytest.mark.asyncio()
async def test_async_sql_alchemy_query_profiler_context_manager(
    db_async_engine: "AsyncEngine",
    db_async_session: "AsyncSession",
) -> None:
    with profilers.SQLAlchemyQueryProfiler(db_async_engine) as profiler:
        stmt = select(MyModel)
        await db_async_session.execute(stmt)
    report = profiler.collect()
    assert len(report) == 1
    assert isinstance(report[0], profilers.QueryInfo)
    assert report[0].text == trim_and_plain_text(str(stmt))
