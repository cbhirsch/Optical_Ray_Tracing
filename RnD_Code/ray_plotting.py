import numpy as np
import matplotlib.pyplot as plt

# Define the points A and B
A = np.array([1, 2, 3])
B = np.array([4, 5, 6])

# Define the origin
O = np.array([0, 0, 0])

# Create a 2D plot
fig, ax = plt.subplots()

# Plot the points A and B
ax.scatter(A[0], A[1], color='blue', label='A')
ax.scatter(B[0], B[1], color='red', label='B')

# Plot the vectors connecting the origin to A and B
ax.arrow(O[0], O[1], A[0], A[1], color='blue', head_width=0.1, length_includes_head=True)
ax.arrow(O[0], O[1], B[0], B[1], color='red', head_width=0.1, length_includes_head=True)

# Set the plot limits and labels
ax.set_xlim([-1, 7])
ax.set_ylim([-1, 7])
ax.set_xlabel('X')
ax.set_ylabel('Y')

# Show the plot
plt.legend()
plt.show()
