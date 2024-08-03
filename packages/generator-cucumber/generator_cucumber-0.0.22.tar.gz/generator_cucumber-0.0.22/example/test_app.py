from pytest_bdd import scenario, given, when, then

@scenario('test_app.feature', 'Начало всех начал')
def test_publish():
    pass

@given("Что-то там и там")
def author_user():
    pass

@given("И там и сям")
def article():
    pass

@when("О и здесь еще")
def go_to_article():
    pass

@when("Как-то так и этак")
def publish_article():
   pass

@then("И что думаешь об этом?")
def no_error_message():
   pass

@then("Пожалуй на этом все")
def article_is_published():
    pass