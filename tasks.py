from robocorp import browser
from robocorp.tasks import task

from RPA.Excel.Files import Files as Excel
from RPA.HTTP import HTTP


@task
def solve_challenge():
    """Solve the RPA challenge"""
    browser.configure(
        browser_engine="chromium",
        screenshot="only-on-failure",
        headless=True,
    )

    HTTP().download("https://rpachallenge.com/assets/downloadFiles/challenge.xlsx")

    excel = Excel()
    excel.open_workbook("challenge.xlsx")
    rows = excel.read_worksheet_as_table("Sheet1", header=True)

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
