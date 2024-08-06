from threading import Thread

from heimdall.lib.singleton.singleton import SingletonMeta


class Singleton(metaclass=SingletonMeta):
    value: str = None
    """
    We'll use this property to prove that our Singleton really works.
    """

    def __init__(self, value: str) -> None:
        self.value = value

    def some_business_logic(self):
        """
        Finally, any singleton should define some business logic, which can be
        executed on its instance.
        """


Singleton("BOOM")


def gen_singleton(value: str) -> None:
    Singleton(value)


def test_singleton():
    from time import sleep

    process1 = Thread(target=gen_singleton, args=("FOO",))
    process2 = Thread(target=gen_singleton, args=("BAR",))
    process1.start()
    sleep(0.001)
    process2.start()
    assert Singleton(value="BAZ").value == "BOOM"
