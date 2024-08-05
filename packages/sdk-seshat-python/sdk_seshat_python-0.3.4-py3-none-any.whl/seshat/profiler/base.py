import cProfile
import inspect
import logging
import os
import pathlib
import pstats
import time
from dataclasses import dataclass, field
from io import StringIO
from typing import Callable
from typing import Literal

from memory_profiler import profile as mem_profile, memory_usage

from seshat.profiler.decorator import track
from seshat.transformer import Transformer
from seshat.utils.patching import patch

LogLevel = Literal[
    logging.INFO, logging.DEBUG, logging.WARNING, logging.ERROR, logging.CRITICAL
]


@dataclass
class MemProfileConfig:
    log_path: str | None
    enable: bool = True


@dataclass
class CProfileConfig:
    log_path: str | None
    enable: bool = True


@dataclass
class ProfileConfig:
    log_level: LogLevel
    log_dir: str = "./logs"
    show_in_console: bool = True
    default_tracking: bool = True
    mem_profile_conf: MemProfileConfig = field(
        default_factory=lambda: MemProfileConfig(log_path=None, enable=False)
    )
    cprofile_conf: CProfileConfig = field(
        default_factory=lambda: CProfileConfig(log_path=None, enable=False)
    )


class Profiler:
    config: ProfileConfig

    _cprofile_stats: pstats.Stats = pstats.Stats()
    _logger: logging.Logger
    _mem_logs = StringIO()

    def run(self, func: Callable, *args, **kwargs):
        method_log = func.__qualname__
        extra = {"method_path": self.get_func_path(func)}
        try:
            self.log("info", description=f"start {method_log}", extra=extra)
            if self.config.mem_profile_conf.enable:
                func = mem_profile(func, stream=self._mem_logs)

            init_mem_usage = memory_usage()[0]
            with cProfile.Profile() as individual_cprofile:
                start = time.time()
                result = func(*args, **kwargs)
                end = time.time()
            final_mem_usage = memory_usage()[0]

            self._cprofile_stats.add(individual_cprofile)
            time_spent = self.get_spent_time(func, individual_cprofile)

            self.log(
                "info",
                description=f"finish {method_log}",
                mem_change=final_mem_usage - init_mem_usage,
                time_spent=time_spent,
                cumulative_time_spent=end - start,
                extra=extra,
            )
            return result

        except Exception as exc:
            self.log("error", description=f"error in {method_log}: {exc}", extra=extra)
            self.tear_down()
            raise

    def tear_down(self):
        if not hasattr(self, "config"):
            return
        if self.config.mem_profile_conf.enable:
            self.save_mem_log()
        if self.config.cprofile_conf.enable:
            self.save_profile_log()

    def save_mem_log(self):
        self._mem_logs.seek(0)
        with open(
            self.get_log_path(self.config.mem_profile_conf.log_path), "w"
        ) as mem_file:
            mem_file.write(self._mem_logs.read())

    def save_profile_log(self):
        with open(self.get_log_path(self.config.cprofile_conf.log_path), "w") as stream:
            self.strip_cprofile(self._cprofile_stats)
            self._cprofile_stats.stream = stream
            self._cprofile_stats.sort_stats("time").print_stats()

    def strip_cprofile(self, stats):
        seshat_path = self.seshat_path
        for key in list(stats.stats.keys()):
            func_name, line, func = key
            if func_name.startswith(seshat_path):
                new_key = (func_name.replace(seshat_path, ""), line, func)
                stats.stats[new_key] = stats.stats.pop(key)
            else:
                stats.stats.pop(key)

    def log(
        self,
        level,
        description,
        mem_change=None,
        time_spent=None,
        cumulative_time_spent=None,
        *args,
        **kwargs,
    ):
        logger = getattr(self._logger, level)
        msg = f">>> {description}:"
        if mem_change:
            msg += f"\n - Memory Changing: {'+' if mem_change >= 0 else ''}{mem_change}"
        if time_spent:
            msg += f"\n - Time Spent in method itself: {time_spent}"
        if cumulative_time_spent:
            msg += f"\n - Cumulative Time Spent: {cumulative_time_spent}"
        msg += "\n"
        return logger(msg=msg, *args, **kwargs)

    @property
    def seshat_path(self):
        here = os.path.abspath(__file__)
        return os.path.dirname(os.path.dirname(here))

    def get_spent_time(self, func, cprofile):
        stat = pstats.Stats(cprofile)
        method = self.get_func_path(func, with_number=False)
        for k, info in stat.stats.items():
            if k[0] == method:
                return info[2]
        return None, None

    @staticmethod
    def get_func_path(func, with_number=True):
        source_path = inspect.getsourcefile(func)
        line_number = inspect.getsourcelines(func)[1]
        return f"{source_path}:{line_number}" if with_number else source_path

    @classmethod
    def setup_logging(cls, config: ProfileConfig):
        if getattr(cls, "_logger", None):
            return
        log_format = "%(asctime)s - %(levelname)s - %(message)s - %(method_path)s"
        logging.basicConfig(
            filename=cls.get_log_path("event.txt"),
            filemode="w",
            level=config.log_level,
            format=log_format,
        )
        if config.show_in_console:
            console = logging.StreamHandler()
            console.setLevel(level=config.log_level)
            console.setFormatter(logging.Formatter(log_format))
            logging.getLogger().addHandler(console)

        cls._logger = logging.getLogger()

    @classmethod
    def track_default_methods(cls):
        seshat_directory = pathlib.Path(__file__).parent.parent.resolve()
        cls.path_method(
            f"{seshat_directory}/transformer",
            "seshat.transformer.",
            {"__call__"},
            lambda klass, attr_name: issubclass(klass, Transformer)
            and attr_name.startswith(klass.HANDLER_NAME),
        )
        cls.path_method(
            f"{seshat_directory}/source",
            "seshat.source.",
            {"fetch", "save", "insert", "update", "copy", "create_table"},
        )
        cls.path_method(
            f"{seshat_directory}/data_class", "seshat.data_class.", {"convert"}
        )

    @classmethod
    def setup(cls, config: ProfileConfig):
        if config.log_dir:
            cls.ensure_dir_exists(config.log_dir)
        if config.default_tracking:
            cls.track_default_methods()
        cls.config = config
        cls.setup_logging(config)

    @staticmethod
    def ensure_dir_exists(path):
        if not os.path.exists(path):
            os.makedirs(path)

    @classmethod
    def get_log_path(cls, filename):
        return os.path.join(cls.config.log_dir, filename)

    @staticmethod
    def path_method(dirname, prefix, to_track, condition: Callable = lambda *_: False):
        return patch(track, **locals())


profiler = Profiler()
