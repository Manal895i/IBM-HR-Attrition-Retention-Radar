# Power BI build guide

## 1. Load and clean
1. **Home → Get data → Text/CSV**, choose the CSV in `data/`, click **Transform Data**.
2. In Power Query, rename the query to `HR`.
3. Remove the constant columns **EmployeeCount**, **Over18**, **StandardHours**.
4. **Close & Apply**.

## 2. Add the DAX
Paste each item from [`DAX_Measures.dax`](DAX_Measures.dax) with **New measure** or **New column**. Format Attrition Rate as a percentage.

## 3. Pages

| Page | Visuals |
|---|---|
| Overview | Cards (Total Employees, Attrition Count, Attrition Rate, Attrition Cost), donut by Attrition, bars by Department and JobRole, slicers for Department and Gender |
| Why People Leave | Columns by OverTime, Age Group, Income Band, BusinessTravel, MaritalStatus (all Attrition Rate) |
| Satisfaction and Tenure | Columns by JobSatisfaction, WorkLifeBalance, EnvironmentSatisfaction; line chart of Attrition Count by YearsAtCompany; matrix Department x Tenure Band |

## 4. Polish
- **View → Themes** for one palette. Use coral for leavers, teal for stayers to match the web dashboard.
- Add titles, align visuals, hide the filter pane if not needed.
- Turn on **Display units: None** for cards.

## 5. Save
Save as `powerbi/HR-Attrition-Dashboard.pbix`, export each page as a screenshot into `docs/images/`.
