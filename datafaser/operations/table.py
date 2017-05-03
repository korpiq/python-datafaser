

def convert(data_tree, directives):
    from_branch = directives['from']['table']['branch']
    to_branch = directives['to']['branch']

    source = data_tree.reach(from_branch)
    headers = source[0]
    target = []
    for row in source[1:]:
        o = {}
        for i in range(0, len(headers)):
            o[headers[i]] = row[i]
        target.append(o)
    data_tree.merge(target, to_branch)
