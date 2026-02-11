"""
Brutalist design theme for Plotly charts matching the documentation site.
This module provides consistent styling across all visualizations.
"""

import plotly.graph_objects as go
import plotly.express as px


# Color scheme - Brutalist monochrome
COLORS = {
    'primary': '#000000',
    'background': '#ffffff',
    'accent_bg': '#f5f5f5',
    'text': '#000000',
    'border': '#000000',
}

# Font configuration
FONTS = {
    'family': 'Space Grotesk, system-ui, sans-serif',
    'family_mono': 'IBM Plex Mono, monospace',
}

# Border/line widths - Brutalist heavy borders
BORDER_WIDTH = 2
TICK_WIDTH = 2


def get_brutalist_layout(**kwargs):
    """
    Returns a Plotly layout dict with Brutalist design styling.

    Parameters:
        **kwargs: Additional layout parameters to merge

    Returns:
        dict: Complete layout configuration
    """
    layout = {
        # Global font configuration
        'font': {
            'family': FONTS['family'],
            'size': 12,
            'color': COLORS['text'],
        },

        # Title styling (if title provided in kwargs)
        'title': {
            'font': {
                'family': FONTS['family'],
                'size': 16,
                'color': COLORS['text'],
            },
            'x': 0.5,
            'xanchor': 'center',
        },

        # X-axis default styling
        'xaxis': {
            'showgrid': False,
            'showline': True,
            'linewidth': BORDER_WIDTH,
            'linecolor': COLORS['border'],
            'ticks': 'outside',
            'tickwidth': TICK_WIDTH,
            'tickcolor': COLORS['border'],
            'tickfont': {
                'family': FONTS['family'],
                'size': 10,
                'color': COLORS['text'],
            },
            'zeroline': False,
            'title': {
                'font': {
                    'family': FONTS['family'],
                    'size': 11,
                    'color': COLORS['text'],
                },
            },
        },

        # Y-axis default styling
        'yaxis': {
            'showgrid': True,
            'gridcolor': COLORS['accent_bg'],
            'gridwidth': 1,
            'showline': True,
            'linewidth': BORDER_WIDTH,
            'linecolor': COLORS['border'],
            'ticks': 'outside',
            'tickwidth': TICK_WIDTH,
            'tickcolor': COLORS['border'],
            'tickfont': {
                'family': FONTS['family'],
                'size': 10,
                'color': COLORS['text'],
            },
            'zeroline': True,
            'zerolinewidth': BORDER_WIDTH,
            'zerolinecolor': COLORS['border'],
            'title': {
                'font': {
                    'family': FONTS['family'],
                    'size': 11,
                    'color': COLORS['text'],
                },
            },
        },

        # Background colors
        'plot_bgcolor': COLORS['background'],
        'paper_bgcolor': COLORS['background'],

        # Legend styling
        'legend': {
            'orientation': 'h',
            'x': 0.5,
            'xanchor': 'center',
            'y': -0.15,
            'yanchor': 'top',
            'font': {
                'family': FONTS['family'],
                'size': 10,
                'color': COLORS['text'],
            },
            'bgcolor': COLORS['background'],
            'bordercolor': COLORS['border'],
            'borderwidth': BORDER_WIDTH,
        },

        # Hover label styling
        'hoverlabel': {
            'bgcolor': COLORS['primary'],
            'font_size': 12,
            'font_family': FONTS['family'],
            'font_color': COLORS['background'],
            'bordercolor': COLORS['border'],
        },

        # Default margins
        'margin': {'l': 50, 'r': 50, 't': 80, 'b': 100},

        # Auto size
        'autosize': True,
    }

    # Deep merge with provided kwargs
    layout = _deep_merge(layout, kwargs)

    return layout


def get_map_layout(**kwargs):
    """
    Returns a Plotly layout specifically for map visualizations.

    Parameters:
        **kwargs: Additional layout parameters to merge

    Returns:
        dict: Layout configuration optimized for maps
    """
    layout = get_brutalist_layout(
        xaxis={
            'title': {'text': 'LONGITUDE'},
            'showgrid': False,
        },
        yaxis={
            'title': {'text': 'LATITUDE'},
            'showgrid': False,
        },
        margin={'l': 50, 'r': 50, 't': 50, 'b': 50},
    )

    layout = _deep_merge(layout, kwargs)

    return layout


