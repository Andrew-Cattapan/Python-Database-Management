"""This program tests Assignment 13"""


import Assignment_13
import pytest


DATABASE = "Northwind.db"
SAMPLE_TABLE = [["Tatertots"], ["Regions"], ["WeIrDsTuFf"]]
dictionary_of_database_contents = {"Headings" : ['name'], "Rows" : [['Regions'], ['Territories'], ['Suppliers'], ['Categories'], ['Products'], ['Employees'], ['Customers'], ['Orders'], ['OrderDetails'], ['InternationalOrders'], ['EmployeesTerritories']]}
regions_with_columns = {"Column Widths" : [10, 19], "Headings" : ["RegionID", "RegionDescription"], "Rows" : [["1", "Eastern"], ["2", "Western"], ["3", "Northern"], ["4", "Southern"]]}
regions = {"Headings" : ["RegionID", "RegionDescription"], "Rows" : [["1", "Eastern"], ["2", "Western"], ["3", "Northern"], ["4", "Southern"]]}
results = {"row" : 3, "column" : 1, "choice" : "Southern", "ref choice" : '4'}


def test_get_input_valid():
    input_values = ["products", -1, 4, 0, 1]
    def input(prompt=None):
        return input_values.pop()
    Assignment_13.input = input
    assert Assignment_13.get_input(SAMPLE_TABLE) == "Tatertots"


def test_get_input_invalid():
    with pytest.raises(AssertionError):
        Assignment_13.get_input(23)
    with pytest.raises(AssertionError):
        Assignment_13.get_input(["not a", "list of", "lists"])


def test_get_dictionary_valid():
    assert Assignment_13.get_dictionary("SELECT name FROM sqlite_master WHERE type='table'") == dictionary_of_database_contents
    assert Assignment_13.get_dictionary("North") == "Database missing."


def test_get_dictionary_invalid():
    with pytest.raises(AssertionError):
        Assignment_13.get_dictionary(23)


def test_attach_column_widths_valid():
    assert Assignment_13.attach_column_widths(regions, "Regions") == regions_with_columns
    dictionary = {"Headings" : ["RegionID", "RegionDescription"], "Rows" : [["potatoes", "molasses"], ["it was", "a dream"]]}
    dictionary_with_columns = {"Column Widths" : [10, 19], "Headings" : ["RegionID", "RegionDescription"], "Rows" : [["potatoes", "molasses"], ["it was", "a dream"]]}
    assert Assignment_13.attach_column_widths(dictionary, "Regions") == dictionary_with_columns 


def test_attach_column_widths_invalid():
    not_a_dictionary = ["random", "list"]
    with pytest.raises(AssertionError):
        Assignment_13.attach_column_widths(not_a_dictionary, "Regions")
    dictionary_without_heading_lists = {"Headings" : 3}
    with pytest.raises(AssertionError):
        Assignment_13.attach_column_widths(dictionary_without_heading_lists, "Regions")
    dictionary_without_row_lists = {"Headings" : ["RegionID", "RegionDescription"], "Rows" : 5}
    with pytest.raises(AssertionError):
        Assignment_13.attach_column_widths(dictionary_without_row_lists, "Regions")
    not_a_list_of_lists = {"Headings" : ["RegionID", "RegionDescription"], "Rows" : [5, 3]}
    with pytest.raises(AssertionError):
        Assignment_13.attach_column_widths(not_a_list_of_lists, "Regions")
    not_the_same_length = {"Headings" : ["RegionID", "RegionDescription"], "Rows" : [["apples", "bananas", "THIRD THING THAT'S NOT SUPPOSED TO BE HERE"], ["whoa", "this"], ["is", "hard"]]}
    with pytest.raises(AssertionError):
        Assignment_13.attach_column_widths(not_the_same_length, "Regions")
    dictionary_valid = {"Headings" : ["RegionID", "RegionDescription"], "Rows" : [["no asserts", "should be"], ["raised by", "this"]]}
    with pytest.raises(AssertionError):
        Assignment_13.attach_column_widths(dictionary_valid, 5)


def test_display_table_valid():
    assert Assignment_13.display_table(regions, "Regions") == 4


