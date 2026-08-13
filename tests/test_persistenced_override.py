import pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent


def test_persistenced_override_content():
    path = REPO_ROOT / "files" / "nvidia-persistenced-override.conf"
    content = path.read_text()
    expected = (
        "[Service]\n"
        "ExecStart=\n"
        "ExecStart=/usr/bin/nvidia-persistenced --user root --persistence-mode --verbose"
    )
    assert content.strip() == expected
