import streamlit as st
import pandas as pd
import numpy as np
import altair as alt


# ============================================================
# 1. PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="iPhone 18 Malaysia Sales Dashboard",
    page_icon="📱",
    layout="wide"
)


# ============================================================
# 2. CUSTOM STYLE
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

h1, h2, h3 {
    font-family: 'Poppins', sans-serif;
}

.explanation-box {
    background-color: #F8F1E5;
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 20px;
    line-height: 1.6;
}

.info-card {
    background-color: #FFFFFF;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #E5E5E5;
    text-align: center;
    min-height: 150px;
}

.metric-card {
    background-color: #F8F1E5;
    padding: 18px;
    border-radius: 12px;
    text-align: center;
}

.small-note {
    font-size: 13px;
    color: #666666;
}

.sidebar-title {
    text-align: center;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# 3. DATA
# ============================================================

np.random.seed(42)

iphone_models = [
    "iPhone 18 Pro",
    "iPhone 18 Pro Max"
]

iphone_colours = [
    "Burgundy",
    "Glacier",
    "Silver",
    "Black"
]

cities = [
    "Kuala Lumpur",
    "Johor Bahru",
    "George Town",
    "Ipoh",
    "Kota Kinabalu",
    "Kuching"
]

city_coordinates = {
    "Kuala Lumpur": {
        "Latitude": 3.1390,
        "Longitude": 101.6869
    },
    "Johor Bahru": {
        "Latitude": 1.4927,
        "Longitude": 103.7414
    },
    "George Town": {
        "Latitude": 5.4141,
        "Longitude": 100.3288
    },
    "Ipoh": {
        "Latitude": 4.5975,
        "Longitude": 101.0901
    },
    "Kota Kinabalu": {
        "Latitude": 5.9804,
        "Longitude": 116.0735
    },
    "Kuching": {
        "Latitude": 1.5533,
        "Longitude": 110.3592
    }
}


# ============================================================
# 4. CREATE SIMULATED DATA
# ============================================================

n = 240

models = np.random.choice(
    iphone_models,
    size=n,
    p=[0.55, 0.45]
)

colours = np.random.choice(
    iphone_colours,
    size=n
)

city_values = np.random.choice(
    cities,
    size=n
)

prices = []

for model in models:

    if model == "iPhone 18 Pro":
        price = np.random.randint(5299, 5799)
    else:
        price = np.random.randint(5999, 6799)

    prices.append(price)


quantities = np.random.randint(5, 80, size=n)

sales = np.array(prices) * quantities

latitudes = []
longitudes = []

for city in city_values:

    latitudes.append(
        city_coordinates[city]["Latitude"]
        + np.random.uniform(-0.08, 0.08)
    )

    longitudes.append(
        city_coordinates[city]["Longitude"]
        + np.random.uniform(-0.08, 0.08)
    )


df = pd.DataFrame({
    "Product": models,
    "Colour": colours,
    "City": city_values,
    "Price": prices,
    "Quantity": quantities,
    "Sales": sales,
    "Country": "Malaysia",
    "Latitude": latitudes,
    "Longitude": longitudes
})


# ============================================================
# 5. COLOUR PALETTE
# ============================================================

colour_palette = {
    "Burgundy": "#7A263A",
    "Glacier": "#BFD8E8",
    "Silver": "#B8B8B8",
    "Black": "#222222"
}


# ============================================================
# 6. SIDEBAR
# ============================================================

st.sidebar.markdown(
    "<h1 style='text-align:center;'>📱</h1>",
    unsafe_allow_html=True
)

st.sidebar.markdown(
    "<h3 style='text-align:center;'>iPhone 18</h3>",
    unsafe_allow_html=True
)

st.sidebar.markdown(
    "<p style='text-align:center;'>Malaysia Sales Dashboard</p>",
    unsafe_allow_html=True
)

st.sidebar.divider()


# ------------------------------------------------------------
# FILTERS
# ------------------------------------------------------------

st.sidebar.markdown("### Choose Your Product")

selected_model = st.sidebar.selectbox(
    "iPhone Model",
    iphone_models
)

selected_colour = st.sidebar.selectbox(
    "Colour",
    iphone_colours
)


st.sidebar.divider()


# ============================================================
# PAGE NAVIGATION
# ============================================================

st.sidebar.markdown("### Dashboard Menu")


# Create session state only once
if "page" not in st.session_state:
    st.session_state.page = "Welcome"


# Page buttons
pages = [
    ("🏠", "Welcome"),
    ("📊", "Sales Comparison"),
    ("📈", "Price & Quantity"),
    ("🥧", "Sales by City"),
    ("🗺️", "Malaysia Map"),
    ("✓", "Conclusion")
]


for icon, page_name in pages:

    # Highlight current page
    if st.session_state.page == page_name:

        if st.sidebar.button(
            f"●  {icon}  {page_name}",
            key=f"nav_{page_name}",
            use_container_width=True,
            type="primary"
        ):
            st.session_state.page = page_name
            st.rerun()

    else:

        if st.sidebar.button(
            f"{icon}  {page_name}",
            key=f"nav_{page_name}",
            use_container_width=True,
            type="secondary"
        ):
            st.session_state.page = page_name
            st.rerun()


st.sidebar.divider()

st.sidebar.caption(
    "TFB3133 / TEB3133 Data Visualization"
)

st.sidebar.caption(
    "Malaysia iPhone Sales Dashboard"
)


# ============================================================
# 7. FILTER DATA
# ============================================================

filtered_df = df[
    (df["Product"] == selected_model) &
    (df["Colour"] == selected_colour)
].copy()


# ============================================================
# 8. PAGE 1 — WELCOME
# ============================================================

if st.session_state.page == "Welcome":

    st.title("Welcome to the iPhone 18 Malaysia Sales Dashboard")

    st.write(
        "This dashboard helps you explore simulated iPhone sales "
        "data across major cities in Malaysia."
    )

    st.markdown(
        """
        <div class="explanation-box">

        <b>How to use this dashboard</b><br><br>

        <b>1. Choose an iPhone model</b> using the sidebar.<br>
        <b>2. Choose a colour</b> using the sidebar.<br>
        <b>3. Click a dashboard page</b> to explore the data.<br>
        <b>4. Compare sales, prices, quantities and cities.</b>

        </div>
        """,
        unsafe_allow_html=True
    )

    try:

        st.image(
            "ip.png",
            use_container_width=True
        )

    except:

        st.warning(
            "ip.png was not found. Please make sure it is inside the lab_3 folder."
        )

    st.markdown("### What can you explore?")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="info-card">

            <h3>Choose</h3>

            Select an iPhone model and colour
            from the sidebar.

            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="info-card">

            <h3>Explore</h3>

            Look at sales, prices and quantities
            using different charts.

            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            """
            <div class="info-card">

            <h3>Compare</h3>

            Compare different cities across Malaysia.

            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("### Understanding the numbers")

    explanation = pd.DataFrame({
        "Term": [
            "Price",
            "Quantity",
            "Sales",
            "City"
        ],
        "Meaning": [
            "Estimated price of one phone in RM",
            "Number of phones sold",
            "Price × Quantity",
            "City where the simulated sales occur"
        ]
    })

    st.table(explanation)

    st.info(
        "Note: The data in this dashboard are simulated for academic "
        "and data visualization purposes."
    )


# ============================================================
# 9. PAGE 2 — SALES COMPARISON
# ============================================================

elif st.session_state.page == "Sales Comparison":

    st.title("Sales Comparison")

    st.markdown(
        """
        <div class="explanation-box">

        <b>What does this page show?</b><br>

        The bar chart compares total sales between iPhone models.
        The scatter chart shows the relationship between price
        and quantity sold.

        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # BAR CHART
    # --------------------------------------------------------

    sales_by_model = (
        df[df["Colour"] == selected_colour]
        .groupby("Product", as_index=False)["Sales"]
        .sum()
    )

    bar_chart = alt.Chart(
        sales_by_model
    ).mark_bar(
        cornerRadiusTopLeft=8,
        cornerRadiusTopRight=8
    ).encode(

        x=alt.X(
            "Product:N",
            title="iPhone Model"
        ),

        y=alt.Y(
            "Sales:Q",
            title="Total Sales (RM)"
        ),

        color=alt.Color(
            "Product:N",
            legend=None
        ),

        tooltip=[
            "Product",
            alt.Tooltip(
                "Sales:Q",
                title="Sales (RM)",
                format=",.0f"
            )
        ]
    ).properties(
        title=f"Total Sales by iPhone Model — {selected_colour}",
        height=400
    )

    st.altair_chart(
        bar_chart,
        use_container_width=True
    )


    # --------------------------------------------------------
    # SCATTER CHART
    # --------------------------------------------------------

    st.subheader(
        f"{selected_model} — Price vs Quantity"
    )

    scatter = alt.Chart(
        filtered_df
    ).mark_circle(
        size=100,
        opacity=0.75
    ).encode(

        x=alt.X(
            "Price:Q",
            title="Price (RM)"
        ),

        y=alt.Y(
            "Quantity:Q",
            title="Quantity Sold"
        ),

        color=alt.Color(
            "City:N",
            title="City"
        ),

        tooltip=[
            "City",
            alt.Tooltip(
                "Price:Q",
                title="Price (RM)",
                format=",.0f"
            ),
            alt.Tooltip(
                "Quantity:Q",
                title="Quantity"
            ),
            alt.Tooltip(
                "Sales:Q",
                title="Sales (RM)",
                format=",.0f"
            )
        ]
    ).properties(
        height=450
    )

    st.altair_chart(
        scatter,
        use_container_width=True
    )


# ============================================================
# 10. PAGE 3 — PRICE & QUANTITY
# ============================================================

elif st.session_state.page == "Price & Quantity":

    st.title("Price and Quantity")

    st.markdown(
        """
        <div class="explanation-box">

        <b>What does this page show?</b><br>

        The line chart shows how the simulated phone prices vary.
        The histogram shows how often different quantities of phones
        were sold.

        </div>
        """,
        unsafe_allow_html=True
    )

    line_df = filtered_df.reset_index(drop=True)
    line_df["Record"] = line_df.index + 1

    line_chart = alt.Chart(
        line_df
    ).mark_line(
        point=True
    ).encode(

        x=alt.X(
            "Record:Q",
            title="Sales Record"
        ),

        y=alt.Y(
            "Price:Q",
            title="Price (RM)"
        ),

        tooltip=[
            "Record",
            alt.Tooltip(
                "Price:Q",
                title="Price (RM)",
                format=",.0f"
            ),
            "City"
        ]
    ).properties(
        title=f"Price Variation — {selected_model} / {selected_colour}",
        height=400
    )

    st.altair_chart(
        line_chart,
        use_container_width=True
    )


    st.subheader("Quantity Distribution")

    histogram = alt.Chart(
        filtered_df
    ).mark_bar().encode(

        x=alt.X(
            "Quantity:Q",
            bin=alt.Bin(maxbins=15),
            title="Quantity Sold"
        ),

        y=alt.Y(
            "count()",
            title="Number of Records"
        ),

        tooltip=[
            alt.Tooltip(
                "count()",
                title="Number of Records"
            )
        ]
    ).properties(
        height=400
    )

    st.altair_chart(
        histogram,
        use_container_width=True
    )


# ============================================================
# 11. PAGE 4 — SALES BY CITY
# ============================================================

elif st.session_state.page == "Sales by City":

    st.title("Sales by City")

    st.markdown(
        """
        <div class="explanation-box">

        <b>What does this page show?</b><br>

        The pie chart compares sales between the two iPhone models.
        The bar chart shows which Malaysian cities have higher
        simulated sales.

        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # PIE CHART
    # --------------------------------------------------------

    pie_df = (
        df[df["Colour"] == selected_colour]
        .groupby("Product", as_index=False)["Sales"]
        .sum()
    )

    pie_chart = alt.Chart(
        pie_df
    ).mark_arc(
        innerRadius=60
    ).encode(

        theta=alt.Theta(
            "Sales:Q"
        ),

        color=alt.Color(
            "Product:N",
            title="iPhone Model"
        ),

        tooltip=[
            "Product",
            alt.Tooltip(
                "Sales:Q",
                title="Sales (RM)",
                format=",.0f"
            )
        ]
    ).properties(
        title=f"Sales Share — {selected_colour}",
        height=400
    )

    st.altair_chart(
        pie_chart,
        use_container_width=True
    )


    # --------------------------------------------------------
    # CITY BAR CHART
    # --------------------------------------------------------

    city_sales = (
        filtered_df
        .groupby("City", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )

    city_bar = alt.Chart(
        city_sales
    ).mark_bar(
        cornerRadiusEnd=8
    ).encode(

        y=alt.Y(
            "City:N",
            sort="-x",
            title="City"
        ),

        x=alt.X(
            "Sales:Q",
            title="Sales (RM)"
        ),

        tooltip=[
            "City",
            alt.Tooltip(
                "Sales:Q",
                title="Sales (RM)",
                format=",.0f"
            )
        ]
    ).properties(
        title=f"Sales by City — {selected_model} / {selected_colour}",
        height=400
    )

    st.altair_chart(
        city_bar,
        use_container_width=True
    )


# ============================================================
# 12. PAGE 5 — MALAYSIA MAP
# ============================================================

elif st.session_state.page == "Malaysia Map":

    st.title("iPhone Sales Across Malaysia")

    st.markdown(
        """
        <div class="explanation-box">

        <b>What does this map show?</b><br>

        The map shows the six cities included in this study.
        Bigger circles represent higher simulated sales.

        Use the city selector below to see more information
        about one city.

        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # MAP DATA
    # --------------------------------------------------------

    map_data = (
        filtered_df
        .groupby("City", as_index=False)
        .agg({
            "Sales": "sum",
            "Quantity": "sum",
            "Price": "mean",
            "Latitude": "mean",
            "Longitude": "mean"
        })
    )


    # --------------------------------------------------------
    # MAP
    # --------------------------------------------------------

    malaysia_map = alt.Chart(
        map_data
    ).mark_circle(
        opacity=0.8
    ).encode(

        longitude=alt.Longitude(
            "Longitude:Q"
        ),

        latitude=alt.Latitude(
            "Latitude:Q"
        ),

        size=alt.Size(
            "Sales:Q",
            title="Total Sales"
        ),

        color=alt.Color(
            "Sales:Q",
            title="Sales"
        ),

        tooltip=[
            "City",
            alt.Tooltip(
                "Sales:Q",
                title="Sales (RM)",
                format=",.0f"
            ),
            alt.Tooltip(
                "Quantity:Q",
                title="Quantity"
            ),
            alt.Tooltip(
                "Price:Q",
                title="Average Price (RM)",
                format=",.0f"
            )
        ]
    ).project(
        type="mercator",
        center=[108, 4],
        scale=800
    ).properties(
        title="Simulated iPhone Sales Locations",
        height=550
    )


    st.altair_chart(
        malaysia_map,
        use_container_width=True
    )

    st.caption(
        "The locations represent approximate city coordinates. "
        "They are not exact customer locations."
    )


    # --------------------------------------------------------
    # CITY SELECTOR
    # --------------------------------------------------------

    st.subheader("Explore One City")

    selected_city = st.selectbox(
        "Choose a city",
        cities
    )

    city_data = filtered_df[
        filtered_df["City"] == selected_city
    ]


    # --------------------------------------------------------
    # CITY METRICS
    # --------------------------------------------------------

    total_sales = city_data["Sales"].sum()
    total_quantity = city_data["Quantity"].sum()

    if len(city_data) > 0:
        average_price = city_data["Price"].mean()
    else:
        average_price = 0


    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            f"""
            <div class="metric-card">

            <h3>Total Sales</h3>

            <h2>RM {total_sales:,.0f}</h2>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="metric-card">

            <h3>Quantity Sold</h3>

            <h2>{total_quantity:,}</h2>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            f"""
            <div class="metric-card">

            <h3>Average Price</h3>

            <h2>RM {average_price:,.0f}</h2>

            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # CITY SCATTER
    # --------------------------------------------------------

    st.subheader(
        f"Sales Details — {selected_city}"
    )

    if len(city_data) > 0:

        city_scatter = alt.Chart(
            city_data
        ).mark_circle(
            size=120,
            opacity=0.8
        ).encode(

            x=alt.X(
                "Quantity:Q",
                title="Quantity Sold"
            ),

            y=alt.Y(
                "Sales:Q",
                title="Sales (RM)"
            ),

            color=alt.Color(
                "Colour:N",
                title="Colour"
            ),

            shape=alt.Shape(
                "Product:N",
                title="Model"
            ),

            tooltip=[
                "Product",
                "Colour",
                "City",
                "Quantity",
                alt.Tooltip(
                    "Price:Q",
                    title="Price (RM)",
                    format=",.0f"
                ),
                alt.Tooltip(
                    "Sales:Q",
                    title="Sales (RM)",
                    format=",.0f"
                )
            ]
        ).properties(
            height=400
        )

        st.altair_chart(
            city_scatter,
            use_container_width=True
        )

    else:

        st.warning(
            "There is no simulated data available for this city "
            "with the selected model and colour."
        )


# ============================================================
# 13. PAGE 6 — CONCLUSION
# ============================================================

elif st.session_state.page == "Conclusion":

    st.title("What Did We Learn?")

    st.markdown(
        """
        <div class="explanation-box">

        This dashboard demonstrates how interactive visualizations
        can help users understand data more easily.

        Instead of looking at a large table of numbers,
        we can use charts and maps to identify patterns quickly.

        </div>
        """,
        unsafe_allow_html=True
    )


    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
            <div class="info-card">

            <h3>1. Compare Products</h3>

            Bar and pie charts make it easier to compare
            the sales performance of different iPhone models.

            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="info-card">

            <h3>2. Understand Numbers</h3>

            Line charts and histograms help us understand
            price and quantity patterns.

            </div>
            """,
            unsafe_allow_html=True
        )


    st.write("")


    col3, col4 = st.columns(2)

    with col3:

        st.markdown(
            """
            <div class="info-card">

            <h3>3. Compare Cities</h3>

            City charts help identify where simulated sales
            are higher or lower.

            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:

        st.markdown(
            """
            <div class="info-card">

            <h3>4. Use a Map</h3>

            Maps make geographical information easier
            to understand.

            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown("### Selected Product")

    st.write(
        f"**Model:** {selected_model}"
    )

    st.write(
        f"**Colour:** {selected_colour}"
    )


    st.markdown("### Available Colours")

    colour_cols = st.columns(4)

    for i, colour in enumerate(iphone_colours):

        with colour_cols[i]:

            st.markdown(
                f"""
                <div style="
                    background-color:{colour_palette[colour]};
                    padding:15px;
                    border-radius:10px;
                    text-align:center;
                    color:white;
                    font-weight:600;
                ">
                {colour}
                </div>
                """,
                unsafe_allow_html=True
            )


    st.success(
        "The main idea of linked and interactive visualization "
        "is to make data easier to explore, compare and understand."
    )

    st.info(
        "All sales values in this project are simulated and are "
        "used only for educational purposes."
    )