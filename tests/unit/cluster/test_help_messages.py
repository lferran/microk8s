from click.testing import CliRunner
from leave import leave as leave_command
from join import join as join_command

import pytest


@pytest.mark.parametrize(
    "command,no_args_should_error,help_string",
    [
        (leave_command, True, "The node will depart from the cluster it is in."),
        (join_command, True, "Join the node to a cluster"),
    ],
)
def test_help_arguments_are_consistent_across_commands(command, no_args_should_error, help_string):
    runner = CliRunner()
    for help_arg in ("-h", "--help"):
        result = runner.invoke(command, [help_arg])
        import pdb; pdb.set_trace()
        assert help_string in result.output

    if no_args_should_error:
        result = runner.invoke(command, [])
        assert result.exit_code != 0
