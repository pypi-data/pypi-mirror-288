import hashlib
import json
import math
import os
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from litdata.constants import _DEFAULT_CACHE_DIR, _INDEX_FILENAME
from litdata.streaming.downloader import get_downloader_cls
from litdata.streaming.item_loader import BaseItemLoader, TokensLoader
from litdata.streaming.resolver import Dir
from litdata.utilities.subsample import shuffle_lists_together, subsample_filenames_and_roi


def subsample_streaming_dataset(
    input_dir: Dir,
    item_loader: Optional[BaseItemLoader] = None,
    subsample: float = 1.0,
    shuffle: bool = False,
    seed: int = 42,
    storage_options: Optional[Dict] = {},
) -> Tuple[List[str], List[Tuple[int, int]]]:
    """Subsample streaming dataset.

    But before doing that, we will do some preprocessing:
    - Make sure input_dir contains cache path and remote url.
    - Check if `index.json` file exists in cache path.
    - If not, download from remote url. If remote url doesn't contain `index.json` file, raise error.
    - Once downloaded, load chunks from `index.json` file.
    - Once chunks are ready, subsample (chunk filenames, region_of_interest).

    """
    subsampled_files: List[str] = []
    roi: List[Tuple[int, int]] = []

    # Make sure input_dir contains cache path and remote url
    if _should_replace_path(input_dir.path):
        cache_path = _try_create_cache_dir(input_dir=input_dir.path if input_dir.path else input_dir.url)
        if cache_path is not None:
            input_dir.path = cache_path

    assert input_dir.path is not None

    cache_index_filepath = os.path.join(input_dir.path, _INDEX_FILENAME)

    # Check if `index.json` file exists in cache path
    if not os.path.exists(cache_index_filepath) and isinstance(input_dir.url, str):
        assert input_dir.url is not None
        downloader = get_downloader_cls(input_dir.url, input_dir.path, [], storage_options)
        downloader.download_file(os.path.join(input_dir.url, _INDEX_FILENAME), cache_index_filepath)

    if os.path.exists(os.path.join(input_dir.path, _INDEX_FILENAME)):
        # load chunks from `index.json` file
        data = load_index_file(input_dir.path)
        original_chunks = data["chunks"]
    else:
        raise ValueError(
            f"The provided dataset `{input_dir.path}` doesn't contain any {_INDEX_FILENAME} file."
            " HINT: Did you successfully optimize a dataset to the provided `input_dir`?"
        )

    assert len(original_chunks) > 0, f"No chunks found in the `{input_dir}/index.json` file"

    # create a (chunk_start, chunk_end) list to indicate our subsample from where we can read.
    roi = generate_roi(original_chunks, item_loader)

    if math.isclose(subsample, 1.0):
        subsampled_files = [chnk["filename"] for chnk in original_chunks]

        return subsampled_files, roi

    # shuffle lists together
    if shuffle:
        random_seed_sampler = np.random.RandomState([seed])
        # checking if subsample is 1, as if user wants complete data, then let shuffler and sampler do the work
        original_chunks, roi = shuffle_lists_together(original_chunks, roi, random_seed_sampler)

    num_items_to_subsample = int(sum([roi[1] - roi[0] for roi in roi]) * subsample)

    subsampled_files, roi, _, _ = subsample_filenames_and_roi(original_chunks, roi, num_items_to_subsample)

    return subsampled_files, roi


def _should_replace_path(path: Optional[str]) -> bool:
    """Whether the input path is a special path to be replaced."""
    if path is None or path == "":
        return True

    return path.startswith("/teamspace/datasets/") or path.startswith("/teamspace/s3_connections/")


def _try_create_cache_dir(input_dir: Optional[str]) -> Optional[str]:
    hash_object = hashlib.md5((input_dir or "").encode())  # noqa: S324
    if "LIGHTNING_CLUSTER_ID" not in os.environ or "LIGHTNING_CLOUD_PROJECT_ID" not in os.environ:
        cache_dir = os.path.join(_DEFAULT_CACHE_DIR, hash_object.hexdigest())
        os.makedirs(cache_dir, exist_ok=True)
        return cache_dir
    cache_dir = os.path.join("/cache", "chunks", hash_object.hexdigest())
    os.makedirs(cache_dir, exist_ok=True)
    return cache_dir


def generate_roi(chunks: List[Dict[str, Any]], item_loader: Optional[BaseItemLoader] = None) -> List[Tuple[int, int]]:
    "Generates default region_of_interest for chunks."
    roi = []

    if isinstance(item_loader, TokensLoader):
        for idx, chunk in enumerate(chunks):
            roi.append((0, chunk["dim"] // item_loader._block_size))
    else:
        for i, chunk in enumerate(chunks):
            end = chunk["chunk_size"]
            roi.append((0, end))

    return roi


def load_index_file(input_dir: str) -> Dict[str, Any]:
    """Load index file from the specified input directory.

    This function supports loading both chunk-based and mds shard-based index files.
    For shard-based files, it adapts the format to be compatible with chunk-based processing.

    Args:
        input_dir (str): The directory containing the index file.

    Returns:
        Dict[str, Any]: The loaded and possibly adapted index data.

    Raises:
        FileNotFoundError: If the index file does not exist in the input directory.

    """
    index_filepath = os.path.join(input_dir, _INDEX_FILENAME)
    try:
        with open(index_filepath) as f:
            data = json.load(f)

        if "chunks" not in data and "shards" in data:
            # load mds shard-based index file and adapt to chunks format
            return adapt_mds_shards_to_chunks(data)

        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Index file not found at {index_filepath}.")


def adapt_mds_shards_to_chunks(data: Dict[str, Any]) -> Dict[str, Any]:
    """Adapt mds shard-based index data to chunk-based format for compatibility.
    For more details about MDS, refer to the MosaicML Streaming documentation: https://github.com/mosaicml/streaming

    Args:
        data (Dict[str, Any]): The original index data containing shards.

    Returns:
        Dict[str, Any]: Adapted index data with chunks format.
    """
    chunks = []
    shards = data["shards"]
    for shard in shards:
        chunks.append(
            {
                "chunk_bytes": shard["zip_data"]["bytes"],
                "chunk_size": shard["samples"],
                "column_sizes": shard["column_sizes"],
                "dim": None,
                "filename": shard["zip_data"]["basename"],
            }
        )
    data["chunks"] = chunks

    data_spec = [
        1,
        {
            "type": "builtins.dict",
            "context": json.dumps(shards[0]["column_names"]),
            "children_spec": [{"type": None, "context": None, "children_spec": []} for _ in shards[0]["column_names"]],
        },
    ]
    data["config"] = {
        "chunk_bytes": sum(shard["zip_data"]["bytes"] for shard in shards),
        "chunk_size": sum(shard["samples"] for shard in shards),
        "compression": shards[0]["compression"],
        "data_format": shards[0]["column_encodings"],
        "format": shards[0]["format"],
        "data_spec": json.dumps(data_spec),
        "encryption": None,
    }
    return data
