# ==============================
# تصنيفات الفعاليات
# ==============================

EVENT_CATEGORIES = [
    ("all", "الكل"),
    ("course", "دورة"),
    ("workshop", "ورشة"),
    ("conference", "مؤتمر"),
    ("seminar", "ندوة"),
]


# ==============================
# حالات الفعاليات
# ==============================

EVENT_STATUS = [
    ("all", "الكل"),
    ("available", "متاح"),
    ("full", "مكتمل"),
    ("cancelled", "ملغي"),
]


# ==============================
# أنواع الفعاليات
# ==============================

EVENT_TYPES = [
    ("all", "الكل"),
    ("onsite", "حضوري"),
    ("online", "أونلاين"),
    ("hybrid", "مختلط"),
]


# ==============================
# المدن
# ==============================

EVENT_CITIES = [
    ("all", "كل المدن"),
    ("sanaa", "صنعاء"),
    ("aden", "عدن"),
    ("taiz", "تعز"),
    ("ibb", "إب"),
    ("hodeidah", "الحديدة"),
    ("hadramout", "حضرموت"),
]


# ==============================
# ترتيب الفعاليات
# ==============================

SORT_OPTIONS = [
    ("newest", "الأحدث"),
    ("oldest", "الأقدم"),
    ("price_high", "الأعلى سعراً"),
    ("price_low", "الأقل سعراً"),
]


# ==============================
# أسماء بديلة للتصنيفات
# ==============================

CATEGORY_ALIASES = {

    "course": [
        "دورة",
        "كورس",
        "دورات",
        "كورسات",
    ],

    "workshop": [
        "ورشة",
        "ورشه",
        "تدريب",
        "تدريبية",
    ],

    "conference": [
        "مؤتمر",
        "كونفرنس",
        "مؤتمرات",
    ],

    "seminar": [
        "ندوة",
        "ندوه",
        "سيمنار",
        "محاضرة",
    ],
}


# ==============================
# دالة الحصول على اسم التصنيف
# ==============================

def get_category_name(category_code):

    for code, name in EVENT_CATEGORIES:

        if code == category_code:
            return name

    return "غير محدد"


# ==============================
# دالة الحصول على اسم الحالة
# ==============================

def get_status_name(status_code):

    for code, name in EVENT_STATUS:

        if code == status_code:
            return name

    return "غير محدد"


# ==============================
# دالة الحصول على اسم نوع الفعالية
# ==============================

def get_type_name(type_code):

    for code, name in EVENT_TYPES:

        if code == type_code:
            return name

    return "غير محدد"


# ==============================
# دالة الحصول على اسم المدينة
# ==============================

def get_city_name(city_code):

    for code, name in EVENT_CITIES:

        if code == city_code:
            return name

    return "غير محددة"


# ==============================
# دالة البحث عن التصنيف
# ==============================

def find_category(value):

    if not value:
        return "all"

    value = value.strip().lower()

    for category, names in CATEGORY_ALIASES.items():

        for name in names:

            if value == name.lower():
                return category

    return "all"