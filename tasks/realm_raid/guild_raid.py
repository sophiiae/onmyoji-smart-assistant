from datetime import datetime, timedelta
import time
from tasks.realm_raid.task_script import TaskScript
from tasks.general.page import page_realm_raid, page_main

class GuildRaid(TaskScript):
    def time_in_range(self, start, end, x):
        """Return true if x is in the range [start, end]"""
        if start <= end:
            return start <= x <= end
        else:
            return start <= x or x <= end

    def start_guild_raid(self):
        total = 6
        hour = datetime.now().hour
        if 6 <= hour < 9:
            total = 100

        print(f"-----> we have {total} battle ticket")

        retry = 0
        while total > 0:
            if retry > 5:
                break
            if self.wait_until_click(self.I_REALM_MEDAL_5, 1):
                time.sleep(0.4)
                if not self.wait_until_appear(self.I_RAID_ATTACK, 1, threshold=0.95):
                    self.swipe(self.S_RAID_UP, duration=700)
                    retry += 1
                    time.sleep(0.5)
                    continue
                self.click(self.I_RAID_ATTACK)
                retry = 0
                if self.wait_for_result(self.I_FIGHT_REWARD, self.I_RAID_FIGHT_AGAIN, 100, 1):
                    time.sleep(0.5)
                    self.random_click_right()
                    total -= 1
                else:
                    self.click(self.I_RAID_BATTLE_EXIT)
        exit()
