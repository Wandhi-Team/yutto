from typing import Any


class aobject(object):
    """Inheriting this class allows you to define an async __ainit__.

    So you can create objects by doing something like `await MyClass(params)`
    Based on : https://stackoverflow.com/questions/33128325/how-to-set-class-attribute-with-await-in-init
    """

    async def __new__(cls, *args: Any, **kwargs: Any):
        instance = super().__new__(cls)
        await instance.__ainit__(*args, **kwargs)
        return instance

    async def __ainit__(self, *args: Any, **kwargs: Any):
        pass
