# Online Courses Study Time Spreader

Some online courses platforms do not give a total of the time per sections and it's sometimes frustrating when you want to plan ahead. This module will pull out the lesson name and length and then spread out the material to be seen by weeks, day, hours, according to your preferences.

## Usage

The script is wrapped in a module, so you can easily import it using:

```bash
import spreader
spreader.main(sys.argv)

```

You can then call it using:

```bash
python <your_python_file> <delimiters> -i <input_file>

```

If you want to use the module directly from within another python script, you simply need to add a list as arguments when you call the `main()` function.

For example, in your python file:

```python
import spreader
spreader.main(["-w2", "-d2-l1", "-i", "data2.txt"])
```

then, simply, from the terminal:

```bash
python test.py
```

Where possible delimiters have the syntax `-<delimiter>-<limiter>(optional)` and can be:

| delimiter | meaning |
| --------- | ------- |
| `-w`      | weeks   |
| `-d`      | days    |
| `-h`      | hours   |
| `-l`      | limiter |

For more precision using delimiters, see [Args](#args) section

You can also simply run the module directly:

```bash
python spreader.py <delimiters> -i <input_file>
```

_note that althout the -i <input_file> option is optional, it is highly recommended as for now the script will only look at the example data in the `data.txt` by default should it be omitted._

### Calling Spreader From Another Python File Example

If you have your data in a file named `testing_data.txt` and you create a `test.py` file with this code inside:

```python
import spreader

spreader.main(["-w2", "-d2-l1", "testing_data.txt"])
```

and you want to spread that data in 2 weeks, 3 days per week for 2 hours per day, then in a terminal you could simply run the **spreader** as such:

```bash
python test.py -w2 -d3-l2

```

The outputs will be in the `testing_data_output.json`, `testing_data_output.csv` and `testing_data.txt` files.

## Args

The script will look for the following args:

**delimiters**

`-w<integer>`: _This is the weeks delimiter and tells the script to split the data in the number of weeks specified by the integer_

example:

```bash
python spreader.py -w3
```

`-d<integer>`: _This is the days delimiter and tells the script to split the data in the number of days specified by the integer_

example:

```bash
python spreader.py -d3
```

`-h<integer>`: _This is the hours delimiter and tells the script to split the data in the number of hours specified by the integer_

example:

```bash
python spreader.py -h3
```

**limiters**

`-l<integer>`: _This is the limiting factor that can be applied right next to a delimiter and which will represent the limiting factor of the delimiter._

example:

```bash
python spreader.py `-w3-l3`
```

would limit each week to 3 days per week.

```bash
python spreader.py `-d4-l2`
```

would limit each day to 2 hours per day.

It is worthy of note that with the `-l` one could argue that the `-h` is redundant as we can always tag the limiter to the days, however, it was important to keep the possibility to simply spread the data in hours. Therefore, for certain situations and data sets, it could come in handy to have simply this call possible:

```
python spreader.py -h5
```

which would ask the spreader to split the data set in 5 hours.

**inputs**

`-i <string>`: _This will take in the data set filename as parameter_

## License

MIT

```

```
