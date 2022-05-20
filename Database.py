"""This program accesses a database and allow the user to insert, update, or delete any file in the database."""


import sqlite3
import sys


DATABASE = "Northwind.db"


def get_input(array_of_tables):
    """Gets the users choice of table to display.

    Args:
        array_of_tables: A list of the tables to be displayed.

    Returns:
        The exact name of the table to be displayed.

    Raises:
        AssertionError: If array_of_tables is not a list.
        AssertionError: If array_of_tables is not a list of lists.
    """
    assert isinstance(array_of_tables, list), "'array_of_tables' must be a list."
    assert isinstance(array_of_tables[0], list), "'arrary_of_tables' must be a list of lists."
    loop_count = 0
    while loop_count < len(array_of_tables):
        print("Press " + str(loop_count + 1) + " for " + str(array_of_tables[loop_count][0]))
        loop_count += 1

    while True:
        matching_table = ""
        print("\nType a number and press enter or press enter with no input to quit.\n")
        answer = input()
        if answer == "":
            break
        try:
            answer = int(answer)
        except:
            print("Answer should be an integer.")
            continue
        print("\nYou entered: '" + str(answer) + "'")
        if 0 < answer and answer < len(array_of_tables) + 1:
            matching_table = array_of_tables[answer - 1][0]
        if matching_table != "":
            break
        else:
            print("Input did not match any table number.")
    return matching_table


def get_dictionary(sql):
    """Executes the SQL code in a database and returns the headings and rows in a dictionary of lists.
    
    Args:
        sql: The SQL code to be executed.

    Returns:
        A dictionary of lists 
    
    Raises:
        AssertionError: If sql is not a string.
    """
    assert isinstance(sql, str), "'sql' must be a string."
    dictionary = {}
    column_headings = []
    rows_contents = []

    connection = sqlite3.connect(DATABASE)
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        
        loop_count = 0
        column_names = cursor.description
        while loop_count < len(column_names):
            column_name = column_names[loop_count][0]
            column_headings.append(column_name)
            loop_count += 1
        dictionary["Headings"] = column_headings

        loop_count = 0
        rows = cursor.fetchall()
        if rows != []:
            while loop_count < len(rows):
                small_loop = 0
                small_row = []
                switch = 0
                while small_loop < len(dictionary["Headings"]):
                    row = str(rows[loop_count][small_loop])
                    if "_" not in row:
                        small_row.append(row)
                        switch = 1
                    small_loop += 1
                if switch == 1:
                    rows_contents.append(small_row)
                loop_count += 1
            dictionary["Rows"] = rows_contents
        else:
            dictionary = "Database missing."
    except Exception as exception:
            print("Error processing %s" % sql)
            print(exception)
    finally:
        connection.close()
    if dictionary == {}:
        dictionary = "Database missing."
    return dictionary


def attach_column_widths(dictionary_of_lists, answer):
    """Finds and attaches a list of the column widths to the dictionary.
    
    Args:
        dictionary_of_lists: A dictionary of lists made from the database.
        answer: The table selected by the user.
    
    Returns:
        The dictionary of lists with an extra entry with the column widths.

    Raises:
        AssertionError: If dictionary_of_lists is not a dictionary.
        AssertionError: If 'Heading' key does not access a list.
        AssertionError: If 'Rows' key does not access a list.
        AssertionError: If 'Rows' key does not access a list of lists.
        AssertionError: If the length of headings and number of values in row are not equal.
        AssertionError: If answer is not a string.
    """
    assert isinstance(dictionary_of_lists, dict), "'dictionary_of_lists ' must be a dictionary."
    assert isinstance(dictionary_of_lists["Headings"], list), "'Headings' key should access a list."
    assert isinstance(dictionary_of_lists["Rows"], list), "'Rows' key should access a list."
    assert isinstance(dictionary_of_lists["Rows"][0], list), "'Rows' key should access a list of lists."
    assert len(dictionary_of_lists["Headings"]) == len(dictionary_of_lists["Rows"][0]), "Length of headings should equal the number of values in a rows."
    assert isinstance(answer, str), "'answer' must be a string."
    loop_count = 0
    list_of_column_widths = []
    while loop_count < len(dictionary_of_lists["Headings"]):
        instance_heading = dictionary_of_lists["Headings"][loop_count]
        sql = "SELECT MAX(LENGTH(" + str(instance_heading) + ")) FROM " + str(answer)
        sql_result = get_dictionary(sql)
        column_width = int(sql_result["Rows"][0][0]) + 2
        if column_width > 40:
            column_width = 40
        if len(instance_heading) + 2 < column_width:
            list_of_column_widths.append(column_width)
        else:
            list_of_column_widths.append(len(instance_heading) + 2)
        loop_count += 1
    dictionary_of_lists["Column Widths"] = list_of_column_widths
    return dictionary_of_lists


