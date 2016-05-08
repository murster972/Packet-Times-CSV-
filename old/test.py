"""
Bar chart demo with pairs of bars grouped for easy comparison.
"""
import numpy as np
import matplotlib.pyplot as plt


n_groups = 10

means_men = (0.010249, 0.009180, 0.009501, 0.011055, 0.009019, 0.010249, 0.009180, 0.009501, 0.011055, 0.009019)
std_men = (1, 3, 4, 1, 2)

means_women = (25, 32, 34, 20, 25)
std_women = (3, 5, 2, 3, 3)

fig, ax = plt.subplots()

index = np.arange(n_groups)
bar_width = 1

opacity = 0.4
error_config = {'ecolor': '0.3'}

rects1 = plt.bar(index, means_men, bar_width,
                 alpha=opacity,
                 color='b',
                 error_kw=error_config,
                 label='Men')

plt.xlabel('Group')
plt.ylabel('Scores')
plt.title('Scores by group and gender')
plt.xticks(index, ('3543, 3544', '5181-5182', 'C', 'D', 'E', 'F', 'G', 'h', 'i', 'j'))
plt.legend()

plt.tight_layout()
plt.show()