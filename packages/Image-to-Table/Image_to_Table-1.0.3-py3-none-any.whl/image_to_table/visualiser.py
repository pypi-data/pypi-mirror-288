import json
from tabulate import tabulate

def json_to_table(json_input:str = None, file_path: str = None, number_char_cell: int = 18) -> None:
    """
    Converts JSON data into a table format and prints it.
    Args:
        json_input (str, optional): The JSON data as a string. Defaults to None.
        file_path (str, optional): The path to the JSON file. Defaults to None.
        number_char_cell (int, optional): The maximum number of characters to display in each cell. Defaults to 18.
    Raises:
        Exception: If neither json_input nor file_path is provided.
    Returns:
        None
    """
    
    output = []
        
    if (json_input != None):
        json_data = json_input
    elif (file_path != None):
        try:
            with open(file_path, "r") as file:
                json_data = file.read()
        except Exception as e:
            print(f"Error reading the content from the json file: {e}")
            return
    else:
        raise("Please provide either a JSON string or a file path.")
        return
        
    json_str = json.loads(json_data)
    
    first_row = ["hours"]
    first_row.extend(list(json_str.keys()))
    
    first_col = [[key] for key in json_str[first_row[1]]]
    
    output.append(first_row)
    output.extend(first_col)
    
    for i in range(1,len(output)):
        row = output[i]
        time = row[0]
        
        for key in json_str.keys():
            appoint = json_str[key][time]
            value = list(appoint.values())
            if value != []:
                row.append(value[0]['course'][:number_char_cell])
            else:
                row.append("-X-")
                
    print(tabulate(output,headers="firstrow",tablefmt="grid"))
    