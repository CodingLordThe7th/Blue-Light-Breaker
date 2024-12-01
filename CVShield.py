import rumps
import pygame
import time
import random
from datetime import timedelta


class CVShield(rumps.App):
    def __init__(self):
        super().__init__("😎 CVShield - Inactive")
        self.icon = None
        self.start_time = None
        self.break_interval = timedelta(minutes=20)  # Default: 20 minutes
        self.break_duration = 20  # Default: 20 seconds
        self.is_monitoring = False
        self.sent_notification = False  # Flag to prevent multiple notifications
        self.current_pun = ""  # Store the pun for the current break
        self.menu.add(rumps.MenuItem("Start Monitoring", callback=self.start_monitoring))
        self.stop_monitoring_button = rumps.MenuItem("Stop Monitoring", callback=self.stop_monitoring)
        self.menu.add(self.stop_monitoring_button)
        self.stop_monitoring_button.set_callback(None)  # Initially disabled
        self.timer = rumps.Timer(self.monitor_screen_time, 1)  # Check every second

    def start_monitoring(self, _):
        self.break_interval = self.get_valid_input(
            "Set break interval (1-20 minutes, default is 20):", 1, 20, 20
        ) * 60  # Default: 20 minutes
        self.break_duration = self.get_valid_input(
            "Set break duration (20-60 seconds, default is 20):", 20, 60, 20
        )  # Default: 20 seconds
        self.start_time = time.time()
        self.is_monitoring = True
        self.sent_notification = False
        self.timer.start()
        self.title = "😎 CVShield - Monitoring..."
        self.stop_monitoring_button.set_callback(self.stop_monitoring)  # Enable stop button

    def stop_monitoring(self, _):
        self.is_monitoring = False
        self.timer.stop()
        self.title = "😎 CVShield - Inactive"
        self.stop_monitoring_button.set_callback(None)  # Disable stop button

    def monitor_screen_time(self, _):
        if not self.is_monitoring:
            return

        elapsed_time = time.time() - self.start_time
        remaining_time = self.break_interval - elapsed_time

        if remaining_time <= 0:
            self.start_break()
            return

        # Display remaining time in countdown format
        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)
        self.title = f"😎 CVShield - Time until break: {minutes}m {seconds}s"

        # Notify 10 seconds before the break
        if remaining_time <= 10 and not self.sent_notification:
            rumps.notification(
                title="Break Reminder",
                subtitle="Heads-up!",
                message="Your break starts in 10 seconds.",
            )
            self.sent_notification = True

    def start_break(self):
        self.timer.stop()  # Pause the timer
        self.title = "😎 CVShield - Break!"
        self.sent_notification = False  # Reset the notification flag for the next cycle
        self.select_random_pun()  # Pick a random pun for this break
        self.block_screen_for_break(self.break_duration)
        self.start_time = time.time()  # Reset the work timer
        self.timer.start()  # Resume the timer
        self.title = "😎 CVShield - Monitoring..."
        rumps.notification(  # Notification for break end
            title="Break Over",
            subtitle="Back to work!",
            message="The break is complete. Monitoring has resumed.",
        )

    def select_random_pun(self):
        """Select a random pun for the break."""
        puns = [
            "Feeling stressed? Leaf it all behind.",
            "Take a break—you're tree-mendously important.",
            "This is your time to pine for some peace.",
            "Relax... you're on cloud nine now.",
            "Don't desert yourself—enjoy the break.",
            "You've earned this paws... just like nature.",
            "Stay grounded, but let your mind soar.",
            "You're rock-solid, but breaks are boulder.",
        ]
        self.current_pun = random.choice(puns)

    def block_screen_for_break(self, break_duration):
        """Display a scenic break screen with a multi-car train and health exercise suggestions."""
        print(f"Blocking screen for {break_duration} seconds...")
        pygame.init()
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Fullscreen mode
        pygame.display.set_caption("Break Time!")
        font = pygame.font.SysFont("Arial", 50)
        exercise_font = pygame.font.SysFont("Arial", 40)  # Font for exercise suggestion
        clock = pygame.time.Clock()

        # Select a random health-related exercise
        exercises = [
            "Blink 20 times before the break ends.",
            "Stretch your back for better posture.",
            "Look at something 20 feet away for 20 seconds.",
            "Rotate your neck gently to relax.",
            "Stand up and walk around briefly.",
            "Stretch your arms and shoulders."
        ]
        selected_exercise = random.choice(exercises)

        start_time = time.time()
        train_x = 0  # Position of the moving "train"
        running = True
        while running:
            elapsed_time = time.time() - start_time
            remaining_time = max(0, break_duration - int(elapsed_time))
            if remaining_time <= 0:
                running = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False  # Allow early quit

            # Sky background
            screen.fill((135, 206, 250))  # Sky blue background

            # Sun
            pygame.draw.circle(screen, (255, 223, 0), (screen.get_width() - 100, 100), 60)

            # Grey mountains with ice caps (back layer)
            pygame.draw.polygon(
                screen, (169, 169, 169), [(100, 600), (300, 250), (500, 600)]
            )  # Left grey mountain
            pygame.draw.polygon(
                screen, (255, 255, 255), [(275, 275), (300, 250), (325, 275)]
            )  # Ice cap for left grey mountain
            pygame.draw.polygon(
                screen, (169, 169, 169), [(500, 600), (700, 300), (900, 600)]
            )  # Right grey mountain
            pygame.draw.polygon(
                screen, (255, 255, 255), [(675, 325), (700, 300), (725, 325)]
            )  # Ice cap for right grey mountain

            # Ground
            pygame.draw.rect(screen, (139, 69, 19), (0, 600, screen.get_width(), screen.get_height()))  # Brown ground

            # Trees
            for x in range(100, screen.get_width(), 150):
                pygame.draw.rect(screen, (139, 69, 19), (x + 25, 570, 20, 50))  # Tree trunk
                pygame.draw.polygon(
                    screen, (34, 139, 34), [(x, 570), (x + 35, 520), (x + 70, 570)]
                )  # Tree foliage

            # Moving object for eye exercise (multi-car train)
            car_color = (0, 0, 255)
            car_spacing = 160
            num_cars = 5
            train_width = num_cars * car_spacing  # Total train length
            for i in range(num_cars):
                car_x = train_x + i * car_spacing
                pygame.draw.rect(screen, car_color, (car_x, 630, 150, 30))  # Train car body
                pygame.draw.circle(screen, (0, 0, 0), (car_x + 25, 660), 10)  # Left wheel
                pygame.draw.circle(screen, (0, 0, 0), (car_x + 125, 660), 10)  # Right wheel
            train_x += 5  # Move train to the right

            # Reset train position when it fully leaves the screen
            if train_x > screen.get_width():
                train_x = -train_width

            # Timer
            second_label = "second" if remaining_time == 1 else "seconds"
            timer_message = font.render(
                f"Break Time! {remaining_time} {second_label} left.",
                True,
                (0, 0, 0),
            )
            screen.blit(
                timer_message,
                (screen.get_width() // 2 - timer_message.get_width() // 2,
                 screen.get_height() // 2 - timer_message.get_height() // 2),
            )

            # Pun message
            pun_message = font.render(self.current_pun, True, (0, 0, 0))
            screen.blit(
                pun_message,
                (screen.get_width() // 2 - pun_message.get_width() // 2,
                 screen.get_height() // 2 + 50),
            )

            # Exercise suggestion
            exercise_message = exercise_font.render(selected_exercise, True, (0, 0, 0))
            screen.blit(
                exercise_message,
                (screen.get_width() // 2 - exercise_message.get_width() // 2,
                 screen.get_height() // 2 + 100),
            )

            pygame.display.flip()
            clock.tick(30)

        pygame.quit()  # Ensure the Pygame window closes properly

    def get_valid_input(self, prompt, min_val, max_val, default_value):
        while True:
            try:
                # Adding default text to the input box
                user_input = rumps.Window(
                    prompt,
                    default_text=str(default_value),  # Set the default text
                ).run().text
                if not user_input:
                    return default_value  # Use the default value if the user doesn't input anything
                value = int(user_input)
                if min_val <= value <= max_val:
                    return value
            except ValueError:
                pass
            rumps.alert(f"Please enter a valid number between {min_val} and {max_val}.")


if __name__ == "__main__":
    CVShield().run()
