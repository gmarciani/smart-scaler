from services.agents_manager.model.qlearning import Action as QLearningAction


class SimpleLearningContext:

    def __init__(self, ctx_id, pod_name, min_replicas=0, max_replicas=10, alpha=0.5, gamma=0.5, state_granularity=10):
        self.ctx_id = ctx_id
        self.pod_name = pod_name
        self.min_replicas = min_replicas
        self.max_replicas = max_replicas
        self.alpha = alpha
        self.gamma = gamma
        self.state_granularity = state_granularity
        
        self.matrix = []
        
        self.current_state = None
        self.last_state = None
        
        self.last_action = QLearningAction.NO_SCALE