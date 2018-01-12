class Nurse:
    """
    Class used to represent a nurse with his/her start time (in seconds from midnight) and availability (in seconds
    """

    def __init__(self, pk, start_time=0, availability=0):
        """
        Instanciates a Nurse object
        :param pk: the nurse's id
        :param start_time: the start time of availability in seconds from midnight
        :param availability: the availability duration (in seconds) of this nurse
        """
        self._pk = pk
        self._start_time = start_time
        self._availability = availability

    def _get_pk(self):
        return self._pk

    def _get_start_time(self):
        return self._start_time

    def _get_availability(self):
        return self._availability

    pk = property(_get_pk)
    start_time = property(_get_start_time)
    availability = property(_get_availability)

    def __str__(self):
        """
        Converts this nurse into a string
        :return: a string representing this nurse
        """
        return "Nurse : pk = {}, availability = {}, start_time = {}".format(self._pk, self._availability,
                                                                            self._start_time)
