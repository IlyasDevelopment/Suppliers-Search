fields_xpaths_regexps = [
    (
        "psrn",
        "//*[@id=\"main-total-card\"]/div/div[7]/div[1]/div[1]/div[1]/p[2]/span",
        r"\d+"
    ),
    (
        "fair_business_rating",
        "//*[@id=\"main-total-card\"]/div/div[2]/div[1]/div/div/div[1]/div/a/span[1]/b",
        r"\d+"
    ),
    (
        "fair_business_rating_comment",
        "//*[@id=\"main-total-card\"]/div/div[2]/div[1]/div/div/div[1]/div/a/span[2]/b",
        r"[а-яА-я]+"
    ),
    (
        "registration_date",
        "//*[@id=\"main-total-card\"]/div/div[7]/div[1]/p[2]",
        r"\d{2}\.\d{2}\.\d{4}"
    ),
    (
        "main_activity",
        "//*[@id=\"main-total-card\"]/div/div[7]/div[1]/div[2]/p[2]/span",
        r">([\S\s]+)<"
    ),
    (
        "authorized_capital",
        "//*[@id=\"main-total-card\"]/div/div[7]/div[1]/div[5]/p[2]/b",
        r"[\d ]+"
    ),
    (
        "profit",
        "//*[@id=\"main-bottom-block\"]/div[2]/div[1]/div[3]/div/p[2]/b",
        r"<b>([\S\s]+) ₽</b>"
        # r"<b>([0-9 а-я]+)*</b>"
        # r".*"
    ),
    (
        "name",
        "//*[@id=\"main-total-card\"]/div/div[1]/div[1]/h2/text()",
        r".+"
    )
]
