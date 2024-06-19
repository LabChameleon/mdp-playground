import unittest

import sys
import os

import numpy as np

import logging

from datetime import datetime

log_filename = (
    "/tmp/test_run_experiments_"
    + datetime.today().strftime("%m.%d.%Y_%I:%M:%S_%f")
    + ".log"
)


class TestRunExperiments(unittest.TestCase):

    # def test_rainbow_hydra(self):
    #
    #     exit_code = os.system(sys.executable + " run_experiments.py -a 0 -n 0 -c experiments/rainbow_hydra.py -e rainbow_hydra") # sys.executable contains "current" Python
    #     assert exit_code == 0

    # def test_dqn_seq_del(self):
    #
    #     exit_code = os.system(sys.executable + " run_experiments.py -a 0 -n 0 -c experiments/dqn_seq_del.py -e dqn_seq_del")
    #     assert exit_code == 0

    def test_dqn_test_expt(self):

        exit_code = os.system(
            sys.executable
            + " run_experiments.py -n 0 -c experiments/dqn_test_expt.py -e dqn_test_expt"
        )
        assert exit_code == 0

        from mdp_playground.analysis import MDPP_Analysis_Multiple as MDPP_Analysis

        save_fig = False
        mdpp_analysis = MDPP_Analysis()
        experiments = {"dqn_test_expt_0": "."}  # dqn_test_expt_0.csv"}
        list_exp_data = mdpp_analysis.load_data(
            experiments, load_eval=False, exp_type="grid"
        )

        final_metrics = np.squeeze(list_exp_data[0]["train_stats"])
        np.testing.assert_allclose(
            final_metrics,
            [10000.0, 80.0, 80.0],
            rtol=1e-01,
            err_msg="Expected training timesteps, episode_reward, episode_len after 10,000 timesteps to be within 10% of [10000., 80.0, 80.0].",
        )

        exit_code = os.system("rm -f dqn_test_expt_0*.csv")
        assert exit_code == 0

    # Similar thing is tested above. These tests are time consuming, so rather have only a few of them.
    # def test_default_config(self):

    #     exit_code = os.system(
    #         sys.executable
    #         + " mdp_playground/scripts/run_experiments.py -n 0 -c default_config.py -e default_config"
    #     )
    #     assert exit_code == 0

    # ###TODO Enable once branches are merged
    # def test_10_random_expts(self):

    #     from glob import glob
    #     expt_list = glob("experiments/*.py")

    #     # sel_expt_list = np.random.integers(0, len(expt_list), 10)
    #     expt_list = np.random.permutation(expt_list)
    #     for i in range(2):
    #         conf_file = expt_list[i]
    #         exp_name = conf_file.split('/')[-1].split('.')[0]

    #         exit_code = os.system(
    #             sys.executable
    #             + " run_experiments.py -n 0 -c " + conf_file + " -e " + exp_name + " -t 2000"
    #         )
    #         assert exit_code == 0


if __name__ == "__main__":
    unittest.main()
