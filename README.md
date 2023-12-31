<div align="center">
<h1 align="center">
<img src="https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.freepik.com%2Fpremium-vector%2Falpaca-logo-design-vector-illustration_31071157.htm&psig=AOvVaw0nHAut8L3z9ux9X37-6lhv&ust=1704073395101000&source=images&cd=vfe&ved=0CBIQjRxqFwoTCIi12ZzGuIMDFQAAAAAdAAAAABAE" width="100" />
<br>PAIRS-TRADING-ALGORITHM</h1>
<h3>◦ Statistical Arbitrage Trading Algorithm</h3>
<h3>◦ Developed to interact with the ALPACA API with the software and tools below.</h3>

<p align="center">
<img src="https://img.shields.io/badge/SciPy-8CAAE6.svg?style=flat-square&logo=SciPy&logoColor=white" alt="SciPy" />
<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat-square&logo=Python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/pandas-150458.svg?style=flat-square&logo=pandas&logoColor=white" alt="pandas" />
<img src="https://img.shields.io/badge/NumPy-013243.svg?style=flat-square&logo=NumPy&logoColor=white" alt="NumPy" />
</p>
<img src="https://img.shields.io/github/license/AidanAlr/Pairs-Trading-Algorithm?style=flat-square&color=5D6D7E" alt="GitHub license" />
<img src="https://img.shields.io/github/last-commit/AidanAlr/Pairs-Trading-Algorithm?style=flat-square&color=5D6D7E" alt="git-last-commit" />
<img src="https://img.shields.io/github/commit-activity/m/AidanAlr/Pairs-Trading-Algorithm?style=flat-square&color=5D6D7E" alt="GitHub commit activity" />
<img src="https://img.shields.io/github/languages/top/AidanAlr/Pairs-Trading-Algorithm?style=flat-square&color=5D6D7E" alt="GitHub top language" />
</div>

---

