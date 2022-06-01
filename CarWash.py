class Reservation:
    def __init__(self, services, date, time):
        self.services = services
        self.time = (date - 1) * 12 * 60 + time  # Every day is 12 hours long
        self.duration = self.reservation_duration(services)

    @staticmethod
    def reservation_duration(services):
        return sum(CarWash.available_services[service] for service in services)

    @staticmethod
    def format_time(time):
        date = time // 12 // 60 + 1
        time = time % (12 * 60)
        hour, minute = divmod(time, 60)
        hour += CarWash.time_schedule['start']
        return '{:02d} {:02d}:{:02d}'.format(date, hour, minute)


class CarWash:
    def __init__(self):
        self.reservations = []

    time_schedule = {
        'start': 9,
        'end': 21
    }
    available_services = {
        'sefrshooyi': 60,
        'rooshooyi': 15,
        'nezafat': 20
    }

    def add_reservation(self, services, date=1, time=0):
        self.reservations.append(Reservation(services, date, time))

    def number_of_reservations(self):
        return len(self.reservations)

    def __iter__(self):
        return _CarWashIterator(self)


class _CarWashIterator:
    def __init__(self, car_wash):
        self.car_wash = car_wash
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.car_wash.reservations):
            raise StopIteration
        reservation = self.car_wash.reservations[self.index]
        self.index += 1
        return reservation


class CommandDispatcher:
    def __init__(self, car_wash):
        self._car_wash = car_wash
        self._commands = {
            'reserve': self._reserve,
            'list-reservations': self._list_reservations,
        }

    def dispatch(self, command):
        command, *parameters = command.split()
        self._handle_command(command, parameters)

    def _handle_command(self, command, parameters):
        if command in self._commands:
            try:
                self._commands[command](
                    parameters) if parameters else self._commands[command]()
            except Exception as e:
                print("ERROR: ", e)
        else:
            print('Unknown command:', command)

    def _reserve(self, *parameters):
        if parameters[0][0] == 'earliest':
            self._reserve_earliest(parameters[0][1].split('+'))
        else:
            self._reserve_exact(
                parameters[0][0], parameters[0][1], parameters[0][2].split('+'))

    def _reserve_earliest(self, services):
        self._car_wash.add_reservation(services)

    def _reserve_exact(self, date, time, services):
        self._car_wash.add_reservation(services, date, time)

    def _list_reservations(self):
        self._print_reservations(self._car_wash)

    def _print_reservations(self, car_wash):
        counter = 0
        print('\n' * 2)
        print("LIST OF RESERVATIONS".center(50))
        print()
        print("%-3s %-35s %-10s %-8s" %
              ('ID', 'SERVICES', 'DATE, TIME', 'DURATION'))
        print("%3s %35s %10s %4s" % ('-' * 3, '-' * 35, '-' * 10, '-' * 8))
        # Print the body.
        for reservation in car_wash:
            print("%3d %-35s %-10s %-8s" % (counter, ', '.join(reservation.services),
                  Reservation.format_time(reservation.time), reservation.duration))
            counter += 1
        # Add a footer.
        print("-" * 3, '-' * 35, '-' * 10, '-' * 8)
        print("Total number of reservations:", (car_wash.number_of_reservations()))
        print('\n' * 2)


def main():
    car_wash = CarWash()
    dispatcher = CommandDispatcher(car_wash)

    while (command := input('Enter command: ')) != 'exit':
        dispatcher.dispatch(command)

    # Sample input:
    # reserve earliest nezafat+sefrshooyi
    # reserve 2 19:00 rooshooyi+nezafat


if __name__ == '__main__':
    main()
