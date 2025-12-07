# IS-6813: MSBA Capstone
## Table of Contents
- [Individual Notebooks](#individual-notebooks)
- [Summary of Business Problem and Project Objective](#summary-of-business-problem-and-project-objective)
 	+ [Business Problem Statement](#business-problem-statement)
	+ [Project Objective](#project-objective)
- [Group 4 Solution to the Business Problem](#group-4-solution-to-the-business-problem)
- [Individual Contribution to the Project](#individual-contribution-to-the-project)
- [The Business Value of the Solution](#the-business-value-of-the-solution)
- [Difficulties Encountered](#difficulties-encountered)
- [Project Learnings](#project-learnings)

## Individual Notebooks
| Notebook Title  | About | Link |
| :---: | :---: | :---: |
| IS 6813 EDA Assignment | Initial Exploratory Data Analysis (EDA) of SWIRE Coca-Cola data| [IS 6813 EDA Assignment.Rmd](https://github.com/thaitlia/IS6813/blob/main/IS%206813%20EDA%20Assignment.Rmd) |
| Additional EDA Notes| Testing computational abilities of Python with data | [additional EDA notes.py ](https://github.com/thaitlia/IS6813/blob/main/additional%20EDA%20notes.py)|
| EDA Python Revised 2 | Script calculating abandoned cart proportion and producing final file to use for modeling stage | [EDA Python Revised 2.py](https://github.com/thaitlia/IS6813/blob/main/EDA%20Python%20Revised%202.py)|
| IS 6813 Modeling Assignment 2 | Individual contribution to modeling for success metric 4 | [IS 6813 Modeling Assignment 2.py](https://github.com/thaitlia/IS6813/blob/main/IS%206813%20Modeling%20Assignment%202.Rmd) |

## Summary of Business Problem and Project Objective
### Business Problem Statement
Swire Coca-Cola’s MyCoke360 ordering platform has been experiencing cases of cart abandonment from their customers, defined as when customers add products to their cart but fail to complete their orders by their next order date. This customer behavior could be contributing to lost revenue and operational inefficiencies. Repeated abandonment may signal a deeper issue such as pricing concerns or misalignment with customer needs. Leadership requires a clear understanding of the drivers of cart abandonment and once identified, provide a recommendation of recovery in order to improve financial and portfolio impact and prioritize interventions that reduce revenue leakage.

### Project Objective
Due to the large dataset containing various features of customer order history and descriptions, a classification model will be implemented to predict the likelihood that a customer will abandon their cart on MyCoke360. A classification model also allows for pattern recognition in order to determine the top key predictors when analyzing the habits of customer cart abandonment. The modeling will seek to fulfill set success metrics as outlined: measure success by tracking reductions in abandonment rate, increases in recovery rate, incremental revenue from prevented abandonment, and identification of at-risk packages. Evaluate whether abandonment patterns highlight portfolio risks requiring adjustments to package mix, pricing, or availability. After initial evaluation, identify areas of weakness in the model and revise - possibly include A/B testing where the new model is compared to older models to see if improvements were made in terms of strength of prediction.

## Group 4 Solution to the Business Problem
After different simulations, logistic regression, and RandomForest classifications, ultimately, Group 4's solution to the business problem was a recommendation to SWIRE to launch a reminder campaign for customers nearing their order-by date for each order window.

1. Automated Email Reminders: Sending out an email reminder to complete cart check out on the busiest cart abandonment day
2. Sales Follow-Up Calls: For customers that have high-potential revenue loss due to repeated abandoned carts, specifically those that meet the 0.5 probability threshold
3. SMS Notification: Send out a SMS notification stating “Your cart is waiting! Complete your MyCoke360 order today to ensure it’s delivered on your upcoming route ” daily before order window closes

## Individual Contribution to the Project
I took the lead on most assignments to schedule times on when to meet and what needs to be done by the next due date. In order to make sure we were submitting quality work, I'd be the one to finalize the RMarkdown documents, read through them to make them sound cohesive, and appended everyone's data in a coherent manner. I also reached out whenever we needed an extension and submitted the assignments. I'd say my biggest contribution, however, was completing the code to calculate the abandoned cart proportion as accurately as possible. While each team member did attempt to get to a better proportion, a large part of re-calculation and re-editing the code was done by myself and it took several for loops, functions, etc. to get the customer based sample, order-by window schedule, and transactional log concatenation right to be able to use for the modeling assignment. 

## The Business Value of the Solution
Analyzing why customers are abandoning their cart and the root causes will allow Swire Coca-Cola to predict customers that are most at risk of cart abandonment and implement strategies to combat the issue as a preventative measure. Benefits may include increased revenue from higher order completion rates, improved customer satisfaction with the ordering platform allowing call center agents to focus more on selling than taking orders, and identifying at-risk packages to create a strong portfolio.

## Difficulties Encountered
The greatest difficulty was finding the abandoned cart proportion rate. There were a lot of transactions recorded in the google analytics data SWIRE provided given that the data was for a whole year, along with customer profile, order, and sales information - it proved to be a challenge matching it all up in one succinct file to use for modeling. That and parsing through the data was initially confusing because there were multiple routes one could take in terms of analyzing, which we ended up doing a customer-based analysis and pulling up all individual records from the google analytics table to base off of. 

## Project Learnings
This Captone project is the penultimate of the MSBA program at the University of Utah, from all the data processing, modeling, and clean-up learned throughout the different courses, these skills were put to the test using real-world data and an actual business objective. Time and time again, real world data is nothing like 'mtcars' where each row and record is perfectly written out. There were a lot of transactional logs made by customers in all the datasets, and our biggest learning was how to balance sampling and computation time. With many projects, there is a deadline in order to meet goals for the year and this was no different. Given how much data we had access too, we had to balance sampling rates and modeling times in order to produce a business recommendation. For the future, we could have made better samples based on demographics from our initial EDA, as well as try other modeling techniques as demonstrated by other groups in the course. 
