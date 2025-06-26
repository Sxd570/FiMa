from shared.logger import logger


class GoalUseCase:
    def __init__(self):
        self.goal_database = GoalDatabase()

        self.user_id = None
        self.goal_total_goals = 0
        self.goal_total_completed = 0
        self.goal_total_saved = 0


    def get_goals_overview(self, user_id):
        try:
            pass

        except Exception as e:
            logger.error(f"Error in get_goals_overview use case: {e}")
            raise e