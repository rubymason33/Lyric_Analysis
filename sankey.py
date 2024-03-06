import plotly.graph_objects as go
import random
import plotly.express as px

def hex_to_rgba(hex_color, alpha=0.5):
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
    return f'rgba{rgb + (alpha,)}'

def generate_color():
    alphabet_colors = px.colors.qualitative.Alphabet
    colors = [hex_to_rgba(color) for color in alphabet_colors]
    return random.choice(colors)


def _code_mapping(df, src, targ):
    # get the distinct labels from src/targ columns
    labels = list(set(list(df[src]) + list(df[targ])))

    # generate n integers for n labels
    codes = list(range(len(labels)))

    # create a map from label to code
    lc_map = dict(zip(labels, codes))

    # substitute names for codes in the dataframe
    df = df.replace({src: lc_map, targ: lc_map})

    # Return modified dataframe and list of labels
    return df, labels


def make_sankey(df, src, targ, vals=None, save=None, **kwargs):
    """
    Create a sankey diagram from a dataframe and specified columns
    :param df:
    :param src:
    :param targ:
    :param vals:
    :param save:
    :param kwargs:
    :return:
    """

    if vals:
        values = df[vals]
    else:
        values = [1] * len(df)

    # convert df labels to integer values
    df, labels = _code_mapping(df, src, targ)

    # stack columns if there are more than 2
    # df = stack_columns(df)

    x = 5

    label_color_dict = {label: generate_color() for label in labels}

    link_colors = [label_color_dict[labels[label]] for label in df[src]]

    link = {'source': df[src], 'target': df[targ], 'value': values,
            'color': link_colors}

    node_thickness = kwargs.get("node_thickness", 50)

    node = {'label': labels, 'pad': 50, 'thickness': node_thickness,
            'line': {'color': 'black', 'width': 1}, 'color': [label_color_dict[label] for label in labels]}

    sk = go.Sankey(link=link, node=node)
    fig = go.Figure(sk)

    fig.show()

    if save:
        fig.write_image(save)
