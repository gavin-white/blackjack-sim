import matplotlib.pyplot as plt

def simulate_blackjack(num_hands):
    bank_values = [100]  # Starting bank value
    plt.ion()  # Enable interactive mode for live updates

    # Create the initial plot
    fig, ax = plt.subplots()
    line, = ax.plot(bank_values, marker='o')
    ax.set_xlabel('Number of Hands')
    ax.set_ylabel('Bank Value')

    for hand in range(1, num_hands + 1):
        # Simulate blackjack gameplay and update bank value
        # Replace this with your own logic for updating the bank value

        # Generate a random change in bank value for demonstration purposes
        bank_value_change = -10 if hand % 5 == 0 else 5
        bank_value = bank_values[-1] + bank_value_change
        bank_values.append(bank_value)

        # Update the plot with the new data
        line.set_data(range(hand + 1), bank_values)
        ax.relim()
        ax.autoscale_view()
        fig.canvas.draw()

        # Pause to allow for live updates
        plt.pause(0.0001)

    # Keep the plot displayed after the simulation is complete
    plt.ioff()
    plt.show()

# Simulate 50 blackjack hands and display live updates
simulate_blackjack(50)
