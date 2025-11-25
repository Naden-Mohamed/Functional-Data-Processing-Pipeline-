# Functional Data Processing Pipeline-
The Functional Data Processing Pipeline is a modular system designed to load datasets, clean them, transform them, and analyze them — all using pure functions, immutability, and function composition.

The project demonstrates how Python can be used in a functional style to build a clean, maintainable, and testable data-processing architecture.

This project supports:
* CSV and JSON input
* Missing-data handling
* Data cleaning, transformation, and aggregation
* Statistical analysis (mean, variance, correlation, etc.)
* Data visualizations
* Exporting processed data

## Functional Programming Principles Used:
This project is intentionally built using functional programming concepts:

* Pure Functions

  - All operations return new datasets instead of modifying them in place.

* Immutability

  - Data is treated as immutable — transformations always produce copies, ensuring predictable behavior.

* Higher-Order Functions

  - Functions are passed as parameters to other functions

* Function Composition

  - Complex operations are built by combining smaller functions together into a pipeline.
