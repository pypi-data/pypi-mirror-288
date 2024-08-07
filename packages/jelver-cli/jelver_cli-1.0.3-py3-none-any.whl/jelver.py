#!/usr/bin/env python3

"""Usage:
  jelver test --api-key=<api-key> <website> [--local] [<website-username> <website-password>] [--browser=<browsertype>]
  jelver cases ls --api-key=<api-key>
  jelver cases add <case_ids> --api-key=<api-key>
  jelver cases rm <case_ids> --api-key=<api-key>
  jelver (-h | --help)

Description:
    Most of the commands to run the end-to-end tests from your application.

Commands:
  test                 Run all the tests recorded from your application
  cases ls             List all the cases that are recorded from your application
  cases add            Include the cases that you want to test
  cases rm             Exclude the cases that you don't want to test

Arguments:
  case_ids             The case ids that you want to include
                       or exclude, they must be separated by a comma (ex: 1,2,344)
  website              The URL of the website to be tested
  website-username     The username to be used to login
  website-password     The password to be used to login
  browsertype          The browser type to be used to run the tests

Options:
  -h --help
  --api-key=<api-key>  The API key to authenticate the user
  --local              Use this option to test on 'localhost'
"""

import sys
from docopt import docopt
from local_tests import LocalTests
from remote_tests import RemoteTests
from cases_management import CasesManagement
from utils.jelver_exceptions import JelverAPIException


def main():
    """
    Main function that runs a command based on the arguments

    Arguments:
    :args: None

    Return: None
    """
    docopt_version = '1.0.3'
    args = docopt(__doc__, version=docopt_version)

    if args['--api-key'] is None:
        raise JelverAPIException("You must provide an API key to authenticate the user")

    if args['test']:
        website = args['<website>']
        if website.startswith("localhost"):
            raise JelverAPIException(
                "Testing on 'localhost' is not supported right now. If you'd like us to " +
                "implement this please send a message to info@jelver.com"
            )
        if not website.startswith("https://"):
            website = f"https://{website}"

        if args['--local']:
            LocalTests(
                url=website,
                api_key=args["--api-key"],
                browser_type=args["--browser"]
            ).run()
        elif not args['--local']:
            RemoteTests(
                url=website,
                username=args.get('<website-username>'),
                password=args.get('<website-password>'),
                api_key=args["--api-key"]
            ).run()
    elif args['cases']:
        if args['ls']:
            CasesManagement(args["--api-key"]).list()
        elif args['add']:
            CasesManagement(args["--api-key"]).add(args['<case_ids>'])
        elif args['rm']:
            CasesManagement(args["--api-key"]).remove(args['<case_ids>'])
    else:
        sys.argv.append('-h')
        docopt(__doc__, version=docopt_version)


if __name__ == '__main__':
    main()
