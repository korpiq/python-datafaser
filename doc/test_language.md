Test Language
=============

Criteria for passing or skipping a piece of data is presented as a data structure.

## Text criteria

### Literal Text

Requires the tested piece to be text exactly equal to specified value.

    "literal text to match"

### pattern

Requires the tested piece to match the given regular expression.

    { pattern: "prefix_[a-z]*_suffix" )

### combines

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

## Number criteria

### exact number

An exact number to match:

    -12.34

### from

Compared value must be a number equal to or more than given number:
 
    { "from": 3 }  # 3 and 3.1 will match, but 2 will not.

### to

Compared value must be a number equal to or less than given number:
 
    { "to": 3 }  # 3 and 2.9 will match, but 3.1 will not.

### above

Compared value must be a number bigger than given number:
 
    { "above": 3 }  # 3.1 will match, but 3 will not.

### below

Compared value must be a number less than given number:
 
    { "below": 3 }  # 2.9 will match, but 3 will not.

### multiple

Compared value must be divisible by (a multiple of) given number:

    { "multiple": 10 }  # accepts only 10, 20, 30...

This can be used to simply require that a number is an integer:

    { "multiple": 1 }  # accepts only integers

## Logical combinations

### all

To require subject data to pass multiple checks, join them in a list under `all`:

    { "all": [list of criteria] }

Empty list of criteria for `All` matches anything (sinceno requirements fail):

    { "all": [] }  # always true

### some

To require subject data to pass one or more checks, join them in a list under `some`:

    { "some": [list of criteria] }

Empty list of criteria for `Some` matches nothing (sinc eat least one match is required):

    { "some": [] }  # always false

#### List elements match any contained values

A list can be used as a shorthand for `some`:

    [ "A", "B" ]  # matches both "A" and "B"
    []  # matches nothing

### not

To require that a criteria shall not be met, put it under `not`:

    { "not": {criteria required to fail} }

## Test functions

Test functions can be defined for later use by name:

    {
        "tests": {
            "begins with letter": { "test": { "pattern": "[A-Z].*" } },
            "is integer": { "test": { "multiple": 1 } },
            "true": { "test": { "all": [] } },
        }
    }

Defined tests can be used by their names:

    { "is integer": {} }

Name of a test can be any string expect those already defined in this document.

### Test function parameters

Test functions can be defined to have parameters:

    {
        "text contains word": {
            "parameters: {
                "word": { "pattern": "\\w+" }
            }
            "test": {
                "pattern": ".*{{ word }}.*"
            }
        }
    }

Parameter values must match the associated criteria.

Parameter values will be embedded into test functions before use:

    { "text contains word": { "word": "karpalo" } }

Above will turn into a test:

    { "pattern": ".*karpalo.*" }

Defined parameters must be referred in function body.
