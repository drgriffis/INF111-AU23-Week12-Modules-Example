class DataRow:
    def __init__(self, row_id, data):
        self.row_id = row_id
        self.data = data

    def keys(self):
        return self.data.keys()

    def getPercentageFeatureNames(self, remove_prefix=True):
        percentage_features = set()
        for col in self.data.keys():
            if col[:4] == 'pct_':
                percentage_features.add(col[4:])
        return percentage_features

    def getCountFeatureNames(self, remove_prefix=True):
        count_features = set()
        for col in self.data.keys():
            if col[:6] == 'count_':
                count_features.add(col[6:])
        return count_features

    def recalculatePercentages(self):
        perc_features = self.getPercentageFeatureNames(remove_prefix=True)
        for feat in perc_features:
          perc_key = 'pct_{0}'.format(feat)
          count_key = 'count_{0}'.format(feat)

          value = self.data[count_key]
          new_perc = value / self.data['count_property']

          self.data[perc_key] = new_perc

    def print(self):
        print(self.row_id, self.data)