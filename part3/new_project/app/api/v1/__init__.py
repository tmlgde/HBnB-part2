from .protected import api as protected_ns
api.add_namespace(protected_ns, path='/api/v1/protected')
