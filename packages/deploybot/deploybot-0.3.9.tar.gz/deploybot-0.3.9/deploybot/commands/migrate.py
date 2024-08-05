import os
import sys
import subprocess

def run_script(script_path, env_vars):
    try:
        process = subprocess.Popen(
            ['bash', '-c', f'bash {script_path}'],
            env=env_vars,
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        process.communicate()
        return process.returncode
    except KeyboardInterrupt:
        print("\nScript execution cancelled by user.")
        sys.exit(0)

def main_migrate(args):
    if args.db_type == 'mysql':
        script_path = '.support/deploybot/migrate'
        if not os.path.exists(script_path):
            print("Migration script not found at: {}".format(script_path))
            return

        print("Running migration script for MySQL: {}".format(script_path))
        env_vars = os.environ.copy()
        run_script(script_path, env_vars)
    else:
        print("Invalid database type. Only 'mysql' is supported.")
