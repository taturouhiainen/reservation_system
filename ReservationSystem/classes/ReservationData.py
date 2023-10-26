class ReservationData:
    def __init__(self):
        self.reservation_number = None
        self.jet_ski = None
        self.reservation_length = None
        self.reservation_date = None
        self.reservation_time = None
        self.reservation_price = None
        self.number_of_riders = None
        self.additional_services = None
        self.customer = None
        self.confirmation_details = None
        self.timestamp = None

    def get_reservation_price(self, reservation_time):
        if isinstance(reservation_time, str):
            reservation_time = int(reservation_time)

        if reservation_time == 1:
            reservation_price = 69
        elif reservation_time == 2:
            reservation_price = 119
        elif reservation_time == 5:
            reservation_price = 199
        elif reservation_time == 10:
            reservation_price = 299
        elif reservation_time == 24:
            reservation_price = 399
        else:
            reservation_price = None
        self.reservation_price = reservation_price
        return reservation_price

    def get_additional_services(self):
        if self.additional_services is None:
            return ""

        service_names = []
        for service in self.additional_services:
            service_names.append(service.get_name())

        return ", ".join(service_names)
