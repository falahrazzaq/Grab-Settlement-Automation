# ==============================================================================
# Copyright (c) 2026 Falaharzq
# All rights reserved.
#
# Project: Grab Settlement Automation
# Author: Falah Ath Thaariq Razzaq
# Repository: https://github.com/falahrazzaq/Grab-Settlement-Automation
# ==============================================================================

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import time



# ============================================================
# CONFIGURATION
# ============================================================

URL = "https://app.metrodata.co.id/Taxivoucher/Default.aspx"


# ------------------------------------------------------------
# HARD-CODED DATA
# ------------------------------------------------------------

RECORDS = [

    # Add more records here
    #
    # {
    #     "booking_code": "booking code from Grab",
    #     "so_number": "number for SO lookup",
    #     "charge_type": "Cost",
    #     "customer_code": "code for customer name lookup",
    #     "customer_pic": "name of customer PIC",
    #     "multiple_location": False,
    #     "trip_purpose": "Purpose of the trip",
    # },
]


# ============================================================
# SELECTORS FROM THE ACTUAL HTML
# ============================================================

BOOKING_CODE = (
    "#ctl00_ContentPlaceHolder1_apSettlement_content_txtBookingCode"
)

SETTLE_BUTTON = (
    "#ctl00_ContentPlaceHolder1_apSettlement_content_btnSettleGrabCode"
)


# ------------------------------------------------------------
# CHARGE TYPE
# ------------------------------------------------------------

CHARGE_TYPE = (
    "#ctl00_ContentPlaceHolder1_apSettlement_content_ddlGrabChargeType"
)


# ------------------------------------------------------------
# SO
# ------------------------------------------------------------

SO_LOOKUP_BUTTON = (
    "#ctl00_ContentPlaceHolder1_apSettlement_content_imgGrabSOLookup"
)

SO_FIELD = (
    "#ctl00_ContentPlaceHolder1_apSettlement_content_txtGrabSO"
)

SO_SEARCH_POPUP = (
    "#ctl00_ContentPlaceHolder1_pnlSOLookup"
)

SO_SEARCH_INPUT = (
    "#ctl00_ContentPlaceHolder1_SOLookup_txtSOSearch"
)

SO_SEARCH_BUTTON = (
    "#ctl00_ContentPlaceHolder1_SOLookup_btnSOSearch"
)

SO_RESULT = (
    "#ctl00_ContentPlaceHolder1_SOLookup_gvSOSAP"
    " #ctl00_ContentPlaceHolder1_SOLookup_gvSOSAP_ctl02_lbSONumber"
)

CHECK_SO_BUTTON = (
    "#ctl00_ContentPlaceHolder1_apSettlement_content_btnGrabCheckSO"
)

VALID_SO = (
    "#ctl00_ContentPlaceHolder1_apSettlement_content_hdnValidSO"
)


# ------------------------------------------------------------
# PART NUMBER  (left as-is, not touched)
# ------------------------------------------------------------

PART_NUMBER = (
    "#ctl00_ContentPlaceHolder1_apSettlement_content_ddlGrabPartnumber"
)


# ------------------------------------------------------------
# COMPANY / DEPARTMENT  (left as-is, not touched)
# ------------------------------------------------------------

CHARGE_COMPANY = (
    "#ctl00_ContentPlaceHolder1_apSettlement_content_ddlGrabChargeToComp"
)

CHARGE_DEPARTMENT = (
    "#ctl00_ContentPlaceHolder1_apSettlement_content_ddlGrabChargeToDept"
)


# ------------------------------------------------------------
# CUSTOMER NAME
#
# CONFIRMED from page HTML:
# ------------------------------------------------------------

CUSTOMER_LOOKUP_BUTTON = (
    "#ctl00_ContentPlaceHolder1_apSettlement_content_imgSearchCustomer"
)

# ------------------------------------------------------------
# CUSTOMER NAME — all confirmed from page HTML
# ------------------------------------------------------------

CUSTOMER_LOOKUP_BUTTON = (
    "#ctl00_ContentPlaceHolder1_apSettlement_content_imgSearchCustomer"
)

CUSTOMER_ID_FIELD = (
    "#ctl00_ContentPlaceHolder1_apSettlement_content_txtGrabCustomerID"
)

CUSTOMER_NAME_FIELD = (
    "#ctl00_ContentPlaceHolder1_apSettlement_content_txtGrabCustomerName"
)

CUSTOMER_SEARCH_POPUP = (
    "#ctl00_ContentPlaceHolder1_pnlCustomerLookup"
)

CUSTOMER_SEARCH_INPUT = (
    "#ctl00_ContentPlaceHolder1_customerLookup_txtCustomerSearch"
)

CUSTOMER_SEARCH_BUTTON = (
    "#ctl00_ContentPlaceHolder1_customerLookup_cmdCustomerSearch"
)

