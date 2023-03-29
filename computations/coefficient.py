import pandas as pd
from scipy.stats import spearmanr, kruskal
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from paths import LIKERT_LABELS_FILE, PULL_DATA_FILE


# Get data
pr_labeled = pd.read_csv(LIKERT_LABELS_FILE)
pr_data = pd.read_csv(PULL_DATA_FILE)
pr_labeled = pr_labeled[pr_labeled.message != 'None']
pr_data = pr_data[pr_data.message != 'None']

# Calculate time to merge
pr_data['time-to-merge'] =   pr_data.apply(lambda x: (datetime.strptime(x['merged'], '%Y-%m-%dT%H:%M:%SZ') - datetime.strptime(x['created'], '%Y-%m-%dT%H:%M:%SZ')).total_seconds(), axis=1)

# Format data
pr_merged = pd.merge(pr_labeled, pr_data, left_index=True, right_index=True)
grouped = pr_merged.groupby('repo_api_url_x')
pr_merged['class_label'] = pr_merged.apply(lambda x: -1 if x['regression_score'] < -0.196244 else (0 if x['regression_score'] < 0.3079949 else 1), axis=1)

print('ANOVA coefficients')
# Calculate ANOVA coefficients (class label)
df_select = pr_merged[['class_label', 'time-to-merge']]
df_select['num'] = df_select.index
df_select.columns = ['class_label', 'time-to-merge', 'index']
df_plot = df_select
df_plot['time-to-merge'] = df_plot['time-to-merge'].div(86400)

ax = sns.boxplot(x='class_label', y='time-to-merge', data=df_plot, color='#99c2a2', showfliers=False)
ylims=ax.get_ylim()
ax = sns.stripplot(x="class_label", y="time-to-merge", data=df_plot, color='#7d0013')
ax.set(ylim=ylims)
ax.set(xlabel='class label', ylabel='time-to-merge (days)')
plt.show()

df_oneway = df_plot.pivot(values='time-to-merge',  columns='class_label')
h, p = kruskal(df_oneway[1].dropna(), df_oneway[2].dropna(), df_oneway[3].dropna(), df_oneway[4].dropna(), df_oneway[5].dropna(),)

#Print ANOVA rank correlation and p-value
print(' On class label: \n    H: {}\n    p: {}'.format(h, p))

# Calculate spearman coefficients (regression score)
r, p = spearmanr(pr_merged['regression_score'], pr_merged['time-to-merge'])

#Print Spearman rank correlation and p-value
print('\n\nSpearman coefficients')
print(' On regression score: \n    r: {}\n    p: {}'.format(r, p))
print('\n  per repo:')

for name, repo in grouped:
    r, p = spearmanr(repo['regression_score'], repo['time-to-merge'])
    print('    {}:\n      r: {}\n      p: {}'.format(name, r, p))


