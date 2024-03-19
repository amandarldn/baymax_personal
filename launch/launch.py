import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, Command
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource

import xacro

def generate_launch_description():

    # use_sim_time = LaunchConfiguration('use_sim_time')
 
    pkg_path = os.path.join(get_package_share_directory('baymax'))
   
    xacro_file = os.path.join(pkg_path, 'description', 'baymax.urdf.xacro')
    
    robot_description_config = Command(['xacro ', xacro_file])
    params = {'robot_description': robot_description_config}

    #GAZEBO
    gazebo_params_file = os.path.join(get_package_share_directory('baymax'),'config','gazebo_params.yaml')

    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'baymax'],
                        output='screen')

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py'
        )])
    )

    rviz_config_file = os.path.join(get_package_share_directory('baymax'), 'config', 'baymax_config.rviz')

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[params]
        ),
        # Node(
        #     package='rviz2',
        #     executable='rviz2', 
        #     name='rviz2',
        #     parameters=['-d', rviz_config_file]
        # ),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            output='screen'
        ),
        gazebo, spawn_entity
    ])