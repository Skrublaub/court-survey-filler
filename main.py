import argparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from typing import Final
from time import sleep
from datetime import date
from shutil import which

BRAVE_PATH: Final[str] = which("brave")
DRIVER_PATH: Final[str] = "./chromedriver"


def main() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--time",
        required=True,
        type=str,
        help="Time slot to reserve. In form of #am or #pm",
    )
    parser.add_argument(
        "-r",
        "--racquetball",
        required=True,
        action="store_true",
        help="Whether to reserve a badminton court or racquetball court. If this flag is passed, a racquetball court "
        "is reserved. If nothing is passed, a badminton court is reserved.",
    )
    parser.add_argument(
        "-f", "--first-name", required=True, type=str, help="First name of user."
    )
    parser.add_argument(
        "-l", "--last-name", required=True, type=str, help="Last name of user."
    )
    parser.add_argument(
        "-p", "--phone-number", required=True, type=str, help="Phone number of user"
    )
    parser.add_argument(
        "-e", "--email", required=True, type=str, help="Umsystem email of user"
    )
    args: argparse.Namespace = parser.parse_args()

    options: webdriver.ChromeOptions = webdriver.ChromeOptions()
    options.binary_location = BRAVE_PATH

    driver = webdriver.Chrome(options=options)
    driver.get("https://studentrec.mst.edu/general-information/reservations/")

    reserve_button: WebElement = driver.find_element(
        By.XPATH,
        "/html/body/div/main/div/div[1]/div/div/span/section[2]/div/div/span/a/div",
    )

    reserve_button.click()

    driver.implicitly_wait(7)

    calendar: WebElement = driver.find_element(By.ID, "QR~QID2")
    calendar.send_keys(str(date.today()))

    time_dropdown: WebElement = driver.find_element(By.ID, "QR~QID11")
    time_dropdown.find_element(By.XPATH, f"//option[. = '{args.time}']").click()

    court: str = "Badminton Court"
    if args.racquetball:
        court = "Racquetball Court"

    court_dropdown: WebElement = driver.find_element(By.ID, "QR~QID10")
    court_dropdown.find_element(By.XPATH, f"//option[. = '{court}']").click()

    fname_box: WebElement = driver.find_element(By.ID, "QR~QID5")
    fname_box.send_keys(args.first_name)

    lname_box: WebElement = driver.find_element(By.ID, "QR~QID6")
    lname_box.send_keys(args.last_name)

    phone_box: WebElement = driver.find_element(By.ID, "QR~QID7")
    phone_box.send_keys(args.phone_number)

    email_box: WebElement = driver.find_element(By.ID, "QR~QID8")
    email_box.send_keys(args.email)

    student_button: WebElement = driver.find_element(By.ID, "QID9-1-label")
    student_button.click()

    submit_button: WebElement = driver.find_element(By.ID, "NextButton")
    # submit_button.click()

    sleep(30)

    driver.quit()

    return


if __name__ == "__main__":
    main()
