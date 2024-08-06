# TODO: token 相关的初始化可以通过 default Callable 来实现
import hashlib
import os
import time
from datetime import datetime
from pathlib import Path
from typing import BinaryIO, Set, List, Optional, Union
from urllib.parse import urlparse

import boto3
import requests

from .dataset import Dataset, DatasetFile, UploadInfo, DatasetList
import random
import string

HEYWHALE_SITE = os.getenv("HEYWHALE_HOST", "https://www.heywhale.com")
HEYWHALE_DS_BUCKET = os.getenv("HEYWHALE_DS_BUCKET", "kesci")


def parse_datetime(date_string: str) -> datetime:
    """
    Parse a datetime string into a datetime object.

    :param date_string: The datetime string to parse.
    :return: A datetime object.
    """
    return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")


def convert_to_dataset_file(files) -> List[DatasetFile]:
    dataset_files = [
        DatasetFile(
            file.get("_id"),
            file.get("Token"),
            file.get("Size"),
            "" if file.get("SubPath") is None else file.get("SubPath"),
        )
        for file in files
    ]
    return dataset_files


def get_dataset(dataset_id: str, token: Optional[str] = None) -> Optional[Dataset]:
    """
    Fetches dataset details from Heywhale.

    :param dataset_id: The ID of the dataset to fetch.
    :param token: The token for authentication. If not provided, the function will use the 'MW_TOKEN' environment variable.
    :return: A Dataset object with the dataset details.
    :raises ValueError: If no token is provided and the 'MW_TOKEN' environment variable is not set.
    """
    if token is None:
        token = os.getenv("MW_TOKEN")
        if not token:
            raise ValueError(
                "No token provided and 'MW_TOKEN' environment variable is not set."
            )

    url = f"{HEYWHALE_SITE}/api/datasets/{dataset_id}"
    headers = {
        "x-kesci-token": token,
        "x-kesci-resource": dataset_id,
    }

    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code == 200:
        # print("get datasets ", response.json())
        files = convert_to_dataset_file(response.json().get("Files"))
        # print("Get Files ", files)
        files_with_subpath = convert_to_dataset_file(
            response.json().get("FilesStructure")
        )
        # print("Get Files with subpath", files_with_subpath)
        # filter the files overlapped with files_with_subpath
        files_key_set = set([file.key for file in files])
        for file in files:
            if file.key not in files_key_set:
                files_with_subpath.append(file)
        # print("files_with_subpath", files_with_subpath)
        # files.extend(files_with_subpath)
        # print("return dataset files",files)
        return Dataset(
            _id=response.json().get("_id"),
            title=response.json().get("Title"),
            short_description=response.json().get("ShortDescription"),
            folder_name=response.json().get("FolderName"),
            files=files_with_subpath,
            created_at=parse_datetime(response.json().get("CreateDate")),
            updated_at=parse_datetime(response.json().get("UpdateDate")),
        )
    else:
        response.raise_for_status()
        return None


def _update_dataset(id: str, files: List[DatasetFile], token: Optional[str] = None):
    """
    Updates the dataset with the given ID by adding or removing files.

    :param id: The ID of the dataset to update.
    :param files: A list of DatasetFile objects representing the files to add or remove.
    :param token: The token for authentication. If not provided, the function will use the 'MW_TOKEN' environment variable.
    :raises ValueError: If no token is provided and the 'MW_TOKEN' environment variable is not set.
    """
    if token is None:
        token = os.getenv("MW_TOKEN")
        if not token:
            raise ValueError(
                "No token provided and 'MW_TOKEN' environment variable is not set."
            )
    url = f"{HEYWHALE_SITE}/api/datasets/{id}/files"
    headers = {"x-kesci-token": token, "x-kesci-resource": id}
    response = requests.put(
        url,
        json={
            "Files": [file.key for file in files],
            "FilesStructure": [
                {"Token": file.key, "SubPath": file.sub_path} for file in files
            ],
        },
        headers=headers,
        timeout=10,
    )
    if response.status_code == 200:
        return
    else:
        print(response.text)
        response.raise_for_status()


