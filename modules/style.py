# Sidebar
SIDEBAR_STYLE = {
    "width": "220px",
    "padding": "20px",
    "backgroundColor": "#EFF3FF",
    "height": "100vh",
}

SIDEBAR_TITLE = {
    "fontFamily": "monospace",
    "textAlign": "center",
    "marginBottom": "20px",
    "color": "#5246AB",
}  # Sidebar title
SIDEBAR_LINK = {
    "fontSize": 18,
    "fontWeight": "bold",
    "color": "#5879FF",
    "display": "block",
    "padding": "12px 20px",
    "textDecoration": "none",
    "marginBottom": "10px",
    "borderRadius": "5px",
    "fontWeight": "500",
    "transition": "0.3s",
}

SIDEBAR_LINK_HOVER = {"backgroundColor": "#5246AB"}

# Header
HEADER_STYLE = {
    "textAlign": "center",
    "fontSize": 32,
    "fontWeight": "bold",
    "padding": "10px",
    "backgroundColor": "#5879FF",
    "color": "white",
}

# Footer
FOOTER_STYLE = {
    "textAlign": "center",
    "fontSize": 12,
    "color": "#5879FF",
}

# Main content area
CONTENT_STYLE = {"flex": 1, "padding": "5px"}

# Main container
MAIN_DIV_STYLE = {"display": "flex", "flexDirection": "row"}

# Cards Row
CARD_STYLE = {"marginBottom": "20px"}

# KPI Cards
KPI_CARD_STYLE = {
    "padding": "10px",
    "backgroundColor": "#5879FF",
    "textAlign": "center",
    "borderRadius": "10px",
    "boxShadow": "0 2px 2px rgba(0,0,0,0.1)",
}

KPI_LABEL_STYLE = {
    "fontWeight": "bold",
    "marginBottom": "5px",
    "fontSize": "20px",
    "color": "#ffffff",
}
KPI_VALUE_STYLE = {"fontWeight": "bold", "fontSize": "18px", "color": "#ffffff"}
KPI_ROW_STYLE = {"margin": "18px 8px 30px 8px"}  # KPI row

# Page title
PAGE_TITLE = {
    "fontFamily": "monospace",
    # "textAlign": "center",
    "marginBottom": "24px",
    "fontWeight": "bold",
    "color": "#5879FF",
}

# Filter row
FILTER_ROW = {"marginBottom": "20px"}

# Dropdown and DatePicker style
FILTER_STYLE = {
    "height": "48px",
    "fontSize": "16px",
    "borderRadius": "5px",
    # "border": "1px solid #C2CFF3",
    "padding": "4px",
}

# Graph
GRAPH_STYLE = {
    "height": "360px",
    "width": "100%",
    "marginBottom": "20px",
    "padding": "10px",
    "borderRadius": "10px",
    "boxShadow": "0 4px 8px rgba(0,0,0,0.15)",
    "marginBottom": "20px",
}
GRAPH_STYLE_VERTICAL = {**GRAPH_STYLE, "height": "90vh"}  # inherit all general styles


# Chartly specific layout options
CHART_LAYOUT = {
    "plot_bgcolor": "#FFFFFF",
    "paper_bgcolor": "#FFFFFF",
    "font": {"family": "Arial, sans-serif", "size": 12, "color": "#5246AB"},
    "margin": {"l": 40, "r": 40, "t": 40, "b": 40},
}
# Line and marker colors for charts
CHART_LINE_COLOR = "#5879FF"
CHART_MARKER_COLOR = "#D9B5C1"


# Table
TABLE_STYLE = {
    "overflowX": "auto",
    "border": "1px solid #ddd",
    "borderRadius": "6px",
    "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
    "marginTop": "15px",
}

TABLE_CELL_STYLE = {
    "textAlign": "left",
    "padding": "8px",
    "fontFamily": "Arial, sans-serif",
    "fontSize": "14px",
    "whiteSpace": "normal",
    "height": "auto",
}

# Header style for DataTable
TABLE_HEADER_STYLE = {
    "backgroundColor": "#5879FF",
    "color": "white",
    "fontWeight": "bold",
    "textAlign": "center",
    "fontSize": "15px",
}

# Alternate row colors + hover effect
TABLE_CONDITIONAL_STYLE = [
    # Alternate row colors
    {"if": {"row_index": "odd"}, "backgroundColor": "#F9F9F9"},
    {"if": {"row_index": "even"}, "backgroundColor": "#FFFFFF"},
    # On hover (mouse over row)
    {
        "if": {"state": "active"},
        "backgroundColor": "#C2CFF3",
        "border": "1px solid #3B6EBF",
    },
    # On select (when row is clicked/selected)
    {
        "if": {"state": "selected"},
        "backgroundColor": "#CCE5FF",
        "border": "1px solid #0056b3",
        "color": "#000000",
    },
]


# Button
BUTTON = {"marginBottom": "10px", "backgroundColor": "#C2CFF3"}

GRAPH_CONFIG = {
    "modeBarButtonsToRemove": ["zoom", "pan", "select", "lasso2d"],
    "displaylogo": False,
}
