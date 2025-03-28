#!/usr/bin/env python3

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

def show_agriculture_dashboard():
    st.title("Agriculture Data Visualization")

    # Hardcoded agriculture data
    raw_data = """Category\tIndicator\tCollected by\tprimary collection method\tsecondary collection method\tFrequency\tInstrument Used\tRemark
1. Crop Production & Yield\tArea under cultivation (hectares)\tAPY\tPer Crop\t\t\t
1. Crop Production & Yield\tCrop-wise production (in metric tons)\tAPY\tPer Crop\t\t\t
1. Crop Production & Yield\tYield per hectare\tAPY\t\t\t\t
1. Crop Production & Yield\tSeasonal cropping patterns (Kharif, Rabi, Zaid)\t Data coming from the block is quarterly, then the DES is kept in the cropping pattern\t\t\t\t
1. Crop Production & Yield\tOrganic vs. conventional farming area\t\t\t\t\t
2. Land & Soil Health\tSoil type and fertility status\tResearch Wing\t\t\t\t
2. Land & Soil Health\tSoil health card distribution and utilization\tResearch Wing\t\t\t\t
2. Land & Soil Health\tpH levels, nutrient content (NPK, micronutrients)\tResearch Wing\t\t\t\t
2. Land & Soil Health\tLandholding patterns (small, marginal, large farmers)\tResearch Wing\t\t\t\t
3. Agricultural Inputs & Resources\tAccess to irrigation (canals, tube wells, rainfed)\tWR\t\t\t\t
3. Agricultural Inputs & Resources\tFertilizer usage (quantity, type)\tCensus\t\t\t\t
3. Agricultural Inputs & Resources\tPesticide and insecticide application\tCensus\t\t\t\t
3. Agricultural Inputs & Resources\tSeed distribution and availability (certified, hybrid, GM)\tOnly for Govt. schemes, collected base on scheme head\t\t\t\t
4. Farmer Welfare & Livelihoods\tNumber of farmers by category (small, marginal, large)\tCensus\t\t\t\t
4. Farmer Welfare & Livelihoods\tFarmers benefiting from government schemes (PM-KISAN, crop insurance, MSP)\tAwareness given, document and verification, register in CSC and data is collected in district\t\t\t\t
4. Farmer Welfare & Livelihoods\tCredit and loan availability (KCC penetration, bank loans)\tBanks - SBLC\t\t\t\t
4. Farmer Welfare & Livelihoods\tFarmer Producer Organizations (FPOs) & cooperative societies\tHorti\t\t\t\t
5. Livestock & Dairy\tNumber of livestock (cattle, poultry, sheep, goats, pigs)\tAH&V\t\t\t\t
5. Livestock & Dairy\tMilk production & dairy cooperatives\tAH&V\t\t\t\t
5. Livestock & Dairy\tVeterinary care access (clinics, AI centers, vaccinations)\tAH&V\t\t\t\t
5. Livestock & Dairy\tFodder availability and grazing land\tAH&V\t\t\t\t
6. Agricultural Infrastructure\tWarehouses and cold storage facilities\tHorti\t\t\t\t
6. Agricultural Infrastructure\tMandis and local market accessibility\tHorti\t\t\t\t
6. Agricultural Infrastructure\tFarm mechanization (tractor ownership, use of harvesters)\tDistrict based on schemes\t\t\t\t
6. Agricultural Infrastructure\tPost-harvest storage losses\t\t\t\t\t
7. Climate & Disaster Resilience\tDrought-prone and flood-prone areas\t\t\t\t\t
7. Climate & Disaster Resilience\tClimate-smart agriculture adoption\t\t\t\t\t
7. Climate & Disaster Resilience\tCrop loss due to natural disasters (hailstorms, floods, droughts)\t\t\t\t\t
8. Supply Chain & Market Linkages\tMarket prices for key crops (trend over time)\tHorti\t\t\t\t
8. Supply Chain & Market Linkages\tDirect farmer-market linkages (e-NAM participation)\tHorti\t\t\t\t
8. Supply Chain & Market Linkages\tExport and inter-state trade data\tHorti\t\t\t\t
8. Supply Chain & Market Linkages\tValue chain analysis for major crops\tHorti\t\t\t\t
"""

    df = parse_data(raw_data)
    st.markdown("### Full Agriculture Dataset")
    st.dataframe(df)
    
    # ---------- Custom Chart with aggregator logic and bar mode/orientation ----------
    df["count"] = 1
    st.markdown("## Custom Agriculture Chart")

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

    custom_title = st.text_input("Chart Title", value="Custom Agriculture Chart")
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
        y_col_choice_bar = st.session_state.get('Bar Y-axis Column', None)
        y_col_choice_line = st.session_state.get('Line Y-axis Column', None)
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
    categories = df["Category"].unique().tolist()
    if not categories:
        st.warning("No categories found in the data!")
        return

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
            file_name="agriculture_chart.png",
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
        file_name="agriculture_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

def parse_data(raw_data: str) -> pd.DataFrame:
    lines = raw_data.strip().split("\n")
    # The first line is the header
    header_line = lines[0]
    data_lines = lines[1:]
    col_names = header_line.split("\t")

    rows = []
    for line in data_lines:
        # Skip blank lines to avoid empty rows
        if not line.strip():
            continue

        parts = line.split("\t")
        # Ensure exactly 8 columns
        if len(parts) < 8:
            parts += [""] * (8 - len(parts))
        else:
            parts = parts[:8]
        rows.append(parts)

    df = pd.DataFrame(rows, columns=col_names)
    return df
