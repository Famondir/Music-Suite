#   -*- coding: utf-8 -*-
from pybuilder.core import use_plugin, init

use_plugin("python.core")
# use_plugin("python.unittest")
use_plugin('pypi:pybuilder_pytest')
use_plugin("python.flake8")
# use_plugin("python.coverage")
use_plugin('pypi:pybuilder_pytest_coverage')
use_plugin("python.distutils")
use_plugin("python.sonarqube")


name = "Music-Suite"
default_task = "publish"


@init
def set_properties(project):
    project.set_property("pytest_coverage_xml", True)
    project.get_property("pytest_extra_args").append("-x")
    # project.get_property("pytest_integration_extra_args").append("-x")
    
    project.set_property("pytest_coverage_break_build_threshold", 70)
    # project.set_property("coverage_break_build", False)
    
    # project.set_property('verbose', False)

    project.set_property("sonarqube_project_key", "musicsuitmusicsuite:2024e")
    # project.set_property("sonarqube_project_name", "Music Suite")