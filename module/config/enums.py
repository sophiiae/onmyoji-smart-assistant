from enum import Enum

class Chapters(str, Enum):
    CHAPTER_1 = "第一章"
    CHAPTER_2 = "第二章"
    CHAPTER_3 = "第三章"
    CHAPTER_4 = "第四章"
    CHAPTER_5 = "第五章"
    CHAPTER_6 = "第六章"
    CHAPTER_7 = "第七章"
    CHAPTER_8 = "第八章"
    CHAPTER_9 = "第九章"
    CHAPTER_10 = "第十章"
    CHAPTER_11 = "第十一章"
    CHAPTER_12 = "第十二章"
    CHAPTER_13 = "第十三章"
    CHAPTER_14 = "第十四章"
    CHAPTER_15 = "第十五章"
    CHAPTER_16 = "第十六章"
    CHAPTER_17 = "第十七章"
    CHAPTER_18 = "第十八章"
    CHAPTER_19 = "第十九章"
    CHAPTER_20 = "第二十章"
    CHAPTER_21 = "第二十一章"
    CHAPTER_22 = "第二十二章"
    CHAPTER_23 = "第二十三章"
    CHAPTER_24 = "第二十四章"
    CHAPTER_25 = "第二十五章"
    CHAPTER_26 = "第二十六章"
    CHAPTER_27 = "第二十七章"
    CHAPTER_28 = "第二十八章"

class ChooseRarity(str, Enum):
    N = "N卡"
    S = "素材"

class WantedQuestType(str, Enum):
    """
        用于区分悬赏封印协作类型
    """
    Gold = "金币"  # 金币协作
    Jade = "勾玉"  # 勾玉协作
    Food = "狗粮"  # 狗/猫粮协作
    Sushi = "体力"  # 体力协作

class GoryouClass(str, Enum):
    RANDOM = "随机",
    Dark_Divine_Dragon = "暗神龙",
    Dark_Hakuzousu = "暗白蔵主",
    Dark_Black_Panther = "暗黑豹",
    Dark_Peacock = "暗孔雀"

class GoryouLevel(str, Enum):
    one = "一层"
    two = "二层"
    three = "三层"

class ScreenshotMethod(str, Enum):
    ADB_nc = "ADB_nc"

class ControlMethod(str, Enum):
    minitouch = "minitouch"

class ErrorHandleMethod(str, Enum):
    wait_10s = "等待10秒"
    restart = "重启"

class ScheduleRule(str, Enum):
    FIFO = 'FIFO'  # 先来后到，（按照任务的先后顺序进行调度）
    PRIORITY = 'Priority'  # 基于优先级，同一个优先级的任务按照先来后到的顺序进行调度，优先级高的任务先调度

class BuffClass(Enum):
    AWAKE = 10  # 觉醒
    SOUL = 20  # 御魂
    GOLD_50 = 30  # 金币50
    GOLD_100 = 40  # 金币100
    EXP_50 = 50  # 经验50
    EXP_100 = 60  # 经验100
    AWAKE_CLOSE = 70  # 觉醒
    SOUL_CLOSE = 80  # 御魂
    GOLD_50_CLOSE = 90  # 金币50
    GOLD_100_CLOSE = 100  # 金币100
    EXP_50_CLOSE = 110  # 经验50
    EXP_100_CLOSE = 120  # 经验100
