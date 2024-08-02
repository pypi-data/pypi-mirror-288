import re
from functools import wraps


def versioned(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        version = request.version
        if not version:
            return func(self, request, *args, **kwargs)

        try:
            version_function = getattr(self, f"{func.__name__}_{version.replace('.', '_')}")
        except:
            r = re.compile(fr"{func.__name__}_(\d+)_(\d+)")
            version_functions = list(filter(r.match, dir(self)))

            if not version_functions:
                raise Exception(f"Version '{version}' not found.")

            version_functions = sorted(
                version_functions,
                key=lambda x: [int(part) if part.isdigit() else part for part in x.split('_')]
            )
            version_function = getattr(self, version_functions[-1])

        return version_function(request, *args, **kwargs)
    return wrapper