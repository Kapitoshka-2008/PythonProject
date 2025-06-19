from src.hh_api import HeadHunterAPI
from src.json_storage import JSONSaver
from src.vacancy import Vacancy
from typing import List


def filter_vacancies(vacancies: List[Vacancy], filter_words: List[str]) -> List[Vacancy]:
    """Filter vacancies by keywords in description"""
    if not filter_words:
        return vacancies

    filtered = []
    for vacancy in vacancies:
        # Handle None values in description and requirements
        description = vacancy.description or ""
        requirements = vacancy.requirements or ""

        if any(word.lower() in description.lower()
               or word.lower() in requirements.lower()
               for word in filter_words):
            filtered.append(vacancy)
    return filtered


def get_vacancies_by_salary(vacancies: List[Vacancy], salary_range: str) -> List[Vacancy]:
    """Filter vacancies by salary range"""
    try:
        min_salary, max_salary = map(int, salary_range.split('-'))
        return [v for v in vacancies if min_salary <= v.average_salary <= max_salary]
    except ValueError:
        return vacancies


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """Sort vacancies by salary"""
    return sorted(vacancies, reverse=True)


def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """Get top N vacancies by salary"""
    return vacancies[:top_n]


def print_vacancies(vacancies: List[Vacancy]) -> None:
    """Print vacancies in a readable format"""
    if not vacancies:
        print("No vacancies found")
        return

    for i, vacancy in enumerate(vacancies, 1):
        print(f"\n{i}. {vacancy.title}")
        print(f"Company: {vacancy.company_name}")
        print(f"Salary: {vacancy.salary_from or 'N/A'} - {vacancy.salary_to or 'N/A'}")
        print(f"URL: {vacancy.url}")
        print(f"Requirements: {vacancy.requirements or 'Not specified'}")
        print("-" * 80)


def user_interaction():
    """Main function for user interaction"""
    # Initialize API and storage
    hh_api = HeadHunterAPI()
    json_saver = JSONSaver()

    while True:
        print("\nJob Search Program")
        print("1. Search for vacancies")
        print("2. View saved vacancies")
        print("3. Filter saved vacancies")
        print("4. Exit")

        choice = input("\nEnter your choice (1-4): ")

        if choice == "1":
            search_query = input("Enter search query: ")
            vacancies_data = hh_api.get_vacancies(search_query)
            vacancies = Vacancy.cast_to_object_list(vacancies_data)

            # Save all found vacancies
            for vacancy in vacancies:
                json_saver.add_vacancy(vacancy)

            print(f"\nFound {len(vacancies)} vacancies")

            # Get top N vacancies
            top_n = int(input("Enter number of top vacancies to display: "))
            filter_words = input("Enter keywords to filter (space-separated): ").split()
            salary_range = input("Enter salary range (e.g., 100000-150000): ")

            filtered = filter_vacancies(vacancies, filter_words)
            ranged = get_vacancies_by_salary(filtered, salary_range)
            sorted_vacancies = sort_vacancies(ranged)
            top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

            print_vacancies(top_vacancies)

        elif choice == "2":
            vacancies = json_saver.get_vacancies()
            print_vacancies(vacancies)

        elif choice == "3":
            filter_words = input("Enter keywords to filter (space-separated): ").split()
            salary_range = input("Enter salary range (e.g., 100000-150000): ")

            vacancies = json_saver.get_vacancies()
            filtered = filter_vacancies(vacancies, filter_words)
            ranged = get_vacancies_by_salary(filtered, salary_range)
            sorted_vacancies = sort_vacancies(ranged)

            print_vacancies(sorted_vacancies)

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    user_interaction()
