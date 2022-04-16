import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
n1 = np.load('agent1.npy')
n2 = np.load('agent2.npy')
# df = pd.DataFrame(np.c_[n1, n2])
sns.displot(n1)
sns.displot(n2)
print(np.mean(n1), np.mean(n2))
plt.show()
