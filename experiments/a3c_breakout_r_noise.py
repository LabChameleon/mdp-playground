num_seeds = 5
timesteps_total = 10_000_000
from collections import OrderedDict
import numpy as np
var_env_configs = OrderedDict({
    'reward_noise': list(np.array([0, 1, 5, 10, 25])/1000), # Std dev. of normal dist.
    'dummy_seed': [i for i in range(num_seeds)],
})

var_configs = OrderedDict({
"env": var_env_configs
})

env_config = {
    "env": "GymEnvWrapper-v0",
    "env_config": {
        "AtariEnv": {
            "game": "breakout",
            'obs_type': 'image',
            'frameskip': 1,
        },
        # "GymEnvWrapper": {
        "atari_preprocessing": True,
        'frame_skip': 4,
        'grayscale_obs': False,
        'state_space_type': 'discrete',
        'action_space_type': 'discrete',
        'seed': 0,
        # },
        # 'seed': 0, #seed
    },
}

algorithm = "A3C"
agent_config = { # Taken from Ray tuned_examples
    'clip_rewards': True,
    'lr': 1e-4,
    # Value Function Loss coefficient
    "vf_loss_coeff": 2.5,
    # Entropy coefficient
    "entropy_coeff": 0.01,
    "min_iter_time_s": 0,
    'num_envs_per_worker': 5,
    'num_gpus': 0,
    'num_workers': 3,
    'rollout_fragment_length': 10,
    'timesteps_per_iteration': 10000,
    # "tf_session_args": {
    #     # note: overriden by `local_tf_session_args`
    #     "intra_op_parallelism_threads": 4,
    #     "inter_op_parallelism_threads": 4,
    #     # "gpu_options": {
    #     #     "allow_growth": True,
    #     # },
    #     # "log_device_placement": False,
    #     "device_count": {
    #         "CPU": 2,
    #         # "GPU": 0,
    #     },
    #     # "allow_soft_placement": True,  # required by PPO multi-gpu
    # },
    # # Override the following tf session args on the local worker
    # "local_tf_session_args": {
    #     "intra_op_parallelism_threads": 4,
    #     "inter_op_parallelism_threads": 4,
    # },
}


model_config = {
    # "model": {
    #     "fcnet_hiddens": [256, 256],
    #     "fcnet_activation": "tanh",
    #     "use_lstm": False,
    #     "max_seq_len": 20,
    #     "lstm_cell_size": 256,
    #     "lstm_use_prev_action_reward": False,
    # },
}

from ray import tune
eval_config = {
    "evaluation_interval": None, # I think this means every x training_iterations
    "evaluation_config": {
        "explore": False,
        "exploration_fraction": 0,
        "exploration_final_eps": 0,
        "evaluation_num_episodes": 10,
        # "horizon": 100,
        "env_config": {
            "dummy_eval": True, #hack Used to check if we are in evaluation mode or training mode inside Ray callback on_episode_end() to be able to write eval stats
            'transition_noise': 0 if "state_space_type" in env_config["env_config"] and env_config["env_config"]["state_space_type"] == "discrete" else tune.function(lambda a: a.normal(0, 0)),
            'reward_noise': tune.function(lambda a: a.normal(0, 0)),
            'action_loss_weight': 0.0,
        }
    },
}