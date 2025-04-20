import datetime as dt

class Timer:
    """
    Convenience timer methods. \n

    Instantiate with: \n
       timer=Timer()

         .start(message='') \n
         .elapsed(message='', periodicity='s')
         .end(periodicity='s')


    """
    def __init__(self):
        self.start_time = None
        self.timestamp = None
        self.end_time = None

    @staticmethod
    def format_time(time_obj):
        return time_obj.strftime('%Y-%m-%d %H:%M:%S')


    def start(self, message=''):
        """Start the timer."""
        self.start_time = dt.datetime.now()
        self.timestamp = self.start_time
        print(f'Start time: {self.format_time(self.start_time)}')
        if message:
            print(f'{message}\n')


    def elapsed(self, message='', periodicity='s'):
        """Print the elapsed time since the last timestamp."""
        if self.timestamp is None:
            print("Timer hasn't been started yet. Use `start()` first.")
            return

        new_timestamp = dt.datetime.now()
        if message:
            print(message)

        if periodicity.lower() in ['m', 'min', 'mins', 'minutes', 'minute']:
            elapsed_minutes = (new_timestamp - self.timestamp).total_seconds() / 60
            print(f'Elapsed time: {elapsed_minutes:.1f} mins since last timestamp at {new_timestamp}\n')
        else:
            elapsed_seconds = (new_timestamp - self.timestamp).total_seconds()
            print(f'Elapsed time: {elapsed_seconds:.0f} seconds since last timestamp at {new_timestamp}\n')

        self.timestamp = new_timestamp

    def end(self, periodicity='s'):
        """End the timer and print total elapsed time."""
        if self.start_time is None:
            print("Timer hasn't been started yet. Use `start()` first.")
            return

        else:
            self.end_time = dt.datetime.now()
            print(f'\nEnd time: {self.format_time(self.end_time)}')

            total_elapsed = (self.end_time - self.start_time).total_seconds()
            since_last_timestamp = (self.end_time - self.timestamp).total_seconds()

            if periodicity.lower() in ['m', 'min', 'mins', 'minutes', 'minute']:
                print(f'Wall time: {total_elapsed / 60:.1f} minutes '
                    f'({since_last_timestamp / 60:.1f} mins since last timestamp)\n')
            else:
                print(f'Wall time: {total_elapsed:.0f} seconds '
                    f'({since_last_timestamp:.0f} seconds since last timestamp)\n')


