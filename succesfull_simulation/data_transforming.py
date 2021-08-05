"""
Plot graphs based on the received data
"""
import matplotlib.pyplot as plt

day_counts = [i for i in range(1, 367)]
print("day_counts=", day_counts)
healthy_counts = []
illness_counts = []
hospital_counts = []

with open("test.txt", "r") as file:
    for line in file:
        line = line.strip()
        print(line)
        numbers = [int(x) for x in line.split() if x.isdigit()]
        print(numbers)
        healthy_counts.append(numbers[1])
        illness_counts.append(numbers[2])
        hospital_counts.append(numbers[3])

x = day_counts
y1 = healthy_counts
y2 = illness_counts
y3 = hospital_counts

plt.title("COVID-19 Simulation")
plt.xlabel("Days")
plt.ylabel("y1, y2")
plt.grid()
plt.plot(x, y1, x, y2, x, y3)

fig, ax = plt.subplots()

ax.plot(x, y1, label='healthy people')
ax.plot(x, y2, label='sick people')
ax.plot(x, y3, label='people in hospital')

ax.legend()

fig.set_figheight(5)
fig.set_figwidth(8)

plt.show()
