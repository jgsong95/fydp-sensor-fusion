#include <iostream>
#include <cv_bridge/cv_bridge.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>

#include <vector>

#include <ros/ros.h>
#include <cv_bridge/cv_bridge.h>
#include <image_transport/image_transport.h>
#include <sensor_msgs/image_encodings.h>
#include <sensor_msgs/PointCloud2.h>
#include <velodyne_pointcloud/point_types.h>
#include "sensor_msgs/Image.h"

#include <pcl_ros/point_cloud.h>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
#include <pcl_conversions/pcl_conversions.h>
#include <pcl/io/pcd_io.h>
#include <pcl/common/transforms.h>

//user generated header files
#include <Projection_Matrices.hpp>
#include <Gaussian_process_regression.hpp>
#include <GP_regressor.h>


//will fix use of global variables in a bit
image_transport::Publisher depth_a;

/*
	Summary: Does a coordinate transformation between lidar and camera frame
	Input:   Raw Lidar PointCloud
	Output:  Partially Depth-Encoded Depth Map

*/

void pointCloudCallback(const sensor_msgs::PointCloud2ConstPtr& PointCloudMsg)
{
	//for loop to go through each msg and multiply the projection matrix to it

	//assuming the casting takes care of the unsigned to signed part - will look at documentation later
	//Vector_double points = Eigen::Map<Vector8u>(PointCloudMsg->data, PointCloudMsg->row_step, PointCloudMsg->height).cast<Vector_double::Scalar>();
	cv_bridge::CvImage depthImage;
	depthImage.encoding = sensor_msgs::image_encodings::TYPE_32FC3;

	pcl::PointCloud< pcl::PointXYZ > points_lidar;
	pcl::fromROSMsg(*PointCloudMsg, points_lidar);

	cv::Mat depth_mat = cv::Mat::zeros(cv::Size(1200, 1920), CV_32FC3);

	for (int point = 0; point < points_lidar.width * points_lidar.height; ++point) {
		std::vector<double> xyzpoint;
		xyzpoint.push_back(static_cast<double>(points_lidar.points[point]).x);
		xyzpoint.push_back(static_cast<double>(points_lidar.points[point]).y);
		xyzpoint.push_back(static_cast<double>(points_lidar.points[point]).z);
		xyzpoint.push_back(1.0f); // don't need the intensity value

		cv::Mat rgb_depth; // can I initialize Mat like this? Do I need to give it a size
		rgb_depth = Extrinsic_Matrix * cv::Mat(xyzpoint, false);
		if (rgb_depth.at<double>(0,2) > 0) {//only looking in front of us
			cv::Mat image_frame_from_rbg_depth = Projection_Matrix * xyzpoint; // gives transformed (x,y) coordinate in image frame (what we see on the screen)
			if (image_frame_from_rbg_depth.at<double>(0,0) >= 0 && image_frame_from_rbg_depth.at<double>(0,0) <= 1200 && image_frame_from_rbg_depth.at<double>(0,1) >= 0 && image_frame_from_rbg_depth.at<double>(0,1) <= 1920) {
				//there are issues with Eigen and stride (it seems Eigen doesn't have multi channel support - I'll look into it further)
				depth_mat.at<double>(image_frame_from_rbg_depth(0), image_frame_from_rbg_depth(1)) = distance_from_xyzpoint(rgb_depth);
			}
		}
	}
	
	
	/*depthImage.image = depth_mat;
	depth_a.publish(depthImage.toImageMsg())*/
}


