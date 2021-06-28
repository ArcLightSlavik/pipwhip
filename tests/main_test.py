from click.testing import CliRunner
from pytest_mock import MockerFixture

from pipwhip.main import pipwhip


def test_execute_fake_package(mocker: MockerFixture) -> None:
    mocker.patch(
        "pipwhip.main.get_versions",
        return_value=(
            "pipwhip_test_package_one",
            ["0.0.2", "0.0.1"],
        ),
    )

    runner = CliRunner()

    with runner.isolated_filesystem():
        with open("requirements_isolated.txt", "w") as f:
            f.write("pipwhip_test_package_one==0.0.1")

        runner.invoke(pipwhip, ["-r", "requirements_isolated.txt"])

        with open("requirements_isolated.txt") as f:
            result = f.read()

        assert result.strip() == "pipwhip_test_package_one==0.0.2"


def test_execute_real_package() -> None:
    runner = CliRunner()

    with runner.isolated_filesystem():
        with open("requirements_isolated.txt", "w") as f:
            f.write("recruiter-utils==0.0.1")

        runner.invoke(pipwhip, ["-r", "requirements_isolated.txt"])

        with open("requirements_isolated.txt") as f:
            result = f.read()

        assert result.strip() == "recruiter-utils==0.0.3"