CUSTOMER_RESULT = (
    "#ctl00_ContentPlaceHolder1_customerLookup_gvCustomer"
    " #ctl00_ContentPlaceHolder1_customerLookup_gvCustomer_ctl02_lbCustomerName"
)


# ------------------------------------------------------------
# CUSTOMER PIC
# ------------------------------------------------------------

CUSTOMER_PIC = (
    "#ctl00_ContentPlaceHolder1_apSettlement_content_txtGrabCustomerPIC"
)


# ------------------------------------------------------------
# MULTIPLE LOCATION
# ------------------------------------------------------------

MULTIPLE_LOCATION = (
    "#ctl00_ContentPlaceHolder1_apSettlement_content_cbxGrabMultiLoc"
)


# ------------------------------------------------------------
# TRIP PURPOSE
# ------------------------------------------------------------

TRIP_PURPOSE = (
    "#ctl00_ContentPlaceHolder1_apSettlement_content_txtGrabTripPurpose"
)


# ------------------------------------------------------------
# CONFIRM
# ------------------------------------------------------------

CONFIRM_BUTTON = (
    "#ctl00_ContentPlaceHolder1_apSettlement_content_btnGrabCorpSubmit"
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def wait_for_page_update(page, milliseconds=1500):
    """
    ASP.NET Web Forms uses AJAX/postback heavily.
    Give the UpdatePanel time to finish updating.
    """
    page.wait_for_timeout(milliseconds)


def select_and_wait(page, selector, value, description):
    """
    Select an option and wait for ASP.NET postback.
    """

    print(f"  -> {description}: {value}")

    locator = page.locator(selector)

    locator.wait_for(
        state="visible",
        timeout=10000
    )

    # Wait until control is enabled
    try:
        locator.wait_for(
            state="attached",
            timeout=5000
        )
    except PlaywrightTimeoutError:
        pass

    # select_option will fail if disabled.
    # Wait a little longer for ASP.NET to enable it.
    for _ in range(20):

        if locator.is_enabled():
            break

        page.wait_for_timeout(500)

    if not locator.is_enabled():

        raise Exception(
            f"{description} is still disabled"
        )

    locator.select_option(value=value)

    wait_for_page_update(page, 1500)


def fill_field(page, selector, value, description):

    print(f"  -> {description}: {value}")

    locator = page.locator(selector)

    locator.wait_for(
        state="visible",
        timeout=10000
    )

    locator.fill(value)


# ============================================================
# SO LOOKUP
# ============================================================

def search_and_select_so(page, so_number):

    print(f"  -> Searching SO: {so_number}")

    # --------------------------------------------------------
    # Open SO popup
    # --------------------------------------------------------

    page.locator(SO_LOOKUP_BUTTON).click()

    page.locator(SO_SEARCH_POPUP).wait_for(
        state="visible",
        timeout=10000
    )

    print("  -> SO lookup opened")

    # --------------------------------------------------------
    # Enter SO number
    # --------------------------------------------------------

    page.locator(SO_SEARCH_INPUT).fill(
        so_number
    )

    # --------------------------------------------------------
    # Search
    # --------------------------------------------------------

    page.locator(SO_SEARCH_BUTTON).click()

    wait_for_page_update(page, 1500)

    # --------------------------------------------------------
    # Wait for result
    # --------------------------------------------------------

    result = page.locator(SO_RESULT)

    result.wait_for(
        state="visible",
        timeout=10000
    )

    found_so = result.inner_text().strip()

    print(f"  -> SO returned: {found_so}")

    # --------------------------------------------------------
    # SAFETY CHECK
    # --------------------------------------------------------

    if found_so != so_number:

        raise Exception(
            f"SO mismatch! "
            f"Expected [{so_number}], "
            f"but website returned [{found_so}]"
        )

    # --------------------------------------------------------
    # Click SO
    # --------------------------------------------------------

    result.click()

    wait_for_page_update(page, 1500)

    # --------------------------------------------------------
    # Verify SO field
    # --------------------------------------------------------

    actual_so = page.locator(
        SO_FIELD
    ).input_value()

    print(f"  -> SO selected: {actual_so}")

    if actual_so != so_number:

        raise Exception(
            f"SO selection failed! "
            f"Expected [{so_number}], "
            f"field contains [{actual_so}]"
        )

    print("  -> SO selection successful")


# ============================================================
# CHECK SO
# ============================================================

def check_so(page):

    print("  -> Checking SO...")

    page.locator(
        CHECK_SO_BUTTON
    ).click()

    # Wait for server-side validation
    wait_for_page_update(page, 2500)

    print("  -> SO check completed")


# ============================================================
# CUSTOMER NAME LOOKUP
# ============================================================

def search_and_select_customer(page, customer_code):
    """
    Same pattern as search_and_select_so, different control.
    """

    print(f"  -> Searching Customer: {customer_code}")

    # --------------------------------------------------------
    # Open Customer lookup popup
    # --------------------------------------------------------

    page.locator(CUSTOMER_LOOKUP_BUTTON).click()

    page.locator(CUSTOMER_SEARCH_POPUP).wait_for(
        state="visible",
        timeout=10000
    )

    print("  -> Customer lookup opened")

    # --------------------------------------------------------
    # Enter customer code
    # --------------------------------------------------------

    page.locator(CUSTOMER_SEARCH_INPUT).fill(
        customer_code
    )

    # --------------------------------------------------------
    # Search
    # --------------------------------------------------------

    page.locator(CUSTOMER_SEARCH_BUTTON).click()

    wait_for_page_update(page, 1500)

    # --------------------------------------------------------
    # Wait for result and select it
    # --------------------------------------------------------

    result = page.locator(CUSTOMER_RESULT)

    result.wait_for(
        state="visible",
        timeout=10000
    )

    found_id = page.locator(
        "#ctl00_ContentPlaceHolder1_customerLookup_gvCustomer_ctl02_lblCustomerID"
    ).inner_text().strip()

    print(f"  -> Customer found: {found_id}")

    if found_id != customer_code:

        raise Exception(
            f"Customer mismatch! "
            f"Expected [{customer_code}], "
            f"but website returned [{found_id}]"
        )

    result.click()

    wait_for_page_update(page, 1500)

    # --------------------------------------------------------
    # Verify customer fields
    # --------------------------------------------------------

    actual_id = page.locator(
        CUSTOMER_ID_FIELD
    ).input_value()

    actual_name = page.locator(
        CUSTOMER_NAME_FIELD
    ).input_value()

    print(f"  -> Customer ID   : {actual_id}")
    print(f"  -> Customer Name : {actual_name}")

    if actual_id != customer_code:

        raise Exception(
            f"Customer selection failed! "
            f"Expected code [{customer_code}], "
            f"field contains [{actual_id}]"
        )

    print("  -> Customer selection successful")


# ============================================================
# PROCESS ONE RECORD
# ============================================================

def process_record(page, record):

    booking_code = record["booking_code"]

    print("")
    print("=" * 70)
    print(f"PROCESSING BOOKING: {booking_code}")
    print("=" * 70)

    # --------------------------------------------------------
    # 1. Booking Code
    # --------------------------------------------------------

    fill_field(
        page,
        BOOKING_CODE,
        booking_code,
        "Booking Code"
    )

    # --------------------------------------------------------
    # 2. Settle
    # --------------------------------------------------------

    print("  -> Clicking Settle")

    page.locator(
        SETTLE_BUTTON
    ).click()

    wait_for_page_update(page, 2500)

    # --------------------------------------------------------
    # 3. Charge Type
    # --------------------------------------------------------

    select_and_wait(
        page,
        CHARGE_TYPE,
        record["charge_type"],
        "Charge Type"
    )

    # --------------------------------------------------------
    # 4. SO Lookup
    # --------------------------------------------------------

    search_and_select_so(
        page,
        record["so_number"]
    )

    # --------------------------------------------------------
    # 5. Check SO
    # --------------------------------------------------------

    check_so(page)

    # --------------------------------------------------------
    # 6. PART NUMBER
    #
    # SKIPPED — leave exactly as the website auto-populates.
    # --------------------------------------------------------

    print("  -> Part Number: LEAVE AS IS")

    # --------------------------------------------------------
    # 7. Charge to Company / Department
    #
    # SKIPPED — leave exactly as the website auto-populates.
    # --------------------------------------------------------

    print("  -> Charge to Company: LEAVE AS IS")
    print("  -> Charge to Department: LEAVE AS IS")

    # --------------------------------------------------------
    # 8. Customer Name lookup
    # --------------------------------------------------------

    search_and_select_customer(
        page,
        record["customer_code"]
    )

    # --------------------------------------------------------
    # 9. Customer PIC
    # --------------------------------------------------------

    fill_field(
        page,
        CUSTOMER_PIC,
        record["customer_pic"],
        "Customer PIC"
    )

    # --------------------------------------------------------
    # 10. Multiple Location
    # --------------------------------------------------------

    multiple_location = page.locator(
        MULTIPLE_LOCATION
    )

    if record["multiple_location"]:

        if not multiple_location.is_checked():

            print("  -> Multiple Location: CHECK")

            multiple_location.check()

    else:

        if multiple_location.is_checked():

            print("  -> Multiple Location: UNCHECK")

            multiple_location.uncheck()

        else:

            print("  -> Multiple Location: NO")


    # --------------------------------------------------------
    # 11. Trip Purpose
    # --------------------------------------------------------

    fill_field(
        page,
        TRIP_PURPOSE,
        record["trip_purpose"],
        "Trip Purpose"
    )

    # --------------------------------------------------------
    # 12. Final validation before submit
    # --------------------------------------------------------

    print("")
    print("  Checking final values...")

    actual_booking = page.locator(
        BOOKING_CODE
    ).input_value()

    actual_so = page.locator(
        SO_FIELD
    ).input_value()

    actual_pic = page.locator(
        CUSTOMER_PIC
    ).input_value()

    actual_purpose = page.locator(
        TRIP_PURPOSE
    ).input_value()

    print(f"    Booking Code : {actual_booking}")
    print(f"    SO           : {actual_so}")
    print(f"    Customer PIC : {actual_pic}")
    print(f"    Trip Purpose : {actual_purpose}")

    # --------------------------------------------------------
    # Safety checks
    # --------------------------------------------------------

    if actual_booking != booking_code:

        raise Exception(
            "Booking Code validation failed"
        )

    if actual_so != record["so_number"]:

        raise Exception(
            "SO validation failed"
        )

    if actual_pic != record["customer_pic"]:

        raise Exception(
            "Customer PIC validation failed"
        )

    if actual_purpose != record["trip_purpose"]:

        raise Exception(
            "Trip Purpose validation failed"
        )

    print("")
    print("  All values look correct.")

    # --------------------------------------------------------
    # 13. Confirm Settlement
    # --------------------------------------------------------

    print("")
    print("  !!! READY TO CONFIRM SETTLEMENT !!!")

    # --------------------------------------------------------
    # SAFETY PAUSE
    #
    # Change this to False when you're comfortable.
    # --------------------------------------------------------

    CONFIRM_AUTOMATICALLY = False

    if not CONFIRM_AUTOMATICALLY:

        print("")
        print(
            "  Automatic confirmation is OFF."
        )

        input(
            "  Press ENTER to Confirm Settlement..."
        )

    print("  -> Clicking Confirm Settlement")

    page.locator(
        CONFIRM_BUTTON
    ).click()

    wait_for_page_update(page, 3000)

    print("")
    print(f"  SUCCESS: {booking_code}")

    return True


# ============================================================
# MAIN
# ============================================================

def main():

    print("")
    print("=" * 70)
    print("GRAB CORPORATE SETTLEMENT AUTOMATION")
    print("=" * 70)
    print("")
    print(f"Records to process: {len(RECORDS)}")
    print("")

    results = []

    with sync_playwright() as p:

        # ----------------------------------------------------
        # Browser
        # ----------------------------------------------------

        browser = p.chromium.launch(
            headless=False
        )

        context = browser.new_context()

        page = context.new_page()

        # ----------------------------------------------------
        # Open website
        # ----------------------------------------------------

        print("Opening website...")

        page.goto(
            URL,
            wait_until="domcontentloaded"
        )

        print("")
        print("Website opened.")
        print("")
        print(
            "If login is required, please login manually."
        )

        input(
            "Press ENTER after you are logged in..."
        )

        # ----------------------------------------------------
        # Process records
        # ----------------------------------------------------

        for index, record in enumerate(RECORDS, start=1):

            print("")
            print(
                f"Record {index}/{len(RECORDS)}"
            )

            try:

                process_record(
                    page,
                    record
                )

                results.append({
                    "booking_code":
                        record["booking_code"],
                    "status":
                        "SUCCESS"
                })

            except Exception as e:

                print("")
                print(
                    f"ERROR processing "
                    f"{record['booking_code']}"
                )

                print(str(e))

                # --------------------------------------------
                # Take screenshot
                # --------------------------------------------

                screenshot_name = (
                    f"error_"
                    f"{record['booking_code']}.png"
                )

                page.screenshot(
                    path=screenshot_name,
                    full_page=True
                )

                print(
                    f"Screenshot saved: "
                    f"{screenshot_name}"
                )

                results.append({
                    "booking_code":
                        record["booking_code"],
                    "status":
                        "ERROR",
                    "error":
                        str(e)
                })

                # --------------------------------------------
                # Don't continue automatically after error
                # --------------------------------------------

                answer = input(
                    "\nContinue with next booking? "
                    "[y/N]: "
                )

                if answer.lower() != "y":

                    print(
                        "Stopping automation."
                    )

                    break

        # ----------------------------------------------------
        # Results
        # ----------------------------------------------------

        print("")
        print("=" * 70)
        print("RESULT")
        print("=" * 70)

        for result in results:

            print(
                f"{result['booking_code']:<25} "
                f"{result['status']}"
            )

        print("")
        print("Automation finished.")

        input(
            "Press ENTER to close browser..."
        )

        browser.close()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
