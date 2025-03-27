import xlwings as xw
import argparse

def refresh_dynamics_365_connection(file_path):
    """Refresh external data connections in an Excel file for all sheets without altering formatting"""
    app = xw.App(visible=False)  # Run Excel in the background
    try:
        wb = xw.Book(file_path)

        # Iterate through all sheets (not strictly necessary for RefreshAll, but ensures accessibility)
        for sheet in wb.sheets:
            print(f"Processing sheet: {sheet.name}")

        wb.api.RefreshAll()  # Refresh all external connections, including Dynamics 365
        wb.save()
        wb.close()
        print(f"Successfully refreshed all connections in {file_path}")

    except Exception as e:
        print(f"Error refreshing file: {e}")
    finally:
        app.quit()  # Ensure Excel closes properly

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Refresh an Excel file's Dynamics 365 connections without opening")
    parser.add_argument("file", help="Path to the Excel file (.xlsx)")

    args = parser.parse_args()
    refresh_dynamics_365_connection(args.file)
