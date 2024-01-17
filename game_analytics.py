class GameAnalytics:
    def __init__(self):
        self.events = {
            'pacman_moved': [],
            'ghost_moved': [],
            'ghost_mode_change': [],
            'pacman_lost': [],
            'brick_collected': [],
            # Add more event types as needed
        }

    def log_event(self, event_name, parameter):
        if event_name in self.events:
            self.events[event_name].append(parameter)
        else:
            print(f"Unknown event: {event_name}")

    def print_events(self):
        for event_name, data in self.events.items():
            print(f"{event_name}: {data}")
