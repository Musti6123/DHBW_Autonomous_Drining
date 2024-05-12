from __future__ import annotations

import argparse

import gymnasium as gym
import numpy as np
from matplotlib import pyplot as plt

from env_wrapper import CarRacingEnvWrapper
from input_controller import InputController
from lane_detection import LaneDetection
from lateral_control import LateralControl
from longitudinal_control import LongitudinalControl
from path_planning import PathPlanning

fig = plt.figure()
plt.ion()
plt.show()


def run(env, input_controller: InputController):
    longitudinal_control = LongitudinalControl()
    path_planning = PathPlanning()
    lane_detection = LaneDetection()
    lateral_control = LateralControl()

    seed = int(np.random.randint(0, int(1e6)))
    state_image, info = env.reset(seed=seed)
    total_reward = 0.0

    speed_history = []
    target_speed_history = []

    while not input_controller.quit:
        cv_image = np.asarray(state_image, dtype=np.uint8)
        left_lane_boundaries, right_lane_boundaries = lane_detection.detect(cv_image)
        trajectory, curvature = path_planning.plan(left_lane_boundaries, right_lane_boundaries)
        steering_angle = lateral_control.control(trajectory, info['speed'])
        target_speed = longitudinal_control.predict_target_speed(curvature, steering_angle)
        acceleration, braking = longitudinal_control.control(info['speed'], target_speed)
        speed_history.append(info['speed'])
        target_speed_history.append(target_speed)

        # Longitudinal control plot
        plt.gcf().clear()
        plt.plot(speed_history, c="green")
        plt.plot(target_speed_history)
        try:
            fig.canvas.flush_events()
        except:
            pass

        # Step the environment
        input_controller.update()
        a = [input_controller.steer, acceleration, braking]
        state_image, r, done, trunc, info = env.step(a)
        total_reward += r

        # Reset environment if the run is skipped
        input_controller.update()
        if done or input_controller.skip:
            print(f"seed: {seed:06d}     reward: {total_reward:06.2F}")

            input_controller.skip = False
            seed = int(np.random.randint(0, int(1e6)))
            state_image, info = env.reset(seed=seed)
            total_reward = 0.0

            speed_history = []
            target_speed_history = []


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no_display", action="store_true", default=False)
    args = parser.parse_args()

    render_mode = 'rgb_array' if args.no_display else 'human'
    env = CarRacingEnvWrapper(gym.make("CarRacing-v2", render_mode=render_mode, domain_randomize=False))
    input_controller = InputController()

    run(env, input_controller)
    env.reset()


if __name__ == '__main__':
    main()
