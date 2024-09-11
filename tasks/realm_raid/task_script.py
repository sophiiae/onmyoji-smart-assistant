from datetime import datetime, timedelta
from functools import cached_property
import random
import time
from module.base.logger import logger
from module.base.exception import TaskEnd
from module.image_processing.rule_image import RuleImage
from tasks.realm_raid.assets import RealmRaidAssets
from tasks.general.page import page_realm_raid, page_main
from module.base.exception import RequestHumanTakeover
from tasks.battle.battle import Battle

class TaskScript(RealmRaidAssets, Battle):
    order = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    name = "Realm Raid"

    def run(self):
        self.rr_config = self.config.model.realm_raid.raid_config

        if not self.check_page_appear(page_realm_raid):
            self.goto(page_realm_raid)

        ticket_min = self.rr_config.tickets_required

        # 检查票数
        if not self.check_ticket(ticket_min):
            self.goto(page_main)
            self.set_next_run(task='RealmRaid', success=True, finish=False)
            raise TaskEnd(self.name)

        image = self.screenshot()
        self.update_partition_prop(image)

        success = True

        # 打乱挑战顺序， 更随机~
        attack_list = self.order.copy()
        random.shuffle(attack_list)

        print(f"----- attack order: {attack_list}")

        # 查看突破票数量
        enough_ticket = self.check_ticket(ticket_min)

        while enough_ticket:
            # 如果都挑战过了，如果上次失败就刷新，没有就更新配置
            if len(attack_list) == 0:
                if not self.click_refresh():
                    break

                attack_list = self.order.copy()
                random.shuffle(attack_list)
                success = True
                del self.partitions_prop

            # 如果最低挑战等级高于57，就降级处理
            self.downgrade()
            # 锁定队伍
            self.toggle_realm_team_lock()
            while len(attack_list):
                # 下一个挑战目标
                attack_index = attack_list.pop()

                # 已经挑战过的就略过
                if self.is_defeated(attack_index - 1) or self.is_lose(attack_index - 1):
                    success = False
                    continue

                time.sleep(1)
                # 最后一个退2次再打， 卡57
                logger.info(f"----- Attacking index {attack_index - 1}.")
                if attack_index == 9:
                    self.quit_and_fight(attack_index)

                self.enter_battle(attack_index)
                if self.run_battle():
                    success = False
                    continue

                # 如果勾选了拿了三次战斗奖励就刷新 >> 刷新
                if self.rr_config.three_refresh:
                    if self.wait_until_appear(self.I_RAID_WIN3, 2, 1):
                        self.click_refresh()
                        break

            # 更新票数
            enough_ticket = self.check_ticket(ticket_min)

        self.goto(page_main, page_realm_raid)
        self.set_next_run(task='RealmRaid', success=success, finish=True)
        raise TaskEnd(self.name)

    def enter_battle(self, index):
        target = self.partitions[index - 1]
        while 1:
            time.sleep(1)
            self.screenshot()
            if not self.appear(self.I_C_REALM_RAID):
                break

            if self.appear(self.I_RAID_ATTACK_MODAL, 0.97):
                if self.appear_then_click(self.I_RAID_ATTACK):
                    continue

            if self.click(target):
                continue

    def run_three_win(self):
        if not self.check_page_appear(page_realm_raid):
            self.goto(page_realm_raid)

        image = self.screenshot()
        ticket, total = self.O_RAID_TICKET.digit_counter(image)

        refresh_time = datetime.now()
        if self.wait_until_appear(self.I_RAID_WIN3, 1):
            self.click_refresh()
            refresh_time = datetime.now()

        self.toggle_realm_team_lock()  # Lock team
        count = 3
        # 打乱挑战顺序， 更随机~
        attack_list = self.order.copy()
        random.shuffle(attack_list)

        while ticket:
            index = attack_list.pop()
            self.enter_battle(index)
            if not self.run_battle():
                continue
            else:
                count -= 1
                ticket -= 1
            if count == 0:
                if not self.click_refresh():
                    time.sleep(refresh_time +
                               timedelta(minutes=5) - datetime.now())
                    self.click_refresh()

                refresh_time = datetime.now()
                count = 3
                attack_list = self.order.copy()
                random.shuffle(attack_list)

        logger.critical("No enough tickets")
        exit()

    # 第一次进突破界面的时候，扫描，记录目前的挑战情况
    def update_partition_prop(self, image):
        for part in self.partitions_prop:
            x, y, w, h = part['flag_area']
            cropped = image[y: y + h, x: x + w]
            if self.I_RAID_BEAT.match_target(cropped, threshold=0.95, cropped=True):
                part['defeated'] = True
            else:
                ax, ay, aw, ah = part['lose_arrow_area']
                arrow_cropped = image[ay: ay + ah, ax: ax + aw]
                if self.I_RAID_LOSE.match_target(arrow_cropped, threshold=0.95, cropped=True):
                    part['lose'] = True

    @cached_property
    def medals(self) -> list:
        return [self.I_REALM_MEDAL_5, self.I_REALM_MEDAL_4, self.I_REALM_MEDAL_3,
                self.I_REALM_MEDAL_2, self.I_REALM_MEDAL_1, self.I_REALM_MEDAL_0]

    @cached_property
    def partitions(self) -> list:
        return [self.I_REALM_PARTITION_1, self.I_REALM_PARTITION_2, self.I_REALM_PARTITION_3,
                self.I_REALM_PARTITION_4, self.I_REALM_PARTITION_5, self.I_REALM_PARTITION_6,
                self.I_REALM_PARTITION_7, self.I_REALM_PARTITION_8, self.I_REALM_PARTITION_9]

    @cached_property
    def partitions_prop(self) -> list:
        # 计算每格位置大小
        w, h = 325, 125
        xl = [150, 480, 810]  # left border
        yl = [150, 280, 415]  # top border

        parts = []
        for y in yl:
            for x in xl:
                parts.append({
                    'partition_area': (x, y, w, h),
                    'flag_area': (), 'medal_area': (),
                    'defeated': False, 'medal': -1,
                    "lose_arrow_area": (), 'lose': False
                })

        # 计算勋章位置大小
        mw, mh = 217, 55
        i = 0
        for y in yl:
            for x in xl:
                mx, my = x + 84, y + 60
                parts[i]['medal_area'] = (mx, my, mw, mh)
                i += 1

        # 计算 “破” 位置大小
        fw, fh = 70, 70
        i = 0
        for y in yl:
            for x in xl:
                fx, fy = x + 250, y + 12
                parts[i]['flag_area'] = (fx, fy, fw, fh)
                i += 1

        # 计算失败箭头位置大小
        aw, ah = 84, 40
        i = 0
        for y in yl:
            for x in xl:
                ax, ay = x + 238, y - 10
                parts[i]['lose_arrow_area'] = (ax, ay, aw, ah)
                i += 1
        return parts

    def quit_and_fight(self, index, quit_count=2) -> bool:
        logger.info(f"Starting quit and fight for {quit_count} times.")

        self.toggle_realm_team_lock(False)
        count = 1
        while count <= quit_count:
            self.click(self.partitions[index - 1])
            if not self.wait_until_click(self.I_RAID_ATTACK, 3):
                logger.error("Not able to enter battle")
                raise RequestHumanTakeover
            logger.info(f"========= quit and fight count: {count}")
            time.sleep(0.5)

            self.run_battle_quit()
            count += 1

        self.toggle_realm_team_lock()

    def is_defeated(self, index):
        return self.partitions_prop[index]['defeated']

    def is_lose(self, index):
        return self.partitions_prop[index]['lose']

    def downgrade(self) -> bool:
        image = self.screenshot()
        level = self.O_RAID_PARTITION_1_LV.digit(image)
        retry = 5
        downgraded = False
        while level > 57:
            logger.info(
                f"-------->>> Current lowest level: {level}  <<<----------"
            )
            # 不锁定退得快点
            self.toggle_realm_team_lock(False)

            for idx, part in enumerate(self.partitions):
                # 已经挑战过的就skip掉
                if self.is_defeated(idx) or self.is_lose(idx):
                    continue

                logger.info(f"** enter and quit for partition {idx + 1}")
                self.click(part, 0.3)

                if self.wait_until_click(self.I_RAID_ATTACK):
                    self.run_battle_quit()
                else:
                    logger.warning(f"No attack button found for {idx}")
                time.sleep(1)

            downgraded = True
            # 都退完了，刷新
            if not self.click_refresh():
                return False
            time.sleep(0.3)

            # 更新现在的最低等级
            image = self.screenshot()
            level = self.O_RAID_PARTITION_1_LV.digit(image)
            retry -= 1

        if retry < 0:
            logger.critical(f"Run out of retry for downgrade")
            return False

        logger.info(f"Current level [{level}] meets requirement.")

        return downgraded

    def click_refresh(self) -> bool:
        """
        检查是否出现了刷新的按钮
        如果可以刷新就刷新, 返回True
        如果在CD中, 就返回False
        :return:
        """
        if self.wait_until_click(self.I_RAID_REFRESH):
            if self.wait_until_click(self.I_BATTLE_FIGHT_AGAIN_CONFIRM, 2):
                return True
            else:
                logger.warning("Unable to refresh, waiting for CD.")
                return False

        logger.critical("No refresh button found")
        raise RequestHumanTakeover

    def find_one(self) -> tuple:
        """
        找到一个可以打的，并且检查一下是不是这一个的是第几个的
        我们约定次序是:
            1 2 3
            4 5 9
            7 8 9
        :return: 返回的第一个参数是一个RuleImage, 第二个参数是位置信息
        如果没有找到, 返回 (None, None)
        """
        image = self.screenshot()

        i = 0
        while i < len(self.medals):
            medal = self.medals[i]
            if medal.match_target(screenshot=image):
                index = self.get_partition_index(medal.roi)
                if index > 0:
                    return (medal, index)
            i += 1

        return (None, None)

    def get_partition_index(self, roi) -> int:
        """将九宫格用井字划分开，计算位置

        Args:
            roi (list): roi of target medal position

        Returns:
            int: index of partition
        """
        x_divider = [475, 794, 1270]
        y_divider = [275, 398, 700]

        x, y, w, h = roi
        r, c = 0, 0
        for idx, divider in enumerate(x_divider):
            if x >= divider:
                continue
            c = idx + 1
            break

        for idx, divider in enumerate(y_divider):
            if y >= divider:
                continue
            r = idx + 1
            break

        index = r * c
        if index < 1 or index > 9:
            logger.error(f"No valid partition found in index {index}")
            return -1

        return index

    def check_ticket(self, tickets_required: int = 0):
        time.sleep(0.2)
        if tickets_required < 0 or tickets_required > 30:
            logger.warning(f'It is not a valid base: {tickets_required}')
            tickets_required = 0

        image = self.screenshot()
        count, total = self.O_RAID_TICKET.digit_counter(image)
        if total == 0:
            # 处理奖励之后，重新识别票数
            self.get_reward(limit=2)
            time.sleep(1)
            image = self.screenshot()
            count, total = self.O_RAID_TICKET.digit_counter(image)
        if count < tickets_required:
            logger.warning(f'Execute raid failed, ticket is not enough')
            return False
        return True

    def get_reward(self, limit: float = 70) -> bool:
        if self.wait_until_appear(self.I_REWARD, limit, interval=0.5):
            time.sleep(0.5)
            self.random_click_right()
            logger.info("Got realm raid fight reward")

            time.sleep(1)
            # 检查是否有自动领取额外奖励
            if self.wait_until_appear(self.I_REWARD, 2, interval=0.5):
                time.sleep(1)
                self.random_click_right()
                logger.info("Got 3 / 6 / 9 extra reward")

            return True
        return False

    def toggle_realm_team_lock(self, lock: bool = True):
        return self.toggle_team_lock(self.I_RAID_TEAM_LOCK, self.I_RAID_TEAM_UNLOCK, lock)
