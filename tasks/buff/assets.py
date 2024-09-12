from module.image_processing.rule_image import RuleImage
from module.image_processing.rule_ocr import RuleOcr
from module.image_processing.rule_swipe import RuleSwipe
from module.image_processing.rule_click import RuleClick

# This file was automatically generated by ./module/impage_processing/assets_extractor.py.
# Don't modify it manually.
class BuffAssets: 

	# Image Rule Assets
	# 庭院左上角的加成灯笼 
	I_BUFF_OPEN = RuleImage(
		roi=(363, 32, 32, 46),
		area=(347, 16, 64, 78),
		file="./tasks/buff/res/buff_open.png"
	)
	# 探索界面加成灯笼 
	I_EXP_BUFF_OPEN = RuleImage(
		roi=(427, 23, 29, 44),
		area=(413, 9, 57, 72),
		file="./tasks/buff/res/exp_buff_open.png"
	)
	# 鬼兵演武界面加成灯笼 
	I_MINAMOTO_BUFF_OPEN = RuleImage(
		roi=(809, 35, 29, 42),
		area=(795, 21, 57, 70),
		file="./tasks/buff/res/minamoto_buff_open.png"
	)
	# 加成窗口下面的云，用来检测和关闭 
	I_BUFF_CLOUD = RuleImage(
		roi=(386, 515, 122, 24),
		area=(374, 503, 146, 48),
		file="./tasks/buff/res/buff_cloud.png"
	)
	# 觉醒加成 
	I_BUFF_AWAKE = RuleImage(
		roi=(377, 132, 47, 46),
		area=(354, 107, 93, 447),
		file="./tasks/buff/res/buff_awake.png"
	)
	# 御魂加成 
	I_BUFF_SOUL = RuleImage(
		roi=(378, 198, 45, 46),
		area=(356, 120, 89, 388),
		file="./tasks/buff/res/buff_soul.png"
	)
	# 金币50%加成 
	I_BUFF_GOLD_50 = RuleImage(
		roi=(374, 269, 52, 36),
		area=(356, 120, 88, 391),
		file="./tasks/buff/res/buff_gold_50.png"
	)
	# 金币100%加成 
	I_BUFF_GOLD_100 = RuleImage(
		roi=(379, 338, 43, 39),
		area=(359, 121, 83, 407),
		file="./tasks/buff/res/buff_gold_100.png"
	)
	# 经验50%加成 
	I_BUFF_EXP_50 = RuleImage(
		roi=(380, 406, 44, 43),
		area=(358, 121, 88, 393),
		file="./tasks/buff/res/buff_exp_50.png"
	)
	# 经验100%加成 
	I_BUFF_EXP_100 = RuleImage(
		roi=(384, 303, 30, 40),
		area=(368, 126, 60, 386),
		file="./tasks/buff/res/buff_exp_100.png"
	)
	# description 
	I_BUFF_OPEN_YELLOW = RuleImage(
		roi=(772,347,21,21),
		area=(766,133,35,366),
		file="./tasks/buff/res/buff_open_yellow.png"
	)
	# description 
	I_BUFF_CLOSE_RED = RuleImage(
		roi=(772,347,21,21),
		area=(766,133,35,366),
		file="./tasks/buff/res/buff_close_red.png"
	)

	# Ocr Rule Assets
	# Ocr-description 
	O_GOLD_50 = RuleOcr(
		roi=(428,120,338,389),
		area=(0,0,100,100),
		keyword="战斗胜利获得的金币增加50%",
		name="gold_50"
	)
	# Ocr-description 
	O_GOLD_100 = RuleOcr(
		roi=(425,118,342,397),
		area=(0,0,100,100),
		keyword="战斗胜利获得的金币增加100%",
		name="gold_100"
	)
	# Ocr-description 
	O_EXP_50 = RuleOcr(
		roi=(426,119,335,394),
		area=(0,0,100,100),
		keyword="战斗胜利获得的经验增加50%",
		name="exp_50"
	)
	# Ocr-description 
	O_EXP_100 = RuleOcr(
		roi=(421,127,342,388),
		area=(0,0,100,100),
		keyword="战斗胜利获得的经验增加100%",
		name="exp_100"
	)


	# Swipe Rule Assets
	# description 
	S_BUFF_UP = RuleSwipe(
		roi_start=(397,124,456,35),
		roi_end=(447,457,386,37),
		name="buff_up"
	)


