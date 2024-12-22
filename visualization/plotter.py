import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseEvent
from matplotlib.patches import Rectangle
from detail.detail import Detail
from visualization.settings import PlotSettings
import numpy as np


class Plotter:
    """
    A class for visualizing detail on a base detail using matplotlib.
    It allows users to add detail, customize plot settings, and interact with the plot.

    Attributes:
        base_detail (Detail): The base detail on which other details will be placed.
        details (list[Detail]): A list of Detail objects to be placed on the base detail.
        plot_settings (PlotSettings): Plot settings controlling the appearance of the plot.
        fig (matplotlib.figure.Figure): The figure object representing the entire plot.
        ax (matplotlib.axes.Axes): The axes object representing the plot area.
        hovered_detail (Detail): The detail currently being hovered by the mouse, if any.
    """

    def __init__(self, base_detail: Detail, details: list[Detail], plot_settings: PlotSettings = None):
        """
        Initialize the plotter.

        :param base_detail: The base detail on which the other detail will be placed.
        :param details: A list of Detail objects to be placed on the base detail.
        :param plot_settings: Optional plot settings. If not provided, default settings will be used.
        """
        self.base_detail = base_detail
        self.details = details
        self.plot_settings = plot_settings or PlotSettings()
        self.fig, self.ax = plt.subplots()
        self.hovered_detail = None
        self._setup_plot()

    def _setup_plot(self) -> None:
        """
        Set up the plot by adding detail on it, assigning colors to detail, adding attributes,
        and connecting events for interactivity.
        """
        base_rectangle = Rectangle(self.base_detail.bottom_left, self.base_detail.width, self.base_detail.height,
                                   edgecolor=self.plot_settings.base_edgecolor,
                                   facecolor=self.plot_settings.base_facecolor)
        self.ax.add_patch(base_rectangle)
        self._set_detail_colors()
        self._add_attributes()
        for detail in self.details:
            if not (self._is_detail_out_of_screen(detail) or self._is_detail_small(detail)):
                self._add_detail(detail)
            if not (self._is_text_out_of_screen(detail) or self._is_text_small(detail)):
                self._add_text_name(detail)
        self.ax.axis('equal')
        self.ax.set_xlim(self.base_detail.bottom_left[0], self.base_detail.top_right[0])
        self.ax.set_ylim(self.base_detail.bottom_left[1], self.base_detail.top_right[1])
        self.ax.figure.canvas.mpl_connect('motion_notify_event', self._on_hover_highlight_detail)
        self.ax.figure.canvas.mpl_connect('motion_notify_event', self._on_motion_change_details)
        self.ax.figure.canvas.mpl_connect('motion_notify_event', self._on_motion_change_text)
        plt.axis('off')

    def _set_detail_colors(self) -> None:
        """
        Assign colors to each type of detail. If a color is not specified for a detail type, a random color is
        generated.
        """
        detail_types = set(detail.detail_type for detail in self.details)
        for detail_type in detail_types:
            if detail_type not in self.plot_settings.detail_colors:
                self.plot_settings.detail_colors[detail_type] = tuple(np.random.rand(3, ))

    def _add_attributes(self) -> None:
        """
        Add attributes to each detail object necessary for graphical representation.
        These attributes include the rectangle representing the detail on the plot,
        and the text associated with the detail (name, width and height).
        """
        for detail in self.details:
            detail.rectangle = None
            detail.text_name = None
            detail.text_width = None
            detail.text_height = None

    def _add_detail(self, detail: Detail) -> None:
        """
        Add a graphical representation of the given detail to the plot.

        :param detail: The detail to be added to the plot.
        """
        rectangle = Rectangle(detail.bottom_left, detail.width, detail.height,
                              edgecolor=self.plot_settings.detail_edgecolor,
                              facecolor=self.plot_settings.detail_colors[detail.detail_type])
        detail.rectangle = rectangle
        self.ax.add_patch(rectangle)

    def _add_text_name(self, detail: Detail) -> None:
        """
        Add text label with detail name to the center of the detail.

        :param detail: The detail for which the text label is to be added.
        """
        x = (detail.bottom_left[0] + detail.top_right[0]) / 2
        y = (detail.bottom_left[1] + detail.top_right[1]) / 2
        detail_name = self._convert_digits_to_subscript(detail.name) \
            if self.plot_settings.convert_digits_to_subscript else detail.name
        detail.text_name = self.ax.text(x, y, f"{detail_name}", ha='center', va='center',
                                        color=self.plot_settings.text_color,
                                        fontsize=self.plot_settings.name_fontsize)

    def _add_text_width_and_text_height(self, detail: Detail) -> None:
        """
        Add text labels with detail's width and height to the plot.

        :param detail: The detail for which the text labels are to be added.
        :return: None
        """
        x = (detail.bottom_left[0] + detail.top_right[0]) / 2
        y = ((detail.bottom_left[1] + detail.top_right[1]) / 2 + detail.top_right[1]) / 2
        detail.text_width = self.ax.text(x, detail.bottom_left[1], f"{detail.width}", ha='center',
                                         va='bottom', color=self.plot_settings.text_color,
                                         fontsize=self.plot_settings.size_fontsize)
        detail.text_height = self.ax.text(detail.bottom_left[0], y, f"{detail.height}", ha='right',
                                          va='center', color=self.plot_settings.text_color,
                                          fontsize=self.plot_settings.size_fontsize)

    def _on_hover_highlight_detail(self, event: MouseEvent) -> None:
        """
        Highlight the detail hovered by the mouse and restore standard color for others.

        This function is called when the mouse hovers over the plot. It checks if the mouse pointer is within
        the boundaries of any detail on the plot. If so, it changes the color of that detail to highlight it.
        If the mouse moves away from the detail, its color is restored to the standard color for detail of that type.

        :param event: The mouse event triggered when hovering over the plot.
        """
        if event.inaxes == self.ax:
            for detail in self.details:
                if detail.rectangle is None:
                    continue
                if detail.bottom_left[0] <= event.xdata <= detail.top_right[0] and \
                        detail.bottom_left[1] <= event.ydata <= detail.top_right[1]:
                    if detail != self.hovered_detail:
                        self._change_detail(True, detail)
                        if self.hovered_detail:
                            self._change_detail(False, self.hovered_detail)
                        self.hovered_detail = detail
                    return
        if self.hovered_detail:
            self._change_detail(False, self.hovered_detail)
            self.hovered_detail = None

    def _change_detail(self, is_hovered: bool, detail: Detail) -> None:
        """
        Change the appearance of the detail based on whether it is hovered by the mouse or not.

        If the detail is hovered, function changes its color to a specified hover color
        and adds text labels with the detail's name, width, and height. If the detail is not hovered,
        it restores its original color and removes the text labels.

        :param is_hovered: A boolean indicating whether the detail is hovered by the mouse.
        :param detail: The detail for which the appearance is to be changed.
        """
        color = self.plot_settings.hover_detail_color if is_hovered else \
            self.plot_settings.detail_colors[self.hovered_detail.detail_type]
        if detail.rectangle is not None:
            detail.rectangle.set_facecolor(color)
        self.ax.figure.canvas.draw_idle()
        if is_hovered:
            if detail.text_name is None:
                self._add_text_name(detail)
            if detail.text_width is None:
                self._add_text_width_and_text_height(detail)
        else:
            if detail.text_width is not None:
                detail.text_width.remove()
                detail.text_width = None
                detail.text_height.remove()
                detail.text_height = None

    def _on_motion_change_details(self, event: MouseEvent) -> None:
        """
        Update the plot by removing small and out-of-screen detail and adding visible detail.

        This function is triggered when mouse motion is detected. It updates the plot by removing detail that are
        too small or out of the current visible area and adds detail that are within the visible area and big enough.

        :param event: The mouse event that triggered the function.
        """
        for detail in self.details:
            if self._is_detail_out_of_screen(detail) or self._is_detail_small(detail):
                if detail.rectangle is not None:
                    detail.rectangle.remove()
                    detail.rectangle = None
            else:
                if detail.rectangle is None:
                    self._add_detail(detail)

    def _on_motion_change_text(self, event: MouseEvent) -> None:
        """
        Update the plot by removing small and out-of-screen text and adding visible text.

        This function is triggered when mouse motion is detected. It updates the plot by removing texts with
        detail name that are too small or out of the current visible area if mouse is not hovering over
        the corresponding detail and adds text that are within the visible area and big enough.

        :param event: The mouse event that triggered the function.
        """
        for detail in self.details:
            if (self._is_text_out_of_screen(detail) or self._is_text_small(
                    detail)) and not detail == self.hovered_detail:
                if detail.text_name is not None:
                    detail.text_name.remove()
                    detail.text_name = None
            else:
                if detail.text_name is None:
                    self._add_text_name(detail)

    def _is_detail_out_of_screen(self, detail: Detail) -> bool:
        """
        Check if the detail is out of the visible area of the screen.
        If the entire detail is outside the visible area, the function returns True, otherwise it returns False.

        :param detail: The detail to be checked.
        :return: A boolean indicating whether the detail is out of the visible part of the screen.
        """
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        x1, y1 = detail.bottom_left
        x2, y2 = detail.top_right
        return x2 < xlim[0] or x1 > xlim[1] or y2 < ylim[0] or y1 > ylim[1]

    def _is_detail_small(self, detail: Detail) -> bool:
        """
        Check if the given detail is too small relative to the visible area of the screen.

        This function determines whether the dimensions of the given detail are too small compared to
        the visible area of the plot screen. It calculates the percentage of the visible area occupied
        by the detail's width and height relative to the total width and height of the visible area.
        If either the width or the height of the detail is less than the specified percentage of
        the visible area, the function returns True, otherwise it returns False.

        :param detail: The detail to be checked.
        :return: A boolean indicating whether the detail is too small relative to the visible area of the screen.
        """
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        return detail.width < (xlim[1] - xlim[0]) * self.plot_settings.detail_visible_percent / 100 or \
               detail.height < (ylim[1] - ylim[0]) * self.plot_settings.detail_visible_percent / 100

    def _is_text_out_of_screen(self, detail: Detail) -> bool:
        """
        Check if the text name of the given detail is out of the visible area of the screen.
        If text is outside the visible area, the function returns True, otherwise it returns False.

        :param detail: The detail whose text name is to be checked.
        :return: A boolean indicating whether the text name of the detail is out of the visible part of the screen.
        """
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        x = (detail.bottom_left[0] + detail.top_right[0]) / 2
        y = (detail.bottom_left[1] + detail.top_right[1]) / 2
        return x < xlim[0] or x > xlim[1] or y < ylim[0] or y > ylim[1]

    def _is_text_small(self, detail: Detail) -> bool:
        """
        Check if the text name of the given detail is too small relative to the visible area of the screen.

        This function determines whether the length of the text name of the given detail is too small
        compared to the visible area of the plot screen. It calculates the percentage of the visible area occupied
        by the detail relative to the total width of the visible area. If the width of the detail
        is less than the specified percentage of the visible area, the function returns True, otherwise it
        returns False.

        :param detail: The detail whose text name is to be checked.
        :return: A boolean indicating whether the text name of the detail is too small relative to the visible area
        of the screen.
        """
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        return detail.width < (xlim[1] - xlim[0]) * self.plot_settings.text_visible_percent / 100 or \
               detail.height < (ylim[1] - ylim[0]) * self.plot_settings.detail_visible_percent / 100

    @staticmethod
    def _convert_digits_to_subscript(name: str) -> str:
        """
        Convert all digits in the detail name to subscript.

        :param name: The name of the detail.
        :return: The modified name with digits converted to subscript.
        """
        subscript = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        return ''.join(c.translate(subscript) if c.isdigit() else c for c in name)

    def zoom_to_detail(self, detail: Detail) -> None:
        """
        Zoom the plot to show the position of a specific detail.

        :param detail: The Detail object whose position needs to be shown.
        """
        if detail in self.details:
            margin_x = (detail.top_right[0] - detail.bottom_left[0]) * 0.1
            margin_y = (detail.top_right[1] - detail.bottom_left[1]) * 0.1
            self.ax.set_xlim(detail.bottom_left[0] - margin_x, detail.top_right[0] + margin_x)
            self.ax.set_ylim(detail.bottom_left[1] - margin_y, detail.top_right[1] + margin_y)

    def plot(self) -> None:
        """
        Display the plot with the placed details.
        """
        plt.show()
