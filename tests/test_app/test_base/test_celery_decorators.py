from app.base.celery_decorators import task


def testWrappedFunctionWillStillBeCallable():
    @task()
    def f():
        return "foo"

    assert f() == "foo"