def display_table(dictionary_of_lists, answer):
    """Prints the information from the dictionary in a table.
    
    Args:
        dictionary_of_lists: A dictionary of lists made from the database.
        answer: The table selected by the user.
    
    Returns:
        The dictionary of lists with an extra entry with the column widths.

    Raises:
        AssertionError: If dictionary_of_lists is not a dictionary.
        AssertionError: If 'Heading' key does not access a list.
        AssertionError: If 'Rows' key does not access a list.
        AssertionError: If 'Rows' key does not access a list of lists.
        AssertionError: If the length of headings and number of values in row are not equal.
        AssertionError: If answer is not a string.
        AssertionError: If 'Column Widths' key does not access a list.
        AssertionError: If 'Column Widths' key does not access a list of integers.
    """
    assert isinstance(dictionary_of_lists, dict), "'dictionary_of_lists ' must be a dictionary."
    assert isinstance(dictionary_of_lists["Headings"], list), "'Headings' key should access a list."
    assert isinstance(dictionary_of_lists["Rows"], list), "'Rows' key should access a list."
    assert isinstance(dictionary_of_lists["Rows"][0], list), "'Rows' key should access a list of lists."
    assert len(dictionary_of_lists["Headings"]) == len(dictionary_of_lists["Rows"][0]), "Length of headings should equal the number of values in a rows."
    assert isinstance(answer, str), "'answer' must be a string."
    loop_count = 0
    top_row = " \t"
    dictionary_of_lists = attach_column_widths(dictionary_of_lists, answer)
    assert isinstance(dictionary_of_lists["Column Widths"], list), "'Column Widths' key should access a list."
    assert isinstance(dictionary_of_lists["Column Widths"][0], int), "'Column Widths' key should access a list of integers."
    while loop_count < len(dictionary_of_lists["Headings"]):
        instance_heading = str(dictionary_of_lists["Headings"][loop_count])
        instance_column_width = int(dictionary_of_lists["Column Widths"][loop_count])
        top_row += f"{instance_heading:{instance_column_width}}"
        loop_count += 1
    print(top_row)

    loop_count = 0
    while loop_count < len(dictionary_of_lists["Rows"]):
        row_count = str(loop_count + 1) + ":"
        row = f"{row_count:{8}}"
        small_loop = 0
        while small_loop < len(dictionary_of_lists["Rows"][loop_count]):
            instance_row = str(dictionary_of_lists["Rows"][loop_count][small_loop])
            if len(instance_row) > 38:
                instance_row = instance_row[0:37] + "..."
            instance_column_width = int(dictionary_of_lists["Column Widths"][small_loop])
            row += f"{instance_row:{instance_column_width}}"
            small_loop += 1
        print(row)
        loop_count += 1
    return loop_count


def execute_sql(sql):
    """Executes the given sql statement.

    Args:
        sql: A valid SQL statement to execute.

    Returns:
        Either 'Database found.' or 'Database missing.' depending on whether the database was accessed.

    Raises:
        AssertionError: If SQL is not a string.
    """
    assert(isinstance(sql, str)), "SQL must be a string."
    result = ""
    try:
        connection = sqlite3.connect(DATABASE)
    except:
        print(f"Unable to connect to {DATABASE}")
        raise

    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        print("Change successful.")
        result = "Database found."
    except Exception as exception:
        print(f"Unable to execute {sql}")
        print(exception)
        result = "Database missing."
    finally:
        connection.close()
    return result


