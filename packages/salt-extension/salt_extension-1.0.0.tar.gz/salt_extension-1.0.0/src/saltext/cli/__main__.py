import copy
import datetime
import os
import pathlib
from typing import Any
from typing import Dict
from typing import Optional
from typing import Tuple

import click
import jinja2.exceptions
from click_params import PUBLIC_URL
from click_params import SLUG
from jinja2 import Template
from saltext.cli import __version__
from saltext.cli import PACKAGE_ROOT
from saltext.cli.templates import LOADER_MODULE_FUNCTIONAL_TEST_TEMPLATE
from saltext.cli.templates import LOADER_MODULE_INTEGRATION_TEST_TEMPLATE
from saltext.cli.templates import LOADER_MODULE_UNIT_TEST_TEMPLATE
from saltext.cli.templates import LOADER_SDB_UNIT_TEST_TEMPLATE
from saltext.cli.templates import LOADER_STATE_FUNCTIONAL_TEST_TEMPLATE
from saltext.cli.templates import LOADER_STATE_UNIT_TEST_TEMPLATE
from saltext.cli.templates import LOADER_TEMPLATE
from saltext.cli.templates import LOADER_UNIT_TEST_TEMPLATE
from saltext.cli.templates import MODULE_LOADER_TEMPLATE
from saltext.cli.templates import PACKAGE_INIT
from saltext.cli.templates import SDB_LOADER_TEMPLATE
from saltext.cli.templates import STATE_LOADER_TEMPLATE

LICENSES: Dict[str, str] = {
    "apache": "License :: OSI Approved :: Apache Software License",
}

SALT_LOADERS = (
    "auth",
    "beacons",
    "cache",
    "cloud",
    "engines",
    "executor",
    "fileserver",
    "grain",
    "log_handlers",
    "matchers",
    "metaproxy",
    "module",
    "netapi",
    "output",
    "pillar",
    "proxy",
    "queue",
    "renderer",
    "returner",
    "roster",
    "runner",
    "serializers",
    "states",
    "thorium",
    "tokens",
    "top",
    "wheel",
    # sdb related
    "sdb",
    "pkgdb",
    "pkgfiles",
    # ssh wrapper
    "wrapper",
)

SINGULAR_MODULE_DIRS = (
    "auth",
    "cache",
    "fileserver",
    "metaproxy",
    "netapi",
    "output",
    "pillar",
    "pkgdb",
    "proxy",
    "roster",
    "sdb",
    "thorium",
    "wheel",
    "wrapper",
)

CURRENT_LATEST_SALT = 3006
SALT_PYTHON_SUPPORT = {
    3003: {"min": (3, 7), "max": (3, 9)},
    3004: {"min": (3, 7), "max": (3, 10)},
    3005: {"min": (3, 7), "max": (3, 10)},
    3006: {"min": (3, 7), "max": (3, 10)},
    3007: {"min": (3, 8), "max": (3, 11)},
}


