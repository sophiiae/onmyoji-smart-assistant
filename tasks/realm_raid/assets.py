from module.image_processing.rule_image import RuleImage
from module.image_processing.rule_ocr import RuleOcr
from module.image_processing.rule_swipe import RuleSwipe

# This file was automatically generated by ./module/impage_processing/assets_extractor.py.
# Don't modify it manually.
class RealmRaidAssets: 

	# Ocr Rule Assets
	# 突破第一格等级位置 
	O_RAID_PARTITION_1_LV = RuleOcr(
		roi=(160, 175, 193, 201),
		area=(160, 175, 193, 201),
		name="raid_partition_1_lv"
	)
	# 突破界面突破票标记位置 
	O_RAID_TICKET = RuleOcr(
		roi=(1146, 18, 1219, 46),
		area=(1146, 18, 1219, 46),
		name="raid_ticket"
	)
	# 突破刷新等待时间位置 
	O_RAID_WAIT_TIME = RuleOcr(
		roi=(1042, 581, 1125, 618),
		area=(1042, 581, 1125, 618),
		name="raid_wait_time"
	)

	# Image Rule Assets
	# 三次胜利奖励 
	I_RAID_WIN3 = RuleImage(
		roi=(419, 573, 62, 57),
		area=(388, 544, 124, 114),
		file="./tasks/realm_raid/res/raid_win3.png"
	)
	# 个人突破刷新 
	I_RAID_REFRESH = RuleImage(
		roi=(963, 569, 172, 57),
		area=(877, 540, 344, 114),
		file="./tasks/realm_raid/res/raid_refresh.png"
	)
	# 突破队伍锁定 
	I_RAID_TEAM_LOCK = RuleImage(
		roi=(823, 581, 25, 36),
		area=(811, 569, 49, 60),
		file="./tasks/realm_raid/res/raid_team_lock.png"
	)
	# 突破队伍未锁定 
	I_RAID_TEAM_UNLOCK = RuleImage(
		roi=(823, 581, 23, 34),
		area=(811, 569, 47, 58),
		file="./tasks/realm_raid/res/raid_team_unlock.png"
	)
	# 进攻 
	I_RAID_ATTACK = RuleImage(
		roi=(987, 361, 124, 53),
		area=(150, 150, 1030, 569),
		file="./tasks/realm_raid/res/raid_attack.png"
	)
	# 再次挑战 
	I_RAID_FIGHT_AGAIN = RuleImage(
		roi=(827, 476, 63, 72),
		area=(796, 440, 126, 144),
		file="./tasks/realm_raid/res/raid_fight_again.png"
	)
	# 破 
	I_RAID_BEAT = RuleImage(
		roi=(403, 303, 54, 54),
		area=(376, 276, 108, 108),
		file="./tasks/realm_raid/res/raid_beat.png"
	)
	# 今天不再提示勾选 
	I_RAID_WARNING_CHECKBOX = RuleImage(
		roi=(538, 341, 36, 37),
		area=(520, 322, 72, 74),
		file="./tasks/realm_raid/res/raid_warning_checkbox.png"
	)
	# 再次挑战确认 
	I_RAID_AGAIN_CONFIRM = RuleImage(
		roi=(672, 403, 172, 57),
		area=(586, 374, 344, 114),
		file="./tasks/realm_raid/res/raid_again_confirm.png"
	)
	# 退出战斗确认 
	I_RAID_BATTLE_EXIT_CONFIRM = RuleImage(
		roi=(679, 396, 124, 52),
		area=(617, 370, 248, 104),
		file="./tasks/realm_raid/res/raid_battle_exit_confirm.png"
	)
	# 突破战斗退出 
	I_RAID_BATTLE_EXIT = RuleImage(
		roi=(21, 17, 35, 33),
		area=(4, 0, 70, 66),
		file="./tasks/realm_raid/res/raid_battle_exit.png"
	)
	# 突破第一格位置(包括头像) 
	I_RAID_PARTITION_1_WHOLE = RuleImage(
		roi=(152, 151, 310, 111),
		area=(0, 96, 620, 222),
		file=""
	)
	# 突破刷新(等待) 
	I_RAID_REFRESH_UNABLE = RuleImage(
		roi=(975, 578, 71, 40),
		area=(940, 558, 142, 80),
		file="./tasks/realm_raid/res/raid_refresh_unable.png"
	)
	# 个人突破1 
	I_REALM_PARTITION_1 = RuleImage(
		roi=(240, 150, 223, 113),
		area=(130, 130, 1000, 420),
		file=""
	)
	# 个人突破2 
	I_REALM_PARTITION_2 = RuleImage(
		roi=(574, 150, 220, 113),
		area=(130, 130, 1000, 420),
		file=""
	)
	# 个人突破3 
	I_REALM_PARTITION_3 = RuleImage(
		roi=(903, 150, 223, 113),
		area=(130, 130, 1000, 420),
		file=""
	)
	# 个人突破4 
	I_REALM_PARTITION_4 = RuleImage(
		roi=(240, 285, 223, 113),
		area=(130, 130, 1000, 420),
		file=""
	)
	# 个人突破5 
	I_REALM_PARTITION_5 = RuleImage(
		roi=(574, 285, 220, 113),
		area=(130, 130, 1000, 420),
		file=""
	)
	# 个人突破6 
	I_REALM_PARTITION_6 = RuleImage(
		roi=(903, 285, 223, 113),
		area=(130, 130, 1000, 420),
		file=""
	)
	# 个人突破7 
	I_REALM_PARTITION_7 = RuleImage(
		roi=(240, 420, 223, 113),
		area=(130, 130, 1000, 420),
		file=""
	)
	# 个人突破8 
	I_REALM_PARTITION_8 = RuleImage(
		roi=(574, 420, 220, 113),
		area=(130, 130, 1000, 420),
		file=""
	)
	# 个人突破9 
	I_REALM_PARTITION_9 = RuleImage(
		roi=(903, 420, 223, 113),
		area=(130, 130, 1000, 420),
		file=""
	)
	# 0个勋章 
	I_REALM_MEDAL_0 = RuleImage(
		roi=(220, 150, 195, 38),
		area=(210, 130, 940, 400),
		file="./tasks/realm_raid/res/medals/medal_0.png"
	)
	# 1个勋章 
	I_REALM_MEDAL_1 = RuleImage(
		roi=(239, 350, 195, 38),
		area=(210, 130, 940, 400),
		file="./tasks/realm_raid/res/medals/medal_1.png"
	)
	# 2个勋章 
	I_REALM_MEDAL_2 = RuleImage(
		roi=(572, 485, 195, 38),
		area=(210, 130, 940, 400),
		file="./tasks/realm_raid/res/medals/medal_2.png"
	)
	# 3个勋章 
	I_REALM_MEDAL_3 = RuleImage(
		roi=(240, 485, 195, 38),
		area=(210, 130, 940, 400),
		file="./tasks/realm_raid/res/medals/medal_3.png"
	)
	# 4个勋章 
	I_REALM_MEDAL_4 = RuleImage(
		roi=(572, 350, 195, 38),
		area=(210, 130, 940, 400),
		file="./tasks/realm_raid/res/medals/medal_4.png"
	)
	# 5个勋章 
	I_REALM_MEDAL_5 = RuleImage(
		roi=(240, 216, 195, 37),
		area=(210, 130, 940, 400),
		file="./tasks/realm_raid/res/medals/medal_5.png"
	)


	# Swipe Rule Assets
	# 寮突破滑到最低 
	S_RAID_TO_END = RuleSwipe(
		roi_start=(1121, 147, 1158, 168),
		roi_end=(1121, 603, 1158, 623),
		name="raid_to_end"
	)
	# 寮突破滑到最高 
	S_RAID_TO_TOP = RuleSwipe(
		roi_start=(1121, 603, 1158, 623),
		roi_end=(1121, 147, 1158, 168),
		name="raid_to_top"
	)
	# 往上翻 
	S_RAID_UP = RuleSwipe(
		roi_start=(700, 300, 800, 300),
		roi_end=(700, 450, 800, 450),
		name="raid_up"
	)
	# 往下翻 
	S_RAID_DOWN = RuleSwipe(
		roi_start=(700, 450, 800, 450),
		roi_end=(700, 300, 800, 300),
		name="raid_down"
	)