def _get_update_token(token: Optional[str] = None) -> Optional[UploadInfo]:
    """
    Retrieves the upload token for updating a dataset.

    :param token: The token for authentication. If not provided, the function will use the 'MW_TOKEN' environment variable.
    :return: An UploadInfo object containing the upload token details.
    :raises ValueError: If no token is provided and the 'MW_TOKEN' environment variable is not set.
    """
    if token is None:
        token = os.getenv("MW_TOKEN")
        if not token:
            raise ValueError(
                "No token provided and 'MW_TOKEN' environment variable is not set."
            )
    url = f"{HEYWHALE_SITE}/api/dataset-upload-token"
    headers = {"x-kesci-token": token}
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code == 200:
        return UploadInfo(
            endpoint=response.json().get("endpoint"),
            ak=response.json().get("accessKeyId"),
            sk=response.json().get("secretAccessKey"),
            token=response.json().get("sessionToken"),
            bucket=response.json().get("bucket"),
            prefix_to_save=response.json().get("prefixToSave"),
            region=response.json().get("region"),
        )
    else:
        response.raise_for_status()
        return None


def generate_timestamped_string(revision: int) -> str:
    """
    Generates a timestamped string based on the current time and a revision number.

    :param revision: The revision number.
    :return: A timestamped string.
    """
    timestamp = int(time.time() * 1000)
    result = f"{timestamp}_{revision}"
    return result


def _upload_file(
    path_or_fileobj: Union[str, Path, bytes, BinaryIO],
    path_in_dataset: str | Path,
    upload_info: UploadInfo,
) -> str:
    """
    Uploads a file to a dataset.

    :param path_or_fileobj: The path or file object of the file to upload.
    :param path_in_dataset: The path to save the file in the dataset.
    :param id: The ID of the dataset.
    :param overwrite: Whether to overwrite an existing file with the same path in the dataset.
    :param token: The token for authentication. If not provided, the function will use the 'MW_TOKEN' environment variable.
    :raises ValueError: If no token is provided and the 'MW_TOKEN' environment variable is not set.
    """

    session = boto3.Session(
        aws_access_key_id=upload_info.ak,
        aws_secret_access_key=upload_info.sk,
        aws_session_token=upload_info.token,
        region_name=upload_info.region,
    )
    s3 = session.client("s3", endpoint_url=upload_info.endpoint)

    bucket_name = upload_info.bucket

    object_key = os.path.join(
        upload_info.prefix_to_save, generate_timestamped_string(1)
    )
    if path_in_dataset != "":
        # get base filename from path_in_dataset
        # 前端是在对象存储中key没有带目录的
        # 目录存在api的SubPath字段里面
        # 这里仿照前端的格式存以防有什么不统一的地方导致错误
        object_key = os.path.join(object_key, os.path.basename(path_in_dataset))
    # print(f"upload object key {object_key}")
    try:
        if isinstance(path_or_fileobj, (str, Path)):
            with open(path_or_fileobj, "rb") as file:
                s3.put_object(Bucket=bucket_name, Key=object_key, Body=file)
        else:
            s3.put_object(Bucket=bucket_name, Key=object_key, Body=path_or_fileobj)
    except Exception as e:
        print(f"Error putting object '{object_key}' from bucket '{bucket_name}': {e}")
    return object_key


