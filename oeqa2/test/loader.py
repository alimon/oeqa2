import os
import sys
import unittest

from .case import OETestCase
from .decorator import OETestDecorator, OETestDepends

def _make_failed_test(classname, methodname, exception, suiteClass):
    """
        When loading tests unittest framework stores the exception in a new
        class created for be displayed into run().

        For our purposes will be better to raise the exception in loading 
        step instead of wait to run the test suite.
    """
    raise exception
unittest.loader._make_failed_test = _make_failed_test

def _add_depends(registry, case, depends):
    module_name = case.__module__
    class_name = case.__class__.__name__

    case_id = case.id()

    for depend in depends:
        dparts = depend.split('.')

        if len(dparts) == 1:
            depend_id = ".".join((module_name, class_name, dparts[0]))
        elif len(dparts) == 2:
            depend_id = ".".join((module_name, dparts[0], dparts[1]))
        else:
            depend_id = depend

        if not case_id in registry:
            registry[case_id] = []
        if not depend_id in registry[case_id]:
            registry[case_id].append(depend_id)

def _validate_test_case_depends(cases, depends):
    for case in depends:
        for dep in depends[case]:
            if not dep in cases:
                raise Exception("TestCase %s depends on %s and isn't available, "\
                       "cases available %s." % (case, dep, str(cases.keys())))

def _order_test_case_by_depends(cases, depends):
    def _dep_resolve(graph, node, resolved, seen):
        seen.append(node)
        for edge in graph[node]:
            if edge not in resolved:
                if edge in seen:
                    raise RuntimeError("Test cases %s and %s have a circular" \
                                       " dependency." % (node, edge))
                _dep_resolve(graph, edge, resolved, seen)
        resolved.append(node)

    dep_graph = {}
    dep_graph['__root__'] = cases.keys()
    for case in cases:
        if case in depends:
            dep_graph[case] = depends[case]
        else:
            dep_graph[case] = []

    cases_ordered = []
    _dep_resolve(dep_graph, '__root__', cases_ordered, [])
    cases_ordered.remove('__root__')

    return [cases[case_id] for case_id in cases_ordered]

class OETestLoader(unittest.TestLoader):
    caseClass = OETestCase

    _registry = {}
    _registry['cases'] = {}
    _registry['depends'] = {}

    kwargs_names = ['testMethodPrefix', 'sortTestMethodUsing', 'suiteClass',
            '_top_level_dir']

    def __init__(self, tc, module_path, modules, modules_required,
            *args, **kwargs):
        self.tc = tc

        self.module_path = module_path
        self.modules = modules
        self.modules_required = modules_required

        for kwname in self.kwargs_names:
            if kwname in kwargs:
                setattr(self, kwname, kwargs[kwname])

    def _registerTestCase(self, case):
        case_id = case.id()
        self._registry['cases'][case_id] = case

    def _handleTestCaseDecorators(self, case):
        def _handle(obj):
            if isinstance(obj, OETestDecorator):
                obj.bind(case)

                if isinstance(obj, OETestDepends):
                    _add_depends(self._registry['depends'], case,
                            obj.depends)

        def _walk_closure(obj):
            if hasattr(obj, '__closure__') and obj.__closure__:
                for f in obj.__closure__:
                    obj = f.cell_contents
                    _handle(obj)
                    _walk_closure(obj)

        method = getattr(case, case._testMethodName, None)
        _walk_closure(method)

    def loadTestsFromTestCase(self, testCaseClass):
        """Return a suite of all tests cases contained in testCaseClass"""
        if issubclass(testCaseClass, unittest.suite.TestSuite):
            raise TypeError("Test cases should not be derived from TestSuite." \
                                " Maybe you meant to derive from TestCase?")
        if not issubclass(testCaseClass, self.caseClass):
            raise TypeError("Test cases need to be derived from %s" % \
                    caseClass.__name__)

        testCaseNames = self.getTestCaseNames(testCaseClass)
        if not testCaseNames and hasattr(testCaseClass, 'runTest'):
            testCaseNames = ['runTest']

        ####
        suite = [testCaseClass(self.tc, tcname)
                for tcname in testCaseNames]
        for case in suite:
            self._registerTestCase(case)
            self._handleTestCaseDecorators(case)
        ####

        loaded_suite = self.suiteClass(suite)
        return loaded_suite

    def loadTestsFromModule(self, module, use_load_tests=True):
        if not self.modules or "all" in self.modules or \
                module.__name__ in self.modules:
            return super(OETestLoader, self).loadTestsFromModule(
                    module, use_load_tests)
        else:
            return self.suiteClass()

    def discover(self):
        suite = super(OETestLoader, self).discover(self.module_path,
                pattern='*.py')

        _validate_test_case_depends(self._registry['cases'],
                self._registry['depends'])
        cases = _order_test_case_by_depends(self._registry['cases'],
                self._registry['depends'])

        return self.suiteClass(cases)