def test_display_table_invalid():
    not_a_dictionary = ["random", "list"]
    with pytest.raises(AssertionError):
        Assignment_13.display_table(not_a_dictionary, "Regions")
    dictionary_without_heading_lists = {"Headings" : 3}
    with pytest.raises(AssertionError):
        Assignment_13.display_table(dictionary_without_heading_lists, "Regions")
    dictionary_without_row_lists = {"Headings" : ["RegionID", "RegionDescription"], "Rows" : 5}
    with pytest.raises(AssertionError):
        Assignment_13.display_table(dictionary_without_row_lists, "Regions")
    not_a_list_of_lists = {"Headings" : ["RegionID", "RegionDescription"], "Rows" : [5, 3]}
    with pytest.raises(AssertionError):
        Assignment_13.display_table(not_a_list_of_lists, "Regions")
    not_the_same_length = {"Headings" : ["RegionID", "RegionDescription"], "Rows" : [["apples", "bananas", "THIRD THING THAT'S NOT SUPPOSED TO BE HERE"], ["whoa", "this"], ["is", "hard"]]}
    with pytest.raises(AssertionError):
        Assignment_13.display_table(not_the_same_length, "Regions")
    dictionary_valid = {"Headings" : ["RegionID", "RegionDescription"], "Rows" : [["no asserts", "should be"], ["raised by", "this"]]}
    with pytest.raises(AssertionError):
        Assignment_13.display_table(dictionary_valid, 5)


def test_execute_sql_valid():
    assert Assignment_13.execute_sql("INSERT INTO Regions(RegionID, RegionDescription) VALUES(2003, 'Relient K');") == "Database found."
    assert Assignment_13.execute_sql("UPDATE Regions SET RegionID = '2008' WHERE RegionDescription = 'Relient K';") == "Database found."
    assert Assignment_13.execute_sql("DELETE FROM Regions WHERE RegionID = 2008;") == "Database found."
    assert Assignment_13.execute_sql("This isn't SQL!!!") == "Database missing."


def test_execute_sql_invalid():
    with pytest.raises(AssertionError):
        Assignment_13.execute_sql(13)


def test_which_sql_valid():
    input_values = ["This isn't in a database.... yet", '777']
    def input(prompt=None):
        return input_values.pop()
    Assignment_13.input = input
    assert Assignment_13.which_sql('Insert', 'Region', regions) == "Success"


def test_which_sql_invalid():
    with pytest.raises(AssertionError):
        Assignment_13.which_sql(12, "Regions", regions)
    with pytest.raises(AssertionError):
        Assignment_13.which_sql("NotInsert", "Regions", regions)
    with pytest.raises(AssertionError):
        Assignment_13.which_sql("Insert", 5, regions)
    with pytest.raises(AssertionError):
        Assignment_13.which_sql(12, "Regions", regions)
    not_a_dictionary = ["random", "list"]
    with pytest.raises(AssertionError):
        Assignment_13.which_sql("Insert", "Regions", not_a_dictionary)
    dictionary_without_heading_lists = {"Headings" : 3}
    with pytest.raises(AssertionError):
        Assignment_13.which_sql("Insert", "Regions", dictionary_without_heading_lists)
    dictionary_without_row_lists = {"Headings" : ["RegionID", "RegionDescription"], "Rows" : 5}
    with pytest.raises(AssertionError):
        Assignment_13.which_sql("Insert", "Regions", dictionary_without_row_lists)
    not_a_list_of_lists = {"Headings" : ["RegionID", "RegionDescription"], "Rows" : [5, 3]}
    with pytest.raises(AssertionError):
        Assignment_13.which_sql("Insert", "Regions", not_a_list_of_lists)
    not_the_same_length = {"Headings" : ["RegionID", "RegionDescription"], "Rows" : [["apples", "bananas", "THIRD THING THAT'S NOT SUPPOSED TO BE HERE"], ["whoa", "this"], ["is", "hard"]]}
    with pytest.raises(AssertionError):
        Assignment_13.which_sql("Insert", "Regions", not_the_same_length)


def test_get_delete_sql_valid():
    input_values = ["This isn't in a database.... yet", '777', 0, 3]
    def input(prompt=None):
        return input_values.pop()
    Assignment_13.input = input
    assert Assignment_13.get_delete_sql("Regions", regions) == "DELETE FROM Regions WHERE RegionID = 3;"


