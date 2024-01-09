from pathlib import Path

import requests
from robocorp import browser
from robocorp.tasks import task

from RPA.Excel.Files import Files as Excel


OUTPUT_DIR = Path("output")
FILE_NAME = "challenge.xlsx"
REMOTE_FILE = f"https://rpachallenge.com/assets/downloadFiles/{FILE_NAME}"


@task
def solve_challenge():
    """Solve the RPA challenge"""
    response = requests.get(REMOTE_FILE)
    response.raise_for_status()
    OUTPUT_DIR.mkdir(exist_ok=True)
    file_path = OUTPUT_DIR / FILE_NAME
    file_path.write_bytes(response.content)

    excel = Excel()
    excel.open_workbook(file_path)
    rows = excel.read_worksheet_as_table("Sheet1", header=True)

    browser.configure(
        browser_engine="chromium",
        screenshot="only-on-failure",
        headless=True,
    )
    page = browser.goto("https://rpachallenge.com/")
    page.click("button:text('Start')")
    for row in rows:
        fill_and_submit_form(row)
    element = page.locator("css=div.congratulations")
    browser.screenshot(element)


def fill_and_submit_form(row):
    page = browser.page()
    page.fill("//input[@ng-reflect-name='labelFirstName']", str(row["First Name"]))
    page.fill("//input[@ng-reflect-name='labelLastName']", str(row["Last Name"]))
    page.fill("//input[@ng-reflect-name='labelCompanyName']", str(row["Company Name"]))
    page.fill("//input[@ng-reflect-name='labelRole']", str(row["Role in Company"]))
    page.fill("//input[@ng-reflect-name='labelAddress']", str(row["Address"]))
    page.fill("//input[@ng-reflect-name='labelEmail']", str(row["Email"]))
    page.fill("//input[@ng-reflect-name='labelPhone']", str(row["Phone Number"]))
    page.click("input:text('Submit')")
