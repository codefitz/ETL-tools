from docxtopdf import convert

def docx_to_pdf(input_path, output_path=None):
    """
    Convert docx file to pdf.

    :param input_path: Path to the input .docx file
    :param output_path: Path to the output .pdf file. If None, it will be the same as input_path with .pdf extension.
    :return: None
    """
    if output_path is None:
        if input_path.endswith('.docx'):
            output_path = input_path[:-5] + '.pdf'
        else:
            output_path = input_path + '.pdf'

    convert(input_path, output_path)

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python script_name.py input_path [output_path]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    docx_to_pdf(input_file, output_file)
    print(f"Converted {input_file} to {output_file if output_file else input_file[:-5] + '.pdf'}")