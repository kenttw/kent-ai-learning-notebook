import json
from typing import List

from io import StringIO


def genOneHotSql(cat_cols, enc_categories, numerical_cols):
    numerical_cols = ",".join(["`{}`".format(x) for x in numerical_cols])

    r = StringIO()
    r.write('CREATE VIEW one_hot_view as \n')
    r.write("select {},\n".format(numerical_cols))
    for i, row in enumerate(enc_categories):
        for c in row:
            r.write("""  case when `{}`='{}' then 1 else 0 end as `{}`,
""".format(cat_cols[i], c, c))
    r.write("  `id`\n")
    r.write("\nfrom raw_data;")
    return r.getvalue()


def xgb2sql(xgb_booster, table_name: str, index_list=[], sql_type='flink'):
    """
    Takes in an XGB Booster and converts it to a SQL query.
    Look, I'm not saying you should use this, but I'm saying it now exists.
    I imagine any sort of tree based model could be relatively easily converted to a SQL query using this.
    Parameters
    ----------
    xgb_booster: xgboost.core.Booster
        https://xgboost.readthedocs.io/en/latest/tutorials/model.html
    table_name: str
        The name of the SQL table to query from. Obviously this table must be the same as the model inputs or else it won't work.
    index_list : list
        Anything in the list will be passed through as a column in your final output.
    sql_type : str
        If there's a better way native to the sql_type to generate the code, it will be used.
        Otherwise defaults to Flink Hive compliant code.
    """

    def _json_parse(xgb_booster) -> str:

        ret = xgb_booster.get_dump(dump_format="json")

        json_string = "[\n"
        for i, _ in enumerate(ret):
            json_string = json_string + ret[i]
            if i < len(ret) - 1:
                json_string = json_string + ",\n"
        json_string = json_string + "\n]"

        return json.loads(json_string)

    def _flink_eval(index_list: List[str], leaf_list: List) -> str:

        column_string = "\n\t+ ".join(columns)
        if len(index_list) > 0:
            query = f"""\nSELECT id,
    {index_string},
    1 / ( 1 + EXP ( - (
    {column_string}) ) ) AS score
FROM booster_output"""
        else:
            query = f"""\nSELECT id,
    1 / ( 1 + EXP ( - (
    {column_string} ) ) ) AS score
FROM booster_output"""

        return query

    def _extract_values(obj, key):

        key_dict = {}
        arr = []
        info_dict = {}

        def _extract(obj, arr, key, prev=None):

            if isinstance(obj, dict):
                try:
                    info_dict.update(
                        {
                            obj["nodeid"]: {
                                "parent": prev,
                                "split_column": obj["split"],
                                "split_number": obj["split_condition"],
                                "if_less_than": obj["yes"],
                                "if_greater_than": obj["no"],
                                "if_null": obj["missing"],
                            }
                        }
                    )

                except:
                    info_dict.update({obj["nodeid"]: {"parent": prev}})

                prev = obj["nodeid"]

                for k, v in obj.items():
                    if isinstance(v, (dict, list)):
                        _extract(v, arr, key, prev)
                    elif k == key:
                        key_dict.update({obj["nodeid"]: v})
            elif isinstance(obj, list):
                for item in obj:
                    _extract(item, arr, key, prev)
            return key_dict

        results = _extract(obj, arr, key)
        return results, info_dict

    def _recurse_backwards(first_node) -> str:

        query_list: List[str] = []

        def _recurse(x) -> None:

            prev_node = x
            next_node = splits[prev_node]["parent"]
            try:
                node = splits[next_node]
                if (node["if_less_than"] == prev_node) & (
                    node["if_less_than"] == node["if_null"]
                ):
                    text = f"(({node['split_column']} < {node['split_number']}) OR ({node['split_column']} IS NULL))"
                    query_list.insert(0, text)
                    _recurse(next_node)
                elif node["if_less_than"] == prev_node:
                    text = f"({node['split_column']} < {node['split_number']})"
                    query_list.insert(0, text)
                    _recurse(next_node)
                elif (node["if_greater_than"] == prev_node) & (
                    node["if_greater_than"] == node["if_null"]
                ):
                    text = f"(({node['split_column']} >= {node['split_number']}) OR ({node['split_column']} IS NULL))"
                    query_list.insert(0, text)
                    _recurse(next_node)
                elif node["if_greater_than"] == prev_node:
                    text = f"({node['split_column']} >= {node['split_number']})"
                    query_list.insert(0, text)
                    _recurse(next_node)
            except:
                pass

        _recurse(first_node)

        s = "\n\t\t\tAND "

        return s.join(query_list)

    tree_json = _json_parse(xgb_booster)

    index_list = [str(i) for i in index_list]
    index_string = ",\n".join(index_list)

    leaf_list = []
    columns = []
    counter = 0
    for i in range(0, len(tree_json)):
        leaves, splits = _extract_values(tree_json[i], "leaf")
        column_list = []

        for base_leaf in leaves:
            leaf_query = (
                "\t\t\tWHEN "
                + _recurse_backwards(base_leaf)
                + f"\n\t\tTHEN {leaves[base_leaf]}"
            )

            column_list.append(leaf_query)

        column = f"column_{counter}"
        column_list = "\t\tCASE\n" + ("\n").join(column_list) + f"\n\t\tEND AS {column}"

        columns.append(column)
        leaf_list.append(column_list)
        counter += 1

    if sql_type == "flink":
        output = _flink_eval(index_list, leaf_list)
    else:
        pass
        raise

    query = (
        "CREATE VIEW moon_table AS (\n\tSELECT id,\n"
        + ", \n".join((index_list + leaf_list))
        + f"\n\tFROM {table_name}"
        + f");\n{output}"
    )

    return query