def test_get_delete_sql_invalid():
    not_a_dictionary = ["random", "list"]
    with pytest.raises(AssertionError):
        Assignment_13.get_delete_sql("Regions", not_a_dictionary)
    dictionary_without_heading_lists = {"Headings" : 3}
    with pytest.raises(AssertionError):
        Assignment_13.get_delete_sql("Regions", dictionary_without_heading_lists)
    dictionary_without_row_lists = {"Headings" : ["RegionID", "RegionDescription"], "Rows" : 5}
    with pytest.raises(AssertionError):
        Assignment_13.get_delete_sql("Regions", dictionary_without_row_lists)
    not_a_list_of_lists = {"Headings" : ["RegionID", "RegionDescription"], "Rows" : [5, 3]}
    with pytest.raises(AssertionError):
        Assignment_13.get_delete_sql("Regions", not_a_list_of_lists)
    not_the_same_length = {"Headings" : ["RegionID", "RegionDescription"], "Rows" : [["apples", "bananas", "THIRD THING THAT'S NOT SUPPOSED TO BE HERE"], ["whoa", "this"], ["is", "hard"]]}
    with pytest.raises(AssertionError):
        Assignment_13.get_delete_sql("Regions", not_the_same_length)
    dictionary_valid = {"Headings" : ["RegionID", "RegionDescription"], "Rows" : [["no asserts", "should be"], ["raised by", "this"]]}
    with pytest.raises(AssertionError):
        Assignment_13.get_delete_sql(5, dictionary_valid)


def test_get_update_sql_valid():
    input_values = [12, 2.5, 'Southern', 'Workplease']
    def input(prompt=None):
        return input_values.pop()
    Assignment_13.input = input
    assert Assignment_13.get_update_sql("Regions", regions, results) == "UPDATE Regions SET RegionDescription = 'Workplease' WHERE RegionID = '4';"


def test_get_update_sql_invalid():
    not_a_dictionary = ["random", "list"]
    with pytest.raises(AssertionError):
        Assignment_13.get_update_sql("Regions", not_a_dictionary, results)
    dictionary_without_heading_lists = {"Headings" : 3}
    with pytest.raises(AssertionError):
        Assignment_13.get_update_sql("Regions", dictionary_without_heading_lists, results)
    dictionary_without_row_lists = {"Headings" : ["RegionID", "RegionDescription"], "Rows" : 5}
    with pytest.raises(AssertionError):
        Assignment_13.get_update_sql("Regions", dictionary_without_row_lists, results)
    not_a_list_of_lists = {"Headings" : ["RegionID", "RegionDescription"], "Rows" : [5, 3]}
    with pytest.raises(AssertionError):
        Assignment_13.get_update_sql("Regions", not_a_list_of_lists, results)
    not_the_same_length = {"Headings" : ["RegionID", "RegionDescription"], "Rows" : [["apples", "bananas", "THIRD THING THAT'S NOT SUPPOSED TO BE HERE"], ["whoa", "this"], ["is", "hard"]]}
    with pytest.raises(AssertionError):
        Assignment_13.get_update_sql("Regions", not_the_same_length, results)
    dictionary_valid = {"Headings" : ["RegionID", "RegionDescription"], "Rows" : [["no asserts", "should be"], ["raised by", "this"]]}
    with pytest.raises(AssertionError):
        Assignment_13.get_update_sql(5, dictionary_valid, results)
    with pytest.raises(AssertionError):
        Assignment_13.get_update_sql("Regions", dictionary_valid, ["this", "is", "a", "list"])


def test_select_row_and_column_valid():
    input_values = [2, 4]
    def input(prompt=None):
        return input_values.pop()
    Assignment_13.input = input
    assert Assignment_13.select_row_and_column("Regions", regions) == results


