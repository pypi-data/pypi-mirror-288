from xuance.mindspore.learners import *


class DDPG_Learner(Learner):
    class ActorNetWithLossCell(nn.Cell):
        def __init__(self, backbone):
            super(DDPG_Learner.ActorNetWithLossCell, self).__init__()
            self._backbone = backbone
            self._mean = ms.ops.ReduceMean()

        def construct(self, x):
            policy_q = self._backbone.Qpolicy(x)
            loss_a = -self._mean(policy_q)
            return loss_a

    class CriticNetWithLossCell(nn.Cell):
        def __init__(self, backbone, gamma):
            super(DDPG_Learner.CriticNetWithLossCell, self).__init__()
            self._backbone = backbone
            self._gamma = gamma
            self._loss = nn.MSELoss()

        def construct(self, x, a, x_, q_target):
            action_q = self._backbone.Qaction(x, a)
            loss_q = self._loss(logits=action_q, labels=q_target)
            return loss_q

    def __init__(self,
                 policy: nn.Cell,
                 optimizers: nn.Optimizer,
                 schedulers: Optional[nn.exponential_decay_lr] = None,
                 model_dir: str = "./",
                 gamma: float = 0.99,
                 tau: float = 0.01):
        self.tau = tau
        self.gamma = gamma
        super(DDPG_Learner, self).__init__(policy, optimizers, schedulers, model_dir)
        # define mindspore trainers
        self.actor_loss_net = self.ActorNetWithLossCell(policy)
        self.actor_train = nn.TrainOneStepCell(self.actor_loss_net, optimizers['actor'])
        self.actor_train.set_train()
        self.critic_loss_net = self.CriticNetWithLossCell(policy, self.gamma)
        self.critic_train = nn.TrainOneStepCell(self.critic_loss_net, optimizers['critic'])
        self.critic_train.set_train()

    def update(self, obs_batch, act_batch, rew_batch, next_batch, terminal_batch):
        self.iterations += 1
        obs_batch = Tensor(obs_batch)
        act_batch = Tensor(act_batch)
        rew_batch = Tensor(rew_batch)
        next_batch = Tensor(next_batch)
        ter_batch = Tensor(terminal_batch)

        target_q = self.policy.Qtarget(next_batch)
        backup = rew_batch + (1 - ter_batch) * self.gamma * target_q
        q_loss = self.critic_train(obs_batch, act_batch, next_batch, backup)
        p_loss = self.actor_train(obs_batch)

        self.policy.soft_update(self.tau)

        actor_lr = self.scheduler['actor'](self.iterations).asnumpy()
        critic_lr = self.scheduler['critic'](self.iterations).asnumpy()

        info = {
            "Qloss": q_loss.asnumpy(),
            "Ploss": p_loss.asnumpy(),
            "actor_lr": actor_lr,
            "critic_lr": critic_lr
        }

        return info
