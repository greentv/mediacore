# import py.test

# from mediacore import ipython
# from mediacore.plugin.abc import AbstractClass, abstractmethod, abstractproperty, ImplementationError, _reset_registry

# def pytest_funcarg__AbstractStuff(request):
#     class AbstractStuff(AbstractClass):
#         @abstractmethod
#         def do_stuff(self):
#             pass
#     return AbstractStuff

# def test_register(AbstractStuff):
#     class StuffDoer(AbstractStuff):
#         def do_stuff(self):
#             return True
#     AbstractStuff.register(StuffDoer)
#     stuffs = list(AbstractStuff)
#     assert len(stuffs) == 1
#     assert stuffs[0] is StuffDoer
#     _reset_registry()

# def test_register_multiple_interfaces(AbstractStuff):
#     class StuffDoer(AbstractStuff):
#         def do_stuff(self):
#             return True
#     AbstractStuff.register(StuffDoer)

#     class AbstractMoreStuff(AbstractStuff):
#         @abstractmethod
#         def do_more_stuff(self):
#             pass
#     class MoreStuffDoer(AbstractMoreStuff):
#         def do_stuff(self):
#             return True
#         def do_more_stuff(self):
#             return True
#     AbstractMoreStuff.register(MoreStuffDoer)

#     assert set(AbstractStuff) == set([StuffDoer, MoreStuffDoer])
#     assert set(AbstractMoreStuff) == set([MoreStuffDoer])
#     _reset_registry()

# def test_implementation_checking(AbstractStuff):
#     class StuffDoer(AbstractStuff):
#         pass
#     py.test.raises(ImplementationError, lambda: AbstractStuff.register(StuffDoer))
#     _reset_registry()


######################################################################

import unittest

class TestAbstractClass(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

class TestAbstractMethod(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def _callFUT(self, func):
        from mediacore.plugin.abc import abstractmethod
        return abstractmethod(func)

    def test_attribute(self):
        marker = object()
        def dummyfunc():
            return marker

        a_dummyfunc = self._callFUT(dummyfunc)

        self.assertEqual(a_dummyfunc(), marker)
        self.assertEqual(a_dummyfunc._isabstract, True)

    def test_isabstract(self):
        from mediacore.plugin.abc import abstractmethod
        from mediacore.plugin.abc import isabstract
        
        @abstractmethod
        def dummyfunc():
            pass

        self.assertEqual(isabstract(dummyfunc), True)

    
class TestAbstractProperty(unittest.TestCase):

    def _makeOne(self):
        from mediacore.plugin.abc import abstractproperty
        return abstractproperty()

    def test_attribute(self):
        prop = self._makeOne()
        
        self.assertEqual(prop._isabstract, True)

    def test_isabstract(self):
        from mediacore.plugin.abc import isabstract

        prop = self._makeOne()

        self.assertEqual(isabstract(prop), True)

    
class Test_isabstract(unittest.TestCase):

    def _callFUT(self, x):
        from mediacore.plugin.abc import isabstract
        return isabstract(x)

    def test_not_implemented(self):
        marker = object()

        self.assertRaises(NotImplementedError, self._callFUT, marker)
        
    def test_property(self):
        pass

    def test_method(self):
        pass

    def test_class(self):
        pass



class TestAbstractClass(unittest.TestCase):

    def setUp(self):
        from mediacore.plugin.abc import _reset_registry
        _reset_registry()

    def tearDown(self):
        from mediacore.plugin.abc import _reset_registry
        _reset_registry()

    def _makeOne(self):
        from mediacore.plugin.abc import AbstractClass, abstractproperty, abstractmethod

        class DummyAbstractClass(AbstractClass):
            prop = abstractproperty()
            
            @abstractmethod
            def meth(self):
                pass

        return DummyAbstractClass
        
    def _makeImplementation(self, c):
        class DummyAbstractClassImplementation(c):
            prop = 'prop'
    
            def meth(self):
                return 'meth'

        return DummyAbstractClassImplementation
        
    def test_isabstract(self):
        from mediacore.plugin.abc import isabstract
        c = self._makeOne()
        self.assertEqual(isabstract(c), True)
        
    def test_imp_isabstract(self):
        from mediacore.plugin.abc import isabstract
        c = self._makeOne()
        imp = self._makeImplementation(c)
        self.assertEqual(isabstract(imp), False)
    
    def test_register(self):
        c = self._makeOne()
        imp = self._makeImplementation(c)
        self.assertEqual(imp in c, False)
        c.register(imp)
        self.assertEqual(imp in c, True)
        
    def test_bad_implementation(self):
        c = self._makeOne()
        from mediacore.plugin.abc import ImplementationError
        class NotAbstract(c):
            pass
        
        self.assertEqual(NotAbstract in c, False)
        self.assertRaises(ImplementationError, c.register, NotAbstract)
        #c.register(NotAbstract)
        self.assertEqual(NotAbstract in c, False)

    def test_add_register_observer(self):
        cl = self._makeOne()
        imp = self._makeImplementation(cl)
        events = []
        def log_event(c):
            events.append(c)

        cl.add_register_observer(log_event)
        cl.register(imp)

        self.assertEqual(events, [imp])
        
    def test_remove_register_observer(self):
        cl = self._makeOne()
        imp = self._makeImplementation(cl)
        events = []
        def log_event(c):
            events.append(c)
        
        cl.add_register_observer(log_event)
        cl.remove_register_observer(log_event)
        cl.register(imp)

        self.assertEqual(events, [])
        