def upload_file(
    path_or_fileobj: Union[str, Path, bytes, BinaryIO],
    path_in_dataset: str | Path,
    id: str | Dataset,
    overwrite: bool = False,
    token: Optional[str] = None,
):
    """
    Uploads a file to a dataset.

    :param path_or_fileobj: The path or file object of the file to upload.
    :param path_in_dataset: The path to save the file in the dataset.
    :param id: The ID of the dataset.
    :param overwrite: Whether to overwrite an existing file with the same path in the dataset.
    :param token: The token for authentication. If not provided, the function will use the 'MW_TOKEN' environment variable.
    :raises ValueError: If no token is provided and the 'MW_TOKEN' environment variable is not set.
    """
    if token is None:
        token = os.getenv("MW_TOKEN")
        if not token:
            raise ValueError(
                "No token provided and 'MW_TOKEN' environment variable is not set."
            )
    if isinstance(id, Dataset):
        id = id._id
    upload_info = _get_update_token(token)
    if upload_info is None:
        raise ValueError("Failed to get upload token.")
    object_key = _upload_file(path_or_fileobj, path_in_dataset, upload_info)
    new_dataset_files: List[DatasetFile] = []
    dataset = get_dataset(id, token)
    if dataset is not None:
        for file in dataset.files:
            if file.path_in_dataset() != path_in_dataset:
                new_dataset_files.append(file)
            elif not overwrite:
                # print("file exists, skip uploading")
                return
        pp = str(Path(path_in_dataset).parent)
        new_dataset_files.append(DatasetFile("", object_key, 0, _norm_path(pp)))
    _update_dataset(id, new_dataset_files, token)


def _norm_path(pp: str) -> str:
    """让目录格式和前端传的一样

    Args:
        path (str): /a/ -> a/ ./ -> "" /a -> a/

    Returns:
        str: 带尾部"/"的相对路径
    """
    print(f"input pp {pp}")
    # 强加一个 /，按照示例格式来，怕没加没处理好。
    if not pp.endswith("/"):
        pp = pp + "/"
    # 开头的也去掉，避免绝对路径的格式。
    if pp.startswith("/"):
        pp = pp[1:]
    # 本地目录直接忽略
    if pp.startswith("./"):
        pp = pp[2:]
    return pp


def upload_folder(
    folder_path: str | Path,
    folder_in_dataset: str,
    id: str | Dataset,
    overwrite: bool = False,
    token: Optional[str] = None,
):
    if token is None:
        token = os.getenv("MW_TOKEN")
        if not token:
            raise ValueError(
                "No token provided and 'MW_TOKEN' environment variable is not set."
            )
    if isinstance(id, Dataset):
        id = id._id
    upload_info = _get_update_token(token)
    if upload_info is None:
        raise ValueError("Failed to get upload token.")
    new_dataset_files: Set[DatasetFile] = set()
    dataset = get_dataset(id, token)
    if dataset is None:
        raise ValueError(f"Dataset '{id}' not found.")
    # Walk through the directory
    # print(f"folder path {folder_path}")
    for root, _dirs, files in os.walk(folder_path):
        # print("files")
        for file in files:
            # print(f"file {file}")
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(os.path.join(root, file), folder_path)
            path_in_dataset = os.path.join(folder_in_dataset, rel_path)
            # print(f"root {root} rel_path {rel_path} upload file {file_path} path in {os.path.join(path_in_dataset,rel_path)} id {id}")
            object_key = _upload_file(file_path, path_in_dataset, upload_info)
            skip_upload = False
            for dfile in dataset.files:
                # print(
                #     f"dfile {dfile.path_in_dataset() } file {path_in_dataset}"
                # )
                if dfile.path_in_dataset() != path_in_dataset:
                    # print(f"add dfile {dfile}")
                    new_dataset_files.add(dfile)
                elif not overwrite:
                    # print("file exists, skip uploading")
                    skip_upload = True
                    break
            if skip_upload:
                break
            else:
                pp = str(Path(path_in_dataset).parent)
                # print(f"Append new file {object_key}, {_norm_path(pp)}")
                new_dataset_files.add(DatasetFile("", object_key, 0, _norm_path(pp)))
    if len(new_dataset_files) == 0:
        # skip update if no files in directory
        return
    # print(new_dataset_files)
    _update_dataset(id, list(new_dataset_files), token)


