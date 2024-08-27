from pydantic import BaseModel, Field
from module.config.enums import *

class DeviceSetting(BaseModel):
    serial: str = Field(default="127.0.0.1:16416")
    screenshot_method: ScreenshotMethod = Field(default="ADB_nc")
    control_method: ControlMethod = Field(default="minitouch")

class Optimization(BaseModel):
    # 执行两次截图之间的最小间隔，限制在 0.1 ~ 0.3，对于高配置电脑能降低 CPU 占用
    screenshot_interval: float = Field(default=0.3, ge=0.1, le=0.3)
    # 执行两次截图之间的最小间隔，限制在 0.1 ~ 1.0，能降低战斗时的 CPU 占用
    combat_screenshot_interval: float = Field(default=1.0, ge=0.1, le=1.0)
    schedule_rule: ScheduleRule = Field(default="FIFO")

class ErrorHandler(BaseModel):
    when_network_abnormal: ErrorHandleMethod = Field(default="等待10秒", title="")
    when_network_error: ErrorHandleMethod = Field(default="重启", title="")
    cache_clear_request: bool = Field(default=True)

# 基础设置
class ScriptSetting(BaseModel):
    device: DeviceSetting = Field(default_factory=DeviceSetting)
    optimization: Optimization = Field(default_factory=Optimization)
    error_handler: ErrorHandler = Field(default_factory=ErrorHandler)

class Scheduler(BaseModel):
    enable: bool = Field(default=True)
    next_run: str = Field(default="2024-08-16 21:13:17")
    priority: int = 5
    success_interval: str = Field(default="00 00:10:00")
    failure_interval: str = Field(default="00 00:10:00")

class HarvestConfig(BaseModel):
    enable_jade: bool = Field(default=True)  # 永久勾玉卡
    enable_sign: bool = Field(default=True)  # 签到
    enable_sign_999: bool = Field(default=True)  # 999天的签到福袋
    enable_mail: bool = Field(default=True)  # 邮件
    enable_soul: bool = Field(default=True)  # 御魂加成
    enable_ap: bool = Field(default=True)  # 体力

class TriflesConfig(BaseModel):
    one_summon: bool = Field(default=False)  # 每日一抽
    guild_wish: bool = Field(default=False)  # 寮祈愿
    friend_love: bool = Field(default=False)  # 友情点
    store_sign: bool = Field(default=False)  # 商店签到

# Daily Routine  每日日常
class DailyRoutine(BaseModel):
    scheduler: Scheduler = Field(default_factory=Scheduler)
    harvest_config: HarvestConfig = Field(default_factory=HarvestConfig)
    trifles_config: TriflesConfig = Field(default_factory=TriflesConfig)

class WantedQuestInvitationConfig(BaseModel):
    start_time: str = Field(default="00:00:00", description="开启时间")
    invite_friend_name: str = Field(default="", description="邀请指定好友名字")
    quest_type: WantedQuestType = Field(
        default=WantedQuestType.Jade, title="协作邀请类型")

class AcceptQuestConfig(BaseModel):
    accept_type: WantedQuestType = Field(
        default=WantedQuestType.Jade, title="接受协作类型")

# 协作任务
class WantedQuests(BaseModel):
    accept_quest_config: AcceptQuestConfig = Field(
        default_factory=AcceptQuestConfig)

class RaidConfig(BaseModel):
    tickets_required: int = Field(default=20)
    exit_two: bool = Field(default=True)  # 最后一个连退两次，卡57
    order_attack: str = Field(default="5 > 4 > 3 > 2 > 1 > 0")
    three_refresh: bool = Field(default=False)
    when_attack_fail: str = Field(default="Continue")

# 个人突破
class RealmRaid(BaseModel):
    scheduler: Scheduler = Field(default_factory=Scheduler)
    raid_config: RaidConfig = Field(default_factory=RaidConfig)

class ExplorationConfig(BaseModel):
    buff_gold_50_click: bool = Field(default=False)  # 50%金币加成
    buff_gold_100_click: bool = Field(default=False)  # 100%金币加成
    buff_exp_50_click: bool = Field(default=True)  # 50%经验加成
    buff_exp_100_click: bool = Field(default=False)  # 100%经验加成
    count_max: int = Field(default=7, title="探索次数", description="默认探索7次")
    chapter: Chapters = Field(default=Chapters.CHAPTER_28,
                              title="探索章节", description="探索章节 默认二十八")
    auto_backup: bool = Field(default=False)
    backup_rarity: ChooseRarity = Field(
        title="选择狗粮稀有度", default=ChooseRarity.N, description=ChooseRarity.N)
    lock_team_enable: bool = Field(default=True)  # 锁定队伍

# 绘卷模式
class ScrollModeConfig(BaseModel):
    scroll_mode_enable: bool = Field(default=True)
    # TODO: create time class for this
    scrolls_cd: str = Field(default="0:30:00", title="间隔时间")
    ticket_threshold: int = Field(title="突破票数量", default=25,
                                  description="满足票数后任务自动转去个人突破")

# 探索
class Exploration(BaseModel):
    scheduler: Scheduler = Field(default_factory=Scheduler)
    exploration_config: ExplorationConfig = Field(
        default_factory=ExplorationConfig, title="探索")
    scroll_mode: ScrollModeConfig = Field(
        default_factory=ScrollModeConfig, title="绘卷模式")

class ClimbConfig(BaseModel):
    enable_ap_mode: bool = Field(default=False)  # 开启体力模式，反之则用活动门票
    auto_switch: bool = Field(default=False)  # 挂完活动门票后自动切换到体力模式
    ticket_max: int = Field(default=50, title="门票爬塔次数",
                            description="默认门票爬塔50次")
    ap_max: int = Field(default=300, title="体力爬塔次数", description="默认体力爬塔300次")
    lock_team_enable: bool = Field(default=True)  # 锁定队伍

# 式神爬塔活动
class ShikigamiActivity(BaseModel):
    scheduler: Scheduler = Field(default_factory=Scheduler)
    climb_config: ClimbConfig = Field(default_factory=ClimbConfig)

# 御灵
class GoryouConfig(BaseModel):
    goryou_class: GoryouClass = Field(
        default=GoryouClass.RANDOM, title="御灵")
    count_max: int = Field(default=50, title="御灵次数", description="默认御灵50次")
    level: GoryouLevel = Field(
        default=GoryouLevel.three, title="御灵难度", description="默认御灵难度第三层")
    lock_team_enable: bool = Field(default=True)  # 锁定队伍

class GoryouRealm(BaseModel):
    scheduler: Scheduler = Field(default_factory=Scheduler)
    goryou_config: GoryouConfig = Field(default_factory=GoryouConfig)
