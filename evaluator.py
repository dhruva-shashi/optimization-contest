def evaluate(input_file_name, output_file_name):
    fin = open(input_file_name, 'r')
    fout = open(output_file_name, 'r')

    try:
        points = 0

        # Write the evaluation code here.
        # Read the input from fin file object
        # Read the output from fout file object

    except Exception as e:
        fin.close()
        fout.close()

        return {'result': 'WA', 'error': str(e), 'points': 0}

    fin.close()
    fout.close()

    return {'result': 'AC', 'points': points}



