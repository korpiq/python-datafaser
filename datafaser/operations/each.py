import copy
import datafaser.operations

help_topic = 'Each operation'
help_text = '''
Do an operation for each list member:

    - "Change field names in all list members":
        - each:
          from:
            branch: "objects from spreadsheet"
          to:
            branch: "objects with new names"
          do:
            change:
              keys:
                old key: new key
              others: keep

Operation under "do" is used to produce an item to to.branch from each item in from.branch:

    objects from spreadsheet:
      - my key: value 1 on row 1
        old key: value 2 on row 1
      - my key: value 1 on row 2
        old key: value 2 on row 2
        
    objects with new names:
      - my key: value 1 on row 1
        new key: value 2 on row 1
      - my key: value 1 on row 2
        new key: value 2 on row 2
'''


def convert(data_tree, directives):
    from_branch = directives['from']['branch']
    to_branch = directives['to']['branch']

    operation_name = list(directives['do'].keys())[0]
    operation_directives = directives['do'][operation_name]
    operation = datafaser.operations.get_default_operations_map(data_tree)[operation_name]

    source = data_tree.reach(from_branch)

    if isinstance(source, list):
        keys = range(0, len(source))
        data_tree.merge([], to_branch)
    else:
        keys = source.keys()
        data_tree.merge({}, to_branch)

    target = data_tree.reach(to_branch)

    for key in keys:
        value = source[key]
        value_class = value.__class__
        if isinstance(source, list):
            target.append(value_class())
        else:
            target[key] = value_class()

        call_directives = copy.deepcopy(operation_directives)
        call_directives['from'] = {'branch': '%s.%s' % (from_branch, key)}
        call_directives['to'] = {'branch': '%s.%s' % (to_branch, key)}

        operation(data_tree, call_directives)
