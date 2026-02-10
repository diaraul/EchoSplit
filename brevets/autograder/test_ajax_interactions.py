"""
Frontend tests for the brevet time calculator.
Tests the UI using Selenium.
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select


def test_page_load(selenium_driver, live_server):
    """Test that the page loads correctly with all required elements."""
    # Load the page
    selenium_driver.get(f"http://localhost:{live_server}")

    # Wait for the form to be present
    WebDriverWait(selenium_driver, 5).until(
        EC.presence_of_element_located((By.TAG_NAME, "form"))
    )

    # Verify page title
    assert "ACP Controle Times" in selenium_driver.title

    # Verify all required elements are present
    assert selenium_driver.find_element(By.NAME, "distance").is_displayed()
    assert selenium_driver.find_element(By.NAME, "begin_date").is_displayed()
    assert selenium_driver.find_element(By.NAME, "begin_time").is_displayed()

    # Verify table structure
    table = selenium_driver.find_element(By.CLASS_NAME, "control_time_table")
    headers = table.find_elements(By.TAG_NAME, "th")
    assert len(headers) == 6  # Miles, Km, Location, Open, Close, Notes

    # Verify at least one control row is present
    control_rows = selenium_driver.find_elements(By.CLASS_NAME, "control")
    assert len(control_rows) > 0


def test_brevet_distance_selection(selenium_driver, live_server):
    """Test that selecting different brevet distances works correctly."""
    selenium_driver.get(f"http://localhost:{live_server}")

    # Get the distance select element and wrap it in a Select object
    select_element = selenium_driver.find_element(By.NAME, "distance")
    select = Select(select_element)

    # Test all available distances
    test_distances = ["200", "300", "400", "600", "1000"]
    for distance in test_distances:
        # Select by value
        select.select_by_value(distance)
        # Verify the selected value
        assert select.first_selected_option.get_attribute("value") == distance


def test_time_conversion(selenium_driver, live_server):
    """Test that entering miles converts to kilometers and vice versa."""
    selenium_driver.get(f"http://localhost:{live_server}")

    # Get the first control row inputs
    miles_input = selenium_driver.find_elements(By.NAME, "miles")[0]
    km_input = selenium_driver.find_elements(By.NAME, "km")[0]

    # Test miles to km conversion
    test_miles = "100"
    miles_input.clear()
    miles_input.send_keys(test_miles)
    # Trigger the change event
    selenium_driver.execute_script(
        "arguments[0].dispatchEvent(new Event('change'))", miles_input
    )

    # Wait for the conversion to complete
    WebDriverWait(selenium_driver, 5).until(
        lambda d: km_input.get_attribute("value") != ""
    )

    expected_km = str(round(float(test_miles) * 1.609344, 1))
    assert km_input.get_attribute("value") == expected_km

    # Test km to miles conversion
    test_km = "100"
    km_input.clear()
    km_input.send_keys(test_km)
    # Trigger the change event
    selenium_driver.execute_script(
        "arguments[0].dispatchEvent(new Event('change'))", km_input
    )

    # Wait for the conversion to complete
    WebDriverWait(selenium_driver, 5).until(
        lambda d: miles_input.get_attribute("value") != ""
    )

    expected_miles = str(round(float(test_km) * 0.621371, 1))
    assert miles_input.get_attribute("value") == expected_miles


def test_open_close_times(selenium_driver, live_server):
    """Test that entering distances populates open and close times correctly."""
    selenium_driver.get(f"http://localhost:{live_server}")

    # Set up test parameters
    select = Select(selenium_driver.find_element(By.NAME, "distance"))
    select.select_by_value("200")  # 200km brevet

    # Set start time
    begin_date = selenium_driver.find_element(By.NAME, "begin_date")
    begin_time = selenium_driver.find_element(By.NAME, "begin_time")
    begin_date.clear()
    begin_date.send_keys("04302025")
    begin_time.clear()
    begin_time.send_keys("0800A")

    # Get the first control row inputs
    miles_input = selenium_driver.find_elements(By.NAME, "miles")[0]
    km_input = selenium_driver.find_elements(By.NAME, "km")[0]
    open_time = selenium_driver.find_elements(By.NAME, "open")[0]
    close_time = selenium_driver.find_elements(By.NAME, "close")[0]

    # Test with a valid distance (100km)
    km_input.clear()
    km_input.send_keys("100")
    # Trigger the change event
    selenium_driver.execute_script(
        "arguments[0].dispatchEvent(new Event('change'))", km_input
    )

    # Wait for AJAX response
    WebDriverWait(selenium_driver, 5).until(
        lambda d: open_time.get_attribute("value") != ""
    )

    # Verify times are populated with correct values
    assert open_time.get_attribute("value") == "Wed 4/30 10:56"
    assert close_time.get_attribute("value") == "Wed 4/30 14:40"


def test_multiple_controls(selenium_driver, live_server):
    """Test that multiple control points can be entered and times calculated."""
    selenium_driver.get(f"http://localhost:{live_server}")

    # Set up test parameters
    select = Select(selenium_driver.find_element(By.NAME, "distance"))
    select.select_by_value("1000")  # 1000km brevet

    # Set start time
    begin_date = selenium_driver.find_element(By.NAME, "begin_date")
    begin_time = selenium_driver.find_element(By.NAME, "begin_time")
    begin_date.clear()
    begin_date.send_keys("04302025")
    begin_time.clear()
    begin_time.send_keys("0800A")

    # Get all control row inputs
    miles_inputs = selenium_driver.find_elements(By.NAME, "miles")
    km_inputs = selenium_driver.find_elements(By.NAME, "km")
    open_times = selenium_driver.find_elements(By.NAME, "open")
    close_times = selenium_driver.find_elements(By.NAME, "close")

    # Test with multiple distances
    test_distances = ["100", "200", "650"]
    for i, distance in enumerate(test_distances):
        # Clear any existing values
        km_inputs[i].clear()
        km_inputs[i].send_keys(distance)
        # Trigger the change event
        selenium_driver.execute_script(
            "arguments[0].dispatchEvent(new Event('change'))", km_inputs[i]
        )

        # Wait for AJAX response
        WebDriverWait(selenium_driver, 5).until(
            lambda d: open_times[i].get_attribute("value") != ""
        )

        # Verify times are populated
        assert open_times[i].get_attribute("value") != ""
        assert close_times[i].get_attribute("value") != ""

        # Verify specific times for 650km
        if distance == "650":
            assert open_times[i].get_attribute("value") == "Thu 5/1 4:35"
            assert close_times[i].get_attribute("value") == "Fri 5/2 4:23"


def test_start_time_change(selenium_driver, live_server):
    """Test that changing the start time updates all control times."""
    selenium_driver.get(f"http://localhost:{live_server}")

    # Set up initial test parameters
    select = selenium_driver.find_element(By.NAME, "distance")
    select.send_keys("400")  # 400km brevet

    # Enter a control distance
    miles_input = selenium_driver.find_elements(By.NAME, "miles")[0]
    miles_input.send_keys("200")

    # Get initial times
    initial_open = selenium_driver.find_elements(By.NAME, "open")[0].get_attribute(
        "value"
    )
    initial_close = selenium_driver.find_elements(By.NAME, "close")[0].get_attribute(
        "value"
    )

    # Change start time
    begin_time = selenium_driver.find_element(By.NAME, "begin_time")
    begin_time.clear()
    begin_time.send_keys("0100A")  # Change to 1:00 AM

    # Get new times
    new_open = selenium_driver.find_elements(By.NAME, "open")[0].get_attribute("value")
    new_close = selenium_driver.find_elements(By.NAME, "close")[0].get_attribute(
        "value"
    )

    # Verify times have changed
    assert initial_open != new_open
    assert initial_close != new_close