def which_sql(command, answer, dictionary_of_lists):
    """Takes a table name, and the dictionary of lists containing the information for the table and performs one of three commands.
    
    Args:
        command: Either 'Insert', 'Update', or 'Delete'.
        answer: The name of the table accessed.
        dictionary_of_lists: The contents of the table.
    
    Returns:
        Either 'Invalid command.' or 'Valid command.' depending on whether or not it works.

    Raises:
        AssertionError: If command is not a string.
        AssertionError: If command is not either 'Insert', 'Update', or 'Delete'.
        AssertionError: If answer is not a string.
        AssertionError: If dictionary_of_lists is not a dictionary.
        AssertionError: If 'Heading' key does not access a list.
        AssertionError: If 'Rows' key does not access a list.
        AssertionError: If 'Rows' key does not access a list of lists.
        AssertionError: If the length of headings and number of values in row are not equal.
        AssertionError: If answer is not a string.
    """
    assert isinstance(command, str), "'command' must be a string."
    assert command == "Insert" or command == "Update" or command == "Delete"
    assert isinstance(answer, str), "'answer' must be a string."
    assert isinstance(dictionary_of_lists, dict), "'dictionary_of_lists ' must be a dictionary."
    assert isinstance(dictionary_of_lists["Headings"], list), "'Headings' key should access a list."
    assert isinstance(dictionary_of_lists["Rows"], list), "'Rows' key should access a list."
    assert isinstance(dictionary_of_lists["Rows"][0], list), "'Rows' key should access a list of lists."
    assert len(dictionary_of_lists["Headings"]) == len(dictionary_of_lists["Rows"][0]), "Length of headings should equal the number of values in a rows."
    status = "Success"
    if command == "Insert":
        sql = get_insert_sql(answer, dictionary_of_lists)
        execute_sql(sql)
    elif command == "Update":
        results = select_row_and_column(answer, dictionary_of_lists)
        sql = get_update_sql(answer, dictionary_of_lists, results)
        execute_sql(sql)
    elif command == "Delete":
        sql = get_delete_sql(answer, dictionary_of_lists)
        execute_sql(sql)
    else:
        status = "Failure"
        print("Error.")
    return status


def get_delete_sql(answer, dictionary_of_lists):
    """Takes the table name, the table info, and user input to create an SQL command line to delete a specific line.

    Args:
        answer: The name of the table accessed.
        dictionary_of_lists: The contents of the table.
    
    Returns:
        The SQL to delete the row the user selects.

    Raises:
        AssertionError: If answer is not a string.
        AssertionError: If dictionary_of_lists is not a dictionary.
        AssertionError: If 'Heading' key does not access a list.
        AssertionError: If 'Rows' key does not access a list.
        AssertionError: If 'Rows' key does not access a list of lists.
        AssertionError: If the length of headings and number of values in row are not equal.
    """
    assert isinstance(answer, str), "'answer' must be a string."
    assert isinstance(dictionary_of_lists, dict), "'dictionary_of_lists ' must be a dictionary."
    assert isinstance(dictionary_of_lists["Headings"], list), "'Headings' key should access a list."
    assert isinstance(dictionary_of_lists["Rows"], list), "'Rows' key should access a list."
    assert isinstance(dictionary_of_lists["Rows"][0], list), "'Rows' key should access a list of lists."
    assert len(dictionary_of_lists["Headings"]) == len(dictionary_of_lists["Rows"][0]), "Length of headings should equal the number of values in a rows."
    headings = dictionary_of_lists["Headings"]
    rows = dictionary_of_lists["Rows"]
    sql = "DELETE FROM " + str(answer) + " WHERE "
    while True:
        print("\nPlease enter the number of the row of the value you want to delete:\n")
        user_row = input()
        print("You entered: " + str(user_row))
        try:
            user_row = int(user_row)
        except:
            print("You must enter an integer.")
            continue
        if user_row < 1 or len(rows) < user_row:
            print("Number entered must be in between 1 and " + str(len(rows)) + ".")
            continue
        break
    user_row = user_row - 1
    row_value = dictionary_of_lists["Rows"][user_row][0]
    sql = sql + str(headings[0]) + " = " + str(row_value) + ";"
    return sql


