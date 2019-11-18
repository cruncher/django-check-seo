# Standard Library
import re

# Third party
from django.utils.translation import gettext as _


def importance():
    """Scripts with higher importance will be executed in first.

    Returns:
        int -- Importance of the script.
    """
    return 1


def run(site):
    no_h2_name = _("No h2 tag")
    no_h2_settings = _("at least 1")
    no_h2_description = _(
        "H2 tags are useful because they are explored by search engines and can help them understand the subject of your page."
    )

    no_keywords_name = _("No keyword in h2")
    no_keywords_settings = _("at least 1")
    no_keywords_description = _(
        "Google uses h2 tags to better understand the subjects of your page."
    )

    h2 = site.soup.find_all("h2")
    if not h2:
        site.warnings.append(
            {
                "name": no_h2_name,
                "settings": no_h2_settings,
                "found": _("none"),
                "description": no_h2_description,
            }
        )
    else:
        occurence = []
        # check if each keyword
        for keyword in site.keywords:
            # is present at least
            for single_h2 in h2:
                occurence.append(
                    sum(
                        1
                        for _ in re.finditer(
                            r"\b%s\b" % re.escape(keyword.lower()),
                            single_h2.text.lower(),
                        )
                    )
                )
        # if no keyword is found in h2
        if not any(i > 0 for i in occurence):
            site.warnings.append(
                {
                    "name": no_keywords_name,
                    "settings": no_keywords_settings,
                    "found": _("none"),
                    "description": no_keywords_description,
                }
            )