def get_colorbar_style(title):
    """
    Returns a Plotly colorbar dict with Brutalist styling.

    Parameters:
        title (str): Title for the colorbar

    Returns:
        dict: Colorbar configuration
    """
    return {
        'title': {
            'text': title.upper(),
            'font': {
                'family': FONTS['family'],
                'size': 11,
                'color': COLORS['text'],
            },
        },
        'orientation': 'h',
        'yanchor': 'top',
        'len': 0.75,
        'thickness': 15,
        'tickfont': {
            'family': FONTS['family'],
            'size': 10,
            'color': COLORS['text'],
        },
        #'outlinecolor': COLORS['border'],
        #'outlinewidth': BORDER_WIDTH,
        #'bgcolor': COLORS['background'],
    }


def get_empty_state_annotation(message):
    """
    Returns an annotation dict for empty state messages.

    Parameters:
        message (str): Message to display (will be converted to uppercase)

    Returns:
        dict: Annotation configuration
    """
    return {
        'text': message.upper(),
        'xref': 'paper',
        'yref': 'paper',
        'x': 0.5,
        'y': 0.5,
        'showarrow': False,
        'font': {
            'size': 16,
            'color': COLORS['text'],
            'family': FONTS['family'],
        },
        'align': 'center',
    }


def apply_brutalist_style(fig):
    """
    Apply Brutalist styling to an existing Plotly figure.

    Parameters:
        fig: Plotly figure object

    Returns:
        fig: Modified figure with Brutalist styling
    """
    fig.update_layout(**get_brutalist_layout())
    return fig


def _deep_merge(base_dict, update_dict):
    """
    Recursively merge two dictionaries, with update_dict taking precedence.

    Parameters:
        base_dict (dict): Base dictionary
        update_dict (dict): Dictionary with updates

    Returns:
        dict: Merged dictionary
    """
    result = base_dict.copy()

    for key, value in update_dict.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value

    return result


# def create_discrete_colorscale(colorscale_name, n_bins=6):
#     """
#     Create a discrete colorscale from a continuous Plotly colorscale.

#     This function samples colors from a continuous colorscale and creates
#     distinct bins with hard boundaries between colors, resulting in a
#     stepped appearance rather than smooth gradients.

#     Parameters:
#         colorscale_name (str): Name of Plotly colorscale (e.g., 'Blues', 'Reds', 'Greys')
#         n_bins (int): Number of discrete color bins (default: 6)

#     Returns:
#         list: Discrete colorscale as list of [position, color] pairs

#     Example:
#         >>> discrete_blues = create_discrete_colorscale('Blues', n_bins=5)
#         >>> # Returns 5 distinct blue shades with hard boundaries
#     """
#     # Get the continuous colorscale from Plotly
#     try:
#         # Get colors from the named colorscale
#         colors = px.colors.sample_colorscale(
#             colorscale_name,
#             n_bins,
#             low=0.0,
#             high=1.0
#         )
#     except:
#         # Fallback if colorscale name not found
#         colors = px.colors.sample_colorscale(
#             'Viridis',
#             n_bins,
#             low=0.0,
#             high=1.0
#         )

#     # Create discrete boundaries
#     # Each color gets a range, with hard transitions between bins
#     discrete_scale = []

#     for i in range(n_bins):
#         # Calculate the position for this bin
#         pos_start = i / n_bins
#         pos_end = (i + 1) / n_bins

#         # Add the color at both start and end of the bin (creates hard boundary)
#         if i == 0:
#             discrete_scale.append([pos_start, colors[i]])
#         else:
#             # Add a tiny gap to create hard boundary
#             discrete_scale.append([pos_start - 0.0001, colors[i-1]])
#             discrete_scale.append([pos_start, colors[i]])

#         if i == n_bins - 1:
#             discrete_scale.append([pos_end, colors[i]])

#     return discrete_scale
