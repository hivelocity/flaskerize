
def _generate(contents, file, mode='w', dry_run=False):
    if not dry_run:
        with open(file, mode) as fid:
            fid.write(contents)
    print(f"Successfully created {file}")


def hello_world(args):
    print('Generating a hello_world app')

    CONTENTS = f"""import os
from flask import Flask, send_from_directory

def create_app():
    app = Flask(__name__)

    # Serve React App
    @app.route('/')
    def serve():
        return 'Hello, Flaskerize!'
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()

    """
    _generate(CONTENTS, args.output_name, dry_run=args.dry_run)
    print("Successfully created new app '{}'".format(args.output_name))


def app(args):
    """
    Serve files using `send_from_directory`. Note this is less secure than
    from_static_filesas anything within the directory can be served.
    """
    print('args = ', args)
    print('Generating a from_static_dir app')

    # The routing for `send_from_directory` comes directly from https://stackoverflow.com/questions/44209978/serving-a-create-react-app-with-flask  # noqa
    CONTENTS = f"""import os
from flask import Flask, send_from_directory


def create_app():
    app = Flask(__name__, static_folder='{args.static_dir_name}')

    # Serve static site
    @app.route('/', defaults={{'path': ''}})
    @app.route('/<path:path>')
    def serve(path):
        if path != "" and os.path.exists(app.static_folder + path):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()

    """
    _generate(CONTENTS, args.output_name, dry_run=args.dry_run)
    print("Successfully created new app '{}'".format(args.output_name))


def blueprint(args):
    """
    Static site blueprint
    """
    print('args = ', args)
    print('Generating a blueprint from static site')

    # The routing for `send_from_directory` comes directly from https://stackoverflow.com/questions/44209978/serving-a-create-react-app-with-flask  # noqa
    CONTENTS = f"""import os
from flask import Blueprint, send_from_directory

site = Blueprint('site', __name__, static_folder='{args.static_dir_name}')

# Serve static site
@site.route('/', defaults={{'path': ''}})
@site.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(site.static_folder + path):
        return send_from_directory(site.static_folder, path)
    else:
        return send_from_directory(site.static_folder, 'index.html')

    """
    _generate(CONTENTS, args.output_name, dry_run=args.dry_run)
    print("Successfully created new blueprint '{}'".format(args.output_name))


# Mapping of keywords to generation functions
a = {
    'hello-world': hello_world, 'hw': hello_world,
    'app': app,
    'blueprint': blueprint, 'bp': blueprint
}
