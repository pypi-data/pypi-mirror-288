class TRAFolder:
    class FolderNotFound(Exception):
        pass

    def __init__(self, folder_path: str):
        self.folder_path = folder_path

        self.file_list = self.getTRAFiles()

        import pandas as pd
        self.results = pd.DataFrame()

        import os
        if not os.path.exists(folder_path + '/plots'):
            os.makedirs(folder_path + '/plots')

    def analyze(self):
        if not self.file_list:
            return

        import pandas as pd

        for file in self.file_list:
            print(file)
            result = TRAFile(file, self.folder_path).analyze()
            result['File'] = file

            self.results = pd.concat([self.results, result])

        self.printCopyrights()
        return self.results.set_index('File').sort_index()

    def getTRAFiles(self):
        import os

        try:
            dir_list = os.listdir(self.folder_path)

            try:
                file_list = [
                    filename for filename in dir_list if filename.endswith('.csv')]

                if not file_list:
                    print('No .csv files found in the folder.')
                    return []
                else:
                    if 'Analysis.csv' in file_list:
                        file_list.remove('Analysis.csv')
                    return file_list

            except FileNotFoundError:
                print('An error occurred while filtering files.')
                raise

        except FileNotFoundError:
            raise TRAFolder.FolderNotFound('Folder not found')

    def printCopyrights(self):
        print("*********************************************")
        print()
        print("by Paride Azzari (C) 2024")
        print()
        print("info on: github.com/azzarip/ciatta")
        print("*********************************************")
        print("RESULTS:")
        print()
        print("Analysis.csv contains the analyzed data")
        print()
        print("The plots folder contains all the figures")
        print("*********************************************")
        print()


class TRAFile:

    def __init__(self, file: str, folder_path: str):
        import os
        import pandas as pd
        self.filename = file.replace('.csv', '')

        if folder_path:
            self.filepath = os.path.join(folder_path, file)
        else:
            self.filepath = file

        self.data = self.read_csv(self.filepath)

    def analyze(self):
        from .fit import Fit
        from .plot import Plot

        fit = Fit(self.data)

        # import matplotlib.pyplot as plt
        # y = 1/fit.fit_results['error']
        # plt.plot(fit.fit_results['x'], y)
        # plt.axhline(y=y.mean(), color='green', linestyle='--')
        # plt.savefig('plots/error' + self.filename + '.png')
        # plt.title(self.filename)
        # plt.close()

        Plot(fit.results, fit.data, self.filename)

        return fit.results

    def read_csv(self, filename):
        import pandas as pd
        df = pd.read_csv(filename, encoding='utf-16', skiprows=9, sep='\t')
        df = df.rename(columns={list(df)[1]: 'index', list(df)[0]: 'drop', list(df)[
                       2]: 'strain', list(df)[3]: 'stress', list(df)[4]: 'force', list(df)[5]: 'speed'})
        df = df.drop(columns=['drop']).set_index('index')
        return df
