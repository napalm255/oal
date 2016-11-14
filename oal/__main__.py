#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Office 365 Address Lists.

Command line interface module.
"""

from __future__ import absolute_import, print_function
import logging
import click
from oal.oal import Office365AddressList, Office365Config


@click.command()
@click.pass_context
@click.option('-d/-nd', '--debug/--no-debug', default=False,
              help='Enable or Disable Debug')
@click.option('-m/-nm', '--mini/--no-mini', default=True,
              help=('Minimize output by shortening URLs to their root '
                    'and collapsing IP networks. Enabled by default.'))
@click.option('-u/-nu', '--urls/--no-urls', default=False,
              help='Output URL List')
@click.option('-4/-n4', '--ipv4/--no-ipv4', default=False,
              help='Output IPv4 Address List')
@click.option('-6/-n6', '--ipv6/--no-ipv6', default=False,
              help='Output IPv6 Address List')
@click.option('-cp/-ncp', '--checkpoint/--no-checkpoint', default=False,
              help='Output Checkpoint dbedit script')
@click.option('-cs/-ncs', '--cisco/--no-cisco', default=False,
              help='Output Cisco ACL')
@click.argument('products', nargs=-1,
                type=click.Choice(Office365Config().products))
def cli(ctx=None, debug=False, mini=False, urls=False, ipv4=False,
        ipv6=False, checkpoint=False, cisco=False, products=None):
    """Office 365 Address Lists."""
    # pylint: disable = too-many-arguments

    def header(msg):
        """Echo."""
        line = '-'*60
        click.echo(line)
        click.echo(msg)
        click.echo(line)

    office = Office365AddressList()
    office.debug = debug
    office.minimize = mini

    logging.debug('Option --debug: %s', debug)
    logging.debug('Option --urls: %s', urls)
    logging.debug('Option --ipv4: %s', ipv4)
    logging.debug('Option --ipv6: %s', ipv6)
    logging.debug('Argument [PRODUCTS]: %s', products)

    if len(products):
        office.selected_products = products
        click.echo('Selected Products: %s\n' %
                   ', '.join(office.selected_products))
    else:
        print(ctx.get_help())
        return

    if urls is True:
        header('Unique URLs: (%s)' % (office.urls_count))
        for url in office.urls:
            click.echo(url)

    if ipv4 is True:
        header('Unique IPv4: (%s)' % (office.ipv4_count))
        for address in office.ipv4:
            click.echo(address)

    if ipv6 is True:
        header('Unique IPv6: (%s)' % (office.ipv6_count))
        for address in office.ipv6:
            click.echo(address)

    if checkpoint is True:
        header(('Unique IPv4 as a Checkpoint dbedit script: '
                '(%s)' % (office.checkpoint_count)))
        click.echo('# Save and copy output to Check Point management server')
        click.echo('# Run "dbedit -local -f /path/to/script.txt"')
        for address in office.checkpoint:
            click.echo(address)
        click.echo('update_all')
        click.echo('savedb')

    if cisco is True:
        header(('Unique IPv4 as a ' 'Cisco ACL: (%s)' % (office.cisco_count)))
        for address in office.cisco:
            click.echo(address)


def main():
    """Main entry point."""
    click.echo('='*60)
    click.echo('Office 365 Address Lists')
    click.echo('='*60)
    cli()


if __name__ == "__main__":
    main()
