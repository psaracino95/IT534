"""
xml_processor.py
================
Module providing utility functions for reading, cleaning non-ASCII characters,
and parsing XML documents using BeautifulSoup.
"""

from bs4 import BeautifulSoup


def clean_xml_file(input_file_path: str, output_file_path: str) -> str:
    """Cleans out non-ASCII characters and writes to output_file_path."""
    with open(input_file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    cleaned = "".join(char for char in content if ord(char) < 128)

    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(cleaned)

    return output_file_path


def parse_employee_xml(xml_file_path: str) -> list[dict]:
    """Parses XML file and extracts all employee dict records containing name, title, profile_pic."""
    with open(xml_file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "lxml-xml")

    employees = []

    # Find all elements that contain all three required tags
    for parent in soup.find_all(True):
        name_elem = parent.find("name", recursive=False)
        title_elem = parent.find("title", recursive=False)
        pic_elem = parent.find("profile_pic", recursive=False)

        if name_elem and title_elem and pic_elem:
            employees.append(
                {
                    "name": name_elem.get_text(strip=True),
                    "title": title_elem.get_text(strip=True),
                    "profile_pic": pic_elem.get_text(strip=True),
                }
            )

    return employees