def test_select_row_and_column_invalid():
    input_values = ['2', '1']
    def input(prompt=None):
        return input_values.pop()
    Assignment_13.input = input
    not_a_dictionary = ["random", "list"]
    with pytest.raises(AssertionError):
        Assignment_13.select_row_and_column("Regions", not_a_dictionary)
    dictionary_without_heading_lists = {"Headings" : 3}
    with pytest.raises(AssertionError):
        Assignment_13.select_row_and_column("Regions", dictionary_without_heading_lists)
    dictionary_without_row_lists = {"Headings" : ["RegionID", "RegionDescription"], "Rows" : 5}
    with pytest.raises(AssertionError):
        Assignment_13.select_row_and_column("Regions", dictionary_without_row_lists)
    not_a_list_of_lists = {"Headings" : ["RegionID", "RegionDescription"], "Rows" : [5, 3]}
    with pytest.raises(AssertionError):
        Assignment_13.select_row_and_column("Regions", not_a_list_of_lists)
    not_the_same_length = {"Headings" : ["RegionID", "RegionDescription"], "Rows" : [["apples", "bananas", "THIRD THING THAT'S NOT SUPPOSED TO BE HERE"], ["whoa", "this"], ["is", "hard"]]}
    with pytest.raises(AssertionError):
        Assignment_13.select_row_and_column("Regions", not_the_same_length)
    dictionary_valid = {"Headings" : ["RegionID", "RegionDescription"], "Rows" : [["no asserts", "should be"], ["raised by", "this"]]}
    with pytest.raises(AssertionError):
        Assignment_13.select_row_and_column(5, dictionary_valid)


def test_validate_input_valid():
    assert Assignment_13.validate_input("Hmm this data isn't consistent", 0, regions["Rows"]) == True
    assert Assignment_13.validate_input(1.5, 0, regions["Rows"]) == True
    assert Assignment_13.validate_input(4, 0, regions["Rows"]) == True
    assert Assignment_13.validate_input(5, 0, regions["Rows"]) == False
    assert Assignment_13.validate_input(1.5, 1, regions["Rows"]) == True
    assert Assignment_13.validate_input('15', 1, regions["Rows"]) == True
    assert Assignment_13.validate_input("Southern", 0, regions["Rows"]) == True
    assert Assignment_13.validate_input("This data is consistent", 1, regions["Rows"]) == False


def test_validate_input_invalid():
    with pytest.raises(AssertionError):
        Assignment_13.validate_input("That's a float, not an integer", 1.5, regions["Rows"])
    with pytest.raises(AssertionError):
        Assignment_13.validate_input("'regions' is a dictionary, not a list", 1, regions)
    with pytest.raises(AssertionError):
        Assignment_13.validate_input("user input", 1, ["This", "isn't", "a", "list", "of", "lists"])
    with pytest.raises(AssertionError):
        Assignment_13.validate_input("Whoa that's outside the bottom limit", -1, regions["Rows"])
    with pytest.raises(AssertionError):
        Assignment_13.validate_input("Wait that's outside the list", 3, regions["Rows"])


def test_get_insert_sql_valid():
    input_values = ['huh', 'Southern', 20, 5.5]
    def input(prompt=None):
        return input_values.pop()
    Assignment_13.input = input
    assert Assignment_13.get_insert_sql("Regions", regions) == "INSERT INTO Regions(RegionID, RegionDescription) VALUES('20', 'huh');"


def test_get_insert_sql_invalid():
    input_values = ['huh', 'Southern', 20, 5.5]
    def input(prompt=None):
        return input_values.pop()
    Assignment_13.input = input
    not_a_dictionary = ["random", "list"]
    with pytest.raises(AssertionError):
        Assignment_13.get_insert_sql("Regions", not_a_dictionary)
    dictionary_without_heading_lists = {"Headings" : 3}
    with pytest.raises(AssertionError):
        Assignment_13.get_insert_sql("Regions", dictionary_without_heading_lists)
    dictionary_without_row_lists = {"Headings" : ["RegionID", "RegionDescription"], "Rows" : 5}
    with pytest.raises(AssertionError):
        Assignment_13.get_insert_sql("Regions", dictionary_without_row_lists)
    not_a_list_of_lists = {"Headings" : ["RegionID", "RegionDescription"], "Rows" : [5, 3]}
    with pytest.raises(AssertionError):
        Assignment_13.get_insert_sql("Regions", not_a_list_of_lists)
    not_the_same_length = {"Headings" : ["RegionID", "RegionDescription"], "Rows" : [["apples", "bananas", "THIRD THING THAT'S NOT SUPPOSED TO BE HERE"], ["whoa", "this"], ["is", "hard"]]}
    with pytest.raises(AssertionError):
        Assignment_13.get_insert_sql("Regions", not_the_same_length)
    dictionary_valid = {"Headings" : ["RegionID", "RegionDescription"], "Rows" : [["no asserts", "should be"], ["raised by", "this"]]}
    with pytest.raises(AssertionError):
        Assignment_13.get_insert_sql(5, dictionary_valid)