def _init_cache(cache_dir: Optional[str | Path] = None) -> Path:
    """
    Initializes the cache directory for the MW SDK.

    :param cache_dir: The path to the cache directory. If not provided, the default cache directory will be used.
    :return: The path to the cache directory.
    """
    if cache_dir is None:
        cache_dir = Path(os.getenv("MW_CACHE_DIR", "~/.cache/mw"))
    if isinstance(cache_dir, str):
        cache_dir = Path(cache_dir)
    cache_dir.expanduser().mkdir(parents=True, exist_ok=True)
    cache_dir.expanduser().joinpath("blobs").mkdir(exist_ok=True)
    cache_dir.expanduser().joinpath("datasets").mkdir(exist_ok=True)
    return cache_dir


def _download_single_file(
    download_url: str,
    id: str,
    filename: str,
    cache_dir: Path,
    local_dir: Optional[str | Path] = None,
) -> Path:
    """
    Downloads a single file from a dataset.

    :param download_url: The URL to download the file from.
    :param id: The ID of the dataset.
    :param filename: The name of the file.
    :param cache_dir: The cache directory.
    :return: The path to the downloaded file.
    """
    response = requests.get(download_url, stream=True, timeout=10)
    total_size = int(response.headers.get("content-length", 0))
    chunk_size = 4096
    slk_path = (
        Path(cache_dir)
        .expanduser()
        .joinpath("datasets")
        .joinpath(id)
        .joinpath("snapshots")
        .joinpath("1")
        .joinpath(filename)
    )
    if local_dir is not None:
        slk_path = Path(local_dir).joinpath(filename)
    if slk_path.exists():
        return slk_path
    file_path = (
        Path(cache_dir).expanduser().joinpath("blobs").joinpath(filename + ".lock")
    )
    file_path.parent.mkdir(parents=True, exist_ok=True)
    if file_path.exists():
        raise ValueError(
            f"File '{filename}' is being downloaded, please wait. If the downloading process is interrupted, please delete the lock file '{file_path}' manually."
        )

    m = hashlib.md5()
    with open(file_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=chunk_size):
            m.update(chunk)
            file.write(chunk)
            # pbar.update(len(chunk))
    etag = m.hexdigest()
    blob_path = file_path.rename(file_path.parent.joinpath(etag))
    slk_path.parent.mkdir(parents=True, exist_ok=True)
    slk_path.symlink_to(blob_path)
    return slk_path


def download_dir(
    id: str,
    cache_dir: Optional[str | Path] = None,
    local_dir: Optional[str | Path] = None,
    token: Optional[str] = None,
) -> Path:
    """Download a directory from the dataset.

    Args:
        id (str): The dataset id.

    Returns:
        str: The path to the downloaded directory.
    """
    if token is None:
        token = os.getenv("MW_TOKEN")
        if not token:
            raise ValueError(
                "No token provided and 'MW_TOKEN' environment variable is not set."
            )
    cache_dir = _init_cache(cache_dir)
    url = f"{HEYWHALE_SITE}/api/datasets/{id}/downloadUrl"
    headers = {
        "x-kesci-token": token,
    }
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code == 200:
        files = response.json().get("files")
        for file in files:
            download_url = file.get("Url")
            # Parse the URL to get components
            parsed_url = urlparse(download_url)
            # Extract the path component
            # 本来返回值应该有个Token和parsed_url.path等价的但是有时候是None
            parts = parsed_url.path.split("/")
            # Remove the first 3 parts and join the remaining parts back into a string
            remaining_parts = parts[
                4:
            ]  # This will slice the list to skip the first 3 elements
            # Join the remaining parts with "/" to form the final string
            filepath_in_dataset = "/".join(remaining_parts)
            _download_single_file(
                download_url,
                id,
                filepath_in_dataset,
                cache_dir,
                local_dir,
            )
    else:
        print(response.text)
        response.raise_for_status()
    if local_dir is None:
        dir = (
            Path(cache_dir)
            .expanduser()
            .joinpath("datasets")
            .joinpath(id)
            .joinpath("snapshots")
            .joinpath("1")
        )
        return dir
    else:
        dir = Path(local_dir)
        return dir


