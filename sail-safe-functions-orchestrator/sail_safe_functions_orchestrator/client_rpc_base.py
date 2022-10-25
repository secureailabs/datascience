class ClientRPCBase:
    def call(self, safe_function_class, *safe_function_arguments):
        raise NotImplementedError()
