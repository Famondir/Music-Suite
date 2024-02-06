#   -*- coding: utf-8 -*-
from pybuilder.core import use_plugin, init

use_plugin("python.core")
# use_plugin('pypi:pybuilder_pytest')
use_plugin("python.unittest")
use_plugin("python.flake8")
use_plugin("python.coverage")
# use_plugin('pypi:pybuilder_pytest_coverage')
use_plugin("python.distutils")


name = "Music-Suite"
default_task = "publish"


@init
def set_properties(project):
    # project.set_property_if_unset("pytest_coverage_break_build_threshold", 0)
    project.set_property("coverage_break_build", False)
