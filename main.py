import csv
import os
import time
from datetime import datetime
from statistics import mean

CPR_LOG_FILE = "cpr_session_log.csv"
AUDIT_LOG_FILE = "cpr_audit.log"

TARGET_CPM = 110
TARGET_INTERVAL = 60 / TARGET_CPM

compression_records = []
compression_intervals = []

total_compressions = 0
cycles_completed = 0


def log_audit_event(action):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entry = (
        f"[{timestamp}] "
        f"Action: {action}\n"
    )

    with open(AUDIT_LOG_FILE, "a") as logfile:
        logfile.write(entry)


def play_compression_tone():
    """
    Distinct compression sound.
    """

    try:
        import winsound

        winsound.Beep(1200, 75)

    except Exception:
        print("BEEP")


def play_cycle_switch_tone():
    """
    Signals rescue breaths.
    """

    try:
        import winsound

        winsound.Beep(800, 250)
        winsound.Beep(600, 250)

    except Exception:
        print("=== RESCUE BREATHS ===")


def play_pulse_check_tone():
    """
    Distinct pulse-check signal.
    """

    try:
        import winsound

        winsound.Beep(400, 350)
        winsound.Beep(400, 350)
        winsound.Beep(400, 350)

    except Exception:
        print("=== PULSE CHECK ===")


def calculate_pacing_accuracy():
    if not compression_intervals:
        return 100.0

    accuracy_scores = []

    for interval in compression_intervals:

        error_percent = (
            abs(interval - TARGET_INTERVAL)
            / TARGET_INTERVAL
        ) * 100

        accuracy = max(
            0,
            100 - error_percent
        )

        accuracy_scores.append(accuracy)

    return round(mean(accuracy_scores), 2)


def record_compression(
    compression_number,
    timestamp,
    interval
):
    compression_records.append([
        compression_number,
        timestamp,
        interval
    ])


def save_session_log():
    with open(
        CPR_LOG_FILE,
        "w",
        newline=""
    ) as logfile:

        writer = csv.writer(logfile)

        writer.writerow([
            "Compression #",
            "Timestamp",
            "Interval (Seconds)"
        ])

        for record in compression_records:
            writer.writerow(record)

        writer.writerow([])
        writer.writerow(["SESSION SUMMARY"])

        writer.writerow([
            "Total Compressions",
            total_compressions
        ])

        writer.writerow([
            "Cycles Completed",
            cycles_completed
        ])

        writer.writerow([
            "Average Pacing Accuracy (%)",
            calculate_pacing_accuracy()
        ])

    log_audit_event("SESSION_LOG_SAVED")


def perform_cpr_cycle():
    global total_compressions
    global cycles_completed

    print("\n--- CPR CYCLE STARTED ---")

    previous_time = None

    for compression in range(1, 31):

        current_time = time.time()

        timestamp = (
            datetime.now()
            .strftime("%Y-%m-%d %H:%M:%S.%f")
        )

        play_compression_tone()

        print(
            f"Compression "
            f"{compression}/30"
        )

        interval = ""

        if previous_time is not None:

            measured_interval = (
                current_time - previous_time
            )

            interval = round(
                measured_interval,
                3
            )

            compression_intervals.append(
                measured_interval
            )

        total_compressions += 1

        record_compression(
            total_compressions,
            timestamp,
            interval
        )

        previous_time = current_time

        time.sleep(TARGET_INTERVAL)

    cycles_completed += 1

    log_audit_event(
        f"CYCLE_{cycles_completed}_COMPLETED"
    )

    play_cycle_switch_tone()

    print(
        "\n*** GIVE 2 RESCUE BREATHS ***"
    )

    input(
        "Press ENTER after rescue breaths..."
    )


def pulse_check():
    print("\n--- PULSE CHECK ---")

    play_pulse_check_tone()

    input(
        "Press ENTER to continue CPR..."
    )

    log_audit_event(
        "PULSE_CHECK_COMPLETED"
    )


def display_session_summary():
    print("\n--- SESSION SUMMARY ---")

    print(
        f"Total Compressions: "
        f"{total_compressions}"
    )

    print(
        f"Cycles Completed: "
        f"{cycles_completed}"
    )

    print(
        f"Average Accuracy: "
        f"{calculate_pacing_accuracy()}%"
    )

    log_audit_event(
        "SESSION_SUMMARY_VIEWED"
    )


def start_cpr_session():
    print("\nCPR METRONOME TRAINER")
    print("----------------------")
    print(
        f"Compression Rate: "
        f"{TARGET_CPM} BPM"
    )

    log_audit_event(
        "CPR_SESSION_STARTED"
    )

    while True:

        perform_cpr_cycle()

        if cycles_completed % 5 == 0:
            pulse_check()

        choice = input(
            "\nStart another cycle? "
            "(y/n): "
        ).lower()

        if choice != "y":
            break

    display_session_summary()

    save_session_log()

    log_audit_event(
        "CPR_SESSION_ENDED"
    )


def main():
    start_cpr_session()


if __name__ == "__main__":
    main()