import os

import ipywidgets as widgets
import nbformat
from IPython.display import FileLink, display
from nbconvert import ScriptExporter
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

from finter.framework_model.submission.config import ModelTypeConfig, get_output_path
from finter.settings import logger
from finter.utils.timer import timer


@timer
def extract_and_convert_notebook(current_notebook_name, model_name, model_type="alpha"):
    """
    Extracts specific cells containing a given class name from a notebook and converts them into a Python script.

    Parameters:
    - current_notebook_name (str): Name of the current notebook file (without .ipynb extension).
    - model_name (str): Directory to save the converted Python script.
    - model_type (str): Type of model (alpha or portfolio).

    Returns:
    - output_path (str): Path to the converted script if successful, False otherwise.
    """

    current_directory = os.getcwd()

    notebook_path = f"{current_notebook_name}.ipynb"
    output_path = get_output_path(model_name, model_type)

    if not current_notebook_name:
        logger.info("No notebook name provided. Skipping extraction and conversion.")
        return output_path

    class_declaration = f"class {ModelTypeConfig[model_type.upper()].class_name}"

    # Log directory
    logger.info(f"Current directory: {current_directory}")
    logger.info(f"Notebook path: {notebook_path}")
    logger.info(f"Output path: {output_path}")

    # Ensure the output directory exists
    os.makedirs(model_name, exist_ok=True)

    # Load the notebook
    try:
        with open(notebook_path, "r", encoding="utf-8") as notebook_file:
            notebook = nbformat.read(notebook_file, as_version=4)
    except IOError:
        logger.error(f"Error: Could not find {current_directory}/{notebook_path}")
        raise

    # Extract cells that contain the class_name
    try:
        extracted_cells = [
            cell for cell in notebook.cells if class_declaration in cell.source
        ]

        if not extracted_cells:
            logger.error(
                f"No cells containing the class name '{class_declaration}' were found."
            )
            raise Exception("No cells found with the specified class name")

        extracted_notebook = nbformat.v4.new_notebook()
        extracted_notebook.cells = extracted_cells
    except Exception as e:
        logger.error(f"Error while extracting cells: {e}")
        raise

    # Convert the notebook to a Python script
    output_path = convert_notebook_to_script(extracted_notebook, output_path)

    try:
        display_file_content(output_path)
    except Exception as e:
        logger.error(f"Error while displaying file content: {e}")

    return output_path


def convert_notebook_to_script(notebook, output_path):
    """
    Converts a notebook object into a Python script and saves it to the specified path.

    Parameters:
    - notebook: Notebook object to convert.
    - output_path (str): Path to save the converted script.

    Returns:
    - output_path (str): Path to the converted script if successful, False otherwise.
    """
    exporter = ScriptExporter()

    try:
        body, resources = exporter.from_notebook_node(notebook)

        with open(output_path, "w", encoding="utf-8") as output_file:
            output_file.write(body)
    except Exception as e:
        logger.error(f"Error during conversion: {e}")
        raise

    return output_path


def display_file_content(file_path):
    """
    Reads the content of the given file path, applies syntax highlighting for Python code,
    and returns it as an HTML widget with a Mac-inspired design. The file download link is displayed separately.
    :param file_path: Path to the file to be displayed
    :return: HTML widget
    """
    if not os.path.exists(file_path):
        return widgets.HTML(value=f"<p>Error: File '{file_path}' does not exist.</p>")

    # Display file download link separately
    file_link = FileLink(
        file_path,
        result_html_prefix="Check the generated Python script:",
        result_html_suffix="<br>If something went wrong, <strong style='color: #ff5f56;'>Please save the notebook</strong> and try again.",
    )
    display(file_link)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            file_content = f.read()
    except Exception as e:
        return widgets.HTML(value=f"<p>File reading error: {str(e)}</p>")

    formatter = HtmlFormatter(style="monokai")
    highlighted_code = highlight(file_content, PythonLexer(), formatter)

    custom_style = """
    <style>
        .mac-window {
            background-color: #2D2D2D;
            border-radius: 6px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            margin: 20px 0;
            overflow: hidden;
            font-family: 'SF Mono', 'Menlo', 'Monaco', 'Courier', monospace;
        }
        .mac-titlebar {
            background: linear-gradient(to bottom, #3a3a3a, #2d2d2d);
            height: 22px;
            padding: 7px 10px;
            display: flex;
            align-items: center;
        }
        .mac-buttons {
            display: flex;
            gap: 6px;
        }
        .mac-button {
            width: 12px;
            height: 12px;
            border-radius: 50%;
        }
        .mac-close { background-color: #ff5f56; }
        .mac-minimize { background-color: #ffbd2e; }
        .mac-zoom { background-color: #27c93f; }
        .mac-content {
            padding: 10px;
            overflow-x: auto;
            max-height: 400px;  /* Set a max height to enable vertical scrolling */
            overflow-y: auto;  /* Enable vertical scrolling */
        }
        .mac-content pre {
            margin: 0;
            padding: 10px;
            font-size: 11px;  /* Reduced font size to 11px */
            line-height: 1.5;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        /* Customize scrollbar for webkit browsers */
        .mac-content::-webkit-scrollbar {
            width: 12px;
            height: 12px;
        }
        .mac-content::-webkit-scrollbar-thumb {
            background: #666;
            border-radius: 6px;
            border: 3px solid #2D2D2D;
        }
        .mac-content::-webkit-scrollbar-track {
            background: #2D2D2D;
        }
    </style>
    """

    style = custom_style + "<style>" + formatter.get_style_defs() + "</style>"

    html_content = f"""
    {style}
    <div class="mac-window">
        <div class="mac-titlebar">
            <div class="mac-buttons">
                <div class="mac-button mac-close"></div>
                <div class="mac-button mac-minimize"></div>
                <div class="mac-button mac-zoom"></div>
            </div>
        </div>
        <div class="mac-content">
            {highlighted_code}
        </div>
    </div>
    """

    display(widgets.HTML(value=html_content))
