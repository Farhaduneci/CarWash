class Reservation:
    def __init__(self, services, date, time):
        self.services = services
        self.time = (date - 1) * 12 * 60 + time  # Every day is 12 hours long
        self.duration = self.reservation_duration(services)

    @staticmethod
    def reservation_duration(services):
        return sum(CarWash.available_services[service] for service in services)


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

    def add_reservation(self, services, date=None, time=None):
        print("Adding reservation", services, date, time)

    def format_time(self, time):
        time = time % 30
        hour, minute = divmod(time, 60)
        hour += self.time_schedule['start']
        return '{:02d}:{:02d}'.format(hour, minute)


class CommandDispatcher:
    def __init__(self, car_wash):
        self._car_wash = car_wash
        self._commands = {
            'reserve': self._reserve,
        }

    def dispatch(self, command):
        command, *parameters = command.split()
        self._handle_command(command, parameters)

    def _handle_command(self, command, parameters):
        self._commands[command](
            parameters) if parameters else self._commands[command]()

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
