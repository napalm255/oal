#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup AUTHORS.rst.

Read git commits and update AUTHORS.rst.
"""
import logging
import re
from git import Repo
from git.exc import InvalidGitRepositoryError
from git.exc import GitCommandError

__title__ = 'Setup AUTHORS.rst'
__author__ = 'Brad Gibson'
__email__ = 'napalm255@gmail.com'
__version__ = '0.1.0'


def update():
    """Main entry point."""
    log_file, log_level = (None, logging.INFO)
    log_format = '%(levelname)s: %(message)s'
    logging.basicConfig(filename=log_file, level=log_level, format=log_format)
    logging.info('Running %s', __file__)

    try:
        repo = Repo()
        assert not repo.bare
    except InvalidGitRepositoryError:
        logging.error('not a git repository')
        exit()

    try:
        master = list(repo.iter_commits('master'))
    except GitCommandError:
        logging.error('git error')
        exit()

    contributors = {}
    for commit in master:
        author = commit.author.name
        author_count = contributors.get(author, 0)
        contributors[author] = author_count + 1
    with open('AUTHORS.rst', 'r') as authors_file:
        authors = authors_file.read()
    logging.debug(authors)

    pattern = re.compile('Contributors.*$', re.M | re.DOTALL)
    authors = pattern.sub('', authors)
    logging.debug(authors)

    authors += 'Contributors\n%s\n\n' % ('-'*12)
    contribs = list(contributors.keys())
    contribs.sort(key=lambda x: contributors[x], reverse=True)
    for key in contribs:
        pattern = re.compile(r'%s \(.*\).*' % key)
        match = pattern.search(authors)
        if not match:
            authors += '* %s (%s commits)\n' % (key, contributors[key])

    logging.info('writing AUTHORS.rst:\n%s', authors)
    with open('AUTHORS.rst', 'w') as authors_file:
        authors_file.write(authors)

if __name__ == '__main__':
    update()
