
 # Customer Intelligence Platform

## Project Overview

The Customer Intelligence Platform is an end-to-end data science and business intelligence project developed using the Brazilian Olist e-commerce dataset.

The platform integrates PostgreSQL, SQL, Python, machine learning, and Power BI to analyse customer purchasing behaviour, predict 60-day repeat-purchase propensity, examine observed merchandise value, and identify opportunities for evidence-based retention decisions.

The analytical workflow covers data preparation, customer-level feature engineering, predictive modelling, model evaluation, customer scoring and segmentation, customer value analysis, and business recommendations across 12 Jupyter notebooks.

The validated customer reporting dataset contains 78,100 historical customers, with an observed 60-day repeat-purchase rate of 2.03% and approximately R$10.61 million in combined initial and subsequent merchandise value.

The analysis identifies meaningful differences across customer profiles, including 20,931 higher-initial-value, low-propensity customers who warrant further investigation.

The platform is a historical analytical and decision-support prototype, not a production-ready automated targeting system. Predictive reliability requires further prospective validation, and the commercial effectiveness of retention interventions remains unproven.

The project concludes with evidence-based business recommendations, a proposed controlled retention experiment, and an assessment of its statistical and commercial feasibility.
**---**

**## Project Structure**

\`\`\`

customer-intelligence-platform/

│

├── data/

│   └── processed/

│

├── notebooks/

│

├── powerbi/

│   └── powerbi.pbix

│

├── scripts/

│

├── sql/

│   ├── 01_create_customer_table.sql

│   ├── 02_create_remaining_tables.sql

│   ├── 03_customer_spending.sql

│   ├── 04_customer_segmentation.sql

│   ├── 05_data_validation.sql

│   └── 06_second_purchase_analysis.sql

│

├── .gitignore

├── README.md

└── requirements.txt

\`\`\`


**## Analytical Workflow**

The Customer Intelligence Platform was developed across 12 Jupyter notebooks, covering the full analytical process from exploratory analysis to business recommendations.

| Notebook | Analytical Stage | Purpose |
|---|---|---|
| 01 | Exploratory Data Analysis | Investigate customer transactions, purchasing patterns, and data quality. |
| 02 | Customer Feature Engineering | Build customer-level features and define the 60-day repeat-purchase target. |
| 03 | Repeat-Purchase Modelling | Develop predictive models using chronological training, validation, and test populations. |
| 04 | Model Evaluation and Insights | Evaluate discrimination, probability reliability, and model performance against baselines. |
| 05 | Model Explainability | Examine model drivers and interpret their relationship with repeat-purchase predictions. |
| 06 | Model Improvement | Investigate alternative modelling approaches and potential performance improvements. |
| 07 | Customer Scoring and Segmentation | Generate propensity-based customer groups and examine historical repeat-purchase behaviour. |
| 08 | Model Reliability and Validation | Investigate temporal stability, evaluation populations, and model reliability limitations. |
| 09 | Historical Customer Value Analysis | Measure observed initial and subsequent merchandise value. |
| 10 | Predictive Customer Value | Explore experimental approaches to predicting customer monetary value. |
| 11 | Customer Value Integration | Integrate validated customer outcomes, propensity segments, and historical merchandise value. |
| 12 | Business Insights and Recommendations | Translate analytical findings into business hypotheses, experiment feasibility assessments, and decision recommendations. |

**### Analytical Outcome**

The platform establishes a reproducible foundation for customer intelligence and evidence-based retention planning.

The historical analysis is complete, but the predictive models require further independent validation before operational deployment. Experimental monetary-value predictions are not approved for production reporting.


**## Key Business Findings**

The final customer intelligence analysis covers 78,100 historical customers and combines purchasing behaviour, repeat-purchase propensity, and observed merchandise value.

**### 1. Customer Retention Remains Low**

- 78,100 customers were included in the historical reporting population.
- 1,589 customers made a qualifying repeat purchase within 60 days.
- The observed 60-day repeat-purchase rate was 2.03%.

This establishes a measurable baseline for understanding customer retention, but does not explain why individual customers return.

**### 2. Initial Customer Spending Does Not Guarantee Repeat Purchasing**

The Higher Value | Low Propensity segment contains:

- 20,931 customers, representing 26.80% of the reporting population.
- An observed 60-day repeat-purchase rate of 1.19%.
- Average observed merchandise value of R$264.28 per customer.

Despite its relatively high observed merchandise value, this segment has a low historical repeat-purchase rate.

**Business implication:** Prioritise investigation into repeat-purchase barriers rather than assuming these customers will respond positively to marketing interventions.

**### 3. Repeat-Purchase Propensity and Customer Value Are Distinct**

The Higher Value | High Propensity segment contains 7,287 customers and recorded:

- A 3.55% observed repeat-purchase rate.
- R$175.70 average observed merchandise value per customer.
- R$5.58 average subsequent 60-day merchandise value per customer.

These findings demonstrate why repeat-purchase propensity and observed monetary value should be considered together, rather than used interchangeably.

**### 4. Observed Merchandise Value Is Not Profitability**

Across the reporting population:

- Initial delivered merchandise value: R$10,395,105.68.
- Subsequent 60-day merchandise value: R$211,295.19.
- Combined observed merchandise value: R$10,606,400.87.

The subsequent-purchase component represents approximately 1.99% of combined observed merchandise value.

These measures do not represent customer lifetime value, contribution margin, or incremental revenue attributable to marketing activity.

**### 5. Retention Experiment Feasibility Is a Significant Constraint**

Using the historical 1.19% repeat-purchase baseline for Higher Value | Low Propensity customers, the sample-size analysis estimated:

| Assumed Relative Improvement | Total Customers Required |
|---|---:|
| 10% | 273,492 |
| 20% | 71,480 |
| 30% | 33,120 |
| 50% | 12,870 |

Assumptions: two-sided test, 5% significance level, 80% statistical power, and equal treatment/control allocation.

These are hypothetical planning scenarios, not predictions of intervention effectiveness.

The historical segment size does not establish the number of customers available for a future experiment.

**## Final Business Recommendations

| Recommendation | Decision |
|---|---|
| Establish a consistent customer performance scorecard | Proceed with descriptive reporting |
| Investigate higher-value, low-propensity customers | Prioritise discovery |
| Test whether targeted engagement generates incremental value | Conditional on experiment feasibility |
| Deploy automated propensity-based targeting | Not yet approved |
| Deploy predicted monetary customer value | Not yet approved |
| Preserve transparent customer and merchandise-value definitions | Proceed with ongoing quality assurance |

**### Final Business Decision**

The Customer Intelligence Platform supports historical customer reporting, customer segmentation, and evidence-based retention planning.

However, historical customer differences do not establish incremental treatment responsiveness.

**The recommended next step is to strengthen customer understanding, validate prospective model reliability, and establish the commercial and statistical feasibility of controlled retention experiments before approving large-scale targeted campaigns.**



**## Power BI Dashboard Preview**

**### Customer Overview**

The Customer Intelligence Platform includes three interactive Power BI dashboards that transform e-commerce transaction data into customer insights. Together, they support customer understanding, repeat-purchase analysis and exploratory retention decision-making.

![Customer Overview Dashboard]\(images/customer_overview\.jpg)

**\*\*Purpose:\*\*** Provide an overview of the customer base, spending patterns and geographic distribution.

**\*\*What the visuals show:\*\***

\- **\*\*KPI cards:\*\*** Summarise total customers, customer spending, repeat customers and repeat-purchase rate.

\- **\*\*Customer distribution by segment:\*\*** Shows the relative size of repeat, high-value one-time and other one-time customer groups.

\- **\*\*Customer spending by segment:\*\*** Compares the total spending contributed by each customer segment.

\- **\*\*Average spending by segment:\*\*** Highlights differences in spending behaviour across customer groups.

\- **\*\*Top 10 states:\*\*** Identifies the geographic markets with the largest customer populations.

**\*\*Business interpretation:\*\*** The dashboard helps distinguish customer volume from customer value, identify where spending is concentrated and highlight customer groups that deserve further investigation.

**### Customer Behaviour & Retention**

![Customer Behaviour and Retention Dashboard]\(images/customer_behaviour_retention.jpg)

**\*\*Purpose:\*\*** Explore historical purchasing behaviour and the factors associated with customers returning to purchase again.

**\*\*What the dashboard helps investigate:\*\***

\- Differences between one-time and repeat purchasers.

\- The timing of subsequent purchases and repeat-purchase behaviour.

\- Customer retention patterns across relevant segments.

\- Potential opportunities for more focused retention analysis.

**\*\*Business interpretation:\*\*** Understanding when customers return and how purchasing behaviour differs can help businesses formulate targeted retention experiments rather than relying on broad, untargeted campaigns.

**### Repeat-Purchase Intelligence Dashboard**

![Repeat-Purchase Intelligence Dashboard]\(images/repeat_purchase_intelligence.jpg)

**\*\*Purpose:\*\*** Combine predictive modelling with historical purchasing behaviour to identify customer groups with different relative likelihoods of repeat purchasing within 60 days.

**\*\*What the visuals show:\*\***

\- **\*\*KPI cards:\*\*** Summarise 78,100 historical customers scored, a 2.03% observed 60-day repeat-purchase rate, 15,620 high-propensity customers and a 3.58% repeat rate within the high-propensity segment.

\- **\*\*Customer distribution by propensity:\*\*** Shows how customers are divided into low (50%), medium (30%) and high (20%) propensity groups.

\- **\*\*Historical repeat-purchase rate by segment:\*\*** Compares observed repeat rates of 1.37%, 2.11% and 3.58% across low-, medium- and high-propensity customers.

\- **\*\*Customer profile heatmap:\*\*** Compares observed repeat-purchase rates across initial spending groups and propensity segments.

\- **\*\*Customer distribution by profile:\*\*** Shows where customer volume is concentrated across combinations of initial spending and propensity.

**\*\*Key business findings:\*\***

The high-propensity segment recorded approximately 2.6 times the historical repeat-purchase rate of the low-propensity segment.

The largest customer profile, **\*\*Higher Value | Low Propensity\*\***, contains 20,931 customers. This group offers an opportunity to investigate barriers to repeat purchasing, although higher initial spending does not necessarily mean higher lifetime value or profitability.

**\*\*Potential business application:\*\*** These insights could help prioritise customer research, design controlled retention experiments and evaluate different engagement strategies.

**\*\*Important limitations:\*\*** The results use historical development data, including customers used during model training. The observed segment differences are descriptive rather than independent validation. Model probabilities also require improved calibration and further testing before being used for operational customer targeting.


**### Customer Value & Decision Intelligence**


![Customer Value and Decision Intelligence Dashboard](images/Customer%20Value%20%26%20Decision%20Intelligence.jpg)

**Purpose:** Integrate customer purchasing behaviour, repeat-purchase propensity, and observed merchandise value to support evidence-based business decisions.

**What the dashboard supports:**

- Comparison of observed merchandise value across customer groups.
- Assessment of customer profiles using initial purchase value and repeat-purchase propensity.
- Identification of customer groups requiring further retention investigation.
- Distinction between historical customer value and predicted future value.
- Exploration of business opportunities without assuming that targeted interventions will increase profitability.

**Business interpretation:**

Customer spending and repeat-purchase propensity provide different perspectives on customer behaviour. Combining them helps identify commercially relevant customer groups and formulate hypotheses for further investigation.

**Important limitation:**

Observed merchandise value is not equivalent to profit or customer lifetime value. Historical customer differences do not establish the incremental impact of retention campaigns.

**---**

**### Dashboard Access**

The interactive Power BI report is available in [\`powerbi/powerbi.pbix\`]\(powerbi/powerbi.pbix). The screenshots above provide a visual preview for reviewers who do not have Power BI Desktop installed.

**---**


**### Current Status

**Status: Historical Customer Intelligence Analysis Complete**

The Customer Intelligence Platform has completed its planned analytical workflow across 12 Jupyter notebooks.

Completed deliverables include:

- PostgreSQL database development and SQL-based customer analysis.
- Reproducible customer feature engineering.
- Repeat-purchase predictive modelling and evaluation.
- Historical customer scoring and segmentation.
- Model reliability and validation assessments.
- Historical customer merchandise-value analysis.
- Experimental predictive customer-value modelling.
- Integration of customer propensity and observed merchandise value.
- Interactive Power BI business intelligence reporting.
- Evidence-based business recommendations and retention experiment feasibility analysis.

The validated historical reporting dataset contains 78,100 customers.

A separate reproducible scoring pipeline successfully generated propensity scores for 76,197 customers, retaining 1,903 customers with an explicit unscored status.

**### Operational Readiness**

The platform is complete as an analytical portfolio project, but it is not approved for automated production targeting.

Further work would require:

- Independent prospective model validation.
- Improved probability calibration and model monitoring.
- Verification of feature availability at the operational decision point.
- Commercial contribution-margin and intervention-cost data.
- Prospective customer eligibility and recruitment estimates.
- Controlled experimentation to establish incremental business impact.

**Final assessment:** The platform provides a defensible foundation for customer understanding, descriptive reporting, and evidence-based retention planning. Operational deployment remains subject to further validation.


**### Data Engineering & SQL**

\- Established the project structure, Git version control and GitHub repository.

\- Imported and validated the Olist e-commerce dataset in PostgreSQL.

\- Developed SQL analyses covering customer spending, segmentation, purchasing frequency and repeat-purchase behaviour.

\- Analysed second-purchase timing, including average and median days between purchases.

**### Customer Feature Engineering**

\- Built a customer-level feature engineering workflow using historical transaction data.

\- Developed customer attributes covering first-order spending, product categories, basket composition, purchase timing and geographic location.

\- Created a 60-day repeat-purchase target with a defined observation window and eligibility criteria.

\- Prepared 78,100 historical customers for scoring and segmentation.


**#### Reproducible Feature Engineering Pipeline**

The customer feature-engineering workflow has been reconstructed as a standalone Python script:

\`scripts/build_customer_features.py\`

The pipeline:

\- Loads and validates five original Olist datasets.

\- Identifies each customer's first recorded order.

\- Applies a 60-day repeat-purchase observation window and an additional 30-day delivery buffer.

\- Excludes customers with uncertain negative repeat-purchase labels.

\- Engineers purchase timing, basket, freight, payment, product-category and geographical features.

\- Compares the reconstructed dataset against the validated reference dataset before exporting results.


**\*\*Run the pipeline\*\***

The pipeline supports two execution modes.

**\*\*Build mode\*\***

Generate customer features directly from the original Olist datasets without requiring the saved reference dataset.

\`\`\`powershell

python scripts/build_customer_features.py --mode build

\`\`\`

Output: \`data/processed/customer_features_built.pkl\`

**\*\*Verify mode\*\***

Reconstruct the features, compare customer identifiers, columns and values against the validated reference dataset, and export only when the comparison passes.

\`\`\`powershell

python scripts/build_customer_features.py --mode verify

\`\`\`

Output: \`data/processed/customer_features_rebuilt.pkl\`

Verify mode requires:

\`data/processed/customer_features_reference.pkl\`

If no execution mode is specified, the script defaults to \`verify\`.

Both modes perform the same upstream data-quality and feature-validation checks.


**\*\*Required inputs\*\***

\- Original Olist CSV files in \`data/\`.

\- Validated reference dataset at \`data/processed/customer_features_reference.pkl\`.

\- Python dependencies listed in \`requirements.txt\`.

The reference dataset is required for the current implementation's comparison and export checks. It must be provided separately if it is not included in the repository.

**\*\*Validated results\*\***

\| Validation metric | Result |

\|---|---:|

\| Customer records | 78,100 |

\| Dataset columns | 29 |

\| Confirmed repeat purchasers | 1,589 |

\| Duplicate customers | 0 |

\| Missing or extra customers | 0 |

\| Columns with value differences | 0 |

The comparison aligns records by customer identifier and checks feature values using a numerical tolerance for floating-point fields.

**\*\*Output\*\***

\`data/processed/customer_features_rebuilt.pkl\`

The pipeline creates this output only after the reference comparison passes. The original feature dataset remains unchanged.

**### Predictive Modelling & Evaluation**

\- Developed a logistic regression baseline for predicting repeat purchases within 60 days.

\- Evaluated alternative approaches, including Random Forest and XGBoost.

\- Compared model performance using ROC-AUC, average precision, Brier score and log loss.

\- Conducted chronological validation and holdout evaluation.

\- Analysed model drivers and explored improvements to missing-value handling and regularisation.

\- Identified limitations in model calibration and generalisation that must be addressed before production deployment.

**### Customer Intelligence & Segmentation**

\- Developed propensity-based customer segmentation for the historical reporting population of 78,100 customers.

\- Independently validated the reproducible scoring pipeline, which successfully scored 76,197 customers and retained 1,903 customers with missing model inputs as unscored.

\- Preserved the distinction between historical dashboard segmentation and the separate reproducible scoring output.

\- Developed low-, medium- and high-propensity customer segments.

\- Combined initial order spending and propensity to create seven customer profiles, including an unknown-value group.

\- Compared observed repeat-purchase behaviour across customer segments.

\- Exported validated customer intelligence datasets in CSV and Parquet formats.

**### PostgreSQL Integration**

\- Developed a reusable Python script to load customer intelligence outputs into PostgreSQL.

\- Successfully loaded 78,100 customer records into \`customer_intelligence_v2\`.

\- Validated record counts, customer uniqueness and propensity-segment metrics using SQL.

\- Preserved the existing Olist database tables.

**### Power BI & Business Intelligence**

\- Developed four Power BI dashboard pages:

  - **\*\*Customer Overview:\*\*** Customer base, spending patterns, segmentation and geographic distribution.

  - **\*\*Customer Behaviour & Retention:\*\*** Historical purchasing behaviour and repeat-purchase analysis.

  - **\*\*Repeat-Purchase Intelligence:\*\*** Propensity segments, customer profiles, observed repeat rates and business insights.

- **\*\*Customer Value & Decision Intelligence:** Observed merchandise value, customer profiles, and evidence-based business decision support.

\- Integrated the historical customer intelligence dataset directly from PostgreSQL.

\- Added interactive reporting, KPIs, customer profile comparisons and a repeat-purchase heatmap.

\- Documented business implications and model limitations.



**---**

**## Future Validation and Production Roadmap**

**### Model Reliability & Validation**

\- Improve probability calibration to ensure predicted repeat-purchase likelihoods better reflect observed outcomes.

\- Evaluate model stability across customer cohorts, product categories and purchasing periods.

\- Establish stronger out-of-time validation using new, independently held-out data.

\- Investigate potential data leakage and confirm feature availability at the intended prediction point.

### Monetary Value Modelling and Commercial Validation
Historical customer merchandise-value analysis and experimental predictive monetary-value modelling have been completed.

Future development should focus on:

- Independently validating monetary-value predictions on future customer cohorts.
- Evaluating prediction accuracy against appropriate business benchmarks.
- Establishing reliable contribution-margin and customer acquisition-cost measures.
- Investigating whether monetary-value predictions improve commercial decisions.
- Introducing predictive monetary-value estimates into operational reporting only after sufficient validation.

Observed merchandise value must remain distinct from predicted customer value, profitability, and customer lifetime value.


**### Retention Strategy & Decision-Making**

\- Translate customer segments into testable retention strategies.

\- Investigate why customers with higher initial spending may not return.

\- Develop hypotheses for personalised customer engagement.

\- Design controlled experiments to measure whether targeted interventions improve repeat purchasing.

**### Platform Engineering & Reproducibility**

\- Improve automation of data preparation, feature engineering and customer scoring.

\- Introduce automated data quality checks and model monitoring.

\- Enhance documentation, dependency management and reproducibility.

\- Explore containerisation using Docker and automated testing through GitHub Actions.


**#### Reproducible Customer Scoring Pipeline**

The customer-scoring workflow is implemented in:

\`scripts/score_customers.py\`

It uses the reconstructed customer features and an existing fitted logistic regression pipeline to generate historical 60-day repeat-purchase probabilities.

**\*\*Run the scoring pipeline\*\***

From the project root directory:

\`\`\`powershell

python scripts/build_customer_features.py --mode build

python scripts/score_customers.py

\`\`\`

**\*\*Required inputs\*\***

\- \`data/processed/customer_features_built.pkl\`

\- \`models/repeat_purchase_logistic_regression.joblib\`

\- Python dependencies listed in \`requirements.txt\`

The saved model includes fitted preprocessing and expects nine customer features. The scoring script selects these features using the model's recorded input schema.

**\*\*Validated scoring results\*\***

\| Metric | Result |

\|---|---:|

\| Total customers | 78,100 |

\| Successfully scored | 76,197 |

\| Not scored due to missing model inputs | 1,903 |

\| Missing probabilities among scored customers | 0 |

\| Duplicate customer identifiers | 0 |

Customers with incomplete model inputs are retained with a missing probability and an explicit scoring status. No default probability is assigned.

**\*\*Output\*\***

\`data/processed/customer_scoring_output.pkl\`

The output contains:

\- \`customer_unique_id\`

\- \`order_id\`

\- \`repeat_purchase_propensity\`

\- \`scoring_status\`

The script validates probability ranges, customer uniqueness, scoring coverage and the saved output.

**\*\*Scope and limitations\*\***

These scores describe historical customers. Running the scoring pipeline does not retrain the model or provide new evidence of predictive performance.

The workflow is intended for reproducible analysis and integration, not live production decisioning.


**### Business Intelligence & Reporting**

\- Enhance Power BI reporting with customer lifetime value and additional commercial KPIs.

\- Improve dashboard navigation, filtering and customer segment comparisons.

\- Develop reporting to track model performance and customer behaviour over time.

\- Support clearer business recommendations through actionable insights.

**### Long-Term Vision**

Evolve the Customer Intelligence Platform from a historical analytics and predictive modelling prototype into a reliable customer decision-support system.

The long-term goal is to help businesses understand customer behaviour, estimate future customer value, identify retention opportunities and evaluate personalised engagement strategies through measurable business outcomes.

**---**

**## Technologies Used**

**### Programming & Data Analysis**

\- **\*\*Python:\*\*** Data processing, customer analysis, feature engineering and predictive modelling.

\- **\*\*Pandas & NumPy:\*\*** Data manipulation, transformation and numerical analysis.

\- **\*\*SQL:\*\*** Customer behaviour analysis, segmentation and data validation.

**### Database & Data Engineering**

\- **\*\*PostgreSQL 17:\*\*** Relational database for storing and analysing customer transactions and intelligence outputs.

\- **\*\*SQLAlchemy & psycopg2:\*\*** Python integration with PostgreSQL.

\- **\*\*Parquet & CSV:\*\*** Data storage and analytical exports.

**### Machine Learning**

\- **\*\*Scikit-learn:\*\*** Logistic regression, Random Forest, preprocessing, model evaluation and hyperparameter tuning.

\- **\*\*XGBoost:\*\*** Alternative repeat-purchase prediction modelling.

\- **\*\*Joblib:\*\*** Saving and loading trained machine learning models.

\- **\*\*Model explainability:\*\*** Logistic regression feature-contribution analysis.

**### Data Visualisation & Business Intelligence**

\- **\*\*Power BI Desktop:\*\*** Interactive customer intelligence dashboards and business reporting.

\- **\*\*Matplotlib:\*\*** Exploratory data analysis and model visualisations.

\- **\*\*Seaborn:\*\*** Statistical data visualisation.

**### Development & Version Control**

\- **\*\*Visual Studio Code:\*\*** Development environment.

\- **\*\*Jupyter Notebooks:\*\*** Exploratory analysis, modelling and evaluation workflows.

\- **\*\*Git & GitHub:\*\*** Version control, documentation and project management.

**### Technologies Planned for Future Development**

\- **\*\*Docker:\*\*** Containerisation and reproducible environments.

\- **\*\*GitHub Actions:\*\*** Automated testing and continuous integration.

\- **\*\*Model monitoring:\*\*** Performance tracking, data quality monitoring and scoring reliability.

**## Author**

**\*\*Esther A\*\***
