import pandas as pd
from ics import Calendar, Event
from datetime import datetime
import pytz


def generate_ics(input_excel_path, output_ics_path, timezone_str="Europe/Rome"):
    """
    Converts an Excel file to an ICS calendar file.

    Parameters:
        input_excel_path (str): Path to the input Excel file.
        output_ics_path (str): Path to save the output ICS file.
        timezone_str (str): Timezone to use for the calendar events.

    Returns:
        None
    """
    # Set the timezone
    timezone = pytz.timezone(timezone_str)

    # Load data from the Excel file
    calendar_df = pd.read_excel(input_excel_path)

    # Initialize the calendar
    calendar = Calendar()

    # Itera su ciascuna riga del dataframe

    for _, row in calendar_df.iterrows():
        if (
            pd.isnull(row.get("Unità formativa"))
            or row["Unità formativa"].strip() == ""
        ):
            continue  # Skip if "Unità formativa" is empty
        if pd.isnull(row["Orario inizio"]) or pd.isnull(row["Orario fine"]):
            continue  # Salta le righe senza orari

        # Crea l'evento
        event = Event()

        # Componi il titolo dell'evento
        subject = row["Unità formativa"]
        description = row["Materia"]
        teacher = row["Professore"]
        event.name = f"{subject} - {description} CON {teacher}"

        # Converte data e orari in datetime
        date_only = datetime.strptime(
            row["Data"], "%d/%m/%Y"
        ).date()  # Assuming the format is day/month/year
        start_time = datetime.combine(
            date_only, datetime.strptime(row["Orario inizio"], "%H,%M").time()
        )
        end_time = datetime.combine(
            date_only, datetime.strptime(row["Orario fine"], "%H,%M").time()
        )

        # Imposta il fuso orario sugli orari
        event.begin = timezone.localize(start_time)
        event.end = timezone.localize(end_time)

        # Aggiunge l'evento al calendario
        calendar.events.add(event)

    with open(output_ics_path, "w") as f:
        f.writelines(calendar)


# Example usage (uncomment to test):
# excel_to_ics("./newCalendar.xlsx", "./calendar.ics")