def download_file(
    id: str,
    filename: str,
    cache_dir: Optional[str | Path] = None,
    local_dir: Optional[str | Path] = None,
    token: Optional[str] = None,
) -> Path:
    """Download a file from the dataset.

    Args:
        id (str): The dataset id.
        filename (str): The file name in the dataset.
        cache_dir (Optional[str | Path], optional): The directory to cache the downloaded file. Defaults to None.
        local_dir (Optional[str | Path], optional): The local directory to save the downloaded file. Defaults to None.

    Returns:
        str: The path to the downloaded file.
    """
    if token is None:
        token = os.getenv("MW_TOKEN")
        if not token:
            raise ValueError(
                "No token provided and 'MW_TOKEN' environment variable is not set."
            )
    cache_dir = _init_cache(cache_dir)
    # dataset_detail = get_dataset(id)
    url = f"{HEYWHALE_SITE}/api/datasets/{id}/downloadUrl"
    headers = {
        "x-kesci-token": token,
    }
    response = requests.get(url, headers=headers, timeout=10)
    download_url: str = ""
    if response.status_code == 200:
        files = response.json().get("files")
        for file in files:
            if file.get("Name") + file.get("Ext") == filename:
                download_url = file.get("Url")
                break
        else:
            raise ValueError(f"File '{filename}' not found in dataset '{id}'.")
    else:
        print(response.text)
        response.raise_for_status()
    slk_path = _download_single_file(download_url, id, filename, cache_dir, local_dir)
    return slk_path


def delete_file(
    id: str,
    filepath_in_dataset: str,
    token: Optional[str] = None,
):
    """Delete a file from the dataset."""
    if token is None:
        token = os.getenv("MW_TOKEN")
        if not token:
            raise ValueError(
                "No token provided and 'MW_TOKEN' environment variable is not set."
            )
    dataset = get_dataset(id, token)
    if dataset is None:
        raise ValueError(f"Dataset '{id}' not found.")
    upload_info = _get_update_token(token)
    if upload_info is None:
        raise ValueError("Failed to get upload token.")
    # print("HHHHH")
    new_dataset_files: List[DatasetFile] = []
    # print("dateset files", dataset.files)
    for file in dataset.files:
        # a = file.path_in_dataset()
        # b = filepath_in_dataset
        # print(f"A {a} B {b}")
        if file.path_in_dataset() != filepath_in_dataset:
            new_dataset_files.append(file)
        else:
            print(f"delete file {file.path_in_dataset()}")
            continue
    _update_dataset(id, new_dataset_files, token)
    return


def delete_folder():
    pass


