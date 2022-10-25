from sail_safe_functions_orchestrator.client_rpc_base import ClientRPCBase


class ClientRPCLocal(ClientRPCBase):
    def call(self, safe_function_class, *safe_function_arguments):
        return safe_function_class.run(*safe_function_arguments)
