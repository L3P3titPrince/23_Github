from point import point
from generator import LCG, SCG
import time
import matplotlib.pyplot as plt
from matplotlib.patches import Circle


SAMPLE_NUM = 1e7
# rescale
test_4 = point(num = SAMPLE_NUM)
test_4_list, x_list, y_list = test_4.coordinate()
print(test_4_list[0:5])
count = 0
for x, y in test_4_list:
    if x**2 + y**2 < 2:
        count+=1
print(count / SAMPLE_NUM/2)


#plot part
circle = Circle((0,0),1, fill=False, linewidth=3)
fig, ax = plt.subplots(figsize=(6,6))
plt.scatter(x_list, y_list, s=0.00001)
ax.add_patch(circle)
plt.xlim((-1, 1))
plt.ylim((-1,1))
plt.show()
