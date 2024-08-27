import traceback
from tasks.general.assets import GeneralAssets as G

class Page():
    def __init__(self, check_button):
        super().__init__()
        self.check_button = check_button
        self.links = {}
        (filename, line_number, function_name,
         text) = traceback.extract_stack()[-2]
        self.name = text[:text.find('=')].strip()

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name

    def link(self, button, destination):
        self.links[destination] = button


# 主界面 Main
page_main = Page(G.I_C_MAIN_QUEST)

# 召唤界面 Summon
page_summon = Page(G.I_C_SUMMON)
page_summon.link(button=G.I_V_SUMMON_TO_MAIN, destination=page_main)
page_main.link(button=G.I_V_MAIN_TO_SUMMON, destination=page_summon)

# 探索界面 Exploration
page_exp = Page(G.I_C_EXP)
page_exp.link(button=G.I_V_EXP_TO_MAIN, destination=page_main)
page_main.link(button=G.I_V_MAIN_TO_EXP, destination=page_exp)

# 结界突破 Realm Raid & Guild Raid
page_guild_raid = Page(G.I_C_GUILD_RAID)
page_realm_raid = Page(G.I_C_REALM_RAID)

page_realm_raid.link(button=G.I_V_REALM_RAID_TO_GUILD_RAID,
                     destination=page_guild_raid)
page_guild_raid.link(button=G.I_V_GUILD_RAID_TO_REALM_RAID,
                     destination=page_realm_raid)
page_realm_raid.link(button=G.I_V_REALM_RAID_TO_EXP, destination=page_exp)
page_guild_raid.link(button=G.I_V_REALM_RAID_TO_EXP, destination=page_exp)

page_exp.link(button=G.I_V_EXP_TO_REALM_RAID, destination=page_realm_raid)
page_realm_raid.link(button=G.I_V_REALM_RAID_TO_EXP, destination=page_exp)

# 商店 Store Street / Market
page_store = Page(G.I_C_MARKET)
page_store.link(button=G.I_V_STORE_TO_MAIN, destination=page_main)
page_main.link(button=G.I_V_MAIN_TO_STORE, destination=page_store)

# 町中 Town - TODO


# 登录 Login
page_login = Page(G.I_C_LOGIN)
page_login.link(button=G.I_V_LOGIN_TO_MAIN, destination=page_main)

# 休眠页面 Sleep
page_sleep = Page(G.I_C_SLEEP)
page_sleep.link(button=G.I_V_SLEEP_TO_MAIN, destination=page_main)
