Feature: random
    In order to test the semi-random module
    I test different functions

Scenario: shuffle
    Given a list containing 1 and 2
    When I call the 'shuffle' function on this list
    Then the list will contain 2 items
