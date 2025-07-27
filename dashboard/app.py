# Imports
faicons
pandas
plotly
shinywidgets

# Reactive Aspects @reactive.calc to filter data by day, then compute the average tip 
@reactive.calc
def filtered_data():
    selected = input.selected_day()
    return df[df["day"] == selected]

# Reactive calculation: calculate average tip
@reactive.calc
def avg_tip():
    data = filtered_data()
    return data["tip"].mean()

# Render output
@render.text
def avg_tip_text():
    return f"Average tip on {input.selected_day()}: ${avg_tip():.2f}"

app = App(ui, server=None) 

# UI Page Inputs
ui.input_select("selected_day", "Choose a day:", choices=sorted(df["day"].unique()))

UI Sidebar Components
from shiny.express import ui

app_ui = ui.page_sidebar(
    ui.sidebar_panel(
        ui.input_select("selected_day", "Choose a day:", choices=sorted(df["day"].unique())),
        # You can add more inputs here, e.g.:
        # ui.input_checkbox("smoker_only", "Show only smokers"),
    ),
    ui.main_panel(
        ui.output_text_verbatim("avg_tip_text")
    )
)
Choose at least one input that the user can interact with to filter the data set
ui.input_checkbox_group(
    "selected_sex",  # input id
    "Select sex:",   # label shown to user
    choices=["Male", "Female"],
    selected=["Male", "Female"],  # default to both selected
)

@reactive.calc
def filtered_data():
    selected_day = input.selected_day()
    selected_sex = input.selected_sex()
    filtered = df[
        (df["day"] == selected_day) &
        (df["sex"].isin(selected_sex))
    ]
    return filtered
  
# UI Main Content
Everything not in the sidebar is the main content.
Will you use a template?  Most likely
Will you use layout columns?  Possibly 
Will you use navigation or accordion components?  I would like to try this: ui.navset_pill() — Pill-style navigation (like tabs but rounded)
Define some output text. Will it be in a card? A value box?   A value box 
Define an output table or grid to show your filtered data set: ui.output_table("filtered_table")
@render.table
def filtered_table():
    # Return the filtered data as a pandas DataFrame
    return filtered_data()
Define an  output widget or chart (e.g., a Plotly Express chart) to show the filtered data graphically
ui.output_plot("scatter_plot")
@render.plot
def scatter_plot():
    df_filtered = filtered_data()  # your reactive filtered DataFrame
    fig = px.scatter(
        df_filtered,
        x="total_bill",
        y="tip",
        color="sex",  # color points by sex
        title="Total Bill vs Tip",
        labels={"total_bill": "Total Bill ($)", "tip": "Tip ($)"}
    )
    return fig
