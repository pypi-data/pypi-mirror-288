import logging

from almanak.interface.environment import EnvironmentInterface
from almanak.interface.environment_helper import EnvironmentHelperInterface
from almanak.interface.metric_helper import MetricHelperInterface


class TestEthereumEnvironment(EnvironmentInterface):
    logger = logging.getLogger(__name__)

    def __init__(self, environment_helper: EnvironmentHelperInterface, metric_helper: MetricHelperInterface):
        self.environment = environment_helper

    def environment_initialization(self):
        self.logger.info('Environment initialization')

    def environment_pre_step(self):
        self.logger.info('Environment pre step')

    def environment_post_step(self):
        self.logger.info('Environment post step')

    def environment_teardown(self):
        self.logger.info('Environment teardown')
