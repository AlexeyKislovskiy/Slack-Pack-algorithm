from matplotlib.typing import ColorType


class PlotSettings:
    """
    A class representing plot settings allowing customizing the appearance of plot.

    Attributes:
        detail_colors (dict[str, ColorType]): Dictionary mapping detail types to their colors.
        hover_detail_color (ColorType): Color used for highlighting a detail on hover.
        detail_edgecolor (ColorType): Edge color for detail.
        text_color (ColorType): Color for text on detail.
        base_edgecolor (ColorType): Edge color for the base.
        base_facecolor (ColorType): Face color for the base.
        detail_visible_percent (float): Percentage of the detail visibility required for it to be visible on the screen.
            Value should be in the range [0, 100].
        text_visible_percent (float): Percentage of text visibility required for it to be visible on the screen.
            Value should be in the range [0, 100].
        name_fontsize (float): Font size for detail names.
        size_fontsize (float): Font size for detail sizes.
        convert_digits_to_subscript (bool): A boolean parameter indicating whether to convert digits in the
            detail names to subscript format.
    """

    def __init__(self,
                 detail_colors: dict[str, ColorType] = None,
                 hover_detail_color: ColorType = 'red',
                 detail_edgecolor: ColorType = 'black',
                 text_color: ColorType = 'black',
                 base_edgecolor: ColorType = 'black',
                 base_facecolor: ColorType = 'lightgray',
                 detail_visible_percent: float = 1,
                 text_visible_percent: float = 10,
                 name_fontsize: float = 15,
                 size_fontsize: float = 10,
                 convert_digits_to_subscript: bool = True):
        """
        Initialize the plot settings.

        :param detail_colors: Dictionary mapping detail types to their colors.
        :param hover_detail_color: Color used for highlighting a detail on hover.
        :param detail_edgecolor: Edge color for detail.
        :param text_color: Color for text on detail.
        :param base_edgecolor: Edge color for the base.
        :param base_facecolor: Face color for the base.
        :param detail_visible_percent: Percentage of the detail visibility required for it to be visible on the screen.
        :param text_visible_percent: Percentage of text visibility required for it to be visible on the screen.
        :param name_fontsize: Font size for detail names.
        :param size_fontsize: Font size for detail sizes.
        :param convert_digits_to_subscript: A boolean parameter indicating whether to convert digits in the
            detail names to subscript format.
        """
        if detail_colors is None:
            detail_colors = {}
        self.detail_colors = detail_colors
        self.hover_detail_color = hover_detail_color
        self.detail_edgecolor = detail_edgecolor
        self.text_color = text_color
        self.base_edgecolor = base_edgecolor
        self.base_facecolor = base_facecolor
        self.detail_visible_percent = self._validate_percent(detail_visible_percent)
        self.text_visible_percent = self._validate_percent(text_visible_percent)
        self.name_fontsize = name_fontsize
        self.size_fontsize = size_fontsize
        self.convert_digits_to_subscript = convert_digits_to_subscript

    @staticmethod
    def _validate_percent(value: float) -> float:
        """
        Validate that the percentage value is between 0 and 100.

        :param value: The value to validate.
        :return: The validated value.
        :raises ValueError: If the value is not within the range [0, 100].
        """
        if not (0.0 <= value <= 100.0):
            raise ValueError("Percentage values must be between 0 and 100.")
        return value
