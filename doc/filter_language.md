Language for combining filters
------------------------------

Top level structure:

    - "Description of phase":
        - operation:
            parameter: value
            ...
        ...
    ...

Each operation receives, handles, and returns one (key: value (single or collection)) item at a time:

    new_key, new_value = operation(key, value, parameters, context)

Context provides methods for access to external facilities such as logging and filesystem.

First operation is called with a single empty value as input.

Operations
==========

### load

Loads data from given source. Produces combination of input and new data.

    load:
        file: "glob"
        [format: "optional name of format to parse"]
        [as: "optional key for added data instead of root of received collection"]

Each call will read and parse all matching files at once. Filenames are used as keys for associated collections.

### save

Stores input to given source. Passes input on unchanged.

    save:
        file: "filename"
        [format: "optional name of format to write"]
        [from: "optional key of data to save from input instead of all input"]

First call for a filename will overwrite that file, subsequent calls append to it.

### check

Verifies that item complies with specified JSON schema. Default schema to use is `schema`.

    check:
        [schema: "optional key of schema to check against"]

### pass

Passes each value on as is.

### skip

Produces no output.

### deny

Produces an error.

### set

Replaces current key and/or value with a substitute value.
References to keys in current item and matched pattern will be replaced in `template`.

    set:
        {text|template}: {substitute}
        as: {key|value}

### fill

Fills in a template.

    fill:
        template: {key in input collection for the templates}
        [with: {key for values collection to use}]
        as: {key for filled in text}

### each

Executes given operations on each (key: value) item in input collection.
If `match` is given, items not matching its criteria will go through `else` instead.
Keys in `with` will be available in operation.

    each:
        [match: {criteria}]
        do: [operations]
        [else: [operations]]
        [with: [keys of values to keep available in `do`]]

Use `skip` and `keep` in `do` and `else` to filter input items. Default is to `deny`.

#### Criteria

Named values from `on: match` criteria can be used for substitution in operations under `on: do`.

##### all

Each criteria listed under `all` must be true.

    all:
    - {criteria}
    ...

##### any

One or more criteria listed under `any` must be true.

    any:
    - {criteria}
    ...

##### not

Criteria under `not` must not be true.

    not: {criteria}

##### contains

Inspected value must be a collection containing keys matching optional `key:` criteria
with values matching optional `value:` criteria.

    contains:
        [key: {criteria}]
        [value: {criteria}]

##### consists

Inspected value must be a collection containing exactly the keys matching optional `key:` criteria
with values matching optional `value:` criteria.

    consists:
      - [key: {criteria}]
        [value: {criteria}]
      ...

##### text

Inspected value must match given text.

    text: "string"

##### pattern

Inspected value must be text matching given regular expression.
Named groups can be used for substitutions under associated `do`.

    pattern: "a regular expression"

##### schema

Inspected value must match given JSON schema.

    schema: {json schema}
