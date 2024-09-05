from functools import cached_property
import sys
from tasks.general.page import *

class PageMap():
    @cached_property
    def MAP(self):
        return {
            page_main: [page_exp, page_summon, page_store],
            page_exp: [page_realm_raid, page_main, page_chapter_entrance],
            page_chapter_entrance: [page_exp],
            page_realm_raid: [page_exp, page_guild_raid],
            page_guild_raid: [page_realm_raid],
            page_store: [page_main],
            page_sleep: [page_main],
            page_login: [page_main],
            page_summon: [page_main]
        }

    def find_path(self, from_page: Page, to_page: Page, path=[]):
        path = path + [from_page]
        if from_page == to_page:
            return path
        if from_page not in self.MAP.keys():
            return None
        for page in self.MAP[from_page]:
            if page not in path:
                newpath = self.find_path(page, to_page, path)
                if newpath:
                    return newpath
        return None


if __name__ == "__main__":
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent.parent))
    from tasks.general.page import *
    m = PageMap()
    path = m.find_path(page_exp, page_summon)
    print([p.name for p in path])
