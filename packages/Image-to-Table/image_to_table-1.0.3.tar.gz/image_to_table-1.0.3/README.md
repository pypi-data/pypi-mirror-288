# Image-to-table

Utilize a MultiModal Large Language Modal `GEMINI` to extract `table data` from an `image` and saves it as a `json`

## Installing

Install from PyPi using

```bash
python -m pip install image-to-table
```

## Documentation
You need a Gemini Api key to use this which you can get from : 
https://ai.google.dev/gemini-api

To generate the table and save it as json:

```bash
from image_to_table import generate_timetable

json_output = generate_timetable(DIR_PATH="..",API_KEY='..',JSON_PATH=None) -> str
```

the input image should be placed in images directory

To visualize the json output you can use :

```bash
from image_to_table import json_to_table

json_to_table(json_input = json_output , number_char_cell = 18)
```

or 

```bash
from image_to_table import json_to_table

json_to_table(file_path= ".." , number_char_cell = 18)
```
this function prints the output to the console like the test below

## Testing

Test with timetable:

![Capture_decran_2024-08-02_165045](https://github.com/user-attachments/assets/9b286d4e-a828-46e4-abe5-158c7d211d98)



Output:

![table generation](https://github.com/user-attachments/assets/3ef866f0-a975-4e8e-8c55-b3d28829bd13)


