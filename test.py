from selenium import webdriver
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
driver.implicitly_wait(30)
driver.get("https://useinsider.com/")
driver.maximize_window()

try:
    WebDriverWait(driver, 10).until(expected_conditions.title_contains("Insider"))

    company_menu = driver.find_element(By.LINK_TEXT, "Company")
    company_menu.click()

    WebDriverWait(driver, 30).until(expected_conditions.visibility_of(company_menu))

    careers_menu = driver.find_element(By.LINK_TEXT, "Careers")
    careers_menu.click()

    WebDriverWait(driver, 10).until(
        expected_conditions.visibility_of_element_located((By.XPATH, "//section[@id='career-our-location']")))
    WebDriverWait(driver, 10).until(
        expected_conditions.visibility_of_element_located((By.XPATH, "//section[@data-id='a8e7b90']")))

    teams_section = driver.find_element(By.XPATH, "//section[@id='career-find-our-calling']")
    driver.execute_script("arguments[0].scrollIntoView();", teams_section)

    WebDriverWait(driver, 10).until(expected_conditions.visibility_of(teams_section))

    see_all_teams_btn = driver.find_element(By.XPATH, "//a[contains(text(), 'See all teams')]")
    driver.execute_script("arguments[0].click();", see_all_teams_btn)

    quality_assurance_link = driver.find_element(By.XPATH, "//h3[contains(text(), 'Quality Assurance')]")
    driver.execute_script("arguments[0].click();", quality_assurance_link)

    see_all_qa_jobs_btn = driver.find_element(By.XPATH, "//section[@id='page-head']//a")
    driver.execute_script("arguments[0].click();", see_all_qa_jobs_btn)

    driver.execute_script("window.scrollBy(0, 500);", "")

    location_dropdown = driver.find_element(By.XPATH, "//select[@id='filter-by-location']")
    WebDriverWait(driver, 10).until(
        expected_conditions.element_to_be_clickable((By.XPATH, "//select[@id='filter-by-location']")))
    driver.execute_script("arguments[0].click();", location_dropdown)

    location_select = Select(location_dropdown)
    location_select.select_by_visible_text('Istanbul, Turkey')  # Veya 'Ankara, Turkey', 'Istanbul, Turkey' gibi

    department_dropdown = driver.find_element(By.XPATH, "//select[@id='filter-by-department']")
    WebDriverWait(driver, 10).until(
        expected_conditions.element_to_be_clickable((By.XPATH, "//select[@id='filter-by-department']")))
    driver.execute_script("arguments[0].click();", department_dropdown)

    department_select = Select(department_dropdown)
    department_select.select_by_visible_text('Quality Assurance')

    WebDriverWait(driver, 10).until(
        expected_conditions.visibility_of_all_elements_located((
            By.XPATH, "//div[contains(@class, 'position-list-item-wrapper')]"))
    )

    job_listings = driver.find_elements(By.XPATH, "//div[contains(@class, 'position-list-item-wrapper')]")

    WebDriverWait(driver, 30).until(
        expected_conditions.visibility_of_all_elements_located((
            By.XPATH, "//div[contains(@class, 'position-list-item-wrapper')]"))
    )

    position_locator = (By.XPATH, "//p[contains(@class, 'position-title')]")
    department_locator = (By.XPATH, "//span[contains(@class, 'position-department')]")
    location_locator = (By.XPATH, "//div[contains(@class, 'position-location')]")

    position_elements = WebDriverWait(driver, 30).until(
        expected_conditions.visibility_of_all_elements_located(position_locator))
    department_elements = WebDriverWait(driver, 30).until(
        expected_conditions.visibility_of_all_elements_located(department_locator))
    location_elements = WebDriverWait(driver, 30).until(
        expected_conditions.visibility_of_all_elements_located(location_locator))

    view_role_btn = driver.find_element(By.XPATH, "//div[contains(@class, 'position-list-item-wrapper')]/a")
    driver.execute_script("arguments[0].click();", view_role_btn)

    for position_element, department_element, location_element in zip(
                position_elements, department_elements, location_elements):
        try:
            position = WebDriverWait(driver, 30).until(expected_conditions.visibility_of(position_element)).text
            department = WebDriverWait(driver, 30).until(expected_conditions.visibility_of(department_element)).text
            location = WebDriverWait(driver, 30).until(expected_conditions.visibility_of(location_element)).text

            assert "qa" in position.lower() or "quality assurance" in position.lower(), \
                f"{position} pozisyonu QA veya Quality Assurance içermiyor!"
            assert "Quality Assurance" in department, f"{department} departmanı Quality Assurance değil!"
            assert "Istanbul, Turkey" in location, f"{location} lokasyonu Istanbul, Turkey değil!"

            print("Position:", position)
            print("Department:", department)
            print("Location:", location)
            print("------------------------------------------------")

        except StaleElementReferenceException:
            print("Bir öğe güncellendi, yeniden deniyor...")

    print("Tüm bölümler erişilebilir.")

except TimeoutException:
    print("Bir veya daha fazla bölüm erişilebilir değil.")

finally:
    driver.quit()
