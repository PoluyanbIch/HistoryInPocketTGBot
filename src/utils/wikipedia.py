import wikipediaapi

wikipedia = wikipediaapi.Wikipedia('ru')


def get_monthly_theme():
    return wikipedia.page("История_России").title
