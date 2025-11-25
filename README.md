# Functional Data Processing Pipeline
The Functional Data Processing Pipeline is a modular system designed to load datasets, clean them, transform them, and analyze them — all using pure functions, immutability, and function composition.

_The project demonstrates how Python can be used in a functional style to build a clean, maintainable, and testable data-processing architecture._

**This project supports:**
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

📦 functional-data-pipeline
│
├── data/row                       # Input datasets
│   ├── sample.csv
│   └── sample.json
│
├── src/
│   ├── __init__.py             
│   ├── load_data.py               # CSV/JSON loading functions
│   ├── clean_data.py              # Missing data handling + standardization
│   ├── transform_data.py          # Filter, compute new columns, aggregation
│   ├── analyze_data.py            # Statistical + correlation functions
│   ├── visualize_data.py          # Produce charts
│   ├── output_data.py             # Save output CSV/JSON
│   └── utils.py                   # Utility functions (ex.display_dataset_info)      
│
├── test/            
│   └── testing.py                 # Tesing Pipeline
│
├── main.py                        # Pipeline entry point
├── requirements.txt               # Required packags
└── README.md                      # Documentation

