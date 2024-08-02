class Fit:
    import pandas as pd

    def __init__(self, data):

        self.data = data
        self.cutOffData()
        self.max_stress_index = self.data['stress'].idxmax()

        self.fit_step = 0.04
        self.step_fraction = 5

        self.fit_results = self.get_fits()

        self.results = self.getResults()

    def getResults(self):
        import pandas as pd

        maxValues = self.data.iloc[self.max_stress_index]

        df = self.fit_results

        df['good'] = 1 / df['error']
        good = df['good']
        mean_good = good.mean()
        df.loc[df['good'] < mean_good, 'good'] = 0

        df['group'] = (df['good'] != 0).astype(
            int).cumsum() * (df['good'] != 0)
        results = df[df['good'] != 0].groupby(
            'group')['good'].max().reset_index(drop=True)

        best_result = df[df['good'] == results.iloc[0]]

        return pd.DataFrame({
            'Max Stress [Pa]': [maxValues['stress']],
            'Max Strain': [maxValues['strain']],
            'Max Force [N]': [maxValues['force']],
            'Young Modulus [Pa]': [best_result['slope'].iloc[0]],
            'Intercept [Pa]': [best_result['intercept'].iloc[0]],
            'pValue': [best_result['p_value'].iloc[0]]
        })

    def cutOffData(self):
        max_stress = self.data['stress'].idxmax()
        self.data = self.data.iloc[0:max_stress + 1]
        self.data = self.data[(self.data['stress'] >= 0)
                              & (self.data['strain'] >= 0)]
        self.data.reset_index(drop=True, inplace=True)

        return None

    def fit(self, df):
        import pandas as pd
        from scipy.stats import linregress

        x = df['strain']
        y = df['stress']
        slope, intercept, r_value, p_value, std_err = linregress(x, y)
        error = y - (slope * x + intercept)

        result = pd.DataFrame({
            'x': [x.mean()],
            'slope': [slope],
            'intercept': [intercept],
            'p_value': [p_value],
            'error': [error.pow(2).sum() / len(x)]
        })
        return result

    def find_step_index(self, start_index):

        start_strain = self.data.loc[start_index, 'strain']

        for i in range(start_index + 1, len(self.data)):
            if self.data.loc[i, 'strain'] - start_strain >= self.fit_step:
                return i
        return len(self.data)

    def get_fits(self):
        import pandas as pd

        index = 0
        results = pd.DataFrame()
        max_size = len(self.data)

        while index < max_size:

            end_index = self.find_step_index(index)

            if end_index >= max_size - 1:
                break

            df = self.data.iloc[index:end_index+1]

            result = self.fit(df)
            results = pd.concat([results, result], ignore_index=True)

            index = index + 1

        return results