def get_update_sql(answer, dictionary_of_lists, results):
    """Takes the table name, the table info, and user input to create an SQL command line to update a specific value.

    Args:
        answer: The name of the table accessed.
        dictionary_of_lists: The contents of the table.
        results: A dictionary with the user selections of the row and column as well as their value.

    Returns:
        The SQL to update the row and column the user selects.

    Raises:
        AssertionError: If answer is not a string.
        AssertionError: If dictionary_of_lists is not a dictionary.
        AssertionError: If 'Heading' key does not access a list.
        AssertionError: If 'Rows' key does not access a list.
        AssertionError: If 'Rows' key does not access a list of lists.
        AssertionError: If the length of headings and number of values in row are not equal.
        AssertionError: If 'results' is not a dictionary.
    """
    assert isinstance(answer, str), "'answer' must be a string."
    assert isinstance(dictionary_of_lists, dict), "'dictionary_of_lists ' must be a dictionary."
    assert isinstance(dictionary_of_lists["Headings"], list), "'Headings' key should access a list."
    assert isinstance(dictionary_of_lists["Rows"], list), "'Rows' key should access a list."
    assert isinstance(dictionary_of_lists["Rows"][0], list), "'Rows' key should access a list of lists."
    assert len(dictionary_of_lists["Headings"]) == len(dictionary_of_lists["Rows"][0]), "Length of headings should equal the number of values in a rows."
    assert isinstance(results, dict), "'result' must be a dictionary."
    headings = dictionary_of_lists["Headings"]
    rows = dictionary_of_lists["Rows"]
    heading = headings[results["column"]]
    other_heading = headings[results["column"] - 1]
    sql = "UPDATE " + str(answer) + " SET " + str(heading) + " = '"
    while True:
        print("\nPlease enter what you want to update '" + str(results["choice"]) + "' to.")
        user_input = input()
        need_to_redo = validate_input(user_input, results["column"], rows)
        if need_to_redo == True:
            continue
        break
    user_input = user_input
    sql = sql + str(user_input) + "' WHERE " + str(other_heading) + " = '" + str(results["ref choice"]) + "';" 
    return sql


def select_row_and_column(answer, dictionary_of_lists):
    """Allows the user to select a row and column in the database.

    Args:
        answer: The name of the table accessed.
        dictionary_of_lists: The contents of the table.
        results: A dictionary with the user selections of the row and column as well as their value.

    Returns:
        The SQL to update the row and column the user selects.

    Raises:
        AssertionError: If answer is not a string.
        AssertionError: If dictionary_of_lists is not a dictionary.
        AssertionError: If 'Heading' key does not access a list.
        AssertionError: If 'Rows' key does not access a list.
        AssertionError: If 'Rows' key does not access a list of lists.
        AssertionError: If the length of headings and number of values in row are not equal.
    """
    assert isinstance(answer, str), "'answer' must be a string."
    assert isinstance(dictionary_of_lists, dict), "'dictionary_of_lists ' must be a dictionary."
    assert isinstance(dictionary_of_lists["Headings"], list), "'Headings' key should access a list."
    assert isinstance(dictionary_of_lists["Rows"], list), "'Rows' key should access a list."
    assert isinstance(dictionary_of_lists["Rows"][0], list), "'Rows' key should access a list of lists."
    assert len(dictionary_of_lists["Headings"]) == len(dictionary_of_lists["Rows"][0]), "Length of headings should equal the number of values in a rows."
    headings = dictionary_of_lists["Headings"]
    rows = dictionary_of_lists["Rows"]
    while True:
        print("\nPlease enter the number of the row of the value you want to update:\n")
        user_row = input()
        print("You entered: " + str(user_row))
        try:
            user_row = int(user_row)
        except:
            print("You must enter an integer.")
            continue
        if user_row < 1 or len(rows) < user_row:
            print("Number entered must be in between 1 and " + str(len(rows)) + ".")
            continue
        break
        
    while True:
        loop_count = 0
        print("\nPlease enter the number of the column of the value you want to update or press enter to quit:\n")
        while loop_count < len(headings):
            print("Press " + str(loop_count + 1) + " for " + str(headings[loop_count]))
            loop_count += 1
        print("")
        user_column = input()
        print("You entered: " + str(user_column))
        try:
            user_column = int(user_column)
        except:
            print("You must enter an integer.")
            continue
        if user_column < 1 or len(headings) < user_column:
            print("Number entered must be in between 1 and " + str(len(headings)) + ".")
            continue
        break
    user_row = user_row - 1
    user_column = user_column - 1
    choice = rows[user_row][user_column]
    reference_choice = rows[user_row][user_column - 1]
    print("You chose: '" + str(choice) + "'")
    results = {"row" : user_row, "column" : user_column, "choice" : choice, "ref choice" : reference_choice}
    return results


