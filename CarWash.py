class Reservation:
    def __init__(self, services, date, time):
        self.services = services
        self.time = (date - 1) * 12 * 60 + time  # Every day is 12 hours long


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
        pass


def main():
    car_wash = CarWash()
    dispatcher = CommandDispatcher(car_wash)

    while (command := input('Enter command: ')) != 'exit':
        dispatcher.dispatch(command)


if __name__ == '__main__':
    main()
