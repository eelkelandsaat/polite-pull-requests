import pandas as pd
from datetime import datetime
from imblearn.over_sampling import SMOTENC
from scipy.stats import spearmanr, kruskal
import seaborn as sns
import matplotlib.pyplot as plt
from paths import LIKERT_LABELS_FILE, PULL_DATA_FILE

# Init
sm = SMOTENC(categorical_features=[0,3,4,5,6,7,8,9,10,11], random_state=42, k_neighbors=2)

# Get data
pr_labeled = pd.read_csv(LIKERT_LABELS_FILE)
pr_data = pd.read_csv(PULL_DATA_FILE)
pr_labeled = pr_labeled[pr_labeled.message != 'None']
pr_data = pr_data[pr_data.message != 'None']

# Calculate time to merge
pr_data['time-to-merge'] = pr_data.apply(lambda x: (datetime.strptime(x['merged'], '%Y-%m-%dT%H:%M:%SZ') - datetime.strptime(x['created'], '%Y-%m-%dT%H:%M:%SZ')).total_seconds(), axis=1)

# Format data
pr_merged = pd.merge(pr_labeled, pr_data, left_index=True, right_index=True)
grouped = pr_merged.groupby('repo_api_url_x')

# Resample with SMOTE
print('Before SMOTE:')
print(pr_merged['class_label'].value_counts())
oversampled_X, oversampled_Y = sm.fit_resample(pr_merged.drop('class_label', axis=1), pr_merged['class_label'])
pr_merged_sampled = pd.concat([pd.DataFrame(oversampled_Y), pd.DataFrame(oversampled_X)], axis=1)
print('After SMOTE:')
print(pr_merged_sampled['class_label'].value_counts())


# Calculations

print('ANOVA coefficients')
# Calculate ANOVA coefficients (class label)
df_plot = pr_merged_sampled[['class_label', 'time-to-merge']]
df_plot['num'] = df_plot.index
df_plot.columns = ['class_label', 'time-to-merge', 'index']

ax = sns.boxplot(x='class_label', y='time-to-merge', data=df_plot, color='#99c2a2', showfliers=False)
ylims=ax.get_ylim()
ax = sns.stripplot(x='class_label', y='time-to-merge', data=df_plot, color='#7d0013')
ax.set(ylim=ylims)
plt.show()

df_oneway = df_plot.pivot(values='time-to-merge',  columns='class_label')
h, p = kruskal(df_oneway[1].dropna(), df_oneway[2].dropna(), df_oneway[3].dropna(), df_oneway[4].dropna(), df_oneway[5].dropna(),)

#Print ANOVA rank correlation and p-value
print(' On class label: \n    H: {}\n    p: {}'.format(h, p))

# Calculate spearman coefficients (regression score)
r, p = spearmanr(pr_merged_sampled['regression_score'], pr_merged_sampled['time-to-merge'])

#Print Spearman rank correlation and p-value
print('\nSpearman coefficients')
print(' On regression score: \n    r: {}\n    p: {}'.format(r, p))