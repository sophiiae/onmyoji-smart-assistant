from functools import cached_property
import random
import time
from module.base.logger import logger
from module.base.exception import TaskEnd
from tasks.general.general import General
from tasks.realm_raid.assets import RealmRaidAssets as RRA
from tasks.general.page import page_realm_raid, page_main, page_exp, page_store

class TaskScript(General, RRA):
    order = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def run(self):
        config = self.config.model.realm_raid

        if not self.check_page_appear(page_realm_raid):
            self.goto(page_realm_raid)

        # 票不够的话就结束任务
        if not self.check_ticket(config.raid_config.tickets_required):
            self.goto(page_main)
            self.set_next_run(task='RealmRaid', success=False, finish=False)
            raise TaskEnd

        image = self.screenshot()
        self.update_partition_prop(image)

        # 如果最低挑战等级高于57，就降级处理
        self.downgrade()

        # 锁定队伍
        self.toggle_team_lock()

        success = True

        # 打乱挑战顺序， 更随机~
        attack_list = self.order.copy()
        random.shuffle(attack_list)

        print(f"-----attack list: {attack_list}")
        while 1:
            # 查看突破票数量
            if not self.check_ticket(config.raid_config.tickets_required):
                break

            # 如果都挑战过了，如果上次失败就刷新，没有就更新配置
            if len(attack_list) == 0:
                if not success:
                    self.click_refresh()

                attack_list = self.order.copy()
                random.shuffle(attack_list)
                success = True
                del self.partitions_prop

            # 下一个挑战目标
            attack_index = attack_list.pop()

            # 已经挑战过的就略过
            if self.is_defeated(attack_index - 1) or self.is_lose(attack_index - 1):
                success = False
                continue

            # 最后一个退2次再打， 卡57
            if attack_index == 9:
                logger.info("attacking last one")
                self.toggle_team_lock(False)  # 解锁队伍

                if self.quit_and_fight(attack_index):
                    self.toggle_team_lock()  # 锁上
                    continue
                else:
                    success = False
                    continue
            else:
                if not self.start_fight(attack_index):
                    success = False
                    continue

            # 如果勾选了拿了三次战斗奖励就刷新 >> 刷新
            self.three_win_refresh(config.raid_config.three_refresh)

        self.goto(page_main)
        self.set_next_run(task='RealmRaid', success=success, finish=True)
        raise TaskEnd

    def three_win_refresh(self, refresh=True):
        if refresh and self.appear(self.I_RAID_WIN3):
            return self.click_refresh()
        return refresh

    # 第一次进突破界面的时候，扫描，记录目前的挑战情况
    def update_partition_prop(self, image):
        for part in self.partitions_prop:
            x, y, w, h = part['flag_area']
            cropped = image[y: y + h, x: x + w]
            if RRA.I_RAID_BEAT.match_target(cropped, threshold=0.95, cropped=True):
                part['defeated'] = True
            else:
                ax, ay, aw, ah = part['lose_arrow_area']
                arrow_cropped = image[ay: ay + ah, ax: ax + aw]
                if RRA.I_RAID_LOSE.match_target(arrow_cropped, threshold=0.95, cropped=True):
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

    def start_fight(self, index) -> bool:
        logger.info(f"----- Attacking index {index}.")
        self.click(self.partitions[index - 1])

        # 等待挑战失败或者成功， 失败直接退出
        if self.wait_until_appear(self.I_RAID_ATTACK, click=True, click_delay=1):
            self.wait_until_appear(self.I_BATTLE_READY,
                                   2, click=True, click_delay=1)
            time.sleep(13)
            if self.wait_for_result(General.I_FIGHT_REWARD, self.I_RAID_FIGHT_AGAIN, 100, 1):
                self.get_reward()
                return True
            else:
                self.click(self.I_RAID_BATTLE_EXIT)
                return False
        logger.error("No attack button found")
        return False

    def quit_and_fight(self, index, quit_count=2) -> bool:
        logger.info(f"Starting quit and fight for {quit_count} times.")

        # 进入战斗
        self.click(self.partitions[index - 1])
        if not self.wait_until_appear(RRA.I_RAID_ATTACK, 15, click=True):
            logger.error("Not able to enter battle")
            return False

        count = 0
        while count < quit_count:
            logger.info(f"========= quit and fight count: {count}")
            time.sleep(1)

            # 退1次
            if self.wait_until_appear(RRA.I_RAID_BATTLE_EXIT, threshold=0.95, click=True, click_delay=1):
                if not self.wait_until_appear(
                    RRA.I_RAID_BATTLE_EXIT_CONFIRM,
                    waiting_limit=4,
                    click=True, click_delay=1
                ):
                    logger.error("Stuck in battle exit")
                    return False

            time.sleep(0.5)
            # 关闭再次挑战提醒
            if self.wait_until_appear(RRA.I_RAID_FIGHT_AGAIN, 2, click=True, click_delay=1):
                # 如果有出现关闭今日提醒 -> 勾选今日不再提示 -> 确认
                if self.wait_until_appear(self.I_RAID_AGAIN_CONFIRM, 3):
                    self.wait_until_appear(
                        self.I_RAID_WARNING_CHECKBOX, 2, click=True)
                    self.wait_until_appear(
                        self.I_RAID_AGAIN_CONFIRM, click=True)
            count += 1

        # 退出战斗界面，再正式挑战
        if self.wait_until_appear(self.I_RAID_FIGHT_AGAIN):
            self.click(self.I_RAID_BATTLE_EXIT)
            if self.wait_until_appear(self.I_RAID_BATTLE_EXIT, click=True):
                if not self.wait_until_appear(
                    RRA.I_RAID_BATTLE_EXIT_CONFIRM,
                    click=True, click_delay=0.7
                ):
                    logger.error("Stuck in battle exit")
                    return False

        return self.start_fight(index)

    def is_defeated(self, index):
        return self.partitions_prop[index]['defeated']

    def is_lose(self, index):
        return self.partitions_prop[index]['lose']

    def downgrade(self) -> bool:
        image = self.screenshot()
        level = self.O_RAID_PARTITION_1_LV.digit(image)
        retry = 5
        downgraded = False
        if level > 57:
            logger.info(
                f"-------->>> Current lowest level: {level}  <<<----------"
            )
            # 不锁定退得快点
            self.toggle_team_lock(False)

            for idx, part in enumerate(self.partitions):
                # 已经挑战过的就skip掉
                if self.is_defeated(idx) or self.is_lose(idx):
                    continue

                logger.info(f"** enter and quit for partition {idx + 1}")
                self.click(part, 0.3)
                if self.wait_until_appear(RRA.I_RAID_ATTACK, 15, click=True):
                    if not self.wait_until_appear(RRA.I_RAID_BATTLE_EXIT, threshold=0.95, click=True, click_delay=1):
                        logger.error("Not able to exit the battle")
                        return False

                    time.sleep(0.5)
                    if self.wait_until_appear(RRA.I_RAID_BATTLE_EXIT_CONFIRM, click=True, click_delay=1):
                        if self.wait_until_appear(RRA.I_RAID_FIGHT_AGAIN):
                            self.click(RRA.I_RAID_BATTLE_EXIT)
                else:
                    logger.warning(f"No attack button found for {idx}")

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
        if self.wait_until_appear(self.I_RAID_REFRESH, threshold=0.95, click=True):
            if self.wait_until_appear(self.I_RAID_AGAIN_CONFIRM):
                self.click(self.I_RAID_AGAIN_CONFIRM)
            return True
        elif self.appear(self.I_RAID_REFRESH_UNABLE, threshold=0.95):
            logger.warning("Unable to refresh, waiting for CD.")
            return False

        logger.critical("No refresh button found")
        return False

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
            self.get_reward(waiting_limit=2)
            time.sleep(1)
            image = self.screenshot()
            count, total = self.O_RAID_TICKET.digit_counter(image)
        if count == 0:
            logger.warning(f'Execute raid failed, no ticket')
            return False
        elif count < tickets_required:
            logger.warning(f'Execute raid failed, ticket is not enough')
            return False
        return True

    def get_reward(self, waiting_limit: float = 70) -> bool:
        if self.wait_until_appear(General.I_FIGHT_REWARD, waiting_limit, waiting_interval=1):
            self.click(RRA.I_RAID_BATTLE_EXIT)
            logger.info("Got realm raid fight reward")

            time.sleep(1)
            # 检查是否有自动领取额外奖励
            if self.wait_until_appear(General.I_FIGHT_REWARD, 2, waiting_interval=0.5, retry_limit=1):
                logger.info("Got 3 / 6 / 9 extra reward")

            return True
        return False

    def toggle_team_lock(self, lock: bool = True):
        # 锁定队伍
        if not lock:
            if self.wait_until_appear(RRA.I_RAID_TEAM_LOCK, waiting_limit=2, retry_limit=2, threshold=0.95, click=True):
                logger.info("Unlock the team")
                return True

        # 不锁定队伍
        if lock:
            if self.wait_until_appear(RRA.I_RAID_TEAM_UNLOCK, waiting_limit=2, retry_limit=2, threshold=0.95, click=True):
                logger.info("Lock the team")
                return True

        logger.error("Team lock icon not found")
        return False
