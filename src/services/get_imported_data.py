def get_imported_data(company):
    out = {}
    out["company_name"] = company.company_name
    out["url"] = company.url
    out["founded_year"] = company.founded_year
    out["total_employees"] = company.total_employees
    out["headquarters_city"] = company.headquarters_city
    out["employee_locations"] = company.employee_locations
    out["employee_growth_2y"] = company.employee_growth_2y
    out["employee_growth_1y"] = company.employee_growth_1y
    out["employee_growth_6m"] = company.employee_growth_6m
    out["description"] = company.description
    out["industry"] = company.industry
    return out