def validate_input(user_input, which_column, rows):
    """Takes a list of column headings and a list of lists containing the row information
    
    Args:
        user_input: The input given by the user.
        which_column: The number of the column chosen.
        rows: the list of lists containing the values from the table.

    Returns:
        True if the data needs to be reentered and False if it does not.

    Raises:
        AssertionError: If 'which_column' is not an integer.
        AssertionError: If 'rows' is not a list.
        AssertionError: If 'rows' is not a list of lists.
        AssertionError: If 'which_column' is not within the range of the lists in the list.
    """
    assert isinstance(which_column, int), "'which_column' should be an integer."
    assert isinstance(rows, list), "'rows' should be a list."
    assert isinstance(rows[0], list), "'rows' should be a list of lists."
    assert len(rows[0]) - 1 >= which_column and 0 <= which_column, "'which_column' should be in between 0 and the length of the lists in the list."
    user_input = str(user_input)
    need_to_redo = False
    while True:
        if ";" in user_input:
            print("Please enter a value without semicolons.")
            need_to_redo = True
            break
        small_loop = 0
        while small_loop < len(rows):    
            if str(user_input) in rows[small_loop]:
                print("Please enter a value that is not already in the database.")
                need_to_redo = True
                break
            instance_in_row = rows[small_loop][which_column]
            try:
                instance_in_row = int(instance_in_row)
                try:
                    user_input = int(user_input)
                except:
                    print("Data must be consistent with data in column.")
                    need_to_redo = True
                    break
            except:
                try:
                    user_input = float(user_input)
                    print("Data must be consisent with data in column.")
                    need_to_redo = True
                    break
                except:
                    user_input = str(user_input)
            if need_to_redo == True:
                break
            small_loop += 1
        break
    return need_to_redo


def get_insert_sql(answer, dictionary_of_lists):
    """Takes a dictionary of lists (a table) and lets the user insert another row.
    
    Args:
        answer: The name of the table accessed.
        dictionary_of_lists: The contents of the table.
        results: A dictionary with the user selections of the row and column as well as their value.

    Returns:
        The SQL to insert data the user selects.

    Raises:
        AssertionError: If answer is not a string.
        AssertionError: If dictionary_of_lists is not a dictionary.
        AssertionError: If 'Heading' key does not access a list.
        AssertionError: If 'Rows' key does not access a list.
        AssertionError: If 'Rows' key does not access a list of lists.
        AssertionError: If the length of headings and number of values in row are not equal.
    """
    assert isinstance(answer, str), "'answer' must be a string."
    assert isinstance(dictionary_of_lists, dict), "'dictionary_of_lists ' must be a dictionary."
    assert isinstance(dictionary_of_lists["Headings"], list), "'Headings' key should access a list."
    assert isinstance(dictionary_of_lists["Rows"], list), "'Rows' key should access a list."
    assert isinstance(dictionary_of_lists["Rows"][0], list), "'Rows' key should access a list of lists."
    assert len(dictionary_of_lists["Headings"]) == len(dictionary_of_lists["Rows"][0]), "Length of headings should equal the number of values in a rows."
    headings = dictionary_of_lists["Headings"]
    rows = dictionary_of_lists["Rows"]
    loop_count = 0
    sql = "INSERT INTO " + str(answer) + "("
    while loop_count < len(headings):
        if loop_count != len(headings) - 1:
            sql = sql + str(headings[loop_count]) + ", "
        else:
            sql = sql + str(headings[loop_count]) + ") VALUES("
        loop_count += 1
    
    which_column = 0
    while which_column < len(headings):
        print("\nPlease enter the new input for " + str(headings[which_column]) + ":\n")
        user_input = input()
        print("You entered: " + str(user_input))    
        need_to_redo = validate_input(user_input, which_column, rows)
        if need_to_redo == True:
            continue
        user_input = "'" + str(user_input) + "'"
        if which_column != len(headings) - 1:
            sql = sql + str(user_input) + ", "
        else:
            sql = sql + str(user_input) + ");"
        which_column += 1
    return sql


def main():
    """Runs the main program logic."""
    while True:
        try:
            sql = "SELECT name FROM sqlite_master WHERE type='table'"
            dictionary = get_dictionary(sql)
            if dictionary == "Database missing.":
                print(dictionary)
                break
            print("\nThe list of tables to choose from:\n")
            answer = get_input(dictionary["Rows"])
            if answer == "":
                break
            sql = "SELECT * from " + answer
            dictionary_of_lists = get_dictionary(sql)
            print()
            display_table(dictionary_of_lists, answer)
            print()
            array = [["Insert"], ["Update"], ["Delete"]]
            command = get_input(array)
            if command == "":
                continue
            which_sql(command, answer, dictionary_of_lists)
        except:
            print("Unexpected error.")
            print("Error:", sys.exc_info()[1])
            print("File: ", sys.exc_info()[2].tb_frame.f_code.co_filename)
            print("Line: ", sys.exc_info()[2].tb_lineno)
            break
    print("Program terminated.")
    sys.exit()


if __name__ == "__main__":
    main()
