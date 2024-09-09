from module.image_processing.rule_image import RuleImage
from module.image_processing.rule_ocr import RuleOcr
from module.image_processing.rule_swipe import RuleSwipe
from module.image_processing.rule_click import RuleClick

# This file was automatically generated by ./module/impage_processing/assets_extractor.py.
# Don't modify it manually.
class MainPageAssets: 

	# Image Rule Assets
	# 邮件 
	I_MAIL = RuleImage(
		roi=(244, 506, 48, 20),
		area=(170, 450, 270, 100),
		file="./tasks/main_page/res/mail.png"
	)
	# 寮礼包 
	I_GUILD_PACK = RuleImage(
		roi=(246, 499, 38, 37),
		area=(200, 450, 270, 150),
		file="./tasks/main_page/res/guild_pack.png"
	)
	# 悬赏封印 
	I_QUEST = RuleImage(
		roi=(235, 337, 44, 34),
		area=(100, 270, 320, 168),
		file="./tasks/main_page/res/quest.png"
	)
	# 菜单绘卷关闭 
	I_SCROLL_CLOSE = RuleImage(
		roi=(1179, 637, 36, 27),
		area=(1161, 624, 72, 54),
		file="./tasks/main_page/res/scroll_close.png"
	)
	# 菜单绘卷开启 
	I_SCROLL_OPEN = RuleImage(
		roi=(1207, 609, 33, 83),
		area=(1190, 568, 66, 166),
		file="./tasks/main_page/res/scroll_open.png"
	)
	# 商店礼包屋入口 
	I_STORE_PACK = RuleImage(
		roi=(1140, 647, 62, 38),
		area=(1109, 628, 124, 76),
		file="./tasks/main_page/res/store/store_pack.png"
	)
	# 商店礼包推荐灯笼 
	I_STORE_REC = RuleImage(
		roi=(1190, 188, 35, 68),
		area=(1172, 50, 70, 350),
		file="./tasks/main_page/res/store/store_rec.png"
	)
	# 商店每日签到奖励 
	I_STORE_DAILY_REWARD = RuleImage(
		roi=(251, 164, 280, 103),
		area=(111, 112, 560, 206),
		file="./tasks/main_page/res/store/store_daily_reward.png"
	)
	# 商店礼包屋退出 
	I_STORE_EXIT = RuleImage(
		roi=(16, 7, 44, 40),
		area=(0, 0, 88, 80),
		file="./tasks/main_page/res/store/store_exit.png"
	)
	# 勾协邀请 
	I_QUEST_JADE = RuleImage(
		roi=(654, 459, 60, 50),
		area=(526, 420, 235, 135),
		file="./tasks/main_page/res/quest/quest_jade.png"
	)
	# 体协邀请 
	I_QUEST_EP = RuleImage(
		roi=(654, 460, 60, 47),
		area=(526, 420, 235, 135),
		file="./tasks/main_page/res/quest/quest_ep.png"
	)
	# 狗粮协作邀请 
	I_QUEST_DOG = RuleImage(
		roi=(204, 514, 64, 55),
		area=(526, 420, 235, 135),
		file="./tasks/main_page/res/quest/quest_dog.png"
	)
	# 猫粮协作邀请 
	I_QUEST_CAT = RuleImage(
		roi=(204, 515, 64, 54),
		area=(526, 420, 235, 135),
		file="./tasks/main_page/res/quest/quest_cat.png"
	)
	# 接受悬赏邀请 
	I_QUEST_ACCEPT = RuleImage(
		roi=(825, 395, 55, 46),
		area=(798, 372, 110, 92),
		file="./tasks/main_page/res/quest/quest_accept.png"
	)
	# 拒绝悬赏邀请 
	I_QUEST_REJECT = RuleImage(
		roi=(826, 495, 53, 49),
		area=(800, 470, 106, 98),
		file="./tasks/main_page/res/quest/quest_reject.png"
	)
	# 关闭/无视悬赏邀请 
	I_QUEST_IGNORE = RuleImage(
		roi=(764, 107, 40, 38),
		area=(744, 88, 80, 76),
		file="./tasks/main_page/res/quest/quest_ignore.png"
	)
	# 协作邀请现世标记位置 
	I_QUEST_VIRTUAL = RuleImage(
		roi=(524, 159, 26, 29),
		area=(511, 144, 52, 58),
		file="./tasks/main_page/res/quest/quest_virtual.png"
	)


