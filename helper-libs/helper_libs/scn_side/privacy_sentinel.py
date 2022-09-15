class PrivacySentinel:
    """
    A helper Library to be used on the SCN side to vet query privacy.
    """

    @staticmethod
    def query_limit_local_n_precompute(list_list_precompute, n=10):
        # Check federated sample is appropriate length
        length = 0
        for list in list_list_precompute:
            length = list[-1] + length
        PrivacySentinel.query_limit_local_n(length, n)

    @staticmethod
    def query_limit_local_n(num_samples: int, n: int = 10) -> bool:
        """
        Blocks a query if the number of samples is under a threshold n.

        :param: samples: The List of samples
        :type: Integer
        :param: n: The threshold limit on number of samples (default=10)
        :type: Integer
        :return: Whether the number of samples is above the threshold
        :type: Boolean
        """
        if num_samples < n:
            raise NameError("Too few samples")
        else:
            return True
