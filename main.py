from algorithm.slack_pack_algorithm import SlackPackAlgorithm
from core.detail_placer import DetailPlacer
from detail.detail import Detail
from detail.detail_generator import HarmonicSquareDetailGenerator
from statistic.listener.default_slack_pack_algorithm_listeners import LrpOccupancyRatioTracker, ExecutionTimeTracker
from statistic.output import ConsoleOutputHandler, FileOutputHandler
from storage.in_memory_box_storage import InMemoryBoxStorage
from visualization.plotter import Plotter
from visualization.settings import PlotSettings

# Example of using the main functionality

n0 = 100
gamma = 4 / 3
max_placed = 100
detail_generator = HarmonicSquareDetailGenerator(n0)
base_width, base_height = detail_generator.get_base_size()
base_bottom_left = (0, 0)
base_top_right = (base_bottom_left[0] + base_width, base_bottom_left[1] + base_height)
base_detail = Detail(base_bottom_left, base_top_right, 'LRP', 'lrp')
execution_time_tracker = ExecutionTimeTracker(10, ConsoleOutputHandler())
lrp_occupancy_ratio_tracker = LrpOccupancyRatioTracker(FileOutputHandler("files/lrp.txt", FileOutputHandler.OVERWRITE))
statistic_listeners = [execution_time_tracker, lrp_occupancy_ratio_tracker]
box_storage = InMemoryBoxStorage()
algorithm = SlackPackAlgorithm(gamma, n0, max_placed, box_storage, statistic_listeners=statistic_listeners,
                               update_placed_details=True)
detail_placer = DetailPlacer(algorithm, detail_generator, base_detail, max_placed)
placed_details = detail_placer.run_algorithm()
detail_colors = {"detail": "lightskyblue", "normal_box_1": "orange", "normal_box_2": "yellow", "endpoint_1": "green",
                 "endpoint_2": "lime", "lrp": "gray"}
plot_settings = PlotSettings(detail_colors=detail_colors, detail_visible_percent=1, text_visible_percent=5)
plotter = Plotter(base_detail, placed_details, plot_settings=plot_settings)
plotter.plot()