def create_dataset(
    title: str,
    short_description: Optional[str] = None,
    folder_name: Optional[str] = None,
    token: Optional[str] = None,
    enable_download: bool = True,
) -> Optional[Dataset]:
    """Creates a empty dataset

    Args:
        title (str): The title of the dataset.
        description (str): The description of the dataset.
        folder_name (Optional[str]): The folder name of the dataset, could be empty.

    Returns:
        Dataset: the created dataset
    """
    if token is None:
        token = os.getenv("MW_TOKEN")
        if not token:
            raise ValueError(
                "No token provided and 'MW_TOKEN' environment variable is not set."
            )
    url = f"{HEYWHALE_SITE}/api/datasets"
    headers = {
        "x-kesci-token": token,
    }
    if folder_name is None:
        folder_name = "".join(random.choices(string.ascii_lowercase, k=8))
    if short_description is None:
        short_description = title
    upload_info = _get_update_token(token)
    if upload_info is None:
        raise ValueError("Failed to get upload token.")
    session = boto3.Session(
        aws_access_key_id=upload_info.ak,
        aws_secret_access_key=upload_info.sk,
        aws_session_token=upload_info.token,
        region_name=upload_info.region,
    )
    s3 = session.client("s3", endpoint_url=upload_info.endpoint)
    bucket_name = upload_info.bucket
    object_key = os.path.join(
        upload_info.prefix_to_save, "I_am_a_fake_key_to_pass_the_validation"
    )
    # 不能创建空文件的数据集，所以上传一个占位文件来绕过检查。
    s3.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body="I_am_a_fake_key_to_pass_the_validation",
    )

    data = {
        "Title": title,
        "ShortDescription": short_description,
        "FolderName": folder_name,
        "EnableDownload": enable_download,
        "Type": 0,
        "Files": [object_key],  # 没用FileStructure，因为本来也是个假文件
    }

    response = requests.post(
        url,
        json=data,
        headers=headers,
        timeout=10,
    )

    if response.status_code == 200:
        document = response.json().get("document")
        files = convert_to_dataset_file(document.get("Files"))
        return Dataset(
            _id=document.get("_id"),
            title=document.get("Title"),
            short_description=document.get("ShortDescription"),
            folder_name=document.get("FolderName"),
            files=files,  # empty actually
            created_at=parse_datetime(document.get("CreateDate")),
            updated_at=parse_datetime(document.get("UpdateDate")),
        )
    else:
        response.raise_for_status()
        return None


def delete_dataset(
    id: str | Dataset,
    token: Optional[str] = None,
):
    if token is None:
        token = os.getenv("MW_TOKEN")
        if not token:
            raise ValueError(
                "No token provided and 'MW_TOKEN' environment variable is not set."
            )
    if isinstance(id, Dataset):
        id = id._id
    url = f"{HEYWHALE_SITE}/api/datasets/{id}"
    headers = {
        "x-kesci-token": token,
        "x-kesci-resource": id,
    }
    response = requests.delete(
        url,
        headers=headers,
        timeout=10,
    )
    if response.status_code == 200:
        return
    else:
        print(response.text)
        response.raise_for_status()
        return


def list_datasets(
    title: str = "",
    limit: int = 10,
    start_date: time = None,
    end_date: time = None,
    token: Optional[str] = None,
):
    if token is None:
        token = os.getenv("MW_TOKEN")
        if not token:
            raise ValueError(
                "No token provided and 'MW_TOKEN' environment variable is not set."
            )
    url = f"{HEYWHALE_SITE}/api/datasets"
    headers = {
        "x-kesci-token": token,
    }
    response = requests.get(
        url,
        headers=headers,
        params={
            "perPage": limit,
            "Title": title,
            "startDate": start_date,
            "endDate": end_date,
        },
        timeout=10,
    )
    if response.status_code == 200:
        document = response.json()
        datasets: List[Dataset] = []
        for d in document.get("data"):
            files = convert_to_dataset_file(d.get("Files"))
            files_with_subpath = convert_to_dataset_file(d.get("FilesStructure"))
            files_key_set = set([file.key for file in files])
            for file in files:
                if file.key not in files_key_set:
                    files_with_subpath.append(file)
            datasets.append(
                Dataset(
                    _id=d.get("_id"),
                    title=d.get("Title"),
                    short_description=d.get("ShortDescription"),
                    folder_name=d.get("FolderName"),
                    files=files_with_subpath,
                    created_at=parse_datetime(d.get("CreateDate")),
                    updated_at=parse_datetime(d.get("UpdateDate")),
                )
            )
        return DatasetList(
            datasets=datasets,
            total=document.get("totalNum"),
            page=document.get("page"),
            limit=document.get("perPage"),
        )
    else:
        response.raise_for_status()
        return None
