Path Language
=============

Path language lets us define criteria for finding data in nested data structures.
Language itself should be nested data easy to read and write by humans.

Nested data structure
---------------------

Nested data leaf items are basic scalar values, just like in JSON:

 - strings (`"text"`)
 - numbers (`-12.34`)
 - booleans (`true` or `false`)
 - None (`null`).

Leaf items can be collected in collections. A collection is either one of

 - a list

       [ "value 1", "value 2", ...]
 - an object (collections of key-value pairs with strings as keys)

       { "key 1": "value 1", "key 2": "value 2", ...}

Values in collections can be other collections or scalars.
Collections can be empty.

Path structure
--------------

A path is a list of elements:

    [ base_level_name, sublevel_1_name, sublevel_2_name, ...]

Each element of a path matches one or more elements at associated path level(s).

### Object elements define filters for elements

#### key

Specify criteria to be met by the key of an object:

    { "key": {text criteria} }

#### index

Specify criteria to be met by the index of an element in a list:

    { "index": {number criteria} }

#### value

Specify criteria to be met by scalar value at this point in `path`:

    { "value": {text or number criteria} }

#### contains

Specify criteria to be met by 

    { "contains": {path criteria} }

#### Text criteria

##### literal

    "literal text to match"

##### pattern

    { pattern: "regular expression to match" )

##### combines

A list of criteria applying to consequent parts that make up the text: literals and other subcriteria.

    { "combines": [list of criteria that match text piece by piece] }

Example:

    {
        "combines": [
            "prefix_",
            { "pattern": "[a-z]*" },
            "_suffix"
        ]
    }

#### Number criteria

##### exact number

An exact number to match:

    -12.34

For instance:

    { "index": 3 }
    { "value": -12.34 }

##### from

Compared value must be a number equal to or more than given number:
 
    { "from": 3 }  # 3 and 3.1 will match, but 2 will not.

##### to

Compared value must be a number equal to or less than given number:
 
    { "to": 3 }  # 3 and 2.9 will match, but 3.1 will not.

##### above

Compared value must be a number bigger than given number:
 
    { "above": 3 }  # 3.1 will match, but 3 will not.

##### below

Compared value must be a number less than given number:
 
    { "below": 3 }  # 2.9 will match, but 3 will not.

##### multiple

Compared value must be divisible by (a multiple of) given number:

    { "multiple": 10 }  # accepts only 10, 20, 30...

This can be used to simply require that a number is an integer:

    { "multiple": 1 }  # accepts only integers

#### Logical combinations

##### all

To require subject data to pass multiple checks, join them in a list under `all`:

    { "all": [list of criteria] }

##### any

To require subject data to pass one or more checks, join them in a list under `any`:

    { "any": [list of criteria] }

##### not

To require that a criteria shall not be met, put it under `not`:

    { "not": {criteria required to fail} }

##### boolean

To make a criteria always pass or fail, make it `true` or `false`:

    true

#### Path Targeting

First element of a path may specify where the path targets at.

##### namespace

Specify which namespace the path refers to:

    { "namespace": "name of namespace" }

Namespace can be combined with other targets.

##### parent

Specify how many path elements from root of namespace toward current branch to start:

    { "parent": 1 }

Use negative numbers to count from current branch:

    { "parent": -1 }

#### Varying number of path levels to match

    { "times": {number criteria} }

Combine `times` with an actual test to match:

    {
        "times": { "from": 0, "to": 2 },
        "key": { "pattern": "prefix_[a-z]*_suffix" }
    }
