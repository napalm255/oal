#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Office 365 Address Lists.

Primary module.
"""

from __future__ import absolute_import, print_function
import logging
from xml.etree import ElementTree
import sys
import re
import ipaddress
import requests
from oal.log import configure_logging


if sys.version_info < (3,):
    import codecs

    def u(x):
        """Unicode function."""
        # pylint: disable = invalid-name
        return codecs.unicode_escape_decode(x)[0]
else:
    def u(x):
        """Unicode function."""
        # pylint: disable = invalid-name
        return x


class Office365Config(object):
    """Class for Office 365 Config."""
    # pylint: disable = too-few-public-methods

    _url = ('https://support.content.office.net'
            '/en-us/static/O365IPAddresses.xml')

    _products = ('all', 'o365', 'lyo', 'planner', 'proplus',
                 'onenote', 'spo', 'wac', 'crls', 'ex-fed',
                 'officeipad', 'exo', 'yammer', 'officemobile',
                 'sway', 'identity', 'office365video', 'rca', 'eop')

    @property
    def url(self):
        """Get url."""
        return self._url

    @property
    def products(self):
        """Get products."""
        return self._products


class Office365AddressList(object):
    """Class for Office 365 Address List."""
    # pylint: disable = too-many-instance-attributes
    # pylint: disable = no-self-use

    _oal_url = Office365Config().url
    _debug = False
    _selected_products = None
    _products = None
    minimize = False
    xml = None

    def __init__(self, debug=False):
        self.debug = debug
        self.load()

    def load(self):
        """Get xml."""
        response = requests.get(self._oal_url)
        self.xml = response.content
        self.products = ElementTree.fromstring(self.xml)
        return response

    def minimize_urls(self, addr):
        """Return minimized url."""
        root = r'(.*\.)?([a-zA-Z0-9-_]+\.[a-zA-Z]+)(\/.*)?$'
        return set([re.search(root, addy).group(2).lower() for addy in addr])

    def minimize_ips(self, addr):
        """Return minimized IP."""
        return set([ipaddr for ipaddr in ipaddress.collapse_addresses(addr)])

    def minimize_list(self, addr, addr_list):
        """Return minimized address list."""
        if 'ipv' in addr_list:
            addr = self.minimize_ips(addr)
        elif 'url' in addr_list:
            addr = self.minimize_urls(addr)
        return addr

    def address_list(self, addr_list):
        """Get sorted list of urls for all selected products."""
        addr = []
        for address_list in self.address_lists:
            if addr_list in address_list.attrib['type'].lower():
                for addy in address_list:
                    if 'ipv4' in addr_list:
                        addr.append(ipaddress.IPv4Network(u(addy.text)))
                    elif 'ipv6' in addr_list:
                        addr.append(ipaddress.IPv6Network(u(addy.text)))
                    elif 'url' in addr_list:
                        addr.append(addy.text)

        if self.minimize is True:
            addr = self.minimize_list(addr, addr_list)

        for addr in sorted(addr):
            yield addr

    def checkpoint_object(self, address):
        """Get checkpoint object."""
        obj_name = 'O365_%s' % address.network_address
        obj_comment = 'Office 365'
        obj_color = 'magenta'
        obj_ref = 'network_objects %s' % obj_name
        obj = '\n'.join([
            'create network %s' % (obj_name),
            'modify %s ipaddr %s' % (obj_ref, address.network_address),
            'modify %s netmask %s' % (obj_ref, address.netmask),
            'modify %s comments "%s"' % (obj_ref, obj_comment),
            'modify %s color "%s"' % (obj_ref, obj_color),
            'update %s' % (obj_ref)])
        return obj

    @property
    def debug(self):
        """Get debug setting."""
        return self.debug

    @debug.setter
    def debug(self, enabled):
        """Setup debugging."""
        level = 'DEBUG' if enabled else 'WARNING'
        configure_logging(level=level)
        logging.debug('Debug enabled for "%s"...', __file__)
        return level

    @property
    def selected_products(self):
        """Get selected products."""
        return self._selected_products

    @selected_products.setter
    def selected_products(self, value):
        if value:
            self._selected_products = value

    @property
    def products(self):
        """Get selected products."""
        for product in self._products:
            if product.attrib['name'].lower() in self.selected_products:
                yield product

    @products.setter
    def products(self, value):
        """Set products."""
        self._products = value

    @property
    def address_lists(self):
        """Get address lists."""
        for product in self.products:
            for address_lists in product:
                yield address_lists

    @property
    def urls(self):
        """Get urls."""
        return self.address_list('url')

    @property
    def urls_count(self):
        """Get number of urls."""
        return len([x for x in self.urls])

    @property
    def ipv4(self):
        """Get ipv4."""
        return self.address_list('ipv4')

    @property
    def ipv4_count(self):
        """Get number of ipv4."""
        return len([x for x in self.ipv4])

    @property
    def ipv6(self):
        """Get ipv6."""
        return self.address_list('ipv6')

    @property
    def ipv6_count(self):
        """Get number of ipv6."""
        return len([x for x in self.ipv6])

    @property
    def checkpoint(self):
        """Get checkpoint objects."""
        for addr in self.address_list('ipv4'):
            yield self.checkpoint_object(addr)

    @property
    def checkpoint_count(self):
        """Get number of checkpoint objects."""
        return len([x for x in self.checkpoint])

    @property
    def cisco(self):
        """Get cisco rules."""
        for addr in self.address_list('ipv4'):
            yield 'permit ip %s %s any' % (addr.network_address,
                                           addr.netmask)

    @property
    def cisco_count(self):
        """Get number of cisco rules."""
        return len([x for x in self.checkpoint])
