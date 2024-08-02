import pathlib
import typing
from unittest.mock import call, patch

import pytest
from packaging.requirements import Requirement

from fromager import context, settings, sources


@patch("fromager.sources.download_url")
def test_invalid_tarfile(mock_download_url, tmp_path: pathlib.Path):
    mock_download_url.return_value = pathlib.Path(tmp_path / "test" / "fake_wheel.txt")
    fake_url = "https://www.thisisafakeurl.com"
    fake_dir = tmp_path / "test"
    fake_dir.mkdir()
    text_file = fake_dir / "fake_wheel.txt"
    text_file.write_text("This is a test file")
    with pytest.raises(TypeError):
        sources._download_source_check(fake_dir, fake_url)


def test_resolve_template_with_no_template():
    req = Requirement("foo==1.0")
    assert sources._resolve_template(None, req, "1.0") is None


def test_resolve_template_with_version():
    req = Requirement("foo==1.0")
    assert sources._resolve_template("url-${version}", req, "1.0") == "url-1.0"


def test_resolve_template_with_no_matching_template():
    req = Requirement("foo==1.0")
    with pytest.raises(KeyError):
        sources._resolve_template("url-${flag}", req, "1.0")


@patch("fromager.sources.resolve_dist")
@patch("fromager.sources._download_source_check")
@patch.object(settings.Settings, "download_source_url")
@patch.object(settings.Settings, "download_source_destination_filename")
def test_default_download_source_from_settings(
    download_source_destination_filename: typing.Callable,
    download_source_url: typing.Callable,
    download_source_check: typing.Callable,
    resolve_dist: typing.Callable,
    tmp_context: context.WorkContext,
):
    resolve_dist.return_value = ("url", "1.0")
    download_source_check.return_value = pathlib.Path("filename.zip")
    download_source_url.return_value = "predefined_url-${version}"
    download_source_destination_filename.return_value = "foo-${version}"
    req = Requirement("foo==1.0")
    sdist_server_url = sources.PYPI_SERVER_URL

    sources.default_download_source(tmp_context, req, sdist_server_url)

    resolve_dist.assert_called_with(tmp_context, req, sdist_server_url, True, False)
    download_source_check.assert_called_with(
        tmp_context.sdists_downloads, "predefined_url-1.0", "foo-1.0"
    )


@patch("fromager.sources.resolve_dist")
@patch("fromager.sources._download_source_check")
@patch.object(settings.Settings, "resolver_include_sdists")
@patch.object(settings.Settings, "resolver_include_wheels")
@patch.object(settings.Settings, "resolver_sdist_server_url")
def test_default_download_source_with_predefined_resolve_dist(
    resolver_sdist_server_url: typing.Callable,
    resolver_include_wheels: typing.Callable,
    resolver_include_sdists: typing.Callable,
    download_source_check: typing.Callable,
    resolve_dist: typing.Callable,
    tmp_context: context.WorkContext,
):
    resolve_dist.return_value = ("url", "1.0")
    download_source_check.return_value = pathlib.Path("filename")
    resolver_include_sdists.return_value = False
    resolver_include_wheels.return_value = True
    resolver_sdist_server_url.return_value = "url"
    req = Requirement("foo==1.0")

    sources.default_download_source(tmp_context, req, sources.PYPI_SERVER_URL)

    resolve_dist.assert_called_with(tmp_context, req, "url", False, True)


@patch("fromager.sources.default_download_source")
def test_invalid_version(mock_default_download, tmp_context: context.WorkContext):
    req = Requirement("fake==1.0")
    sdist_server_urls = [sources.PYPI_SERVER_URL]
    mock_default_download.return_value = (
        "fake-1.tar.gz",
        "fake version 1.0",
        "fakesdisturl.com",
    )
    mock_default_download.__name__ = "mock_default_download"
    with pytest.raises(ValueError):
        sources.download_source(tmp_context, req, sdist_server_urls)


@patch("logging.Logger.warning")
def test_warning_for_older_patch(mock, tmp_path: pathlib.Path):
    source = "deepspeed-0.5.0"
    patches_dir = tmp_path / source
    patches_dir.mkdir()
    patch_file = patches_dir / "deepspeed-0.5.0.patch"
    patch_file.write_text("This is a test patch")

    sources._warn_for_old_patch(patches_dir, patch_file)
    mock.assert_called_with(
        "deepspeed: patches for version 0.5.0 exist but will not be applied"
    )


@patch("fromager.sources._apply_patch")
def test_patch_sources_apply_unversioned_and_versioned(
    apply_patch: typing.Callable,
    tmp_path: pathlib.Path,
    tmp_context: context.WorkContext,
):
    patches_dir = tmp_path / "patches_dir"
    patches_dir.mkdir()
    tmp_context.patches_dir = patches_dir

    deepspeed_version_patch = patches_dir / "deepspeed-0.5.0"
    deepspeed_version_patch.mkdir()
    version_patch_file = deepspeed_version_patch / "deepspeed-0.5.0.patch"
    version_patch_file.write_text("This is a test patch")

    deepspeed_unversioned_patch = patches_dir / "deepspeed"
    deepspeed_unversioned_patch.mkdir()
    unversioned_patch_file = deepspeed_unversioned_patch / "deepspeed-update.patch"
    unversioned_patch_file.write_text("This is a test patch")

    source_root_dir = tmp_path / "deepspeed-0.5.0"
    source_root_dir.mkdir()

    sources.patch_source(tmp_context, source_root_dir, Requirement("deepspeed==0.5.0"))
    assert apply_patch.call_count == 2
    apply_patch.assert_has_calls(
        [
            call(unversioned_patch_file, source_root_dir),
            call(version_patch_file, source_root_dir),
        ]
    )


@patch("fromager.sources._apply_patch")
def test_patch_sources_apply_only_unversioned(
    apply_patch: typing.Callable,
    tmp_path: pathlib.Path,
    tmp_context: context.WorkContext,
):
    patches_dir = tmp_path / "patches_dir"
    patches_dir.mkdir()
    tmp_context.patches_dir = patches_dir

    deepspeed_version_patch = patches_dir / "deepspeed-0.5.0"
    deepspeed_version_patch.mkdir()
    version_patch_file = deepspeed_version_patch / "deepspeed-0.5.0.patch"
    version_patch_file.write_text("This is a test patch")

    deepspeed_unversioned_patch = patches_dir / "deepspeed"
    deepspeed_unversioned_patch.mkdir()
    unversioned_patch_file = deepspeed_unversioned_patch / "deepspeed-update.patch"
    unversioned_patch_file.write_text("This is a test patch")

    source_root_dir = tmp_path / "deepspeed"
    source_root_dir.mkdir()

    sources.patch_source(tmp_context, source_root_dir, Requirement("deepspeed==0.5.0"))
    assert apply_patch.call_count == 1
    apply_patch.assert_has_calls(
        [
            call(unversioned_patch_file, source_root_dir),
        ]
    )
