from collections.abc import Iterator
from pathlib import Path
from typing import Literal

from requests import Session

from dbnomics_fetcher_toolbox.file_utils import write_chunks
from dbnomics_fetcher_toolbox.sources.http.requests import RequestsHttpSource

__all__ = ["download_http_url", "fetch_http_url"]


def download_http_url(
    url: str,
    *,
    output_file: Path,
    response_dump_dir: Path | None = None,
    session: Session | None = None,
    user_agent: str | Literal[False] | None = None,
) -> None:
    response_dump_file = None
    if response_dump_dir is not None:
        response_dump_dir.mkdir(exist_ok=True, parents=True)
        response_dump_file = response_dump_dir / f"{output_file.name}.response.txt"

    source_bytes_iter = fetch_http_url(
        url, response_dump_file=response_dump_file, session=session, user_agent=user_agent
    )
    write_chunks(source_bytes_iter, output_file=output_file)


def fetch_http_url(
    url: str,
    *,
    response_dump_file: Path | None = None,
    session: Session | None = None,
    user_agent: str | Literal[False] | None = None,
) -> Iterator[bytes]:
    source = RequestsHttpSource(url, session=session, user_agent=user_agent)
    return source.iter_bytes(response_dump_file=response_dump_file)
