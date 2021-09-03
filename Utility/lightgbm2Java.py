# Extract Code Rule

class Lightgbm2Java:

    def parseOneTree(self,root, index, array_type='double', return_type='double'):
        def ifElse(node):
            if 'leaf_index' in node:
                return 'return ' + str(node['leaf_value']) + ';'
            else:
                head = self.fnames[node['split_feature']]  # 'arr[' + str(node['split_feature']) + ']'
                condition = ''
                if node['decision_type'] in ['no_greater', '<='] :
                    condition = condition + head + ' <= ' + str(node['threshold'])
                else:

                    for x in node['threshold'].split("||"):
                        value = self.all_dict[head][int(x)]
                        if type(value) != int:
                            condition = condition + head + """.equals("{}") || """.format(value)
                        else:
                            condition = condition + head + "=={} || ".format(value)

                    condition += ' 2==1'

                left = ifElse(node['left_child'])
                right = ifElse(node['right_child'])
                return 'if ( ' + condition + ' ) { ' + left + ' } else { ' + right + ' }'

        return return_type + ' predictTree' + str(index) + '(' + self.vars + ') { ' + ifElse(root) + ' }'


    def parseAllTrees(self,trees, array_type='double', return_type='double'):
        import_str = """
import java.lang.Math;        

"""
        return import_str + '\n\n'.join(
            [self.parseOneTree(tree['tree_structure'], idx, array_type, return_type) for idx, tree in enumerate(trees)]) \
               + '\n\n' + return_type + ' predict(' + self.vars + ') { ' \
               + 'double score= ' + ' + '.join(['predictTree' + str(i) + '(' + self.vars_notype + ')' for i in range(len(trees))]) + ';' \
               + """
return  1/(1+ Math.exp(score*-1));
                 
                
                """


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
    gbm_pickle = joblib.load("/Users/kentshih/Downloads/clf.pkl")
    lightgbm2java = Lightgbm2Java()
    code = lightgbm2java.doProcess(gbm_pickle._Booster.dump_model())
    print(code)