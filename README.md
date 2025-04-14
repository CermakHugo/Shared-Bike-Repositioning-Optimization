# Optimising the rebalancing of self-service bicycles

## TEAM
- LE CHAIX Marie-Zita (MZ)
- CERMAK Hugo (HC)
- VIGAND Joseph (JV)
- JACQUET Alexis (AJ)

  
## Description

This research project aims to optimise the rebalancing of bicycles in a self-service system. The aim is to propose models and algorithms to improve the availability of bicycles and free spaces in stations while minimising logistical costs.


## Objectives
The study aims to minimize unmet demand with the following objectives:

- Utilizes robust models to forecast short to medium-term station utilization by identifying daily trends and providing real-time or near-real-time estimates. 

- Develops and compares route-planning and capacity-allocation methods, including heuristics and genetic algorithms to effectively manage truck-based redistribution in response to station surpluses or deficits. 

- Assesses the necessary number of trucks and dispatch intervals while balancing operational costs, complexity, equity considerations, and feasibility within standard computational resources.

## Annotated Literature Review

- Ashqar, H.I., Elhenawy, M., Almannaa, M.H., Ghanem, A., Rakha, H.A., House, L. (2020). Modeling Bike Availability in a Bike-Sharing System Using Machine Learning. arXiv preprint arXiv:2006.08352.
  -> developed random forest and boosting techniques to predict short-term bike availability. 

- Albuquerque V., Andrade F., Ferreira J., Dias M., Bacao F. Bike-sharing mobility patterns: A data-driven analysis for the city of Lisbon. EAI Endorsed Transactions on Smart Cities. 2021;5(16):1–20
  -> demonstrated the effectiveness of machine learning in modeling station demand in dynamic environments. 

- Liu, J., Sun, L., Chen, W., et al. (2016). Rebalancing Bike Sharing Systems: A Multi-Source Data Smart Optimization. Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, San Francisco, CA, USA, 13-17 August 2016.
  -> incorporated multi-source data for route planning.

- Cho, J.-H., Seo, Y.-H., Kim, D.-K. (2021). Efficiency Comparison of Public Bike-Sharing Repositioning Strategies Based on Predicted Demand Patterns. Transportation Research Record, 2675(11), 104–118.
  -> emphasized how demand forecasts can minimize unmet demand. 

- Xanthopoulos, S., van der Tuin, M., Sharif Azadeh, S., Correia, G.H.A., van Oort, N., Snelder, M. (2024). Optimization of the location and capacity of shared multimodal mobility hubs to maximize travel utility in urban areas. Transportation Research Part A, 179, 103934
  -> utilized a genetic algorithm to optimize location and capacity, an approach that can be adapt for repositioning. 

- Conrow, L., Murray, A.T., Fischer, H.A. (2018). An Optimization Approach for Equitable Bicycle Share Station Siting. Journal of Transport Geography, 69, 163–170.
  -> highlighted the importance of addressing coverage equity in system planning, which is conceptually significant for ensuring that no sub-region of the city is overlooked.

## Technologies used

- Languages**: Python

- Main libraries**: Pandas, NumPy, SciPy, NetworkX, Scikit-learn

- Visualisation tools**: Matplotlib, Seaborn, Plotly

- Optimisation**: PuLP, OR-Tools


## Data

Data used for this project includes:

- Open data from public bike systems.

- Historical bike flows between stations.

- Weather and event data that can influence demand.

## Project Contribution
|Project component|Description|MZ|HC|JV|AJ|
|-|-|-|-|-|-|
|Code|Contributing code for the tasks of the project|5|45|45|5|
|Communication|Communication with stakeholders and facilitator role within the team|20|35|30|15|
|Research|Module-specific research to direct the development|30|25|30|15|
|Presentation|Presentation of the project results|0|0|0|0|
|Management|Planning individual work as well as collaboration within the assigned module|30|25|25|20|
|**Overall**|Involvement optimality score|0|0|0|0|

## Directory structure

```

├── data/ # Raw and pre-processed data

├── notebooks/ # Jupyter notebooks for exploratory analysis and development

├── src/ # Source code for models and algorithms

├── results/ # Simulation and optimisation results

├── docs/ # Project documentation

├── requirements.txt # List of dependencies

├── README.md # This file

```



## Installation

1. Clone this repository:

   ``bash

   git clone https://github.com/votre-utilisateur/optimisation-reequilibrage-velo.git

   cd optimisation-reequilibrage-velo

   ```

2. Create a virtual environment and install the dependencies:

   ``bash

   python -m venv

   source venv/bin/activate # (or `venv\Scripts\activate` on Windows)

   pip install -r requirements.txt

   ```



## Usage

- Run the notebooks in the `notebooks/` folder to explore the data and test the models.

- Use the `src/` folder to run the optimisation scripts and generate rebalancing recommendations.



## Contributions

Contributions are welcome!

- Fork this repository

- Create a branch: `git checkout -b feature-new-feature`

- Make your changes and commit: `git commit -m ‘Add new feature’`.

- Push the branch: `git push origin feature-new-feature

- Create a Pull Request



## License

This project is licensed under the MIT license - see the [LICENSE](LICENSE) file for more details.



## Contact

If you have any questions or suggestions, please contact :

- Name**: Hugo CERMAK

- Email**: huce62694@eleve.isep.fr


---



Thank you for checking out this project! 🚲
