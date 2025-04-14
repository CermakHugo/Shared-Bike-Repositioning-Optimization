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

## Research and Developement
Selection of Strategies to Compare

Cho et al. (2021) demonstrated that more accurate demand prediction leads to more effective vehicle rebalancing in shared mobility systems. Similarly, Albuquerque et al. (2021) highlighted the effectiveness of machine learning techniques for forecasting demand. Among these, Random Forest has emerged as one of the most promising algorithms, especially when incorporating historical and weather-related data, as shown by Ashqar et al. (2020). Given the strong consensus in the literature regarding the performance of Random Forest for demand prediction, our study focuses instead on the decision-making phase of the rebalancing process. This allows for a more meaningful comparison of rebalancing strategies, as the prediction component is considered largely resolved.

Selection of Decision-Making Strategies for E-bike Rebalancing

For the decision-making process in e-bike rebalancing, Xanthopoulos et al. (2024) demonstrated that genetic algorithms, a class of evolutionary metaheuristics, can effectively solve complex optimization problems, such as determining the location and allocation of shared vehicles. Based on this insight, we selected two decision-making strategies to compare. The first is a fully automated approach using a genetic algorithm to dynamically optimize the rebalancing process. The second represents a more practical, human-centered strategy supported by a small-scale Vehicle Routing Problem (VRP) solver, which is used to generate optimal routes within each time slot. This comparison aims to evaluate the added value of advanced algorithmic approaches over more traditional operational strategies that rely on human expertise and classic optimization tools.


## Annotated Literature Review

- Liu, J., Sun, L., Chen, W., et al. (2016). Rebalancing Bike Sharing Systems: A Multi-Source Data Smart Optimization. Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, San Francisco, CA, USA, 13-17 August 2016.

This paper predicts bike demand and optimizes rebalancing using historical and weather data. It uses MSWK for predicting pickups and ISBT for drop-offs. Rebalancing is solved with MINLP and clustering (AdaCCKC), grouping stations and assigning vehicles. MSWK and ISBT outperform baseline models, especially on weekends. Tested on NYC Citi Bike data, the method improves demand prediction and rebalancing.

- Conrow, L., Murray, A.T., Fischer, H.A. (2018). An Optimization Approach for Equitable Bicycle Share Station Siting. Journal of Transport Geography, 69, 163–170.

This paper explores how bike share stations can be more effectively distributed across a city to improve accessibility and ensure both spatial and social equity. It points out that traditional designs, which tend to cluster stations in central areas, often fail to meet equity objectives. Although adding more stations does increase access and coverage, the results also show that the benefits level off compared to the rising costs highlighting the importance of planning that balances efficiency with fairness.

- Ashqar, H.I., Elhenawy, M., Almannaa, M.H., Ghanem, A., Rakha, H.A., House, L. (2020). Modeling Bike Availability in a Bike-Sharing System Using Machine Learning. arXiv preprint arXiv:2006.08352.

This paper predicts the number of bikes at each station using machine learning. Random Forest (RF) performs best, with a Mean Absolute Error (MAE) of 0.37 bikes/station, outperforming LSBoost and PLSR. Predictions are most accurate with a 15-minute horizon. Key features include station neighbors and weather (temperature, rain, humidity, wind, visibility). The study suggests adding memory (past availability) for future improvements.


- Cho, J.-H., Seo, Y.-H., Kim, D.-K. (2021). Efficiency Comparison of Public Bike-Sharing Repositioning Strategies Based on Predicted Demand Patterns. Transportation Research Record, 2675(11), 104–118. 

This study shows that improving the efficiency of bike-sharing systems requires adapting bike repositioning strategies to meet daily demand variations. The researchers tested several strategies and found that those that use additional constraints (such as station imbalance or prediction error) are more effective at reducing bike shortages, especially when demand varies greatly. To determine which strategy to use, they created two indicators: RRPI (which measures inventory variations within the day) and SVUD (which measures shortage differences between stations). These two indices allow for classifying days according to the type of demand, and thus choosing the most appropriate strategy in advance. In short, the best strategy depends on the type of day, and this method allows for smarter, data-driven decisions.

- Albuquerque V., Andrade F., Ferreira J., Dias M., Bacao F. Bike-sharing mobility patterns: A data-driven analysis for the city of Lisbon. EAI Endorsed Transactions on Smart Cities. 2021;5(16):1–20

This study explored how people use Lisbon’s bike-sharing system (BSS) and how usage changed between 2018 and 2020. It found that most trips happen on weekdays, especially in the afternoon and during good weather—without rain and with mild temperatures. In 2019, the number of trips doubled compared to 2018, showing growing adoption of bikes for daily commuting. However, in 2020, the COVID-19 pandemic caused a sharp drop in bike usage, especially during lockdown months. The most popular routes were around business and university areas, and patterns suggest that bikes are mainly used for short, regular trips between key urban zones. A key insight from the study is that better demand prediction improves the quality of rebalancing, particularly through the use of logit models and detailed input data.


- Xanthopoulos, S., van der Tuin, M., Sharif Azadeh, S., Correia, G.H.A., van Oort, N., Snelder, M. (2024). Optimization of the location and capacity of shared multimodal mobility hubs to maximize travel utility in urban areas. Transportation Research Part A, 179, 103934

This research developed a genetic algorithm to optimize location and capacity, an approach that can be adapt for repositioning for deciding where to install shared mobility hubs (cars, bicycles, electric scooters) in a large city like Amsterdam. The goal is to maximize benefits for users, while taking into account the available budget. The model shows that it is better to install several small, well-distributed hubs rather than a few large ones, in order to better cover the city and bring services closer to people. However, the study also reveals that without policies to limit car use (such as increasing parking costs), the environmental benefits remain low, as the majority of users instead abandon cycling or public transport in favor of these shared modes.


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
