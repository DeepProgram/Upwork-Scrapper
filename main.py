import time
import re
from automation import create_Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


def load_individual_job_page(driver, job_page_element):
    data_dict = {}
    time.sleep(0.5)
    ActionChains(driver).move_to_element(driver.find_element(By.CSS_SELECTOR, "li[class='why-upwork-dropdown "
                                                                              "nav-dropdown my-5 my-lg-0']")).perform()
    time.sleep(0.5)
    job_page_element.click()
    time.sleep(2)
    data_dict["title"] = get_job_title(driver)
    data_dict["details"] = get_job_details(driver)
    return data_dict


def get_job_title(driver):
    data = driver.find_element(By.CSS_SELECTOR, "h1[class='my-0 mr-10 display-rebrand']")
    job_title = data.text
    return job_title


def get_job_details(driver):
    job_details_dict = {}
    section_elements = driver.find_elements(By.CSS_SELECTOR, "section[class='up-card-section']")
    for index, content in enumerate(section_elements[:5]):
        if index == 0:
            job_applicable_location, job_posted_time = process_job_applicable_location_time(content)
            job_details_dict["job_applicable_location"] = job_applicable_location
            job_details_dict["job_posted_time"] = job_posted_time
        elif index == 1:
            job_description = content.text
            job_details_dict["job_description"] = job_description
        elif index == 2:
            job_type_details_dict = process_job_type_details(content)
            job_details_dict["job_type_details"] = job_type_details_dict
        elif index == 3:
            required_job_skill_dict = process_job_skills(content)
            job_details_dict["required_skills"] = required_job_skill_dict
        elif index == 4:
            job_activity_dict = process_job_activity(content)
            job_details_dict["job_activity"] = job_activity_dict
    return job_details_dict


def process_job_applicable_location_time(content):
    job_applicable_location_and_post_time = re.split(r"Posted |Renewed ", content.text)[1].split("\n")
    job_applicable_location = job_applicable_location_and_post_time[1]
    job_posted_time = job_applicable_location_and_post_time[0]
    return [job_applicable_location, job_posted_time]


def process_job_type_details(content):
    job_info_dict = {}
    for list_element in content.find_elements(By.TAG_NAME, "li"):
        job_info = list_element.text.split("\n")
        if len(job_info) == 1:
            job_info_dict["job_location"] = job_info[0]
        else:
            job_info_dict[job_info[1]] = job_info[0]
    return job_info_dict


def process_job_skills(content):
    job_skills_required_dict = {}
    for skills in content.find_elements(By.XPATH, "div/div/div"):
        skills_list = skills.text.split("\n")
        job_skills_required_dict[skills_list[0]] = \
            skills_list[1:] if "more" not in skills_list[-1] else skills_list[1:-1]
    return job_skills_required_dict


def process_job_activity(content):
    job_activity_dict = {}
    for values in content.find_elements(By.XPATH, "div/ul/li"):
        each_activity = values.text.split("\n")
        job_activity_dict[each_activity[1]] = each_activity[0]
    return job_activity_dict


def load_job_search_page(driver):
    driver.get("https://www.upwork.com/search/jobs/?q=web+scraping")
    time.sleep(1)
    elements = driver.find_elements(By.CSS_SELECTOR,
                                    "section[class='up-card-section up-card-list-section up-card-hover']")
    job_list = []
    for element in elements:
        job_list.append(load_individual_job_page(driver, element))
        button_element = driver.find_element(By.CSS_SELECTOR, "button[class='up-btn up-btn-link up-slider-prev-btn "
                                                              "d-block']")
        button_element.click()
    print(job_list)


if __name__ == '__main__':
    print(time.ctime())
    driver_main = create_Driver()
    print("After Driver Creation")
    print(time.ctime())
    load_job_search_page(driver_main)
    print(time.ctime())