## 📖 Table of Contents
- [📖 Table of Contents](#-table-of-contents)
- [📍 Overview](#-overview)
- [📦 Features](#-features)
- [📂 Repository Structure](#-repository-structure)
- [⚙️ Modules](#modules)
- [🚀 Getting Started](#-getting-started)
    - [🔧 Installation](#-installation)
    - [🤖 Running Pairs-Trading-Algorithm](#-running-Pairs-Trading-Algorithm)
    - [🧪 Tests](#-tests)
- [🛣 Roadmap](#-roadmap)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [👏 Acknowledgments](#-acknowledgments)

---


## 📍 Overview

► This Algorithm is separated into Analysis and Trading Functions.
Analysis contains the statistical methods required to implement a statistical arbitrage strategy.
Trading contains the methods that interact with the Alpaca API to execute the strategy.  
The algorithm is configured to use my ALPACA paper account API key and secret.



---

## 📦 Features

► Analysis


---


## 📂 Repository Structure

```sh
└── Pairs-Trading-Algorithm/
    ├── AidanUtils/
    │   ├── MyTimer.py
    │   ├── ProgressBar.py
    │   ├── formatting_and_logs.py
    ├── Analysis/
    │   ├── DATES.py
    │   ├── errors.py
    │   ├── statistical_methods.py
    │   ├── stock_data.py
    │   └── visualisation.py
    ├── Executors/
    │   ├── alpaca_executor.py
    │   ├── analysis_executor.py
    │   └── cli_controller.py
    ├── Tests/
    │   ├── test_alpaca.py
    │   └── test_collect_metrics_for_pair.py
    ├── Trading/
    │   └── alpaca_functions.py
    ├── requirements.txt
    └── to_do_list.txt

```


---


## ⚙️ Modules

<details closed><summary>Root</summary>

| File                                                                                               | Summary       |
| ---                                                                                                | ---           |
| [requirements.txt](https://github.com/AidanAlr/Pairs-Trading-Algorithm/blob/main/requirements.txt) | ► Requirements needed to run program, use "pip install -r requirements.txt" |

</details>

<details closed><summary>Analysis</summary>

| File                                                                                                                  | Summary       |
| ---                                                                                                                   | ---           |
| [Visualisation.py](https://github.com/AidanAlr/Pairs-Trading-Algorithm/blob/main/Analysis/Visualisation.py)           | ► Functions to visualise important metrics |
| [StockData.py](https://github.com/AidanAlr/Pairs-Trading-Algorithm/blob/main/Analysis/StockData.py)                   | ► StockData class and methods |
| [Dates.py](https://github.com/AidanAlr/Pairs-Trading-Algorithm/blob/main/Analysis/Dates.py)                           | ► Enum for dates |
| [StatisticalMethods.py](https://github.com/AidanAlr/Pairs-Trading-Algorithm/blob/main/Analysis/StatisticalMethods.py) | ► Functions performing statisticaly analysis on StockData |

</details>

<details closed><summary>Tests</summary>

| File                                                                                                 | Summary       |
| ---                                                                                                  | ---           |
| [test_alpaca.py](https://github.com/AidanAlr/Pairs-Trading-Algorithm/blob/main/Tests/test_alpaca.py) | ► Testing the Alpaca Functions |

</details>

<details closed><summary>Executors</summary>

| File                                                                                                                 | Summary       |
| ---                                                                                                                  | ---           |
| [AnalysisExecutor.py](https://github.com/AidanAlr/Pairs-Trading-Algorithm/blob/main/Executors/AnalysisExecutor.py)   | ► Executor for analysis |
| [AlgorithmExecutor.py](https://github.com/AidanAlr/Pairs-Trading-Algorithm/blob/main/Executors/AlgorithmExecutor.py) | ► Executor for algorithm |

</details>

<details closed><summary>Aidanutils</summary>

| File                                                                                                      | Summary       |
| ---                                                                                                       | ---           |
| [MyTimer.py](https://github.com/AidanAlr/Pairs-Trading-Algorithm/blob/main/AidanUtils/MyTimer.py)         | ► INSERT-TEXT |
| [ProgressBar.py](https://github.com/AidanAlr/Pairs-Trading-Algorithm/blob/main/AidanUtils/ProgressBar.py) | ► INSERT-TEXT |

</details>

<details closed><summary>Trading</summary>

| File                                                                                                           | Summary       |
| ---                                                                                                            | ---           |
| [AlpacaFunctions.py](https://github.com/AidanAlr/Pairs-Trading-Algorithm/blob/main/Trading/AlpacaFunctions.py) | ► INSERT-TEXT |

</details>

---

## 🚀 Getting Started

### 🔧 Installation

1. Clone the Pairs-Trading-Algorithm repository:
```sh
git clone https://github.com/AidanAlr/Pairs-Trading-Algorithm
```

2. Change to the project directory:
```sh
cd Pairs-Trading-Algorithm
```

3. Install the dependencies:
```sh
pip install -r requirements.txt
```

### 🤖 Running Program
1. Change to the Executors directory:
```sh
cd Pairs-Trading-Algorithm/Executors
```


#### Running Analysis

```sh
python -m AnalysisExecutor
```



### 🤖 Running Pairs-Trading-Algorithm

```sh
python -m AlgorithmExecutor
```

### 🧪 Tests

```sh

```

---


## 🛣 Project Roadmap

> - [X] `ℹ️  Task 1: Implement X`
> - [ ] `ℹ️  Task 2: Implement Y`
> - [ ] `ℹ️ ...`


---

## 🤝 Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Submit Pull Requests](https://github.com/AidanAlr/Pairs-Trading-Algorithm/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
- **[Report Issues](https://github.com/AidanAlr/Pairs-Trading-Algorithm/issues)**: Submit bugs found or log feature requests for AIDANALR.

#### *Contributing Guidelines*

<details closed>
<summary>Click to expand</summary>

1. **Fork the Repository**: Start by forking the project repository to your GitHub account.
2. **Clone Locally**: Clone the forked repository to your local machine using a Git client.
   ```sh
   git clone <your-forked-repo-url>
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear and concise message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to GitHub**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.

Once your PR is reviewed and approved, it will be merged into the main branch.

</details>

---

[**Return**](#Top)

---

