# Simple script to initialize template project

import shlex
import subprocess
from pathlib import Path

YES = object()
NO = object()

def prompt(prompt, value=None):
    if value is YES:
        prompt = f"{prompt} [Y/n] "
        value = "y"
    elif value is NO:
        prompt = f"{prompt} [y/N] "
        value = "n"
    elif value:
        prompt = f"{prompt} [{value}]: "
    else:
        prompt = f"{prompt}: "

    result = input(prompt)
    if value and not result:
        result = value

    return result


def run(cmd, **kwargs):
    line = " ".join(shlex.quote(c) for c in cmd)
    print(f"$ {line}")
    return subprocess.run(cmd, **kwargs)


def main():
    author = email = username = project = package = description = correct = ""

    while correct.lower() != "y":
        author = prompt("Author name", author)
        email = prompt("Email address", email)
        username = prompt("Github username/organization", username)
        project = prompt("Project name", project)
        package = package or project.lower()
        package = prompt("Package name", package)
        description = prompt("Short description", description)

        print()
        print(f"{username = !r}")
        print(f"{author = !r}")
        print(f"{email = !r}")
        print(f"{project = !r}")
        print(f"{package = !r}")
        print(f"{description = !r}")
        correct = prompt("\nCorrect?", NO)
        print()

    root = Path(__file__).parent
    queue = list(root.iterdir())

    pkgdir = root / "PACKAGE"
    if pkgdir.is_dir():
        run(["git", "mv", pkgdir.as_posix(), pkgdir.with_name(package).as_posix()])

    proc = run(["git", "ls-files"], encoding="utf-8", capture_output=True)
    queue = [Path(p) for p in proc.stdout.splitlines()]
    for path in queue:
        if path.name == "init.py":
            continue

        original = path.read_text()
        updated = (
            original.replace("GITHUB_USERNAME", username)
            .replace("AUTHOR_NAME", author)
            .replace("AUTHOR_EMAIL", email)
            .replace("PROJECT_NAME", project)
            .replace("PACKAGE_NAME", package)
            .replace("PROJECT_DESCRIPTION", description)
        )

        if path.name == "makefile" and "@python init.py" in updated:
            updated = "\n".join(updated.splitlines()[:-2])

        if original != updated:
            print(f"Writing {path}")
            path.write_text(updated)

    run(["git", "add", "."])
    run(["git", "rm", __file__])

    commit = prompt("\nCommit changes?", YES)
    if commit.lower() == "y":
        run(["git", "commit"])


if __name__ == "__main__":
    main()
