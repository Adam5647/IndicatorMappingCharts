#!/usr/bin/env python3

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

def show_health_dashboard():
    st.title("Health Data Visualization")

    # Hardcoded health data
    raw_data = """Category\tIndicator\tCollected by\tprimary collection method\tsecondary collection method\tFrequency\tInstrument Used\tRemark
Demographic Indicators\tPopulation size and growth rate\t\t\t\t\t\t
Demographic Indicators\tBirth rate (Crude birth rate)\tASHA\tHouse visit + MPR\tHMIS\tBi Annual (Feb-Mar & Sep-Oct)\t\tHouse Visit happen on Demand
Demographic Indicators\tDeath rate (Crude death rate)\tASHA\tHouse visit + MPR\tHMIS\tBi Annual (Feb-Mar & Sep-Oct)\t\tHouse Visit happen on Demand
Demographic Indicators\tInfant mortality rate (IMR)\tASHA\tHouse visit + MPR\tHMIS\tBi Annual (Feb-Mar & Sep-Oct)\t\tHouse Visit happen on Demand
Demographic Indicators\tNeonatal mortality rate\tASHA\tHouse visit + MPR\tHMIS\tBi Annual (Feb-Mar & Sep-Oct)\tWeighing Scale. With ANW\tHouse Visit happen on Demand
Demographic Indicators\tUnder-five mortality rate (U5MR)\tASHA + ANM\tHouse visit + MPR\tHMIS\tBi Annual (Feb-Mar & Sep-Oct)\tWeighing Scale. With ANW\tHouse Visit happen on Demand
Demographic Indicators\tMaternal mortality ratio (MMR)\tASHA + ANM\tHouse visit + MPR\tHMIS\tBi Annual (Feb-Mar & Sep-Oct)\t\tHouse Visit happen on Demand
Demographic Indicators\tLife expectancy at birth\t\t\tHMIS\t\t\t
Demographic Indicators\tFertility rate (Total fertility rate)\tASHA\tHouse visit + MPR\tHMIS\tBi Annual (Feb-Mar & Sep-Oct)\t\tHouse Visit happen on Demand
Demographic Indicators\tSex ratio (Male to female ratio)\tASHA\tHouse visit + MPR\tBirths and Dealth Registration\tBi Annual (Feb-Mar & Sep-Oct)\t\tHouse Visit happen on Demand
Demographic Indicators\tAge structure (Percentage of population by age groups)\tASHA\tHouse visit + MPR\tHMIS\tBi Annual (Feb-Mar & Sep-Oct)\t\tHouse Visit happen on Demand
Demographic Indicators\tDependency ratio (Proportion of the working-age population to dependents)\tASHA\tHouse visit + MPR\t\tBi Annual (Feb-Mar & Sep-Oct)\t\tHouse Visit happen on Demand
Demographic Indicators\tMigration rate (Internal and external migration)\tASHA\tHouse visit + MPR\t\tBi Annual (Feb-Mar & Sep-Oct)\t\tHouse Visit happen on Demand
Health and Mortality Indicators\tCause-specific mortality rates (e.g., mortality from communicable diseases, non-communicable diseases, injuries)\tASHA + ANM\tHouse visit + MPR\tHMIS & Births and Deaths\tMonthly \tNCD - BP & Gluco Metre\tHouse Visit happen on Demand
Health and Mortality Indicators\tPrevalence of major diseases (e.g., tuberculosis, malaria, HIV/AIDS, diabetes)\tASHA + ANM\tHouse visit + MPR\tHMIS \tMonthly \tNCD - BP & Gluco Metre\t"House Visit happen on Demand

Identifying by ASHA and Screening by Lab Tech at HC"
Health and Mortality Indicators\tIncidence of communicable diseases (e.g., diarrheal diseases, dengue, cholera)\tASHA \tHouse visit + MPR\tHMIS \tMonthly \t\tHouse Visit happen on Demand
Health and Mortality Indicators\tLife expectancy at age 60 (Healthy life expectancy)\tASHA \tHouse visit + MPR\t\tMonthly \t\tHouse Visit happen on Demand
Health and Mortality Indicators\tPrevalence of undernutrition (e.g., stunting, wasting)\tANW\t\t\t\t\t
Health and Mortality Indicators\tChildhood vaccination rates (e.g., BCG, polio, measles)\tASHA \tHouse visit + MPR\tHMIS\tMonthly \t\tHouse Visit happen on Demand
Health and Mortality Indicators\tImmunization coverage rate\tASHA \tHouse visit + MPR\tHMIS \tMonthly \t\t"House Visit happen on Demand

Under the supervision of the ANM"
Health and Mortality Indicators\tDisease-specific burden (DALYs - Disability-Adjusted Life Years)\tASHA \tHouse visit + MPR\t\tMonthly \t\t"House Visit happen on Demand 

Identifying by ASHA and Screening by Lab Tech at HC"
Health and Mortality Indicators\tPrevalence of non-communicable diseases (NCDs: hypertension, heart disease, cancer)\tASHA \tHouse visit + MPR\tNCD Portal\tMonthly \t\t"House Visit happen on Demand 

Identifying by ASHA and Screening by Lab Tech at HC"
Health and Mortality Indicators\tPrevalence of mental health disorders\tASHA \tHouse visit + MPR\tDMHP\tMonthly \t\t"House Visit happen on Demand

Identifying by ASHA and Screening by Doctor at SC"
Reproductive and Maternal Health Indicators\tAntenatal care coverage\tASHA \tHouse visit + MPR\tHMIS\tMonthly \t\tHouse Visit happen on Demand
Reproductive and Maternal Health Indicators\tInstitutional delivery rate\tASHA \tHouse visit + MPR\tHMIS\tMonthly \t\tHouse Visit happen on Demand
Reproductive and Maternal Health Indicators\tSkilled birth attendance rate\t\t\tHMIS\t\t\tNot done
Reproductive and Maternal Health Indicators\tPostnatal care coverage\tASHA \tHouse visit + MPR\tHMIS\tMonthly \t\tHouse Visit happen on Demand
Reproductive and Maternal Health Indicators\tPercentage of deliveries with cesarean sections\tASHA \tHouse visit + MPR\tHMIS\tMonthly \t\tHouse Visit happen on Demand
Reproductive and Maternal Health Indicators\tPercentage of adolescent pregnancies\tASHA \tHouse visit + MPR\tHMIS\tMonthly \t\tHouse Visit happen on Demand
Reproductive and Maternal Health Indicators\tFamily planning use rate (contraceptive prevalence rate)\tASHA \tHouse visit + MPR\tHMIS\tMonthly \t\tHouse Visit happen on Demand
Reproductive and Maternal Health Indicators\tTeenage fertility rate\tASHA \tHouse visit + MPR\tHMIS\tMonthly \t\tHouse Visit happen on Demand
Reproductive and Maternal Health Indicators\tPercentage of women receiving iron and folic acid supplementation\tASHA \tHouse visit + MPR\tHMIS\tMonthly \t\tHouse Visit happen on Demand
Reproductive and Maternal Health Indicators\tPercentage of women with anemia\tASHA \tHouse visit + MPR\tHMIS\tMonthly \t\tHouse Visit happen on Demand
Reproductive and Maternal Health Indicators\tMaternal morbidity (e.g., eclampsia, hemorrhage)\tASHA \tHouse visit + MPR\tHMIS\tMonthly \t\tHouse Visit happen on Demand
Reproductive and Maternal Health Indicators\tAccess to safe abortion services\t\t\tHMIS\t\t\tCollected through ASHA and referred to HC
Child Health Indicators\tExclusive breastfeeding rate\tASHA \tHouse visit + MPR\tHMIS\tMonthly \t\tHouse Visit happen on Demand
Child Health Indicators\tInfant and young child feeding practices\tASHA \tHouse visit + MPR\t\tMonthly \t\tHouse Visit happen on Demand
Child Health Indicators\tImmunization coverage (e.g., DTP, hepatitis B, MMR)\tASHA \tHouse visit + MPR\tHMIS\tMonthly \t\tHouse Visit happen on Demand
Child Health Indicators\tPrevalence of malnutrition (e.g., underweight, stunting, wasting)\tASHA \tHouse visit + MPR\t\tMonthly \t\tHouse Visit happen on Demand
Child Health Indicators\tVitamin A supplementation rate\tASHA \tHouse visit + MPR\tHMIS\tMonthly \t\tHouse Visit happen on Demand
Child Health Indicators\tPrevalence of anemia in children\tASHA \tHouse visit + MPR\t\tMonthly \t\tHouse Visit happen on Demand
Child Health Indicators\tEarly childhood development indicators\tASHA \tHouse visit + MPR\t\tMonthly \t\tHouse Visit happen on Demand
Child Health Indicators\tInfant and child vaccination dropout rates\tASHA \tHouse visit + MPR\tHMIS\tMonthly \t\tHouse Visit happen on Demand
Nutrition Indicators\tUndernutrition (stunting, wasting, underweight)\tASHA + ANW\tHouse visit + MPR\t\tMonthly \t\t"House Visit happen on Demand

BMI screening by HC"
Nutrition Indicators\tMicronutrient deficiencies (e.g., Vitamin A, iron, iodine)\tASHA + ANW\tHouse visit + MPR\tHMIS\tMonthly \t\t"House Visit happen on Demand

BMI screening by HC"
Nutrition Indicators\tOverweight and obesity prevalence\tASHA + ANW\tHouse visit + MPR\t\tMonthly \t\t"House Visit happen on Demand

BMI screening by HC"
Nutrition Indicators\tDietary intake patterns (e.g., fruit, vegetable, and protein consumption)\tASHA + ANW\tHouse visit + MPR\t\tMonthly \t\t"House Visit happen on Demand

BMI screening by HC"
Nutrition Indicators\tAccess to clean water and sanitation\tASHA + ANW\tHouse visit + MPR\t\tMonthly \t\t"House Visit happen on Demand

BMI screening by HC"
Nutrition Indicators\tHousehold food security\tASHA + ANW\tHouse visit + MPR\t\tMonthly \t\t"House Visit happen on Demand

BMI screening by HC"
Nutrition Indicators\tPercentage of households with access to fortified foods\tASHA + ANW\tHouse visit + MPR\t\tMonthly \t\t"House Visit happen on Demand

BMI screening by HC"
Nutrition Indicators\tFoodborne diseases\tASHA + ANW\tHouse visit + MPR\t\tMonthly \t\t"House Visit happen on Demand

BMI screening by HC"
Environmental Health Indicators\tAir quality index (PM2.5, PM10 levels)\t\t\tState Pollution Control Board\t\t\tNot Done
Environmental Health Indicators\tAccess to safe drinking water (Percentage of households with access to piped water)\tASHA\tHouse visit + MPR\t\tYearly\t\t"House Visit happen on Demand

Collected through CBAC"
Environmental Health Indicators\tAccess to sanitation facilities (Percentage of households with toilets)\tASHA\tHouse visit + MPR\t\tYearly\t\t"House Visit happen on Demand

Collected through CBAC"
Environmental Health Indicators\tWaste management (Waste segregation, disposal, and recycling rates)\tASHA\tHouse visit + MPR\t\tYearly\t\t"House Visit happen on Demand

Collected through CBAC"
Environmental Health Indicators\tMalaria vector control measures (e.g., bed nets, indoor spraying)\tASHA\tHouse visit + MPR\tDistrict Vector Borne Disease Control Programme\tYearly\t\t"House Visit happen on Demand

Collected through CBAC"
Environmental Health Indicators\tIndoor air pollution (Use of biomass fuels, solid fuels)\tASHA\tHouse visit + MPR\t\tYearly\t\t"House Visit happen on Demand

Collected through CBAC"
Environmental Health Indicators\tAccess to clean cooking fuels (LPG, biogas)\tASHA\tHouse visit + MPR\t\tYearly\t\t"House Visit happen on Demand

Collected through CBAC"
Environmental Health Indicators\tVector-borne diseases prevalence (Dengue, malaria, chikungunya)\tASHA\tHouse visit + MPR\tDistrict Vector Borne Disease Control Programme\tYearly\t\t"House Visit happen on Demand

Referred to HC"
Environmental Health Indicators\tWaterborne diseases prevalence (e.g., cholera, typhoid)\tASHA\tHouse visit + MPR\tIDSP\tYearly\t\t"House Visit happen on Demand

Referred to HC"
Environmental Health Indicators\tFloods and natural disaster mortality rates\t\t\tDisaster Mangement\t\t\tNot Done in State
Environmental Health Indicators\tSoil contamination and pesticide use\t\t\tAgri\t\t\tNot Done in State
Health Infrastructure and Service Access\tNumber of healthcare facilities (Primary health centers, sub-centers, district hospitals, etc.)\tDMHO\tPhysically Collected\t\tReal Time\t\tCollected at the District Level
Health Infrastructure and Service Access\tHealth facility utilization rate\tDMHO\tHMIS\t\tReal Time\t\tCollected at the District Level
Health Infrastructure and Service Access\tAvailability of medical staff (Doctors, nurses, specialists)\tDMHO\tPhysically Collected\t\tReal Time\t\tCollected at the District Level
Health Infrastructure and Service Access\tHealth expenditure per capita\tDMHO\tFinance\t\tReal Time\t\tCollected at the District Level
Health Infrastructure and Service Access\tPublic health insurance coverage (e.g., Ayushman Bharat)\tDMHO\tMHIS\t\tReal Time\t\tCollected at the District Level
Health Infrastructure and Service Access\tAvailability of essential medicines\tDMHO\tMMDSL\t\tReal Time\t\tCollected at the District Level
Health Infrastructure and Service Access\tAccess to mental health services\tDMHO\tDMHP\t\tReal Time\t\tCollected at the District Level
Health Infrastructure and Service Access\tTelemedicine services usage\tDMHO\tEsaanjeevani\t\tReal Time\t\tCollected at the District Level
Health Infrastructure and Service Access\tAccess to diagnostic services\tDMHO\tMMDSL\t\tReal Time\t\tCollected at the District Level
Health Infrastructure and Service Access\tAvailability of emergency medical services (EMS)\tDMHO\tMMDSL\t\tReal Time\t\tCollected at the District Level
Behavioral and Lifestyle Indicators\tPrevalence of smoking and tobacco use\tASHA\tHouse visit + MPR\tNational Tobacco Control Programme\tYearly\t\t"House Visit happen on Demand

Collected through CBAC"
Behavioral and Lifestyle Indicators\tAlcohol consumption rates\tASHA\tHouse visit + MPR\t\tYearly\t\t"House Visit happen on Demand

Collected through CBAC"
Behavioral and Lifestyle Indicators\tPhysical activity levels\tASHA\tHouse visit + MPR\t\tYearly\t\t"House Visit happen on Demand

Collected through CBAC"
Behavioral and Lifestyle Indicators\tPrevalence of drug abuse (e.g., opioid addiction)\tASHA\tHouse visit + MPR\tDMHP\tYearly\t\t"House Visit happen on Demand

Collected through CBAC"
Behavioral and Lifestyle Indicators\tPrevalence of high-risk behaviors (e.g., unsafe sexual practices, substance abuse)\tASHA\tHouse visit + MPR\tDMHP - Substance Abuse\tYearly\t\t"House Visit happen on Demand

Collected through CBAC"
Behavioral and Lifestyle Indicators\tDietary habits (e.g., salt consumption, junk food intake)\tASHA\tHouse visit + MPR\t\tYearly\t\t"House Visit happen on Demand

Collected through CBAC"
Behavioral and Lifestyle Indicators\tMental health and well-being (Depression, anxiety, stress)\tASHA\tHouse visit + MPR\tDMHP\tYearly\t\t"House Visit happen on Demand

Collected through CBAC"
Social Determinants of Health\tEducation level (Literacy rates, school enrollment rates)\t\t\t\t\t\tEducation Department
Social Determinants of Health\tEmployment status (Unemployment rate, workforce participation)\t\t\t\t\t\tLabour Department
Social Determinants of Health\tIncome inequality (e.g., Gini index)\t\t\t\t\t\t
Social Determinants of Health\tSocial safety net program participation (PDS, MGNREGA)\t\t\t\t\t\t
Social Determinants of Health\tHousing conditions (Overcrowding, slum population)\t\t\t\t\t\t
Social Determinants of Health\tGender inequality (Sex-based disparities in healthcare access)\t\t\tPCPNDT Act\t\t\t
Social Determinants of Health\tDisability rates (Prevalence of persons with disabilities)\tANW + SRC\t\t\t\t\t
Social Determinants of Health\tAccess to social services (Welfare programs, public health initiatives)\tANW + SRC\t\t\t\t\t
Social Determinants of Health\tWater, sanitation, and hygiene (WASH) practices\tASHA\tHouse visit + MPR\t\tYearly\t\t"House Visit happen on Demand

Collected through MAS"
Health System Indicators\tHealth insurance coverage rates (Public, private, and universal schemes like Ayushman Bharat)\tHealth Centre (HC)\tMPR\tMHIS\tMonthly\t\t
Health System Indicators\tHealthcare worker availability and distribution (Doctors, nurses per 1000 population)\tHC\tMPR\tDMHO\tMonthly\t\t
Health System Indicators\tMedical equipment availability\tHC\tMPR\tMMDSL\tMonthly\t\t
Health System Indicators\tTelemedicine infrastructure\tHC\tMPR\tDHMO\tMonthly\t\t
Health System Indicators\tReferral systems (Percentage of patients referred from primary to secondary/tertiary care)\tHC\tMPR\t\tMonthly\t\t
Health System Indicators\tReferral delays or obstacles (Access to transport, road infrastructure)\tHC\tMPR\t\tMonthly\t\t
Health System Indicators\tWaiting times for healthcare services\tHC\tMPR\t\tMonthly\t\t
Health and Disability Surveys\tDisability prevalence (Number of persons with disabilities)\tANW\t\tSRC\t\t\t
Health and Disability Surveys\tDisability-adjusted life years (DALYs)\tANW\t\tSRC\t\t\t
Health and Disability Surveys\tQuality of life indices (e.g., for people with chronic conditions)\tASHA\tHouse visit + MPR\t\tMonthly\t\tHouse Visit happen on Demand
Health and Disability Surveys\tChronic disease management\tASHA\tHouse visit + MPR\tNCD\tMonthly\t\tHouse Visit happen on Demand
HIV/AIDS and Tuberculosis\tHIV prevalence (By population group, regions, etc.)\tASHA\tHouse visit + MPR\tMeghalaya Aids Control Society\tMonthly\t\tHouse Visit happen on Demand
HIV/AIDS and Tuberculosis\tTuberculosis (TB) incidence rate\tASHA\tHouse visit + MPR\tDistrict TB Office\tMonthly\t\tHouse Visit happen on Demand
HIV/AIDS and Tuberculosis\tTB treatment success rate\tDistrict Hospital\t\tDistrict TB Office\t\t\t
HIV/AIDS and Tuberculosis\tHIV treatment coverage and adherence\tASHA\tHouse visit + MPR\tMeghalaya Aids Control Society\tMonthly\t\t"House Visit happen on Demand

Referred to Civil Hospital or Ganesh Das"
HIV/AIDS and Tuberculosis\tPrevalence of co-morbidities (TB and HIV)\tASHA\tHouse visit + MPR\tDistrict TB + Meghalaya Aids Control Society\tMonthly\t\t"House Visit happen on Demand

Referred to Civil Hospital or Ganesh Das"
Mental Health Indicators\tPrevalence of mental health disorders\tASHA\tHouse visit + MPR\tDMHP\tMonthly\t\t"House Visit happen on Demand

Referred to HC"
Mental Health Indicators\tAccess to mental health services\tASHA\tHouse visit + MPR\tDMHP\tMonthly\t\t"House Visit happen on Demand

Referred to HC"
Mental Health Indicators\tSuicide rate\tASHA\tHouse visit + MPR\tDMHP\tMonthly\t\t"House Visit happen on Demand

Referred to HC"
Mental Health Indicators\tPsychiatric care facility availability\tASHA\tHouse visit + MPR\tDMHP\tMonthly\t\t"House Visit happen on Demand

Referred to HC"
Mental Health Indicators\tSubstance use disorders\tASHA\tHouse visit + MPR\tDMHP\tMonthly\t\t"House Visit happen on Demand

Referred to HC"
"""

    df = parse_data(raw_data)
    st.markdown("### Full Health Dataset")
    st.dataframe(df)

    # Category-wise analysis
    categories = df["Category"].unique().tolist()
    if not categories:
        st.warning("No categories found in the data!")
        return
    
    # ---------- Custom Chart with aggregator logic and bar mode/orientation ----------
    df["count"] = 1
    st.markdown("## Custom Health Chart")

    chart_type = st.selectbox("Select chart type", ["Bar", "Line", "Pie", "Bar + Line"])
    bar_mode = st.selectbox("Bar Mode (if Bar)", ["group", "stack"])
    bar_orientation = st.selectbox("Bar Orientation (if Bar)", ["vertical", "horizontal"])
    legend_title = st.text_input("Legend Title (optional)", value="Indicator")

    x_col = st.selectbox("X-axis / Names Column", df.columns)
    color_col = st.selectbox("Color Column (optional)", [None] + list(df.columns))

    y_col = None
    if chart_type in ["Bar", "Line", "Pie"]:
        y_col_options = [None] + list(df.columns)
        y_col_choice = st.selectbox("Y-axis/Values Column (optional)", y_col_options, index=0)
        if y_col_choice is not None:
            y_col = y_col_choice
    else:
        y_col_options = [None] + list(df.columns)
        y_col_choice_bar = st.selectbox("Bar Y-axis Column", y_col_options, index=0)
        y_col_choice_line = st.selectbox("Line Y-axis Column", y_col_options, index=0)

    custom_title = st.text_input("Chart Title", value="Custom Health Chart")
    template_choice = st.selectbox("Chart Template", ["plotly_white", "presentation", "ggplot2", "seaborn"])
    color_seq_choice = st.selectbox(
        "Color Sequence",
        ["Plotly", "Set1", "Set2", "Dark2", "Pastel1", "Pastel2", "Viridis", "Cividis"]
    )
    color_seq_map = {
        "Plotly": px.colors.qualitative.Plotly,
        "Set1": px.colors.qualitative.Set1,
        "Set2": px.colors.qualitative.Set2,
        "Dark2": px.colors.qualitative.Dark2,
        "Pastel1": px.colors.qualitative.Pastel1,
        "Pastel2": px.colors.qualitative.Pastel2,
        "Viridis": px.colors.sequential.Viridis,
        "Cividis": px.colors.sequential.Cividis,
    }
    chosen_colors = color_seq_map[color_seq_choice]

    if chart_type == "Bar":
        orientation = "h" if bar_orientation == "horizontal" else "v"
        if y_col is None:
            # aggregator logic
            if color_col:
                grouped = df.groupby([x_col, color_col], as_index=False)["count"].sum()
                fig_custom = px.bar(
                    grouped,
                    x=x_col if orientation == "v" else "count",
                    y="count" if orientation == "v" else x_col,
                    color=color_col,
                    title=custom_title,
                    template=template_choice,
                    color_discrete_sequence=chosen_colors,
                    barmode=bar_mode,
                    orientation=orientation
                )
            else:
                grouped = df.groupby(x_col, as_index=False)["count"].sum()
                fig_custom = px.bar(
                    grouped,
                    x=x_col if orientation == "v" else "count",
                    y="count" if orientation == "v" else x_col,
                    title=custom_title,
                    template=template_choice,
                    color_discrete_sequence=chosen_colors,
                    barmode=bar_mode,
                    orientation=orientation
                )
        else:
            fig_custom = px.bar(
                df,
                x=x_col if orientation == "v" else y_col,
                y=y_col if orientation == "v" else x_col,
                color=color_col,
                title=custom_title,
                template=template_choice,
                color_discrete_sequence=chosen_colors,
                barmode=bar_mode,
                orientation=orientation
            )
        fig_custom.update_layout(
            legend_title_text=legend_title if legend_title else None
        )

    elif chart_type == "Line":
        fig_custom = px.line(
            df,
            x=x_col,
            y=y_col,
            color=color_col,
            title=custom_title,
            template=template_choice,
            color_discrete_sequence=chosen_colors
        )
    elif chart_type == "Pie":
        if y_col:
            fig_custom = px.pie(
                df,
                names=x_col,
                values=y_col,
                color=color_col,
                title=custom_title,
                template=template_choice,
                color_discrete_sequence=chosen_colors
            )
        else:
            counts = df[x_col].value_counts().reset_index()
            counts.columns = [x_col, "Count"]
            fig_custom = px.pie(
                counts,
                names=x_col,
                values="Count",
                title=custom_title,
                template=template_choice,
                color_discrete_sequence=chosen_colors
            )
    else:
        # "Bar + Line"
        fig_custom = go.Figure()
        if y_col_choice_bar:
            fig_custom.add_trace(go.Bar(
                x=df[x_col],
                y=df[y_col_choice_bar],
                name=f"Bar: {y_col_choice_bar}",
                marker_color=chosen_colors[0]
            ))
        if y_col_choice_line:
            fig_custom.add_trace(go.Scatter(
                x=df[x_col],
                y=df[y_col_choice_line],
                mode='lines+markers',
                name=f"Line: {y_col_choice_line}",
                line=dict(color=chosen_colors[1] if len(chosen_colors) > 1 else 'red', width=2)
            ))
        fig_custom.update_layout(
            title=custom_title,
            barmode=bar_mode,
            template=template_choice
        )

    st.plotly_chart(fig_custom, use_container_width=True)

    st.markdown("## Category-wise Analysis")
    tabs = st.tabs(categories)
    for i, cat in enumerate(categories):
        with tabs[i]:
            st.subheader(f"Category: {cat}")
            subset = df[df["Category"] == cat]
            st.dataframe(subset)

            # 1) Indicator Distribution
            st.markdown("**Indicator Distribution**")
            if not subset.empty:
                indicator_counts = subset["Indicator"].value_counts().reset_index()
                indicator_counts.columns = ["Indicator", "Count"]
                fig1 = px.bar(
                    indicator_counts,
                    x="Indicator",
                    y="Count",
                    color="Indicator",
                    title=f"Indicator Count for {cat}",
                    template="plotly_white"
                )
                st.plotly_chart(fig1, use_container_width=True)

            # 2) Collected by Distribution
            st.markdown("**Collected by Distribution**")
            if not subset.empty:
                coll_counts = subset["Collected by"].value_counts().reset_index()
                coll_counts.columns = ["collected by", "Count"]
                fig2 = px.bar(
                    coll_counts,
                    x="collected by",
                    y="Count",
                    color="collected by",
                    title=f"'Collected by' Count for {cat}",
                    template="plotly_white"
                )
                st.plotly_chart(fig2, use_container_width=True)

            # 3) Frequency Distribution
            st.markdown("**Frequency Distribution**")
            if not subset.empty:
                freq_counts = subset["Frequency"].value_counts().reset_index()
                freq_counts.columns = ["Frequency", "Count"]
                fig3 = px.bar(
                    freq_counts,
                    x="Frequency",
                    y="Count",
                    color="Frequency",
                    title=f"Frequency Count for {cat}",
                    template="plotly_white"
                )
                st.plotly_chart(fig3, use_container_width=True)

    # Download
    st.markdown("### Downloads")
    try:
        png_bytes = fig_custom.to_image(format="png")
        st.download_button(
            label="Download chart as PNG",
            data=png_bytes,
            file_name="health_chart.png",
            mime="image/png"
        )
    except Exception as e:
        st.warning("Could not generate PNG. Make sure 'kaleido' is installed.")
        st.error(str(e))

    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False)
    st.download_button(
        label="Download data as Excel",
        data=excel_buffer.getvalue(),
        file_name="health_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

def parse_data(raw_data: str) -> pd.DataFrame:
    lines = raw_data.strip().split("\n")
    header_line = lines[0]
    data_lines = lines[1:]
    col_names = header_line.split("\t")

    rows = []
    for line in data_lines:
        parts = line.split("\t")
        # Ensure exactly 8 columns
        if len(parts) < 8:
            parts += [""] * (8 - len(parts))
        else:
            parts = parts[:8]
        rows.append(parts)

    df = pd.DataFrame(rows, columns=col_names)
    return df
