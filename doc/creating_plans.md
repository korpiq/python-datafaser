Creating Datafaser Run Plans
----------------------------

Define one small part of your work at a time to avoid getting stuck with complex problem sets.
Repeat steps below until you can generate everything you need.

Define a data loading phase
===========================

 1. Add a base data file with reasonable defaults and empty customization fields to a data directory
    - TODO: create and refer to an example of base data
 2. Add schema that matches complete data from the added file filled with customizations
    - TODO: create and refer to instructions on schemas
 3. Add to `runplan.yaml`:

    - load:
        files:
        - "path/to/your/data" 
        - "path/to/your/customization" # create later

 4. Run `datafaser`. It should fail with missing customizations.
 5. Run `datafase --instantiate` to create the missing data customization template.
 6. Fill in the customization template.
 7. Fix base data, schema, and customization until the run succeeds.

Define data generation phase
============================

Do this when necessary data can be generated from earlier data instead of entering it manually.
This reduces problems caused by manual work.

 1. Create a template that generates data in your preferred format from the data already available.
 2. Create a schema for the data to generate.
 3. Add to `runplan.yaml`:

    - modify:
        from: "path.to.input.data" # if you can make do with a subset of data
        to: "path.to.output.data"  # try to produce data that can be entered in a specific place
        templates:
        - files:
          - "path/to/your/data/generation/template"
        schema:
        - files:
          - "path/to/schema/for/generated/data"

 4. Run `datafaser` and fix your generation and schema until the run succeeds.

Define templates and their results 
==================================

 1. Create such a template that you can get working with the data you have. 
 2. Add to `runplan.yaml`:

    - fill:
        templates:
        - files:
          - "path/to/your/template"
        results: # TODO: describe results verification

 3. Run `datafaser` and fix the template, data, schema, and customization until the run succeeds.

Commit to version control
=========================

Keep all the files you create (except customizations specific for single runs) in version control.
Commit every time you have completed a small, working change.
This way it becomes easy to reason about what affects the results in what ways.

Define templates for scripts to use the results
===============================================

Put results to use when they have been successfully created and verified.

Write templates for scripts that do whatever you need to do (such as build, package, publish).
Keep them simple and straightforward to avoid problems with complex generated code.

#### Separate version control for results

Save all results to a different version control.
This way you can inspect published stuff separately from all the details needed to create it.

Do not commit manual changes to the results repository.
That will confuse people using the generation system.
It will be easier even for yourself to not have to remember such modifications.

Single step from changes to publication
=======================================

Store a single script in your project that does two things:

 1. Runs `datafaser` to generate all necessary files, together with a script to run any later steps.
 2. Runs the generated post-processing script.

