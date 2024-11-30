def pretty_date(yyyymmdd):
    year = yyyymmdd[:4]
    month = yyyymmdd[4:6]
    date = yyyymmdd[6:]
    return f"{year}-{month}-{date}"


def register_custom_filters(env):
    env.filters["pretty_date"] = pretty_date
