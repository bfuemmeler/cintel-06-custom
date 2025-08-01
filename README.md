# cintel-06-custom

# P6 Files & Packages
.gitignore
app.py

# requirements.txt 
import pandas as pd
import plotly.express as px
import faicons as fa

from shiny import reactive, render
from shiny.express import ui, input, output
from shinywidgets import render_plotly
from faicons import icon_svg

# Load Data
tips = pd.read_csv(
    "https://raw.githubusercontent.com/bfuemmeler/cintel-06-custom/main/dashboard/tips.csv"
)
# Define range for slider input
bill_rng = (min(tips["total_bill"]), max(tips["total_bill"]))

# Define reactive calc
@reactive.calc
def filtered_data():
    bill = input.total_bill()
    gender = input.gender()
    times = input.selected_time()

    df = tips[
        tips["total_bill"].between(bill[0], bill[1])
        & tips["sex"].isin(gender)
        & tips["time"].isin(times)
    ].copy()
    df["tip_pct"] = df["tip"] / df["total_bill"]
    return df
    
# Define ICONS
ICONS = {
    "users": fa.icon_svg("users", "solid"),
    "pen": fa.icon_svg("pen", "solid"),
    "receipt": fa.icon_svg("receipt", "solid"),
}
# Define Shiny Express UI
## Title
ui.page_opts(title="Tips Dashboard", fillable=True)
## Sidebar with slider, checkbox groups
with ui.sidebar():
    ui.input_slider(
        "total_bill", 
        "Total Bill:", 
        min=bill_rng[0],
        max=bill_rng[1],
        value=bill_rng,
        pre="$",
    )

    ui.input_checkbox_group(
        "gender",
        "Select Gender:",
        choices={
            "Male": ui.span("Male", style="color:red;"),
            "Female": ui.span("Female", style="color:green;"),
        },
        selected=["Male", "Female"],
    )

    ui.input_checkbox_group(
        "selected_time",
        "Choose Time of Service:",
        choices=["Lunch", "Dinner"],
        selected=["Lunch", "Dinner"],
        inline=True,
    )

## Value Boxes
with ui.layout_columns():
    @render.text
    def guests_count():
        return str(filtered_data().shape[0])
    
    ui.value_box(
        title="Guests in View",
        value=guests_count,
        showcase=ICONS["users"],
        theme="bg-gradient-blue-yellow",
    )
    @render.text
    def avg_tip_pct():
        df = filtered_data()
        return "N/A" if df.empty else f"{(df['tip_pct'].mean() * 100):.1f}%"
        
    ui.value_box(
        title="Avg Tip %",
        value=avg_tip_pct,
        showcase=ICONS["pen"],
        theme="bg-gradient-blue-yellow",
    )
    @render.text
    def avg_bill():
        df = filtered_data()
        return "N/A" if df.empty else f"${df['total_bill'].mean():.2f}"
        
    ui.value_box(
        title="Avg Bill",
        value=avg_bill,
        showcase=ICONS["receipt"],
        theme="bg-gradient-blue-yellow",
    )
## Charts & Tables
with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Tips Table")

        @render.data_frame
        def show_data():
            return render.DataGrid(filtered_data())

    with ui.card(full_screen=True):
        ui.card_header("Average Tip by Gender")

        @render_plotly
        def plot_tips_by_gender():
            df = filtered_data()
            if df.empty:
                return px.bar(title="No Data")
            summary = df.groupby("sex")["tip"].mean().reset_index()
            return px.bar(summary, x="sex", y="tip", color="sex", title="Avg Tip by Gender")

    with ui.card(full_screen=True):
        ui.card_header("Tips by Day")

        @render_plotly
        def day_plot():
            df = filtered_data()
            if df.empty:
                return px.bar(title="No data")
            summary = df.groupby("day")["tip"].sum().reset_index()
            return px.bar(
                summary,
                x="day",
                y="tip",
                color="day",
                title="Total Tips by Day",
                labels={"tip": "Total Tips ($)", "day": "Day"},
                category_orders={"day": ["Thur", "Fri", "Sat", "Sun"]},
            )

