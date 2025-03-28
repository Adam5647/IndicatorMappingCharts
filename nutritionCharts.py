#!/usr/bin/env python3

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

def show_nutrition_dashboard():
    st.title("Nutrition Data Visualization")

    # Hardcoded nutrition data
    raw_data = """Catergory\tIndicator\tcollected by\tprimary collection method\tsecondary collection method\tFrequency\tInstrument Used\tRemark
Anthropometric Indicators\tHeights\tAnganwadi Worker (ANW)\tPoshan Tracker (PT)\tMonthly Progress Report (MPR)\tMonthly\tGrowth Monitoring Device\t
Anthropometric Indicators\tWeight\tANW\tPT\tMPR\tMonthly\tGrowth Monitoring Device\t
Anthropometric Indicators\tBMI\tANW\tPT\tMPR\tMonthly\tReflects through PT Calculator\t
Anthropometric Indicators\tMid-Upper Arm Circumference\t\t\t\t\t\tNot in use anymore
Anthropometric Indicators\tWeight for Age Ratio\tANW\tPT\tMPR\tMonthly\tGrowth Monitoring Device\t
Anthropometric Indicators\tHeight for Age Ratio\tANW\tPT\tMPR\tMonthly\tGrowth Monitoring Device\t
Prevalance on Malnutrition\tStunting\tANW\tPT\tMPR\tMonthly\tGrowth Monitoring Device\t
Prevalance on Malnutrition\tWasting\tANW\tPT\tMPR\tMonthly\tGrowth Monitoring Device\t
Prevalance on Malnutrition\tUnderweight \tANW\tPT\tMPR\tMonthly\tGrowth Monitoring Device\t
Prevalance on Malnutrition\tSevere Acute Malnitrition (SAM)\tANW\tPT\tMPR\tMonthly\tGrowth Monitoring Device\t
Prevalance on Malnutrition\tModerate Acute Malnutrition (MAM)\tANW\tPT\tMPR\tMonthly\tGrowth Monitoring Device\t
Prevalance on Malnutrition\tAdoloscent Malnitrition Rates\t\t\t\t\t\tNot in practice much. Only when anemia testing is done
Micronutrition Deficiencies\tAnemia Prevalence\t\t\t\t\tKit given to test. But not always in use.\tRecord given through Health
Micronutrition Deficiencies\tIron & Folic Deficiency\t\t\t\t\t\tRecord given through Health
Micronutrition Deficiencies\tVitamin A & Iodine Deficiencies\t\t\t\t\t\tRecord given through Health
Pregnancy and Maternal Nutrition \tLow Birth Weight\tANW\tPT\tMPR\tMonthly\tGrowth Monitoring Device\t
Pregnancy and Maternal Nutrition \tMaternal Weight Gain\t\t\tMPR\t\t\tMostly done with Health
Pregnancy and Maternal Nutrition \tAntenatal Care\tANW\tPT\tMPR\tMonthly\t4 ANC Visit as Mandated\tMostly done with Health
Pregnancy and Maternal Nutrition \tMaternal Anemia\t\t\t\t\t\tMostly done with Health
Infant and Child Feeding\tExclusive Breastfeeding\tANW\tPT\tMPR\tMonthly\t\tMostly through MPR
Infant and Child Feeding\tComplementary Breastfeeding\tANW\tPT\tMPR\tMonthly\t\tMostly through MPR
Infant and Child Feeding\tTimely initiation of Breastfeefing\tANW\tPT\tMPR\tMonthly\t\tMostly through MPR
Infant and Child Feeding\tMinimum Acceptable Diet (MAD)\t\t\t\t\t\tNot there in tracker
Nutrition Status of School-Aged Children\tNutritional Intake & Diversity\tANW\tPT\tMPR\tMonthly\t\tDone with Education 
Nutrition Status of School-Aged Children\tAttendance & Nutrition Support in School\tANW\tPT\tMPR\tMonthly\t\tDone with Education 
Nutrition Status of School-Aged Children\tPrevalence of Overweight and Obesity\tANW\tPT\tMPR\tMonthly\t\t
Nutrition Intake\tDietary Diversity Scores\t\t\t\t\t\tNothing collected 
Nutrition Intake\tPer capita Calorie Intake\tANW\t\tMPR\tMonthly\t\tDone manually through Lady Supervisor
Nutrition Intake\tMicronutrient Intake\tANW\t\tMPR\tMonthly\t\tNot good on PT, too complicated for ANW
Nutrition Intake\tConsumption of Fortified Foods\tANW\t\tMPR\tMonthly\t\tNot good on PT, too complicated for ANW
Food Security and Accessibility\tHousehold Food Security\tPDS\t\t\t\t\t
Food Security and Accessibility\tPDS Coverage\tPDS\t\t\t\t\t
Food Security and Accessibility\tAdequacy of Food Rations\tPDS\t\t\t\t\t
Food Security and Accessibility\tFood Assistance\tPDS\t\t\t\t\t
Health and Sanitation Indicators\tDiarrhea Prevalence\t\t\t\t\tOnly counseling\tMostly done with Health
Health and Sanitation Indicators\tAccess of Clean Water and Toilets\tANW\tPT\tMPR\tMonthly\t\t
Health and Sanitation Indicators\tStunting and Wasting due to Infections\tANW\tPT\tMPR\tMonthly\t\t
Nutrition Education and Awareness\tBehavior Change Programmes\tANW\tPT\tMPR\tMonthly\t\tCommunity based programme
Nutrition Education and Awareness\tOther Social Schemes for IEC\tANW\tPT\tMPR\tMonthly\t\tPBPB, PMMVY, Poshan Abhiyan
Nutrition Scheme Monitoring\tPOSHAN, MDM Scheme\t\t\t\t\t\tDone by Education Department
Nutrition Scheme Monitoring\tICDS,Anganwadi Centres & Supplementary Nutrition Programmes\tANW\tPT\tMPR\tMonthly\t\t
Nutrition Scheme Monitoring\tIndigenous Community Nutrition Programmes\t\t\t\t\t\tSelection is centralised here so this doesn't work
Large-Scale Surveys\tNFHS, NNMB,CNNS, MICS\tHealth\t\t\t\t\tRecord given through Health
Large-Scale Surveys\tHMIS, Poshan Tracker, Anemia Mukt Bharat\tANW\tPT\tMPR\tMonthly\t\tMostly done with Health
"""

    df = parse_data(raw_data)
    st.markdown("### Full Nutrition Dataset")
    st.dataframe(df)
    
    # ---------- Custom Chart with aggregator logic and bar mode/orientation ----------
    df["count"] = 1
    st.markdown("## Custom Nutrition Chart")

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

    custom_title = st.text_input("Chart Title", value="Custom Nutrition Chart")
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

    # Category-wise analysis
    categories = df["Catergory"].unique().tolist()
    if not categories:
        st.warning("No categories found in the data!")
        return

    st.markdown("## Category-wise Analysis")
    tabs = st.tabs(categories)
    for i, cat in enumerate(categories):
        with tabs[i]:
            st.subheader(f"Category: {cat}")
            subset = df[df["Catergory"] == cat]
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
                collected_counts = subset["collected by"].value_counts().reset_index()
                collected_counts.columns = ["collected by", "Count"]
                fig2 = px.bar(
                    collected_counts,
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
            file_name="nutrition_chart.png",
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
        file_name="nutrition_data.xlsx",
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
