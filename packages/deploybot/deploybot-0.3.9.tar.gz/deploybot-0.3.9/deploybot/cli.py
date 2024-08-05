import argparse
from deploybot.commands.configure import configure
from deploybot.commands.shared import main_ecs, main_lambda, main_migrate
from deploybot.utils.version import get_version
import sys

def main():
    VERSION = get_version()
    
    parser = argparse.ArgumentParser(prog='deploybot', description='Deploybot CLI')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s {}'.format(VERSION))

    subparsers = parser.add_subparsers(dest='command')

    # Configure command
    parser_configure = subparsers.add_parser('configure', help='Configure AWS account ID and environment')
    parser_configure.set_defaults(func=configure)

    # ECS command
    parser_ecs = subparsers.add_parser('ecs', help='ECS related commands')
    parser_ecs.add_argument('action', choices=['deploy'], help='Action to perform')
    parser_ecs.add_argument('service_name', help='Name of the service')
    parser_ecs.set_defaults(func=main_ecs)

    # Lambda command
    parser_lambda = subparsers.add_parser('lambda', help='Lambda related commands')
    parser_lambda.add_argument('action', choices=['deploy'], help='Action to perform')
    parser_lambda.add_argument('service_name', help='Name of the service to deploy')
    parser_lambda.set_defaults(func=main_lambda)

    # Migrate command
    parser_migrate = subparsers.add_parser('migrate', help='Database migration commands')
    parser_migrate.add_argument('db_type', choices=['mysql'], help='Type of the database to migrate')
    parser_migrate.set_defaults(func=main_migrate)

    args = parser.parse_args()

    try:
        if hasattr(args, 'func'):
            args.func(args)
        else:
            parser.print_help()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)

if __name__ == '__main__':
    main()
