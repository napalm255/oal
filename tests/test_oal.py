#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `oal` module."""

import pytest
from contextlib import contextmanager
from click.testing import CliRunner
from oal.oal import cli


class TestOal(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_command_line_interface(self):
        runner = CliRunner()
        result = runner.invoke(cli)
        assert result.exit_code == 0
        assert 'oal.cli' in result.output
        help_result = runner.invoke(cli, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output

    def test_something(self):
        pass

    @classmethod
    def teardown_class(cls):
        pass


if __name__ == '__main__':
    sys.exit(pytest.main())
