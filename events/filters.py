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
# عربي + إنجليزي
# ==============================

CATEGORY_ALIASES = {

    "course": [
        "دورة",
        "دورات",
        "كورس",
        "كورسات",
        "course",
        "courses",
        "training",
        "train",
    ],

    "workshop": [
        "ورشة",
        "ورشه",
        "ورش",
        "workshop",
        "workshops",
    ],

    "conference": [
        "مؤتمر",
        "مؤتمرات",
        "كونفرنس",
        "conference",
        "conferences",
        "summit",
        "forum",
    ],

    "seminar": [
        "ندوة",
        "ندوه",
        "ندوات",
        "سيمنار",
        "seminar",
        "seminars",
        "lecture",
        "lectures",
    ],
}


# ==============================
# مرادفات الكلمات المهمة
# ==============================

SEARCH_SYNONYMS = {

    # الأمن السيبراني
    "امن": [
        "امن",
        "أمن",
        "امان",
        "security",
        "secure",
    ],

    "سيبراني": [
        "سيبراني",
        "سيبرانية",
        "الكتروني",
        "إلكتروني",
        "cyber",
        "cybersecurity",
        "cyber security",
    ],

    # الذكاء الاصطناعي
    "ذكاء": [
        "ذكاء",
        "ai",
        "artificial",
    ],

    "اصطناعي": [
        "اصطناعي",
        "artificial",
        "intelligence",
    ],

    # البرمجة
    "برمجة": [
        "برمجة",
        "برمجيات",
        "programming",
        "program",
        "software",
        "coding",
        "code",
    ],

    # قواعد البيانات
    "قواعد": [
        "قواعد بيانات",
        "قاعدة بيانات",
        "database",
        "databases",
        "db",
    ],

    # الشبكات
    "شبكات": [
        "شبكات",
        "شبكة",
        "network",
        "networks",
    ],

    # تطوير الويب
    "ويب": [
        "ويب",
        "مواقع",
        "web",
        "website",
        "websites",
    ],

    # تطوير التطبيقات
    "تطبيقات": [
        "تطبيق",
        "تطبيقات",
        "app",
        "apps",
        "application",
        "applications",
    ],
}


# ==============================
# تطبيع النص
# ==============================

def normalize_text(value):

    if not value:
        return ""

    value = str(value).strip().lower()

    # توحيد بعض الحروف العربية
    replacements = {
        "أ": "ا",
        "إ": "ا",
        "آ": "ا",
        "ة": "ه",
        "ى": "ي",
        "ؤ": "و",
        "ئ": "ي",
    }

    for old, new in replacements.items():
        value = value.replace(old, new)

    # توحيد المسافات
    value = " ".join(value.split())

    return value


# ==============================
# الحصول على اسم التصنيف
# ==============================

def get_category_name(category_code):

    for code, name in EVENT_CATEGORIES:

        if code == category_code:
            return name

    return "غير محدد"


# ==============================
# الحصول على اسم الحالة
# ==============================

def get_status_name(status_code):

    for code, name in EVENT_STATUS:

        if code == status_code:
            return name

    return "غير محدد"


# ==============================
# الحصول على اسم النوع
# ==============================

def get_type_name(type_code):

    for code, name in EVENT_TYPES:

        if code == type_code:
            return name

    return "غير محدد"


# ==============================
# الحصول على اسم المدينة
# ==============================

def get_city_name(city_code):

    for code, name in EVENT_CITIES:

        if code == city_code:
            return name

    return "غير محددة"


# ==============================
# البحث عن التصنيف
# يدعم العربي والإنجليزي
# ويدعم أكثر من كلمة
# ==============================

def find_category(value):

    value = normalize_text(value)

    if not value:
        return "all"

    for category, names in CATEGORY_ALIASES.items():

        for name in names:

            name = normalize_text(name)

            if name and name in value:
                return category

    return "all"


# ==============================
# توسيع كلمات البحث بالمرادفات
# ==============================

def expand_search_terms(value):

    value = normalize_text(value)

    if not value:
        return []

    terms = [value]

    words = value.split()

    for key, synonyms in SEARCH_SYNONYMS.items():

        key_normalized = normalize_text(key)

        for word in words:

            if word == key_normalized:
                for synonym in synonyms:

                    synonym = normalize_text(synonym)

                    if synonym not in terms:
                        terms.append(synonym)

    # أيضًا نفحص العبارات الكاملة
    for key, synonyms in SEARCH_SYNONYMS.items():

        key_normalized = normalize_text(key)

        if key_normalized in value:

            for synonym in synonyms:

                synonym = normalize_text(synonym)

                if synonym not in terms:
                    terms.append(synonym)

    return terms


# ==============================
# هل النص يحتوي على كلمة مشابهة؟
# ==============================

def matches_search(text, search_value):

    text = normalize_text(text)
    search_value = normalize_text(search_value)

    if not search_value:
        return True

    terms = expand_search_terms(search_value)

    for term in terms:

        if term and term in text:
            return True

    return False