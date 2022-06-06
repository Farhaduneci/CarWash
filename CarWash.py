from collections import defaultdict


class Reservation:
    def __init__(self, services, date, time):
        self.services = services
        self.time = self._parse_time(date, time)
        self.duration = self.reservation_duration(services)

    @staticmethod
    def _parse_time(date, time):
        return ((date - 1) * CarWash.time_schedule['work_hours'] * 60) + time

    @staticmethod
    def reservation_duration(services):
        return sum(CarWash.available_services[service] for service in services)

    @staticmethod
    def format_time(time):
        work_hours = CarWash.time_schedule['work_hours']
        date = time // work_hours // 60 + 1
        time = time % (work_hours * 60)
        hour, minute = divmod(time, 60)
        hour += CarWash.time_schedule['start']
        return '{:02d}, {:02d}:{:02d}'.format(date, hour, minute)

    @staticmethod
    def time_string_to_time(time):  # time is a string
        return (int(time[:2]) - CarWash.time_schedule['start']) * 60 + int(time[3:5])

    @staticmethod
    def time_get_date(time):
        return time // (CarWash.time_schedule['work_hours'] * 60) + 1

    @staticmethod
    def time_get_hour(time):
        return time // 60 % CarWash.time_schedule['work_hours']

    @staticmethod
    def time_to_hour(time):
        return time % (CarWash.time_schedule['work_hours'] * 60) // 60 + CarWash.time_schedule['start']

    def __str__(self):
        return '{} {} {}'.format(self.services,
                                 self.format_time(self.time),
                                 self.format_time(self.time + self.duration))


class CarWash:
    def __init__(self):
        self.reservations = defaultdict(list)

    time_schedule = {
        'work_hours': 12,
        'start': 9,
        'end': 21,
    }
    available_services = {
        'sefrshooyi': 60,
        'rooshooyi': 15,
        'nezafat': 20
    }

    def add_reservation(self, services, date=None, time=None):
        if date and time:
            self.reservations.append(Reservation(services, date, time))
        else:
            duration = Reservation.reservation_duration(services)
            self.reservations.append(Reservation(
                services, *self.find_empty_date_time(duration)))

    def find_empty_date_time(self, duration):
        date, time = 1, 0
        for index, reservation in enumerate(self.reservations):
            date, time = Reservation.time_to_date(
                reservation.time), Reservation.time_to_hour(reservation.time)
            print(date, time)
        return (date, time)

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
            'help': self._help,
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

    def _help(self):
        print('Available commands:')
        for command in self._commands:
            print(u'\u25C6', command)

    def _reserve(self, *parameters):
        if parameters[0][0] == 'earliest':
            self._reserve_earliest(parameters[0][1].split('+'))
        else:
            self._reserve_exact(
                parameters[0][0], parameters[0][1], parameters[0][2].split('+'))

    def _reserve_earliest(self, services):
        self._car_wash.add_reservation(services)

    def _reserve_exact(self, date, time, services):
        time_in_minutes = Reservation.parse_time(time)
        self._car_wash.add_reservation(services, int(date), time_in_minutes)

    def _list_reservations(self):
        self._print_reservations(self._car_wash)

    def _print_reservations(self, car_wash):
        number_of_reservations = car_wash.number_of_reservations()
        if number_of_reservations == 0:
            print('No reservations')
            return
        counter = 0
        print('\n' * 2)
        print("LIST OF RESERVATIONS".center(50))
        print()
        print("%-3s %-35s %-10s %-8s" %
              ('ID', 'SERVICES', 'DATE, TIME', 'DURATION'))
        print("%3s %35s %10s %4s" % ('-' * 3, '-' * 35, '-' * 10, '-' * 8))
        # Print the body.
        for reservation in car_wash:
            print("%03d %-35s %-10s %-8s" % (counter, ', '.join(reservation.services),
                  Reservation.format_time(reservation.time), reservation.duration))
            counter += 1
        # Add a footer.
        print("-" * 3, '-' * 35, '-' * 10, '-' * 8)
        print("Total number of reservations:",
              (number_of_reservations))
        print('\n' * 2)


def main():
    car_wash = CarWash()
    dispatcher = CommandDispatcher(car_wash)

    print("Welcome to the car wash reservation system.")
    print("Type 'help' for a list of commands.")
    print("Type 'exit' to exit the program.")

    while (command := input('\nEnter command: ')) != 'exit':
        dispatcher.dispatch(command)

    # Sample input:
    # reserve earliest nezafat+sefrshooyi
    # reserve 2 19:00 rooshooyi+nezafat


if __name__ == '__main__':
    main()
