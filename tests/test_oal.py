#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `oal` module."""

import pytest
from contextlib import contextmanager
from click.testing import CliRunner
from oal.__main__ import cli


class TestOal(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_command_line_interface(self):
        """Test command line interface."""
        runner = CliRunner()
        result = runner.invoke(cli)
        assert result.exit_code == 0
        assert 'Office 365' in result.output

    def test_help(self):
        """Test help."""
        runner = CliRunner()
        help_result = runner.invoke(cli, ['--help'])
        assert help_result.exit_code == 0
        assert 'Show this message and exit.' in help_result.output

    def test_options(self):
        """Test options."""
        runner = CliRunner()
        product_url_result = runner.invoke(cli, ['-u', 'o365'])
        assert product_url_result.exit_code == 0
        assert 'Selected Products: o365' in product_url_result.output
        product_v4_result = runner.invoke(cli, ['-4', 'o365'])
        assert product_v4_result.exit_code == 0
        assert 'Selected Products: o365' in product_v4_result.output
        product_v6_result = runner.invoke(cli, ['-6', 'eop'])
        assert product_v6_result.exit_code == 0
        assert 'Selected Products: eop' in product_v6_result.output

    @classmethod
    def teardown_class(cls):
        pass


if __name__ == '__main__':
    sys.exit(pytest.main())
