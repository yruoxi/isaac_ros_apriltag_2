# SPDX-FileCopyrightText: NVIDIA CORPORATION & AFFILIATES
# Copyright (c) 2021-2022 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

import launch
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode


def generate_launch_description():
    apriltag_node_list = []
    for camera_name in ["fryer_left", "fryer_mid", "fryer_right"]:
        apriltag_node = ComposableNode(
            package="isaac_ros_apriltag",
            plugin="nvidia::isaac_ros::apriltag::AprilTagNode",
            name=f"apriltag_{camera_name}",
            parameters=[{"size": 0.16, "max_tags": 64}],
            remappings=[
                (
                    "/image",
                    f"/cameras/{camera_name}/infra1/aruco_detect/ros2_images",
                ),
                (
                    "/camera_info",
                    f"/cameras/fryer_mid/infra1/camera_info", #Changed here f"/cameras/{camera_name}/infra1/camera_info"
                ),
                (
                    "/tag_detections",
                    f"/cameras/{camera_name}/infra1/aruco_detect/tag_detections",
                ),
            ],
        )
        apriltag_node_list.append(apriltag_node)

    apriltag_container = ComposableNodeContainer(
        package="rclcpp_components",
        name="apriltag_container",
        namespace="",
        executable="component_container_mt",
        composable_node_descriptions=apriltag_node_list,
        output="screen",
    )

    return launch.LaunchDescription([apriltag_container])
