class SpecNotFound(RuntimeError):
    pass


exception_to_exit_code = dict(SpecNotFound=1, IOError=7)
