import pathlib

import jinja2
import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULTS = yaml.safe_load((REPO_ROOT / "defaults" / "main.yml").read_text())


def _render(value, context):
    if isinstance(value, list):
        return [_render(item, context) for item in value]
    if isinstance(value, str) and "{{" in value:
        return jinja2.Template(value, undefined=jinja2.StrictUndefined).render(context)
    return value


def _package_context(suffix=None):
    ctx = dict(DEFAULTS)
    ctx["nvidia_driver_ubuntu_branch"] = _render(
        ctx["nvidia_driver_ubuntu_branch"], ctx
    )
    if suffix is not None:
        ctx["nvidia_driver_ubuntu_packages_suffix"] = suffix
    return ctx


def test_default_branch_and_ubuntu_packages():
    ctx = _package_context()
    assert ctx["nvidia_driver_branch"] == "580"
    assert ctx["nvidia_driver_ubuntu_branch"] == "580"
    assert ctx["nvidia_driver_ubuntu_packages_suffix"] == "-server"
    packages = _render(ctx["nvidia_driver_ubuntu_packages"], ctx)
    assert packages == [
        "nvidia-headless-580-server",
        "nvidia-utils-580-server",
        "nvidia-headless-no-dkms-580-server",
        "nvidia-kernel-source-580-server",
    ]
    cuda = _render(ctx["nvidia_driver_ubuntu_cuda_package"], ctx)
    assert cuda == "cuda-drivers-580"


def test_ubuntu_packages_without_server_suffix():
    ctx = _package_context(suffix="")
    packages = _render(ctx["nvidia_driver_ubuntu_packages"], ctx)
    assert packages == [
        "nvidia-headless-580",
        "nvidia-utils-580",
        "nvidia-headless-no-dkms-580",
        "nvidia-kernel-source-580",
    ]
