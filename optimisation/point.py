class Point:
    """
    Class used to represent a point on the map, given its address or latitude/longitude
    """

    def __init__(self, address=None, x=0., y=0., identifier=""):
        """
        Instanciates a Point object. If no address is specified, the address is x,y
        :param identifier: a string identifier for this point
        :param address: a string which represents the address of the point
        :param x: the x coordinate (longitude) of this point
        :param y: the y coordinate (latitude) of this point
        """
        self._identifier = identifier
        if address is None:
            self._address = str(x) + "," + str(y)
        else:
            self._address = address

    def _get_identifier(self):
        return self._identifier

    def _get_address(self):
        return self._address

    identifier = property(_get_identifier)
    address = property(_get_address)

    def __str__(self):
        """
        Converts this point into a string
        :return: a string representing this point
        """
        return "identifier : {}, address : {}".format(self._identifier, self._address)


class Patient(Point):
    """
    Class that iherits from Point, representing a patient on the map
    """

    def __init__(self, address=None, x=0., y=0., identifier="", duration_of_care=0, pk=-1,
                 must_be_visited_exactly_at=-1):
        """
        Instanciates a Patient object. If no address is specified, the address is x,y
        :param address: a string which represents the address of the patient
        :param x: the x coordinate (longitude) of this patient
        :param y: the y coordinate (latitude) of this patient
        :param identifier: a string identifier for this patient
        :param duration_of_care: the duration of the care in seconds
        :param pk: the id of the patient
        :param must_be_visited_exactly_at: the time (in seconds from midnight) when the patient should be exactly
                    visited (-1 if no constraint)
        """
        Point.__init__(self, address=address, x=x, y=y, identifier=identifier)
        self._duration_of_care = duration_of_care
        self._pk = pk
        self._must_be_visited_exactly_at = must_be_visited_exactly_at

    def _get_duration_of_care(self):
        return self._duration_of_care

    def _get_pk(self):
        return self._pk

    def _get_must_be_visited_exactly_at(self):
        return self._must_be_visited_exactly_at

    def _set_must_be_visited_exactly_at(self, must_be_visited_exactly_at):
        self._must_be_visited_exactly_at = must_be_visited_exactly_at

    duration_of_care = property(_get_duration_of_care)
    pk = property(_get_pk)
    must_be_visited_exactly_at = property(_get_must_be_visited_exactly_at, _set_must_be_visited_exactly_at)

    def __str__(self):
        """
        Converts this patient into a string
        :return: a string representing this patient
        """
        result = "identifier : {}, address : {}, duration of care : {}, pk : {}".format(self._identifier, self._address,
                                                                               self._duration_of_care, self._pk)
        if self._must_be_visited_exactly_at != -1:
            result += ", must be exactly visited at : {}".format(self._must_be_visited_exactly_at)
        return result


class Office(Point):
    """
    Class that inherits from Point, used to represent the central office of the service,
     where all nurses start their rounds from
    """

    def __init__(self, address=None, x=0., y=0., identifier=""):
        """
        Instanciates an Office object. If no address is specified, the address is x,y
        :param identifier: a string identifier for this point
        :param address: a string which represents the address of the office
        :param x: the x coordinate (longitude) of this point
        :param y: the y coordinate (latitude) of this point
        """
        Point.__init__(self, address=address, x=x, y=y, identifier=identifier)
