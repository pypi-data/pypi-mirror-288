# Copyright (c) 2022,2023,2024 Kian-Meng Ang

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Generals Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Nox configuration."""

import nox


@nox.session()
def deps(session: nox.Session) -> None:
    """Update pre-commit hooks and deps."""
    session.install("pre-commit", "pipenv")
    session.run("pre-commit", "autoupdate", *session.posargs)
    session.run("pipenv", "update", env={"PIPENV_VERBOSITY": "-1"})


@nox.session()
def lint(session: nox.Session) -> None:
    """Run pre-commit linter."""
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files", *session.posargs)


@nox.session(python=["3.8", "3.9", "3.10", "3.11", "3.12"])
def test(session: nox.Session) -> None:
    """Run test."""
    _pipenv_install(session)
    session.run(
        "pipenv", "run", "pytest", "--numprocesses", "auto", *session.posargs
    )


@nox.session(python="3.12")
def cov(session: nox.Session) -> None:
    """Run test coverage."""
    _pipenv_install(session)
    session.run(
        "pipenv",
        "run",
        "pytest",
        "--numprocesses",
        "auto",
        "--cov",
        "--cov-report=term",
        "--cov-report=html",
    )


@nox.session(python="3.12")
def doc(session: nox.Session) -> None:
    """Build doc with sphinx."""
    _pipenv_install(session)
    session.run("sphinx-build", "docs/source/", "docs/build/html")


@nox.session(python="3.12")
def readme(session: nox.Session) -> None:
    """Update console help menu to readme."""
    _pipenv_install(session)
    with open("README.md", "r+", encoding="utf8") as f:
        help_message = session.run("fotolab", "-h", silent=True)
        help_codeblock = f"\n\n```console\n{help_message}```\n\n"

        content = f.read()
        marker = content.split("<!--help !-->")[1]
        readme_md = content.replace(marker, help_codeblock)

        f.seek(0)
        f.write(readme_md)


def _pipenv_install(session: nox.Session) -> None:
    session.install("pipenv")
    session.run("pipenv", "install", "--dev", env={"PIPENV_VERBOSITY": "-1"})
