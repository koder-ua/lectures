import matplotlib.pyplot as plt

x = [1, 2, 4, 8, 16, 32, 40, 50, 60, 64]
y = [180, 200, 240, 280, 310, 340, 350, 350, 350, 350]
y_lat = [10, 10, 11, 12, 14, 30, 30 + 20 * 8. / 32, 30 + 20 * 18. / 32, 30 + 20 * 28. / 32, 50]
y_lat = [i * 7 for i in y_lat]
plt.plot(x, y)
plt.plot(x, y_lat)
plt.ylim([0, 400])
plt.show()
