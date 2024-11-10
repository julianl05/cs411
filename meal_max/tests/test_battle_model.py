import pytest
from unittest.mock import ANY
from contextlib import contextmanager


from meal_max.models.battle_model import *
from meal_max.models.kitchen_model import *


@pytest.fixture()
def battle_model():
    """Fixture to provide a new instance of BattleModel for each test."""
    return BattleModel()

"""Fixture providing sample songs for the tests."""
@pytest.fixture
def sample_meal1():
    return Meal(1, 'Spaghetti Bolognese', 'Italian', 15, 'MED')

@pytest.fixture
def sample_meal2():
    return Meal(2, 'Pizza', 'Italian', 12, 'LOW')

@pytest.fixture
def sample_meal2():
    return Meal(3, 'Sushi', 'Japanese', 12, 'HIGH')


@pytest.fixture
def mock_cursor(mocker):
    mock_conn = mocker.Mock()
    mock_cursor = mocker.Mock()

    # Mock the connection's cursor
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None  # Default return for queries
    mock_cursor.fetchall.return_value = []
    mock_conn.commit.return_value = None

    # Mock the get_db_connection context manager from sql_utils
    @contextmanager
    def mock_get_db_connection():
        yield mock_conn  # Yield the mocked connection object

    mocker.patch('meal_max.models.kitchen_model.get_db_connection', mock_get_db_connection)

    return mock_cursor  # Return the mock cursor so we can set expectations per test

@pytest.fixture
def mock_update_meal_stats(mocker):
    """Mock the update_play_count function for testing purposes."""
    return mocker.patch("meal_max.models.battle_model.update_meal_stats")

def test_battle(battle_model, sample_meal1, sample_meal2, mock_update_meal_stats, mock_cursor):
    """ Tests whether Battle method:
        1) Raises the correct error if not enough combatants are present
        2) Returns a winner of the battle
        3) Removes the loser of the battle from the instance of BattleModel()
    """
    #logger = logging.getLogger(__name__)
    #configure_logger(logger)
    #DB_PATH = os.getenv("DB_PATH", "/sql/meal_max.db")
    mock_cursor.fetchone.return_value = [False]

    battle_model.prep_combatant(sample_meal1)
    assert len(battle_model.combatants) == 1, "Expected only 1 meal to be added as a combatant"
    battle_model.prep_combatant(sample_meal2)
    assert len(battle_model.combatants) == 2, "Expected only 2 meals to be added as combatants"
    # with pytest.raises(ValueError, match="Two combatants must be prepped for a battle."):
    
    a = battle_model.battle()

    mock_update_meal_stats.assert_called_with(ANY, ANY)
    mock_update_meal_stats.assert_called_with(ANY, ANY)
    

    assert a == sample_meal1.meal or a == sample_meal2.meal, "Expected winner to be a meal name from the list of combatants"
    #assert isinstance(a, str), "Expected string to be returned""
    assert len(battle_model.combatants) == 1,"Expected the loser to be removed from instance of BattleModel "


def test_battle_too_little_combatants(battle_model, sample_meal1, mock_cursor):
    """ Tests whether the battle() method raises the correct error when more than two combatants are present."""
    mock_cursor.fetchone.return_value = [False]
    battle_model.prep_combatant(sample_meal1)

    with pytest.raises(ValueError, match="Two combatants must be prepped for a battle."):
        battle_model.battle()


def test_battle_empty_combatants(battle_model, mock_cursor):
    """ Tests whether the battle() method raises the correct error when more than two combatants are present."""
    mock_cursor.fetchone.return_value = [False]

    with pytest.raises(ValueError, match="Two combatants must be prepped for a battle."):
        battle_model.battle()


def test_clear_combatants_empty(battle_model):
    """ Tests whether the clear_combatants() method in the BattleModel class works on an instance of that class with
        no combatants
    """
    a = battle_model.clear_combatants()
    assert a == None, "Expected all combatants to be cleared"
#end test

def test_clear_combatants_one(battle_model, sample_meal1):
    """ Tests whether the clear_combatants() method in the BattleModel class works on an instance of that class with
        one combatant
    """
    battle_model.prep_combatant(sample_meal1)
    a = battle_model.clear_combatants()
    assert a ==None, "Expected all combatants to be cleared"
#end test

def test_clear_combatants_empty(battle_model, sample_meal1, sample_meal2):
    """ Tests whether the clear_combatants() method in the BattleModel class works on an instance of that class with
        two combatants
    """
    battle_model.prep_combatant(sample_meal1)
    battle_model.prep_combatant(sample_meal2)
    a = battle_model.clear_combatants()
    assert a ==None, "Expected all combatants to be cleared"
#end test

def test_get_battle_score(battle_model, sample_meal1):
    """ Tests whether the get_battle_score() outputs correct score as per formula below"""

    difficulty_modifier = {"HIGH": 1, "MED": 2, "LOW": 3}
    score = (sample_meal1.price * len(sample_meal1.cuisine)) - difficulty_modifier[sample_meal1.difficulty]

    a = battle_model.get_battle_score(sample_meal1)
    assert score == a, "Expected scores to be the same."
#end test


def test_get_combatants_zero(battle_model):
    """ Tests whether the get_combatants() method returns the correct results with zero combatants."""
    assert len(battle_model.get_combatants())==0, "Expected only one combatant to be returned"
#end test 

def test_get_combatants_one(battle_model, sample_meal1):
    """ Tests whether the get_combatants() method returns one combatant and if return result is of type Meal"""
    battle_model.prep_combatant(sample_meal1)
    a = battle_model.get_combatants()
    assert len(a) == 1, "Expected only one combatant to be returned"
    assert isinstance(a[-1], Meal), "Expected returned element to be of type Meal"
# end test

def test_get_combatants_two(battle_model, sample_meal1, sample_meal2):
    """ Tests whether the get_combatants() method returns two combatants and if return result is of type Meal"""
    battle_model.prep_combatant(sample_meal1)
    battle_model.prep_combatant(sample_meal2)

    a = battle_model.get_combatants()
    assert len(a) == 2, "Expected only one combatant to be returned"
    assert isinstance(a[-1], Meal), "Expected returned element to be of type Meal"
# end test

def test_prep_combatant(battle_model, sample_meal1, sample_meal2):
    """ Tests whether prep_combatant() can successfully add meals to an empty instance of BattleModel."""
    battle_model.prep_combatant(sample_meal1)
    assert len(battle_model.combatants) ==1, "Expected only 1 meal to be added as a combatant"

    battle_model.prep_combatant(sample_meal2)
    assert len(battle_model.combatants) == 2, "Expected only 2 meals to be added as combatants"
#end test

def test_error_prep_combatant(battle_model, sample_meal1, sample_meal2):
    """ Tests whether prep_combatant() raises the correct error when a third combatant is added to an instance of
        BattleModel
    """
    battle_model.prep_combatant(sample_meal1)
    battle_model.prep_combatant(sample_meal2)
    with pytest.raises(ValueError, match="Combatant list is full, cannot add more combatants."):
        battle_model.prep_combatant(sample_meal2)
#end test