@click.command()
@click.version_option(version=__version__)
@click.help_option("-h", "--help")
@click.option("-A", "--author", help="Author name", type=str, prompt=True)
@click.option("-E", "--author-email", help="Author Email", type=str, prompt=True)
@click.option("-S", "--summary", help="Project summary", type=str, prompt=True)
@click.option("-U", "--url", help="Project URL", type=PUBLIC_URL, prompt=True)
@click.option("--source-url", help="Project Source URL", type=PUBLIC_URL)
@click.option("--tracker-url", help="Project Tracker URL", type=PUBLIC_URL)
@click.option("--docs-url", help="Project Documentation URL", type=PUBLIC_URL)
@click.option("--package-name", help="Project Package name 'saltext.<package-name>'", type=str)
@click.option(
    "--no-saltext-namespace",
    help="Don't use the 'saltext' package namespace",
    is_flag=True,
    default=False,
    expose_value=True,
)
@click.option(
    "-F",
    "--force-overwrite",
    help="Force overwrites",
    is_flag=True,
    default=False,
    expose_value=True,
)
@click.option(
    "-V", "--salt-version", help="The minimum Salt version to target", default="3005", type=str
)
@click.option(
    "--python-requires", help="The minimum Python version to support", default="", type=str
)
@click.option(
    "--max-salt-version",
    help="The maximum Salt major version to support",
    default=CURRENT_LATEST_SALT,
    type=int,
)
@click.option(
    "-l",
    "--loader",
    help="Which loaders should the project support",
    type=click.Choice(SALT_LOADERS),
    multiple=True,
)
@click.option(
    "-L",
    "--license",
    help="Project License",
    type=click.Choice(sorted(LICENSES) + ["other"]),
    prompt=True,
)
@click.option(
    "--dest",
    help="The path where to create the new project. Defaults to current directory",
    type=click.Path(
        file_okay=False, dir_okay=True, writable=True, readable=True, resolve_path=True
    ),
    default=os.getcwd(),
)
@click.argument("project-name", type=SLUG)
def main(
    project_name: str,
    author: str,
    author_email: str,
    summary: str,
    url: PUBLIC_URL,
    source_url: Optional[PUBLIC_URL],
    tracker_url: Optional[PUBLIC_URL],
    docs_url: Optional[PUBLIC_URL],
    package_name: Optional[str],
    license: str,
    loader: Tuple[str],
    dest: str,
    salt_version: str,
    force_overwrite: bool,
    no_saltext_namespace: bool,
    python_requires: str,
    max_salt_version: int,
):
    destdir: pathlib.Path = pathlib.Path(dest)

    try:
        salt_version = float(salt_version)
    except ValueError as err:
        raise ValueError(
            f"Cannot parse Salt version: '{salt_version}'. "
            "Please specify it like `3006` or `3006.3`."
        ) from err
    if int(salt_version) == salt_version:
        salt_version = int(salt_version)
    if python_requires:
        python_requires = tuple(int(x) for x in python_requires.split("."))
        if not (3,) <= python_requires < (4,):
            raise ValueError(
                f"Invalid Python version specified: '{python_requires}'. Example: '3.8'"
            )
    salt_python_requires = SALT_PYTHON_SUPPORT[int(salt_version)]["min"]
    if not python_requires:
        python_requires = salt_python_requires
    elif salt_python_requires > python_requires:
        click.secho(
            f"The minimum Salt version ({salt_version}) requires a higher minimum Python "
            f"version '{salt_python_requires}'. Adjusting accordingly.",
            fg="bright_red",
        )
        python_requires = salt_python_requires
    max_python_minor = SALT_PYTHON_SUPPORT[max_salt_version]["max"][1]

    templating_context: Dict[str, Any] = {
        "project_name": project_name,
        "author": author,
        "author_email": author_email,
        "summary": summary,
        "url": url,
        "salt_version": salt_version,
        "copyright_year": datetime.datetime.today().year,
        "python_requires": python_requires,
        "max_python_minor": max_python_minor,
        "max_salt_version": max_salt_version,
        "salt_python_support": copy.deepcopy(SALT_PYTHON_SUPPORT),
        "singular_loader_dirs": SINGULAR_MODULE_DIRS,
    }
    if no_saltext_namespace:
        package_namespace = package_namespace_path = package_namespace_pkg = ""
        templating_context["package_namespace"] = ""
    else:
        package_namespace = "saltext"
        package_namespace_pkg = f"{package_namespace}."
        package_namespace_path = f"{package_namespace}/"
        templating_context["package_namespace"] = "saltext"
    templating_context["package_namespace_pkg"] = package_namespace_pkg
    templating_context["package_namespace_path"] = package_namespace_path

    if not package_name:
        package_name = project_name.replace(" ", "_").replace("-", "_")

    templating_context["package_name"] = package_name

    if not source_url or not tracker_url and "github.com" in url:
        if not source_url:
            source_url = url
        if not tracker_url:
            tracker_url = "{}/issues".format(url.rstrip("/"))
    elif not tracker_url and source_url and "github.com" in source_url:
        tracker_url = "{}/issues".format(source_url.rstrip("/"))

    templating_context.update(
        {
            "source_url": source_url,
            "tracker_url": tracker_url,
        }
    )
    if docs_url:
        templating_context["docs_url"] = docs_url

    if license == "other":
        click.secho(
            "You can choose your license at https://choosealicense.com and then match "
            "it with the python license classifiers at https://pypi.org/classifiers",
            bold=True,
            fg="bright_yellow",
        )
        click.secho(
            "Make sure you update the 'license' field and also the classifiers on "
            "the generated 'setup.cfg'.",
            bold=True,
            fg="bright_yellow",
        )
    elif license:
        license_classifier: str = LICENSES[license]
        license_name: str = license_classifier.split(" :: ")[-1]
        templating_context["license_name"] = license_name
        templating_context["license_classifier"] = license_classifier

    templating_context["loaders"] = loader

    if not destdir.is_dir():
        destdir.mkdir(0o755)

    project_template_path = PACKAGE_ROOT / "project"
    for src in sorted(project_template_path.rglob("*")):
        if "__pycache__" in src.parts:
            # We're not interested in python pyc cache files
            continue
        if license == "other" and "LICENSE.j2" in src.parts:
            continue
        dst_parts = []
        templating_context["loader"] = loader
        for part in src.relative_to(project_template_path).parts:
            if part.endswith(".j2"):
                dst_parts.append(part[:-3])
                continue
            dst_parts.append(part)
        dst = destdir.joinpath(*dst_parts)
        if src.is_dir():
            if dst.exists():
                continue
            dst.mkdir(src.stat().st_mode, exist_ok=True)
            continue
        if dst.exists() and force_overwrite is False:
            click.secho(
                "Not overwriting '{}'. New name will be '{}'.".format(
                    dst.relative_to(dest), dst.relative_to(dest).with_suffix(".new")
                ),
                fg="bright_red",
            )
            dst = dst.with_suffix(".new")
        contents = src.read_text()
        if src.name.endswith(".j2"):
            try:
                contents = Template(contents).render(**templating_context)
            except jinja2.exceptions.TemplateError as exc:
                click.secho(
                    f"Failed to render template {src}: {exc}",
                    fg="bright_red",
                )
                raise
        if contents:
            dst.write_text(contents.rstrip() + "\n")
        else:
            dst.touch()

    loaders_package_path = destdir / "src" / package_namespace / package_name
    loaders_package_path.mkdir(0o755, parents=True)
    loaders_package_path.joinpath("__init__.py").write_text(
        Template(PACKAGE_INIT).render(**templating_context).rstrip() + "\n"
    )
    loaders_unit_tests_path = destdir / "tests" / "unit"
    loaders_integration_tests_path = destdir / "tests" / "integration"
    loaders_functional_tests_path = destdir / "tests" / "functional"
    for loader_name in loader:
        templating_context["loader"] = loader_name
        loader_dir = None
        if loader_name in SINGULAR_MODULE_DIRS:
            loader_dir = loaders_package_path / loader_name.rstrip("s")
        else:
            loader_dir = loaders_package_path / (loader_name.rstrip("s") + "s")
        loader_dir.mkdir(0o755)
        loader_dir_init = loader_dir / "__init__.py"
        if not loader_dir_init.exists():
            loader_dir_init.write_text("")
        if loader_name == "module":
            loader_template = MODULE_LOADER_TEMPLATE
        elif loader_name == "states":
            loader_template = STATE_LOADER_TEMPLATE
        elif loader_name == "sdb":
            loader_template = SDB_LOADER_TEMPLATE
        else:
            loader_template = LOADER_TEMPLATE
        loader_module_contents = Template(loader_template).render(**templating_context)
        loader_dir_module = loader_dir / f"{package_name}_mod.py"
        if loader_dir_module.exists() and force_overwrite is False:
            loader_dir_module = loader_dir_module.with_suffix(".new")
        loader_dir_module.write_text(loader_module_contents.rstrip() + "\n")

        loader_unit_tests_dir = None
        if loader_name in SINGULAR_MODULE_DIRS:
            loader_unit_tests_dir = loaders_unit_tests_path / loader_name.rstrip("s")
        else:
            loader_unit_tests_dir = loaders_unit_tests_path / (loader_name.rstrip("s") + "s")
        loader_unit_tests_dir.mkdir(0o755, exist_ok=True)
        loader_unit_tests_dir_init = loader_unit_tests_dir / "__init__.py"
        if not loader_unit_tests_dir_init.exists():
            loader_unit_tests_dir_init.write_text("")
        if loader_name == "module":
            loader_test_template = LOADER_MODULE_UNIT_TEST_TEMPLATE
        elif loader_name == "states":
            loader_test_template = LOADER_STATE_UNIT_TEST_TEMPLATE
        elif loader_name == "sdb":
            loader_test_template = LOADER_SDB_UNIT_TEST_TEMPLATE
        else:
            loader_test_template = LOADER_UNIT_TEST_TEMPLATE
        loader_unit_test_contents = Template(loader_test_template).render(**templating_context)
        loader_unit_test_module = loader_unit_tests_dir / f"test_{package_name}.py"
        if loader_unit_test_module.exists() and not force_overwrite:
            loader_unit_test_module = loader_unit_test_module.with_suffix(".new")
        loader_unit_test_module.write_text(loader_unit_test_contents.rstrip() + "\n")

        if loader_name in SINGULAR_MODULE_DIRS:
            loader_functional_tests_dir = loaders_functional_tests_path / loader_name.rstrip("s")
        else:
            loader_functional_tests_dir = loaders_functional_tests_path / (
                loader_name.rstrip("s") + "s"
            )
        loader_functional_tests_dir.mkdir(0o755, exist_ok=True)
        loader_functional_tests_dir_init = loader_functional_tests_dir / "__init__.py"
        if not loader_functional_tests_dir_init.exists():
            loader_functional_tests_dir_init.write_text("")
        if loader_name in ("module", "states"):
            if loader_name == "states":
                loader_test_template = LOADER_STATE_FUNCTIONAL_TEST_TEMPLATE
            else:
                loader_test_template = LOADER_MODULE_FUNCTIONAL_TEST_TEMPLATE
            loader_functional_test_contents = Template(loader_test_template).render(
                **templating_context
            )
            loader_functional_test_module = loader_functional_tests_dir / f"test_{package_name}.py"
            if loader_functional_test_module.exists() and not force_overwrite:
                loader_functional_test_module = loader_functional_test_module.with_suffix(".new")
            loader_functional_test_module.write_text(
                loader_functional_test_contents.rstrip() + "\n"
            )

        loader_integration_tests_dir = None
        if loader_name in SINGULAR_MODULE_DIRS:
            loader_integration_tests_dir = loaders_integration_tests_path / loader_name.rstrip("s")
        else:
            loader_integration_tests_dir = loaders_integration_tests_path / (
                loader_name.rstrip("s") + "s"
            )
        loader_integration_tests_dir.mkdir(0o755, exist_ok=True)
        loader_integration_tests_dir_init = loader_integration_tests_dir / "__init__.py"
        if not loader_integration_tests_dir_init.exists():
            loader_integration_tests_dir_init.write_text("")
        if loader_name != "module":
            continue
        loader_test_template = LOADER_MODULE_INTEGRATION_TEST_TEMPLATE
        loader_integration_test_contents = Template(loader_test_template).render(
            **templating_context
        )
        loader_integration_test_module = loader_integration_tests_dir / f"test_{package_name}.py"
        if loader_integration_test_module.exists() and not force_overwrite:
            loader_integration_test_module = loader_integration_test_module.with_suffix(".new")
        loader_integration_test_module.write_text(loader_integration_test_contents.rstrip() + "\n")

    requirements_dir = destdir / "requirements"
    for python_version in range(python_requires[1], max_python_minor + 1):
        reqdir = requirements_dir / f"py3.{python_version}"
        reqdir.mkdir(0o755, exist_ok=True)
        for extra in ("docs", "lint", "tests"):
            (reqdir / f"{extra}.txt").touch()

    click.secho("Bare bones project is created.", fg="bright_green", bold=True)
    click.secho("You should now run the following commands:")
    click.secho(f"  python3 -m venv .env --prompt {project_name!r}")
    click.secho("  source .env/bin/activate")
    click.secho("  git init .")
    click.secho("  python -m pip install -e .[dev,tests,docs]")
    click.secho("  pre-commit install")
    click.secho("  git add .")
    click.secho("  git commit -a")
    click.secho("The above command will fail because it's pinning the project dependencies.")
    click.secho("Now run the following commands:")
    click.secho("  git add .")
    click.secho("  git commit -a -m 'Initial extension layout'")
    click.secho("To run the included test suite, run the following command:")
    click.secho("  nox -e tests-3 -- tests/")
    click.secho("Please update these tests :)")
    click.secho("Start Hacking!", fg="bright_green", bold=True)


if __name__ == "__main__":
    main()
