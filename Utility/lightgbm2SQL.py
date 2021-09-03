# Extract Code Rule

class Lightgbm2SQL:

    def parseOneTree(self,root, index, array_type='double', return_type='double'):
        def ifElse(node):
            if 'leaf_index' in node:
                return ' ' + str(node['leaf_value']) + ''
            else:
                head = self.fnames[node['split_feature']]  # 'arr[' + str(node['split_feature']) + ']'
                condition = ''
                if node['decision_type'] in ['no_greater', '<='] :
                    condition = condition + head + ' <= ' + str(node['threshold'])
                else:

                    for x in node['threshold'].split("||"):
                        value = self.all_dict[head][int(x)]
                        if type(value) != int:
                            condition = condition + "`{}`".format(head) + """='{}' or """.format(value)
                        else:
                            condition = condition + "`{}`".format(head) + "={} or ".format(value)

                    condition += ' 2=1'

                left = ifElse(node['left_child'])
                right = ifElse(node['right_child'])
                return 'case when ( ' + condition + ' )  \nthen  ' + left + '  \nelse ' + right + '  end'
        return  "("+ ifElse(root) + ") ".format(index)


    def parseAllTrees(self,trees, array_type='double', return_type='double'):
        all_vars = ",".join("`"+x+"`"  for x in self.fnames)

        pre_sql = "select id,"+  all_vars + ',\n' +  '+\n\n'.join(
            [self.parseOneTree(tree['tree_structure'], idx, array_type, return_type) for idx, tree in enumerate(trees)]) \
               + '\n\n'
        all_sql = ''

        # for i in range(len(trees)):
        #     all_sql += "select id,{},score from t_{} \n union all \n".format(all_vars,i,)
        # all_sql = all_sql[:-11]

        result_sql = """
create view result_view as 
select {},\ncast( 1/(1+EXP(-1*score)) as double) from score_view
;
        """.format(all_vars)


        return "create view score_view as \n(\n" +  pre_sql + "as score \nfrom raw_data)\n;\n" + result_sql

    def doProcess(self,dm):


        self.fnames = dm['feature_names']
        self.cmaping = dm['pandas_categorical']
        self.feature_infos = dm['feature_infos']
        self.types = {}

        for fs in self.feature_infos:
            if len(self.feature_infos[fs]['values']) == 0:
                self.types[fs] = 'double'
            else:
                self.types[fs] = 'String'


        self.vars = ''
        for i, f in enumerate(self.fnames):

            if f in self.types:
                self.vars += self.types[f] + " " + f + ", "

        self.vars = self.vars[:-2]

        self.vars_notype = ''
        for i, f in enumerate(self.fnames):
            self.vars_notype += " " + f + ", "
        self.vars_notype = self.vars_notype[:-2]

        self.all_dict = {}

        c = 0
        for fn in  self.fnames:
             if fn not in self.types: continue
             if  self.types[fn] == 'String':
                if len(self.cmaping[c]) == 1:
                    c = c + 1
                m = dict()
                for i,vv in enumerate(self.cmaping[c]):
                    m[i] = vv
                self.all_dict[fn] = m
                c = c + 1

        return self.parseAllTrees(dm['tree_info'])


if __name__ == '__main__':
    import joblib

    # save model
    # load model
    gbm_pickle = joblib.load("/Users/kentshih/PycharmProjects/ds-utility/tests/lightgbm.pkl")
    ls = Lightgbm2SQL()
    code = ls.doProcess(gbm_pickle._Booster.dump_model())
    print(code)