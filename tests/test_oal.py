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

    def test_no_args(self):
        """Test No Arguments."""
        runner = CliRunner()
        result = runner.invoke(cli)
        assert result.exit_code == 0
        assert 'Office 365' in result.output

    def test_help(self):
        """Test Help."""
        runner = CliRunner()
        help_result = runner.invoke(cli, ['--help'])
        assert help_result.exit_code == 0
        assert 'Show this message and exit.' in help_result.output

    def test_urls(self):
        """Test URLs."""
        runner = CliRunner()
        product_url_result = runner.invoke(cli, ['-u', 'o365'])
        assert product_url_result.exit_code == 0
        assert 'Selected Products: o365' in product_url_result.output
        assert 'URLs' in product_url_result.output

    def test_ipv4(self):
        """Test IPv4."""
        runner = CliRunner()
        product_v4_result = runner.invoke(cli, ['-4', 'o365'])
        assert product_v4_result.exit_code == 0
        assert 'Selected Products: o365' in product_v4_result.output
        assert 'IPv4' in product_v4_result.output

    def test_ipv6(self):
        """Test IPv6."""
        runner = CliRunner()
        product_v6_result = runner.invoke(cli, ['-6', 'eop'])
        assert product_v6_result.exit_code == 0
        assert 'Selected Products: eop' in product_v6_result.output
        assert 'IPv6' in product_v6_result.output

    def test_checkpoint(self):
        """Test Checkpoint."""
        runner = CliRunner()
        product_cp_result = runner.invoke(cli, ['-cp', 'o365'])
        assert product_cp_result.exit_code == 0
        assert 'Selected Products: o365' in product_cp_result.output
        assert 'Checkpoint' in product_cp_result.output

    def test_cisco(self):
        """Test Cisco."""
        runner = CliRunner()
        product_cisco_result = runner.invoke(cli, ['-cs', 'o365'])
        assert product_cisco_result.exit_code == 0
        assert 'Selected Products: o365' in product_cisco_result.output
        assert 'Cisco' in product_cisco_result.output

    @classmethod
    def teardown_class(cls):
        pass


if __name__ == '__main__':
    sys.exit(pytest.main())
