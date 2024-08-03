# -*- coding: utf-8 -*-
import pytest

from arkindex_cli.git import LocalGitRepository


def test_repo_url_gitlab_ci(gitlab_ci_env):
    repo = LocalGitRepository()
    assert repo.url == "https://gitlab.teklia.com/arkindex/cryptominer"


@pytest.mark.parametrize(
    "output",
    [
        b"git@gitlab.teklia.com:arkindex/cryptominer.git",
        b"git@gitlab.teklia.com:arkindex/cryptominer",
    ],
)
def test_repo_url_local(output, mocker):
    subprocess_mock = mocker.MagicMock()
    subprocess_mock.check_output.return_value = output
    mocker.patch("arkindex_cli.git.subprocess", subprocess_mock)

    repo = LocalGitRepository()
    assert repo.url == "https://gitlab.teklia.com/arkindex/cryptominer"
    subprocess_mock.check_output.assert_called_once_with(
        ("git", "remote", "get-url", "origin")
    )


def test_repo_hash_gitlab_ci(gitlab_ci_env):
    repo = LocalGitRepository()
    assert repo.hash == "decafbadcafefacedeadbeef1337c0de4242f00d"


def test_repo_hash_local(mocker):
    subprocess_mock = mocker.MagicMock()
    subprocess_mock.check_output.return_value = (
        b"decafbadcafefacedeadbeef1337c0de4242f00d"
    )
    mocker.patch("arkindex_cli.git.subprocess", subprocess_mock)

    repo = LocalGitRepository()
    assert repo.hash == "decafbadcafefacedeadbeef1337c0de4242f00d"
    subprocess_mock.check_output.assert_called_once_with(("git", "rev-parse", "HEAD"))


def test_repo_message_gitlab_ci(gitlab_ci_env):
    repo = LocalGitRepository()
    assert repo.message == "this code very faster\n\nCloses #9001"


def test_repo_message_local(mocker):
    subprocess_mock = mocker.MagicMock()
    subprocess_mock.check_output.side_effect = [
        # The hash is requested before the message
        b"decafbadcafefacedeadbeef1337c0de4242f00d",
        b"this code very faster\n\nCloses #9001",
    ]
    mocker.patch("arkindex_cli.git.subprocess", subprocess_mock)

    repo = LocalGitRepository()
    assert repo.message == "this code very faster\n\nCloses #9001"

    assert subprocess_mock.check_output.call_count == 2
    subprocess_mock.check_output.assert_has_calls(
        [
            mocker.call(("git", "rev-parse", "HEAD")),
            mocker.call(
                (
                    "git",
                    "show",
                    "--no-patch",
                    "--format=%B",
                    "decafbadcafefacedeadbeef1337c0de4242f00d",
                )
            ),
        ]
    )


def test_repo_author_gitlab_ci(gitlab_ci_env):
    repo = LocalGitRepository()
    assert repo.author == "Teklia Bot"


def test_repo_author_local(mocker):
    subprocess_mock = mocker.MagicMock()
    subprocess_mock.check_output.side_effect = [
        # The hash is requested before the author
        b"decafbadcafefacedeadbeef1337c0de4242f00d",
        b"Teklia Bot",
    ]
    mocker.patch("arkindex_cli.git.subprocess", subprocess_mock)

    repo = LocalGitRepository()
    assert repo.author == "Teklia Bot"

    assert subprocess_mock.check_output.call_count == 2
    subprocess_mock.check_output.assert_has_calls(
        [
            mocker.call(("git", "rev-parse", "HEAD")),
            mocker.call(
                (
                    "git",
                    "--no-pager",
                    "show",
                    "--no-patch",
                    "--format=%an",
                    "decafbadcafefacedeadbeef1337c0de4242f00d",
                )
            ),
        ]
    )


def test_repo_branch_gitlab_ci(gitlab_ci_branch):
    repo = LocalGitRepository()
    assert repo.branch == "fix-all-the-bugs"


def test_repo_branch_gitlab_ci_tag(gitlab_ci_tag):
    repo = LocalGitRepository()
    assert repo.branch is None


def test_repo_branch_local(mocker):
    subprocess_mock = mocker.MagicMock()
    subprocess_mock.check_output.return_value = b"fix-all-the-bugs"
    mocker.patch("arkindex_cli.git.subprocess", subprocess_mock)

    repo = LocalGitRepository()
    assert repo.branch == "fix-all-the-bugs"
    subprocess_mock.check_output.assert_called_once_with(
        ("git", "branch", "--show-current")
    )


def test_repo_tags_gitlab_ci(gitlab_ci_tag):
    repo = LocalGitRepository()
    assert repo.tags == ["v9.9.9"]


def test_repo_tags_gitlab_ci_branch(gitlab_ci_branch):
    repo = LocalGitRepository()
    assert repo.tags == []


def test_repo_tags_local(mocker):
    subprocess_mock = mocker.MagicMock()
    subprocess_mock.check_output.side_effect = [
        # The hash is requested before the tags
        b"decafbadcafefacedeadbeef1337c0de4242f00d",
        b"v9.9.9\nbase-9.9.9",
    ]
    mocker.patch("arkindex_cli.git.subprocess", subprocess_mock)

    repo = LocalGitRepository()
    assert repo.tags == ["v9.9.9", "base-9.9.9"]

    assert subprocess_mock.check_output.call_count == 2
    subprocess_mock.check_output.assert_has_calls(
        [
            mocker.call(("git", "rev-parse", "HEAD")),
            mocker.call(
                (
                    "git",
                    "--no-pager",
                    "tag",
                    "--points-at",
                    "decafbadcafefacedeadbeef1337c0de4242f00d",
                )
            ),
        ]
    )
