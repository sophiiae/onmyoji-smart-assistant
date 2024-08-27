from module.config.config_model import ConfigModel

class ProcessManager:
    config: ConfigModel = None
    is_running: bool = False
    task_queue = []

    def __init__(self, config: ConfigModel) -> None:
        self.config = config

    def start_processing(self):
        self.is_running = True
        print("start...")
        # self.get_tasks()

    def stop_processing(self):
        self.is_running = False
        print("stop...")

    def get_tasks(self):
        model = self.config.model_dump()
        for key in model.keys():
            task = getattr(self.config, key)
            if isinstance(task, str) or key == "script":
                continue
            scheduler = getattr(task, "scheduler")
            if scheduler:
                is_enabled = getattr(scheduler, "enable")
                if is_enabled:
                    self.task_queue.append(task)

        print(self.task_queue)
