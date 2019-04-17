# Példa osztály
class Foo:
    """Documentation string"""
    i = 5

    # __init__ függvény gyakorlatilag a constructor
    def __init__(self):
        self.array = []

    def do_something(self):
        return 'Hello world'

    def do_something_with_self(self):
        print(self.array)  # self mindig kell, ha egy member-t szeretnénk elérni

    @staticmethod
    def something_static():
        print('this is a static function')

    @classmethod
    def new_with_existings(cls):
        instance = cls()
        instance.array.append('existing')
        return instance


foo = Foo()
foo.array.append('alma')
print(foo.array)
# Elérhetjük a static változókat instancen és class namespacen keresztül is
print(foo.i)
print(Foo.i)
foo.do_something_with_self()
Foo.something_static()
existing = Foo.new_with_existings()
print(existing.array)


# Egyszeres leszármaztatás
class BaseClass:
    def __init__(self):
        self.i = 5


class DerivedClass(BaseClass):
    def __init__(self):
        BaseClass.__init__(self)


derived = DerivedClass()
print(derived.i)

print(f'derived isinstance of BaseClass={isinstance(derived, BaseClass)}')  # Példány egy BaseClass példány?
print(f'DerivedClass issubclass of BaseClass={issubclass(DerivedClass, BaseClass)}')  # DerivedClass egy BaseClass leszármazott?


# Többszörös öröklődés
class BaseClassA:
    def something(self):
        print('something in BaseClassA')


class BaseClassB:
    def something(self):
        print('something in BaseClassB')


class MultipleDerived(BaseClassA, BaseClassB):
    pass


multiple_derived = MultipleDerived()
multiple_derived.something()


# Name mangling
class ClassWithPrivate:
    def __init__(self):
        self.__update()

    def __update(self):
        print('update')


with_private = ClassWithPrivate()
# AttributeError: 'ClassWithPrivate' object has no attribute '__update'
# with_private.__update()
